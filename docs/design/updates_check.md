# Startup Update Check Design

## Issue

ALS does not currently tell users when a newer release is available.

The update check must remain lightweight and must not interfere with the main
use case. In particular:

- application startup must not wait for a network request;
- network failure must not affect normal operation;
- no popup or download prompt should interrupt a session;
- ALS must not depend on a release API or platform-specific release metadata;
- users must explicitly choose whether ALS performs the startup request.

All supported platforms are released together under the same ALS version.
Therefore the application only needs to compare its local version with one
remote version. It does not need to select an artifact or identify the current
platform.

## Current Code Context

Important files and responsibilities:

- `src/als/version.py`
  - Provides the source-tree version.
  - Distribution builds replace this value with the CI-generated version.
- `src/als/model/data.py`
  - Exposes the running application version as `VERSION`.
- `ci/builds/setup_build.sh`
  - Accepts stable and prerelease tags such as `v1.0`, `v1.0-alpha1`, and
    `v1.0-beta1`.
  - Gives untagged builds a development suffix containing the commit and
    pipeline identifiers.
- `src/als/main.py`
  - Creates the application, controller, and main window.
- `src/als/ui/windows.py`
  - Builds and shows the main window.
  - Already uses Qt facilities for opening network URLs, but does not currently
    perform HTTP requests.
- `src/als/config.py`
  - Owns persisted preferences and their defaults.
  - Removes unsupported settings, so the new preference must be registered in
    `_DEFAULTS`.
- `src/als/ui/dialogs.py`
  - Loads and saves Preferences dialog values.
- `src/als/ui/prefs_ui.ui`
  - Defines the Preferences dialog.
- `src/als/ui/als_ui.ui`
  - Defines the main controls panel.
- `i18n/als_fr.ts` and `i18n/als_ru.ts`
  - Provide French and Russian translations.
- `website/static/current-stable.txt`
  - Publishes the current release version as a Hugo-managed static asset.

The project already depends on PyQt 5.13 and `setuptools`. The implementation
should use Qt networking and project-owned version parsing without adding a new
dependency.

## Agreed Behavior

Add a **Check for updates on startup** preference.

- The preference is disabled by default.
- It is independent from anonymous usage statistics.
- When disabled, ALS makes no update request.
- When enabled, ALS starts one check after the main window is visible.
- The request is asynchronous and must not block the GUI thread.
- The request timeout is 20 seconds.
- Network errors, timeouts, empty responses, and invalid remote versions are
  ignored silently.

The remote endpoint is:

```text
https://als-app.org/current-stable.txt
```

The response contains one version string with optional surrounding whitespace.
An optional leading `v` is accepted.

If the remote version is newer, ALS displays a passive label in the main
controls panel:

```text
ALS 1.0.1 is available
```

The label:

- is hidden by default;
- contains no download link;
- triggers no popup or other action;
- remains hidden when ALS is current or the check cannot be completed.

## Version Policy

### Published Versions

Accepted published version formats are:

```text
N.N[.N...]
N.N[.N...]-alphaNN
N.N[.N...]-betaNN
```

Examples:

```text
1.0
1.0.1
1.0-alpha1
1.0-alpha12
1.0-beta1
```

Numeric components and qualifier numbers must be compared numerically, not as
strings.

For the same numeric base version, ordering is:

```text
alpha < beta < qualifier-less release
```

Within one qualifier:

```text
1.0-alpha2 < 1.0-alpha10
1.0-beta2 < 1.0-beta10
```

The remote file must contain a published version. A development-build value
inadvertently written to the remote file is invalid and must be ignored.

### Local Development Builds

Local development builds remain eligible for update notices.

Their generated suffix must be removed to recover the numeric base version for
comparison. A local development build is considered earlier than a published
version with the same numeric base.

Consequences:

```text
local 1.0-dev...  remote 1.0  -> show 1.0
local 1.0-dev...  remote 1.0-beta1 -> show 1.0-beta1
local 1.1-dev...  remote 1.0  -> no notice
```

This development-build handling applies only to the local version. The remote
value must still match the published-version grammar.

### Comparison Ownership

Keep parsing and comparison in a small application module, separate from the
Qt request lifecycle. The module should expose behavior-oriented functions for:

- parsing a valid remote published version;
- interpreting the local release or development version;
- determining whether the remote version is newer.

The UI should receive only a valid newer version or no result. It should not
contain version grammar or ordering logic.

## Network Lifecycle

Use `QNetworkAccessManager` in the main window. Qt networking is asynchronous,
so a separate worker thread is unnecessary.

The manager, active reply, and timeout timer must remain referenced by the main
window for the duration of the request.

After the main window is shown:

1. Check the persisted preference.
2. Schedule the request through the Qt event loop.
3. Send one HTTP GET request to the static endpoint.
4. Start a single-shot 20-second `QTimer`.
5. When the reply finishes:
   - stop the timeout timer;
   - require a successful network result;
   - decode and strip the response;
   - apply the version policy;
   - show the label only when an update is available;
   - release the reply.
6. If the timer expires:
   - abort the reply;
   - leave the label hidden;
   - clean up without notifying the user.

PyQt 5.13 does not provide the newer request-level transfer-timeout API used by
recent Qt versions. The explicit timer is therefore part of the required
implementation rather than a fallback.

Only one request is made per application run. No retry, polling, caching, or
manual check action is needed.

## Preferences Impact

Add a boolean config entry such as:

```text
check_updates_on_startup = 0
```

Add matching getter and setter functions in `src/als/config.py`.

Add a checkbox to the Preferences dialog's existing general data settings:

```text
Check for updates on startup
```

The Preferences dialog must load and save it independently from the usage
statistics checkbox. Changing it does not require an application restart; it
controls the check performed on the next startup.

## Main Window Impact

Add a dedicated label to the main controls panel.

The label should:

- use an action-oriented name describing its purpose;
- be hidden initially;
- support translated text;
- wrap if necessary within the dock width;
- avoid link handling or interaction styling.

The main window owns the request lifecycle because it also owns the label and
knows when the visible UI is ready. The controller and image-processing
pipelines should not be involved.

## Translations

New visible strings require English source text plus French and Russian
translations:

- `Check for updates on startup`
- `ALS %s is available`, or the Qt formatting equivalent selected by the
  implementation

Update translation sources with:

```text
pylupdate5 -noobsolete -verbose als.pro
```

New or changed translations remain marked `type="unfinished"` for Qt Linguist
review. Translation release generation is outside this task.

## Published Version File

Store `current-stable.txt` under `website/static/` so Hugo includes it in every
website build and the production deployment publishes it automatically.

Release preparation must update this source file to the version being
published. No special deployment-script logic or reminder is required.

## Guardrails

Do not:

- block application startup on the request;
- create a worker thread for Qt networking;
- display a popup, download link, or failure message;
- couple update checks to usage-statistics consent;
- call the GitHub releases API;
- add platform or architecture selection;
- accept arbitrary remote development versions;
- compare versions as plain strings;
- retry a failed request;
- add website-side application logic.

Do:

- keep the preference disabled by default;
- perform at most one asynchronous request after the UI is visible;
- enforce the 20-second timeout;
- fail silently;
- isolate and test version parsing and ordering;
- keep the user-facing notice passive.

## Implementation Sequence

1. Add pure version parsing and comparison behavior with focused tests.
2. Add the persisted opt-in preference and Preferences dialog control.
3. Add the hidden update-available label to the main controls panel.
4. Add the asynchronous request lifecycle to the main window.
5. Add French and Russian translation entries.
6. Add the Hugo-managed current stable version file.
7. Regenerate UI and translation sources required by the changed source files.

Keep these points reviewable as separate semantic changes where practical.

## Testing And Validation

### Version Behavior

Add focused tests using Given/When/Then names for:

- equal stable versions;
- newer and older numeric versions;
- numeric comparison of multi-digit components;
- alpha ordering;
- beta ordering;
- alpha before beta;
- prerelease before qualifier-less release;
- optional leading `v`;
- surrounding whitespace in the remote response;
- malformed remote values;
- remote development values being ignored;
- local development builds advertising the same-base published release;
- local development builds not advertising an older-base release.

Tests should exercise the public version-comparison behavior rather than private
parsing details.

### Configuration Behavior

Verify:

- the preference defaults to disabled;
- enabled and disabled values persist through the existing config mechanism;
- unrelated config values remain unchanged.

### Qt Behavior

Verify the user-visible state transitions:

- the label starts hidden;
- a newer valid remote version shows the translated notice;
- an equal or older version leaves the label hidden;
- timeout, network failure, and invalid content leave the label hidden;
- the request is not started when the preference is disabled.

Avoid tests that only assert signal connection order or internal Qt object
plumbing.

### Project Validation

Verify the Hugo build publishes `website/static/current-stable.txt` at the site
root with the expected release version.

Also verify manually that:

- the main window appears before the request is made;
- the GUI remains responsive while the request is pending;
- the label fits the main controls panel in English, French, and Russian;
- no notification appears when the endpoint is unavailable.
