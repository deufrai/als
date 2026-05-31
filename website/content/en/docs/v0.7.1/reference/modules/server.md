---
title: "Server"
description: "Detailed documentation of the ALS image server module"
author: "ALS Team"
lastmod: 2026-05-31T12:11:39Z
keywords: ["ALS image server", "ALS web module", "ALS remote view"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "server", "utility", "web", "stream"]
weight: 71362
---

# Overview {#overview}

The **Server** utility module exposes ALS processing results through a lightweight HTTP and WebSocket service.

It is responsible for:

- Publishing the **latest stacked image** and session metrics in the configured **web folder**
- Serving the **viewer web application** (`index.html`, JavaScript and icons)
- Streaming live **new-image notifications** to connected browsers over WebSockets

The module runs in its own asyncio event loop and accepts concurrent browser clients. It never alters the processing 
pipeline; it only serves the web image written by the **Save** module.

{{% alert color="info" %}}
ℹ️ The server delivers the content stored in the **web folder**. By default, this folder is an alias of the 
**work folder**; you can dedicate a separate folder from the [Output preferences](../../userguide/preferences/output/#web-dedicated).
{{% /alert %}}

# Configuration {#configuration}

| Setting                   | Source                                                                           | Data Type            | Required  | Default Value        |
|---------------------------|----------------------------------------------------------------------------------|----------------------|-----------|----------------------|
| **Web Folder**            | Preferences: [Output Tab](../../userguide/preferences/output/#web-folder)        | Path to a folder     | Yes       | Work folder alias    |
| **Dedicated Web Folder**  | Preferences: [Output Tab](../../userguide/preferences/output/#web-dedicated)     | Boolean              | No        | Disabled             |
| **Displayed Address**     | Preferences: [Output Tab](../../userguide/preferences/output/#server-address)    | String (`auto` or `ip:<address>`) | Yes       | Auto - recommended   |
| **Port Number**           | Preferences: [Output Tab](../../userguide/preferences/output/#server-port)       | Integer (1024–65535) | Yes       | 8000                 |

# Control {#control}

| Source                                                             | Type              | Response                                                                                            |
|--------------------------------------------------------------------|-------------------|-----------------------------------------------------------------------------------------------------|
| [`Main controls`](../../userguide/ui/controls/#server-section) | Command: `START`  | Prepare web assets and launch the server thread                                                     |
| [`Main controls`](../../userguide/ui/controls/#server-section) | Command: `STOP`   | Notify clients and shut the server down. Keep web assets available on disk                          |

# Outputs {#outputs}

Once started, the module maintains the following artefacts inside the web folder:

| Artefact                      | Description                                                              |
|-------------------------------|--------------------------------------------------------------------------|
| `index.html`                  | The embedded viewer that displays the live stacked image                 |
| `favicon.ico` & `icons/*.png` | Viewer assets copied from the ALS resources bundle                       |
| `data.json`                   | Session metrics (`STACK_SIZE`, `EXPO`) refreshed after each stack update |
| `web_image.jpg`               | Latest processed frame saved in JPEG for browser consumption             |
| `openseadragon.min.js`        | Deep-zoom viewer script used by the web interface                        |

# Behavior {#behavior}

## Startup sequence {#startup-sequence}

1. **Publish static assets** — `index.html`, icons, and the waiting image are written (or refreshed) in the web folder so that first-time clients load instantly.
2. **Expose session metrics** — `data.json` is generated with the current stack size and cumulative exposure time.
3. **Validate availability** — the module attempts the actual server bind on `0.0.0.0:<port>`. A `PortInUseError` is raised if the configured port cannot be used.
4. **Run the server loop** — an asyncio loop starts in a dedicated thread, serves HTTP on all local IPv4 interfaces, and accepts WebSocket connections on `/ws`.
5. **Advertise availability** — ALS resolves the configured **Displayed Address** preference and updates its UI with the selected address.

## Binding and displayed address {#binding-and-displayed-address}

The bind address and the displayed address are intentionally separate:

- The server binds to `0.0.0.0` so it can accept connections through any available local IPv4 interface.
- The **Displayed Address** is a concrete local address that another device can use to browse the image server.

If the selected **Displayed Address** is a loopback address, the module keeps running but reports that image server access is limited so that you can choose another **Displayed Address** when one is available.

## Live updates {#live-updates}

- After each processed image, the latest JPEG and `data.json` are overwritten in the web folder.
- `notify_browsers_about_new_image()` pushes `{ "type": "new_image" }` to all WebSocket clients so that browsers reload the image without polling.
- The same infrastructure is used to deliver `{ "type": "disconnect" }` right before shutdown, allowing clients to display an appropriate message.

## Shutdown {#shutdown}

When the `STOP` command is triggered:

1. All connected clients receive a `disconnect` message.
2. The module waits briefly (2 seconds) for browsers to close the socket.
3. The asyncio runner is cleaned up and the dedicated thread stops.
4. UI status and QR code are reset; the static files remain on disk for the next session.

# WebSocket reference {#websocket-reference}

| Message      | Payload                    | Trigger                                     |
|--------------|----------------------------|---------------------------------------------|
| `new_image`  | `{ "type": "new_image" }`  | A freshly processed frame becomes available |
| `disconnect` | `{ "type": "disconnect" }` | Server is shutting down                     |

{{% alert title="Troubleshooting" color="warning" %}}
- Change the port number in preferences if ALS reports that the port is already in use.
- If another device cannot browse the image server, select a **Displayed Address** that belongs to the same network as the browser device, then retry the URL or QR code.
- Check that your firewall allows inbound connections on the configured port.
{{% /alert %}}
