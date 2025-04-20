---
title: "Session Log"
description: "Documentation for the ALS Session Log Panel"
author: "ALS Team"
lastmod: 2025-04-20T17:32:13Z
keywords: [ "session log", "follow", "errors", "log", "panels" ]
type: "docs"
tags: [ "log", "issues", "errors", "panels" ]
categories: [ "usage" ]
weight: 323
---

# Introduction

This section explains how to stay informed about events occurring during your session.

# Overview

The `Session Log` is divided into two main parts:

- [**Log View:**](#log-view) A chronological list of recorded messages displayed in real time.
- [**Control Buttons:**](#control-buttons) Interactive options to filter, follow, and manage log entries.

It is designed not only to monitor processes but also to assist in troubleshooting and performance analysis.

{{< center >}}
{{< figure src="log.png"
caption="The Session Log Panel"
width="1307px"
height="210px"
alt="The ALS Session Log Panel displaying processing messages." >}}
{{< /center >}}

---

# Log View {#log-view}

The **Log View** displays messages in chronological order, with the most recent ones at the bottom.

Each entry includes:
- **Timestamp:** The exact time the message was recorded.
- **Type:** The importance level of the message, such as INFO, WARNING, or ERROR.
- **Details:** A description of the event.

When an unexpected event occurs during a session (e.g., file processing error or task failure), it is logged as a **WARNING** or **ERROR** depending on its severity:
- **WARNING:** A problem that can likely be ignored without significantly affecting the session.
- **ERROR:** A problem that may impact the session’s results.

Examples of messages:
- INFO: Image saved: web_image.jpg
- WARNING Could not stack image \[...\] Image is DISCARDED
- ERROR: Failed to save image \[...\]

### Copying Messages

Clicking on any log entry automatically copies its content to the clipboard, making it easier to share or analyze.

---

# Control Buttons {#control-buttons}

The `Session Log` panel includes several buttons to manage the display and alerts.

<div class="row">
<div class="col-md-8">

## Acknowledge

The `Acknowledge` button is paired with a built-in issue indicator.  
The indicator appears on the button whenever a new issue is detected, helping you quickly identify critical events.

🖱️ Click `Acknowledge` to confirm you’ve reviewed the new messages. The indicator disappears.

## Issues Only

The `Issues Only` button allows you to filter the log to display only critical messages.

🖱️ Click `Issues Only` to toggle the filter on or off.

ℹ️ Default: OFF

## Follow

The `Follow` button ensures that the latest message in the log is always visible.

🖱️ Click `Follow` to enable or disable automatic scrolling to the newest message.

ℹ️ Default: ON

</div>

<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="controls.png"
caption="The Session Log Control Buttons"
width="164px"
height="210px"
alt="The Follow, Issues Only, and Acknowledge buttons on the Session Log Panel." >}}
{{< /center >}}
</div>
</div>

---

# Conclusion

Now you know how to stay informed throughout your sessions.

Next step: Discover the invaluable keyboard shortcuts.
