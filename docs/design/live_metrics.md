# Live Metrics Draft

## Issue

The existing analyzer notebook exposes useful ALS runtime and astronomy metrics,
but it is an offline analysis tool. ALS should expose those signals live during
a session, in a dedicated tool window, so users can monitor processing health,
alignment quality, and system pressure while observing.

The system metrics slice uses lightweight custom-painted Qt widgets. The UI must
stay responsive with dense live data and should avoid feature-heavy plotting
widgets unless a future graph genuinely needs that interaction model.

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
Both values are stored and displayed in MiB. The preserved-memory preference is
stored in configuration as a code and must be mapped to bytes before the metrics
sample is recorded.

Worker status is binary: idle or busy.

Queue sizes and worker status use the same absolute timestamp range as memory.
Each worker has one combined graph:

- a status lane showing idle/busy duration from each status-change event;
- queue-size bars showing the queue size held until the next queue-size sample.

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

Use lightweight Qt widgets for live drawing. Graph widgets should expose only the
interaction needed for field monitoring; panning, zooming, hover inspection, and
other heavier plotting features are not required for the first implementation.

All graphs inside the system section share one absolute-timestamp X-axis range
so memory, queues, and worker activity can be compared by time.

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
- optional graph image export if it remains cheap to provide from the custom
  widgets.

Export UI or commands are not required in the first implementation.


## Data Collection Code Map

### Session Lifecycle

- `src/als/logic.py`
  - `Controller.start_session()` is the reset/start hook for session-scoped
    metrics.
  - `Controller.stop_session()` stops folder scanning and purges upstream
    queues, but downstream workers may still drain already-consumed images.
    System metrics must keep collecting after this point.
  - `Controller.pause_session()` stops folder scanning only. Metrics must keep
    collecting while downstream workers continue.

### Ticket and Overall Processing Time

- `src/als/logic.py`
  - `Controller.on_new_image_path()` starts per-ticket timing by storing
    `self._image_timings[image_path] = time.time()`.
  - `Controller.on_new_post_processor_result()` computes total frame processing
    time from `image.ticket`, logs `*SD-FRMTIME*`, updates
    `DYNAMIC_DATA.last_timing`, then sends the image to saving.
- `src/als/processing.py`
  - `FileReader.process_image()` assigns `image.ticket = image_path`.
- `src/als/model/base.py`
  - `Image.ticket` is the existing code concept used to carry the ticket.

Metrics must reuse the existing ticket value. For input subs, that value is the
image path.

### System Metrics

- `src/als/logic.py`
  - `Controller.collect_metrics()` is the current periodic memory sampling hook.
    It should record available memory and the current preserved-memory margin in
    one aligned sample.
  - `Controller.on_pre_process_queue_size_changed()`,
    `Controller.on_stacker_queue_size_changed()`,
    `Controller.on_post_processor_queue_size_changed()`, and
    `Controller.on_saver_queue_size_changed()` are the queue-size hooks.
  - `Controller.on_pre_processor_busy()` /
    `Controller.on_pre_processor_waiting()`,
    `Controller.on_stacker_busy()` / `Controller.on_stacker_waiting()`,
    `Controller.on_post_processor_busy()` /
    `Controller.on_post_processor_waiting()`, and
    `Controller.on_saver_busy()` / `Controller.on_saver_waiting()` are the
    worker idle/busy hooks.
- `src/als/code_utilities.py`
  - `SignalingQueue.size_changed_signal` is emitted on `put()`, `put_nowait()`,
    `get()`, and `get_nowait()`.
- `src/als/processing.py`
  - `QueueConsumer.run()` emits `busy_signal` after taking work from the queue
    and `waiting_signal` after handling the item.
- `src/als/config.py`
  - `config.get_preserved_mem()` returns the user-configured memory margin.

### Stack Size

- `src/als/stack.py`
  - `Stacker.stack_size_changed_signal` is emitted when the stack size changes.
- `src/als/logic.py`
  - `Controller.on_stack_size_changed()` receives the value and updates
    `DYNAMIC_DATA.stack_size`.

### Alignment Metrics

- `src/als/stack.py`
  - `Stacker._find_transformation()` is the source for:
    - configured required matches count;
    - accepted matches count;
    - search subset ratio;
    - rotation;
    - translation;
    - scale;
    - accepted/rejected alignment result.
  - These values are currently debug-log-only through tags such as `*SD-REQ*`,
    `*SD-RATIO*`, `*SD-ROT*`, `*SD-TRANS*`, `*SD-SCALE*`,
    `*SD-MATCHES*`, and `*SD-ALIGNOK*`.

Implementation must add structured metric emission in this function before or
beside those debug logs.

### Per-Process Timings

- `src/als/processing.py`
  - `QueueConsumer.run()` wraps each queue consumer item with `Timer()` and logs
    whole-worker time.
  - `Pipeline._handle_item()` iterates image processors, but does not currently
    expose structured per-processor timing.
  - Individual processors sometimes use `Timer()` internally for specific
    sub-steps, such as dark subtraction, flat division, or data conversion.
- `src/als/stack.py`
  - `Stacker._align_image()` times `_find_transformation()` and
    `_apply_transformation()`.
  - `Stacker._handle_item()` owns stacking flow around alignment and stack
    update.
- `src/als/streams/output.py`
  - `ImageSaver._handle_item()` calls `_save_image()`.
  - `ImageSaver._save_image()` owns filesystem write and final rename.

Implementation must add structured timing samples around process/family
boundaries instead of deriving timings from log messages.

Timing collection must reuse the existing `Timer` context-manager pattern used
in `src/als/main.py`:

```python
with Timer() as timer:
    # work being timed

metrics.record_timing(..., timer.elapsed_in_milli)
```

Store raw numeric milliseconds for metrics/export. Keep
`timer.elapsed_in_milli_as_str` for logs and user messages.

### Failure Causes and Filesystem Success

- `src/als/processing.py`
  - `Pipeline._handle_item()` catches `ProcessingError` and logs that an image
    will be ignored.
  - Several processors emit warnings for degraded or skipped behavior, such as
    missing calibration files, shape mismatch, unsupported Bayer pattern, or
    invalid flat data.
- `src/als/stack.py`
  - `Stacker._handle_item()` catches `StackingError` and logs that the image is
    discarded.
  - `Stacker._find_transformation()` distinguishes alignment rejection while
    searching for a valid transform.
- `src/als/streams/output.py`
  - `ImageSaver._save_image()` dispatches `"Image saved : {}"` on success and
    `"Failed to save image : {}"` on failure.
  - `ImageSaver.save_completed_signal` is emitted only after successful save and
    carries the destination path.
- `src/als/logic.py`
  - `Controller.on_image_saved()` receives successful save completion.

Failure metrics should be emitted immediately before the existing warning/error
dispatch where the root cause is known. Filesystem success should be recorded
from the successful save path, not inferred from absence of errors.

## Implementation Sequence

Completed foundation:

- split live metrics into clean models:
   - `SystemMetrics`
   - `AstroSessionMetrics`
   - a small container exposed by the controller.
- implement the first system metrics slice:
   - available memory plus preserved-memory margin;
   - queue-size history;
   - worker idle/busy history;
   - scrollable sectioned UI with custom-painted timelines for those metrics.

Remaining sequence:

1. Add astro stack/session basics:
   - stack size history;
   - overall processing time history.
2. Add alignment metrics:
   - matches vs required;
   - ratio;
   - translation, rotation, scale.
3. Add per-process timings by family.
4. Add structured failure-cause collection and display.
5. Add export support when the model shape is stable.
