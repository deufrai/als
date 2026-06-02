# Live Metrics Draft

## Issue

The existing analyzer notebook exposes useful ALS runtime and astronomy metrics,
but it is an offline analysis tool. ALS should expose those signals live during
a session, in a dedicated tool window, so users can monitor processing health,
alignment quality, and system pressure while observing.

The proof of concept validated `pyqtgraph` as a viable plotting dependency and
confirmed that a modeless tool window can display live bounded data. The POC is
not the target architecture; it should be replaced cleanly before the feature is
expanded.

## Code Context

Existing ALS code already has most data sources needed for collection:

- The controller receives queue-size signals for pre-process, stacker,
  post-process, and saver queues.
- The processing workers already emit busy/waiting signals.
- Available memory is already sampled by `Controller.collect_metrics()`.
- The configured memory margin is available from preferences/config.
- Stack size changes are already signaled by the stacker.
- Overall processing time is already tracked through the controller ticket
  system.
- For input subs, the ticket value is the image path.
- Alignment details and timing values are currently logged from processing code.
- Failure causes are already known at warning/error points; metrics should
  receive structured events immediately before those existing logs are emitted.

Metrics collection must use structured data emitted at the point where the value
or cause is known. It must not parse log text.

## Goals

- Ship as a v1.0 feature.
- Display live metrics in a dedicated modeless tool window.
- Keep metrics observational: do not move processing decisions into the metrics
  model.
- Preserve raw data as much as practical for future export.
- Keep graph image export as an optional follow-up if PyQtGraph makes it easy.
- Keep display useful in the field: only show information that helps diagnose
  processing backlog, worker activity, memory pressure, alignment quality,
  rejected subs, or slow processing stages.

## Metrics Domains

Use separate metric models by domain and lifecycle.

### System Metrics

System metrics are session-scoped for display, but they continue collecting
after session stop so users can monitor downstream drain-down.

Collection starts on session start. Data remains visible when the session is
stopped, paused, or drained, and resets only on the next session start.

System metrics:

- available memory
- configured preserved-memory margin
- queue sizes for each worker queue
- worker status for each worker

System graph X-axis uses absolute timestamps.

Available memory and preserved-memory margin must be sampled together and shown
on the same graph. If the user changes the preserved-memory margin during a
session, later samples use the new value without backfilling earlier samples.

Worker status is binary: idle or busy.

### Astro Session Metrics

Astro metrics are per-session. They reset on new session start and remain visible
until the next session starts.

Astro graph X-axis uses sub index/order.

Astro metrics:

- alignment matches count vs required matches
- alignment search subset ratio
- applied alignment transformations:
  - translation X
  - translation Y
  - rotation
  - scale
- aggregated count of subs that did not reach the filesystem, grouped by root
  cause
- overall processing time history
- timing history for image processes, grouped by family
- stack size history

Alignment scale and ratio are distinct metrics:

- scale is the image scaling applied during alignment;
- ratio is the size of the search subset compared to the full image that was
  sufficient to find the required matches count.

Ratio is meaningful only for the EAA profile. It can have three values:

- `1/10`
- `1/3`
- `1`

Ratio is an alignment effort and image-quality proxy. Deteriorating ratio can
indicate degraded focus, clouds, or similar observing conditions.

## Failure Causes

The displayed metric is: subs that did not reach the filesystem.

A sub counts as successful only when save completion confirms that it reached the
filesystem. Save failures therefore belong to the failure-cause aggregate.

Failure causes must be normalized internal codes in storage/export, not
localized log text. Display labels should be localized.

Metrics collection should emit the structured event immediately before the
existing warning/error dispatch when the cause is known.

Example shape:

```python
metrics.record_sub_terminal_failure(ticket, cause_code)
MESSAGE_HUB.dispatch_warning(...)
```

Use the existing ticket concept. Do not introduce a second per-sub identifier.

Alignment failures should be as specific as existing warning/error points allow,
with a fallback only where the code genuinely cannot distinguish the cause.

Display rules:

- do not show a failure cause until its count is greater than zero;
- group causes by pipeline area;
- show specific alignment causes expanded under the alignment group;
- export keeps fully specific causes even when the UI groups them.

## Timing Families

Timing families:

- pre-process
- stacking
- post-process
- save

Display one graph per family. Each graph shows one curve per process in that
family.

Process display labels must be user-facing and i18n-ready. Export should include
stable internal process codes plus localized labels where practical.

## Display

Use one scrollable modeless tool window with sections. Sections should be
collapsible if practical.

Collapsed sections continue collecting data but skip plot redraw until expanded.

### System Section

Display:

- memory graph with available memory and preserved-memory margin on the same
  absolute-timestamp axis;
- one worker block per worker;
- each worker block combines:
  - binary idle/busy status lane;
  - queue-size bars for that worker queue.

Queue bars use one bar per sample, with height equal to the queue size.

### Alignment Section

Display:

- matches and required matches as historized line graph;
- ratio as bars aligned with the matches graph;
- translations graph with X and Y values;
- rotation graph;
- scale graph.

### Processing Timings Section

Display:

- one graph per timing family;
- one curve per user-facing process label in each family;
- overall processing time history.

### Session Results Section

Display:

- stack size as historized bars;
- active failure-cause list/table;
- only causes with count greater than zero.

## Update Policy

Astro metrics update when astro events occur, mostly during sub progression.

System metrics update when system samples are collected. The current memory
sampling period is two seconds, and memory redraw should happen on that sample.

Because normal sub cadence ranges from about one or two seconds to several
minutes, event-driven astro redraws are acceptable for the first implementation.

Do not downsample display data for the first implementation. Export should keep
raw samples as much as practical.

## Export

Build the model API as export-ready from the start.

Preferred export direction:

- raw data as much as practical;
- stable internal codes for process names and failure causes;
- localized labels where useful;
- separate raw series for system and astro metrics;
- optional graph image export if PyQtGraph provides an easy path.

Export UI or commands are not required in the first implementation.

## Implementation Sequence

1. Replace the POC metrics class with clean split models:
   - `SystemMetrics`
   - `AstroSessionMetrics`
   - a small container exposed by the controller.
2. Implement the first real slice: system metrics.
   - available memory plus preserved-memory margin;
   - queue-size history;
   - worker idle/busy history;
   - scrollable sectioned UI for those metrics.
3. Add astro stack/session basics:
   - stack size history;
   - overall processing time history.
4. Add alignment metrics:
   - matches vs required;
   - ratio;
   - translation, rotation, scale.
5. Add per-process timings by family.
6. Add structured failure-cause collection and display.
7. Add export support when the model shape is stable.

