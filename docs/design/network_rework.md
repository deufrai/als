# Network Server Rework Draft

## Purpose

This document tracks the ALS network/server rework discussion so the design can
continue across multiple Codex sessions without losing context.

It is a working draft. Treat it as the current handoff note and update it when
decisions change.

## Issue

ALS includes an integrated HTTP/WebSocket image server. The server publishes the
latest web image, session data, and static web viewer assets so another device
can view the live stack in a browser.

The current implementation uses one auto-detected host IP for both:

- the address the server binds to;
- the address ALS displays and encodes in the QR code.

The IP is detected by creating a UDP socket toward `10.255.255.255` and asking
the OS which local address would be used for that route. This usually returns
the machine's default outbound route address.

That works in simple LAN setups, but it is fragile on machines with multiple
network interfaces.

The reported failure case is ALS running on a machine that also acts as a Wi-Fi
hotspot. In that topology, there are usually at least two relevant interfaces:

- an upstream interface, such as normal Wi-Fi, Ethernet, cellular, or VPN;
- a hotspot/AP interface with its own local subnet for connected client devices.

The current heuristic can select the upstream interface address. ALS then binds
only to that address. A phone or tablet connected to the hotspot needs to reach
the hotspot interface address instead, but ALS is not listening there.

Practical result:

- ALS can report that the server started successfully.
- The displayed/QR URL can point at an address unreachable from hotspot clients.
- Even if the user guesses the hotspot gateway address manually, the server may
  still reject the connection because it is bound to another interface.

## Current Code Map

Important files and responsibilities:

- `src/als/main.py`
  - Parses `--start_server`.
  - Creates `Controller` and `MainWindow`.
  - Calls `controller.start_www()` directly for startup server mode.
- `src/als/streams/network.py`
  - `get_host_ip()` implements the current route-based IP heuristic.
  - `is_port_in_use(ip, port)` checks one IP/port combination.
  - `Server.start()` starts aiohttp with `web.TCPSite(..., host, port)`.
  - `Server.send_message()` synchronously dispatches WebSocket messages from
    another thread via `asyncio.run_coroutine_threadsafe(...).result()`.
- `src/als/logic.py`
  - `Controller.__init__()` creates one `Server(config.get_web_folder_path())`.
  - `Controller.start_www()` checks the selected IP/port, prepares web assets,
    starts the server thread, stores `DYNAMIC_DATA.web_server_ip`, and marks the
    web server as running.
  - `Controller.stop_www()` stops the server thread.
  - `Controller.notify_browsers_about_new_image()` sends WebSocket update
    messages.
- `src/als/streams/output.py`
  - `ImageSaver._handle_item()` notifies browsers after saving a web image.
- `src/als/model/data.py`
  - `DYNAMIC_DATA.web_server_ip` stores the single advertised/server IP today.
- `src/als/config.py`
  - `_DEFAULTS` defines persisted config keys.
  - `setup()` removes config options that are not listed in `_DEFAULTS`.
  - New persisted settings must be added to `_DEFAULTS`.
- `src/als/ui/dialogs.py`
  - `PreferencesDialog` initializes and saves output/server preferences.
  - `QRDisplay.update_code()` builds the QR URL from
    `DYNAMIC_DATA.web_server_ip` and the configured port.
- `src/als/ui/windows.py`
  - Web start/stop buttons call `Controller.start_www()` / `stop_www()`.
  - Main/statusbar web server labels build a URL from
    `DYNAMIC_DATA.web_server_ip`.
- `src/als/ui/prefs_ui.ui`
  - Qt Designer source for the Preferences dialog.
- `src/als/ui/qr_ui.ui`
  - Qt Designer source for the QR dialog.
- `src/generated/*.py`
  - Generated UI files. Regenerate from `.ui` files with
    `utils/compile_ui_and_rc.py`.

## Non-Negotiable Goal

The web server must be reliable on all ALS target platforms, including hotspot
setups and ordinary LAN setups.

The current CI build matrix defines these target runtime families:

- Windows amd64 installer: `ci/builds/build_dist_amd64_win.sh`
- Linux amd64 desktop build: `ci/builds/build_dist_amd64_linux.sh`
- Linux arm64 / Raspberry Pi build: `ci/builds/build_dist_arm64_linux.sh`
- macOS Intel build: `ci/builds/build_dist_amd64_osx.sh`
- macOS Apple Silicon build: `ci/builds/build_dist_arm64_osx.sh`

The relevant dependency already present on every build path is `psutil`.
Versions vary by target requirements file, but `psutil` is part of each build
environment:

- `requirements.txt`: `psutil==5.6.6`
- `ci/builds/build_dist_amd64_win_req.txt`: `psutil==5.6.6`
- `ci/builds/build_dist_arm64_linux_req.txt`: `psutil==5.6.6`
- `ci/builds/build_dist_amd64_linux_req.txt`: `psutil==6.1.0`
- `ci/builds/build_dist_arm64_osx_req.txt`: unpinned `psutil`

Therefore the first implementation should rely on Python standard library plus
`psutil`, not platform-specific shell commands such as `ipconfig`, `ifconfig`,
`ip`, or `networksetup`.

## Release Branch Constraint

This rework is being implemented on a v0.7-based feature branch for the v0.7.1
release. In parallel, unrelated development continues on the `release/1.0`
branch for the upcoming v1.0 release.

The v0.7.1 implementation should therefore make the smallest architectural
change that satisfies the reliability goal. Keep the work tightly scoped to the
existing server/address-selection flow, preserve the current controller, UI, and
server structure where practical, and avoid broad cleanups or ownership moves
that are not required for the network fix.

This constraint is intended to make the finished change easy to review,
cherry-pick, or manually upfit into `release/1.0`. Prefer small additive helpers
and narrow call-site updates over a larger redesign, even when a larger redesign
could be attractive for v1.0.

### release/1.0 Upfit Risk Check

A read-only comparison of `v0.7..release/1.0` against the planned network-rework
files found no conflicting design work. The v1.0 branch does not currently change
`src/als/streams/network.py`, `src/als/ui/qr_ui.ui`, or `src/generated/*`.

The likely upfit pressure is textual rather than conceptual:

- `src/als/logic.py` keeps the same `start_www()` / `stop_www()` behavior, with
  only nearby unrelated processing changes.
- `src/als/config.py` and `src/als/model/data.py` add unrelated v1.0 settings and
  runtime fields, so new network settings should be additive and easy to port.
- `src/als/ui/dialogs.py`, `src/als/ui/windows.py`, and
  `src/als/ui/prefs_ui.ui` have the highest conflict risk because v1.0 touches
  preferences, slot naming, theme handling, and UI layout around areas this task
  will also update.

Keep handwritten UI/controller edits small and keep generated/XML UI changes in
separate commits where practical. This should make the later `release/1.0`
upfit mostly mechanical.

## Design Direction

Separate server binding from advertised address selection.

### Binding

The server should always bind to all IPv4 interfaces:

```text
0.0.0.0:<configured-port>
```

This makes the server accept inbound connections on normal LAN interfaces,
hotspot interfaces, and other local interfaces allowed by the OS/firewall.

The bind address should not be shown to users as the browser URL. `0.0.0.0` is
not a destination address for another device.

### Advertised Address

ALS should separately choose an advertised address for display, links, and QR
codes:

```text
http://<selected-local-ip>:<configured-port>
```

There is no single always-correct heuristic for every multi-interface machine.
The reliable UX is:

- enumerate usable local IPv4 addresses;
- rank them to choose a sensible default;
- expose the candidate list to the user;
- allow a preferred address to be selected and remembered.

## Guardrails

Do not:

- use the preferred advertised address as the bind address;
- display `0.0.0.0` as the user-facing URL;
- rely on interface names as hard filters;
- hide all virtual/VPN-looking interfaces;
- implement separate command-line probing for Windows, Linux, and macOS unless
  `psutil` proves insufficient;
- mark the web server as running before the actual bind has succeeded.

Do:

- bind aiohttp to `0.0.0.0`;
- use the preferred address only for links, status text, docs, and QR codes;
- keep all usable IPv4 candidates visible somewhere;
- fall back gracefully when a saved address is no longer present;
- keep hotspot users in mind when ranking and presenting candidates.

## Candidate Address Discovery

Use `psutil.net_if_addrs()` as the cross-platform discovery source.

Candidate filtering should keep:

- IPv4 addresses;
- non-loopback addresses by default;
- private LAN-style addresses, such as `10.x.x.x`, `172.16-31.x.x`, and
  `192.168.x.x`.

Candidate filtering should deprioritize, but not necessarily hide:

- loopback addresses;
- link-local addresses like `169.254.x.x`;
- virtual or VPN-looking interfaces.

Interface names vary across platforms and languages, so names should be weak
hints only. Address availability matters more than interface naming.

Suggested internal model:

```python
@dataclass
class NetworkAddress:
    interface_name: str
    ip: str
    url: str
    is_loopback: bool
    is_link_local: bool
    is_private: bool
    score: int
    label: str
```

Keep the pure discovery/ranking code independent from Qt and aiohttp so it can
be reused by Preferences, QR display, and server startup.

## Selection Heuristic

The advertised address selector should support an `Auto` mode.

Initial `Auto` behavior proposal:

1. If the current route-based address is usable and present in the candidate
   list, prefer it.
2. Otherwise prefer the highest-ranked private IPv4 address.
3. Prefer physical-looking Wi-Fi/Ethernet names only as a weak tie-breaker.
4. Deprioritize link-local and loopback addresses.
5. If nothing else exists, fall back to `127.0.0.1`.

This preserves the current LAN-friendly behavior while making the complete
candidate list visible for hotspot and multi-interface setups.

The heuristic should not remove candidates just because they look virtual or
unusual. Some users may intentionally connect through a VPN, bridge, or virtual
adapter.

## Preferences Impact

The Output preferences pane should gain a network/server address dropdown.

Current server preferences include the web server port. The new preference
should sit in the same network/server section.

Suggested dropdown entries:

```text
Auto - recommended
Wi-Fi - 192.168.1.42
Ethernet - 192.168.0.23
Network adapter - 192.168.137.1
wlan0 - 10.42.0.1
```

Each dropdown item should store a stable value in item data. The UI must not
parse display text.

For v0.7.1, persist only:

```text
auto
ip:<address>
```

Do not add interface-identity persistence such as `iface:<interface-name>` in
the first implementation. Interface identity can become platform-specific and is
not required for the reliability fix.

The preference should control the advertised address, not the bind address.

If the saved address is not available on a later run, ALS should fall back to
`Auto` and keep the available candidates visible.

Current preferences behavior disables the server settings while the web server
is running. That remains sensible for the port and persistent advertised-address
preference. Runtime QR flexibility is handled separately in the QR dialog.

## QR Dialog Impact

The QR dialog currently generates a QR code from the single runtime IP and the
configured port.

The new QR dialog should include its own address dropdown. This allows users to
switch the QR target while the server is running without changing persistent
preferences.

Suggested behavior:

- Default QR address follows the configured preferred advertised address.
- Changing the dropdown immediately regenerates the QR code.
- The dropdown contains all currently available advertised URLs.
- The selected QR address is a runtime choice, not a persisted preference.
- The runtime QR choice should be kept in memory while ALS is running, so hiding
  and reopening the QR dialog does not force the user to select the same address
  again.

This is important in field use: if a phone cannot reach the first URL, the user
can switch QR codes without stopping the server.

## Runtime Data Impact

The current runtime model stores one `web_server_ip`.

The rework likely needs runtime state for:

- the bind host, always `0.0.0.0`;
- the configured port;
- the selected advertised address;
- the selected advertised URL;
- the selected runtime QR address/URL, if the QR dialog has been manually
  switched during this ALS run;
- the full list of candidate advertised addresses/URLs.

For v0.7.1, the main window should display only the selected advertised URL.
Avoid adding a separate address-detail view as part of the first implementation.

Possible naming direction:

```python
DYNAMIC_DATA.web_server_bind_host
DYNAMIC_DATA.web_server_advertised_ip
DYNAMIC_DATA.web_server_advertised_url
DYNAMIC_DATA.web_server_qr_ip
DYNAMIC_DATA.web_server_qr_url
DYNAMIC_DATA.web_server_address_candidates
```

Exact names can change, but avoid continuing to use `web_server_ip` for both
binding and advertisement. That ambiguity is part of the current problem.

## Server Startup Impact

Port availability checks should match the actual bind behavior.

Current logic checks whether the chosen IP/port is in use. After binding to all
interfaces, checking only one advertised IP is not enough.

Preferred behavior:

- attempt the actual aiohttp bind on `0.0.0.0:<port>`;
- report bind failures back to the controller/UI;
- only mark the web server as running after bind success is known.

This is adjacent to, but separate from, address advertisement.

Also note the existing lifecycle concern: `Server` owns an event loop created in
`Server.__init__()`. If stop/start behavior is touched while implementing this
work, verify that the server can still restart cleanly after being stopped.

## Implementation Sequence

Implement this as a chain of small, behavior-focused commits. Each commit should
answer one review question, avoid unrelated cleanup, and keep generated UI churn
separate from hand-written logic where practical.

Suggested commit sequence:

1. Add pure IPv4 candidate discovery/ranking helpers in
   `src/als/streams/network.py` or a small adjacent module.
2. Add the persisted advertised-address preference default and accessors.
3. Add runtime fields for bind host, advertised address/URL, candidate list, and
   QR runtime address/URL.
4. Change server binding to `0.0.0.0` and make startup report bind failure
   accurately before the controller marks the server as running.
5. Resolve the advertised address during `Controller.start_www()` and update
   main/statusbar labels to use the selected advertised URL.
6. Add the Preferences address dropdown.
7. Add the QR address dropdown, including runtime memory for the last QR address
   selected during the current ALS run.
8. Regenerate generated UI files with `utils/compile_ui_and_rc.py`.
9. Add focused tests for address discovery/selection helpers if the current test
   setup supports them without requiring live network changes.
10. Update user-facing documentation and translatable strings only where the
    settled UI behavior requires it.

## Documentation Impact

User documentation should explain:

- ALS listens on all local network interfaces;
- the displayed address is the address another device should use;
- hotspot users may need to choose the hotspot/local-network address;
- firewall permissions can still block inbound access, especially on Windows
  and macOS.

## Testing Notes

Testing is intentionally deferred for now.

When this moves from design to implementation hardening, the address selection
logic should be isolated enough to test without live network changes. Useful
eventual cases include:

- one private LAN address selects that address;
- route address plus hotspot address keeps both candidates visible;
- configured IP present selects that IP;
- configured IP missing falls back to `Auto`;
- link-local is deprioritized below private IPv4;
- loopback is used only as fallback;
- virtual/VPN-looking addresses are deprioritized but still available.

## Executed Validations

The following validation was executed after the implementation work began. This
section records observed behavior without rewriting the original roadmap above.

- LAN-only setups were tested on all target platforms. The application behaved
  as expected: the web server started, advertised a reachable local address, and
  the browser view was accessible from another device on the same LAN.
- Web server stop/start and application restart flows were tested. The server
  restarted cleanly after being stopped, and the runtime server state updated as
  expected.
- QR runtime address switching was tested while the web server was running.
  Selecting another available address updated the QR target as expected, without
  changing the persisted Preferences address selection.

## Implementation Report

The v0.7.1 implementation follows the roadmap's main design direction: server
binding is separated from user-facing address advertisement.

The web server now binds to all IPv4 interfaces with `0.0.0.0`, while ALS
separately resolves an advertised local address for the main window, status bar,
Preferences, and QR dialog. Address discovery uses `psutil.net_if_addrs()` and
keeps the selection logic independent from Qt and aiohttp so it can be tested
without live network changes.

Implemented behavior:

- ALS discovers local IPv4 addresses and ranks them for Auto selection.
- Auto mode selects the highest-ranked discovered address.
- Private local addresses are preferred over link-local and loopback addresses.
- Virtual or VPN-looking interfaces are deprioritized, but their addresses remain
  available to the user.
- The server bind address is never used as the displayed browser URL.
- The preferred advertised address is persisted as either `auto` or
  `ip:<address>`.
- If a persisted IP address is no longer available, the UI falls back to Auto.
- Preferences expose the displayed server address without parsing display text.
- While the server is running, the displayed-address preference remains
  selectable, but port-number controls are disabled.
- When Preferences are accepted while the server is running, the main
  window/status advertised URL is refreshed from the selected displayed-address
  preference.
- The QR dialog exposes runtime address choices while the server is running.
- QR address switching updates the QR target without changing the persisted
  Preferences address.
- Web server startup waits for the actual bind result before marking the server
  as running.

Intentional implementation choices:

- Auto address selection intentionally uses only candidate scoring. The earlier
  default-route preference was removed to keep behavior simpler and easier to
  reason about across hotspot and multi-interface setups.
- Runtime QR state stores the selected QR URL, not a separate QR IP field. The
  URL is the value consumed by QR generation, so this avoids keeping duplicate
  runtime state synchronized.
- The legacy `web_server_ip` runtime field was removed after the new explicit
  advertised address fields replaced its remaining live-code usage.
- The temporary `web_server_bind_host` runtime field was also removed after bind
  behavior settled. Binding to `0.0.0.0` is handled directly by the server
  startup path rather than carried in dynamic runtime state.
- While the server is running, Preferences still allow changing the displayed
  address selection. Accepting the dialog updates the advertised URL shown in
  the main controls/status area. Only port-number controls are disabled because
  changing the port requires restarting the server.
- Preferences address changes do not reset the QR runtime URL. This keeps the QR
  dialog's runtime override independent from the persisted displayed-address
  preference.
- QR dialog UI was added to the translation project, the QR image placeholder
  was marked non-translatable, and FR/RU address-related translations were
  updated.
- Server startup error naming and user-facing messages still follow the existing
  port-oriented path. This is accepted for v0.7.1 because the expected
  actionable failure is a port collision, and broader error taxonomy can wait.
- Focused tests were added during implementation rather than deferred. They
  cover address discovery and selection, preference persistence, runtime state,
  QR address selection, Preferences port-control enablement, and advertised URL
  refresh after Preferences changes.
- Web server stop/start and restart remain covered by executed manual
  validation rather than an additional automated lifecycle test in this v0.7.1
  branch.
- The first v0.7.1 implementation remains IPv4-only, as planned.

## v0.7.1 Decisions

- Persist advertised-address preference as `auto` or `ip:<address>` only.
- Do not persist interface identity in the first implementation.
- Show a single selected advertised URL in the main window.
- Keep QR address changes runtime-only, with persistence controlled only by
  Preferences.
- Store the current runtime QR address in `DYNAMIC_DATA` or equivalent runtime
  state so closing and reopening the QR dialog keeps the user's last runtime
  choice.
- Use conservative generic labels for ambiguous adapters. Do not try to infer
  hotspot status aggressively from interface names or subnets.
- Explicitly ignore IPv6 for the first implementation.

## Codex Session Resume Point

- Latest implementation/review work can be resumed from Codex session
  `019e69b1-01ea-7201-9fc8-bd6f3fdae7f1`.
