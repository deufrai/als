---
title: "main controls"
description: "documentation of the main controls panel of ALS"
author: "ALS Team"
lastmod: 2024-12-31T17:55:17Z
keywords: [ "main controls of ALS" ]
type: "docs"
categories: [ "user guide" ]
tags: [ "interface", "controls", "stack", "session", "module", "threshold" ]
weight: 321
---

# Introduction

At the end of this chapter, you will have:

- Understood the organization and function of each section of the `Main Controls` panel
- Deepened your knowledge of the features controlled by these sections

<div class="row">
  <div class="col-md-8">

# Overview

The `Main Controls` panel is located on the left side of the interface.

It organizes the most used controls and displays into sections.

- [**Session**](#session-section)

  Session controls, stack information, and session status

- [**Stack**](#stack-section)

  Stacking settings: Alignment, stacking mode, and detection threshold

- [**Image Server**](#server-section)

  Image server controls and status

- [**Image Saver**](#saver-section)

  Image saving tools

- [**Workers**](#workers-section)

  Information on the usage status of the main modules

- [**Issues**](#issues-section)

  Issues indicator

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="The main controls panel" width="100%" alt="The main controls panel of ALS, with several sections: Session controls with START, PAUSE, and STOP buttons, Stack Size 39, Stack Exposure 0:02:36, Status started; Stack settings with Align, mean, and threshold slider at 19; Image server with START and STOP buttons, Status started with URL http://10.0.2.15:8000; Image saver with options Save current image and Save each image; Modules with Queue size and Busy status; Issues with a warning icon and the label Issues." >}}
  </div>

</div>

---

# Session {#session-section}

The **session** section of the panel includes 3 areas:

<div class="row">
<div class="col-md-8">

## Session Controls {#session-controls}

- <span class="als-ks">R</span> or 🖱️ click `START` to start a new session or resume a paused session.
- <span class="als-ks">R</span> or 🖱️ click `PAUSE` to pause the current session.
- <span class="als-ks">X</span> or 🖱️ click `STOP` to stop the current session.

{{% alert color="info" %}}
ℹ️ Stopping a session with at least one sub in the **stack** displays a confirmation prompt.
{{% /alert %}}

## Stack Information

Below the session controls, you will find information about the **stack**:

- the number of subs currently in the **stack**
- the cumulative exposure times of the subs in the **stack**.

_In this example, we have stacked 39 subs for a total of 2m 36s._

## Session Status

Finally, the status of the current session.

_In this example, the session is running._

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="session.png"
caption="The session section"
width="294px"
height="127px"
alt="User interface of the session section showing the START, PAUSE, and STOP buttons. Below, information about the current session: Stack Size 39, Stack Exposure 0:02:36, and status started." >}}
{{< /center >}}

</div>
</div>

---

# Stack {#stack-section}

The **stack** section of the panel controls the **Stacker** module.

<div class="row">
<div class="col-md-8">

## Alignment and Stacking Mode {#controls}

{{% alert color="info" %}}
ℹ️ These controls are accessible only when the session is stopped.
{{% /alert %}}
- <span class="als-ks">A</span> or 🖱️ check `Align` to enable subs **alignment**

- Use the dropdown list to set the **stacking mode** to use:
    - `mean`

      Used for electronically assisted astronomy or for monitoring a series of acquisitions.

      ⚙️ _The value of each pixel in the generated stack is the **average value** of that pixel across all subs in the **stack**._

    - `sum`

      Used for creating star trails or circumpolar images.

      ⚙️ _The value of each pixel in the generated stack is the **sum** of the values of that pixel across all subs in the **stack**._

## Detection Threshold {#threshold}

Alignment works by comparing the subs with the **alignment reference**, looking for similar star groups.

Poor quality subs, with too few or distorted stars, are discarded using a threshold:

Any sub with a number of similarities **below** this threshold is discarded.

🖱️ Use the `Threshold` slider to adjust the value of this **detection threshold**.

**When a sub is discarded**:

- The sub is not added to the stack and the **Stacker** module waits for the next sub.
- A **WARNING** is added to the **Session log**. It contains the text '_Alignment matches count is lower than configured threshold_'
- The `Acknowledge` button in the `Session Log` panel is activated.

  _If the_ `session log` _panel is hidden, the issue indicator appears in the_ **Issues** _section._

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="stack.png"
caption="The stack section"
width="294px"
height="92px"
alt="User interface of the stack section showing a checkbox labeled Align, checked, and a dropdown menu with the mean option selected. Below, a slider labeled Threshold set to 19, positioned towards the left side of its range." >}}
{{< /center >}}

</div>
</div>

{{% alert title="💡" color="light" %}}
- Aim to set the detection threshold as high as possible without causing sub discards.
- Lowering the stacking threshold is useful for long focal length shots where stars are few.
{{% /alert %}}

{{% alert title="ℹ️" color="info" %}}
- Alignment is enabled at each ALS startup.
- The stacking mode is set to **mean** at each ALS startup.
- The detection threshold is global and constantly saved.
{{% /alert %}}

---

# Image Server {#server-section}

The **Image Server** section of the panel controls the **Server** module.

<div class="row">
<div class="col-md-8">

## Server Controls

- <span class="als-ks">W</span> or 🖱️ click `START` to start the server.
- <span class="als-ks">W</span> or 🖱️ click `STOP` to stop the server.

## Server Information

Below the server controls, you will find its status display.

When the server is **started**:
- its URL is added to the status.
- <span class="als-ks">Q</span> toggles the display of the QR code for the server URL.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="server.png"
caption="The server section"
width="294px"
height="92px"
alt="The image server section, containing the 2 buttons START (grayed out) and STOP, the status: started and the server URL" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️" color="info" %}}
Additional settings for the web server are available in the [Preferences](../../preferences/).
{{% /alert %}}

---

# Image Saver {#saver-section}

The **Image Saver** section of the panel allows triggering additional saves beyond the default operation of the **Save** module.

<div class="row">
<div class="col-md-8">

## Save Controls {#save-controls}

- <span class="als-ks">S</span> or 🖱️ click `Save current` to save the **last** processing result with a timestamp.
- <span class="als-ks">F</span> or 🖱️ check `Save every frame` to enable saving **each next** processing result with a timestamp.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="saver.png"
caption="The image saver section"
width="294px"
height="69px"
alt="Image Saver section of the user interface showing a button labeled Save current image and a checkbox labeled Save each image. The checkbox is unchecked." >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
`Save every frame` is disabled at ALS startup.
{{% /alert %}}

---

# Modules {#modules-section}

The **Modules** section of the panel displays details of each main module.

- The size of the associated queue.
- The module status: Displays **busy** when the module is processing an image.

{{< center >}}
{{< figure src="modules.png"
caption="The Modules section"
width="294px"
height="153px"
alt="Modules section of the user interface showing a table with three columns: Modules, Queue size, and Status. The table lists four modules: Pre-process, Stack, Process, and Save. The queue size for all modules is 0. The status of the Stack module is busy, while the statuses of the other modules are indicated by a dash (-)." >}}
{{< /center >}}

---

# Issues {#issues-section}

When a new issue is detected **and the `Session Log` is hidden**, the `Issues` button appears in this section.

{{< center >}}
{{< figure src="problems.png"
caption="The issue indicator"
width="294px"
height="44px"
alt="The issues section with the issues button and its red panel" >}}
{{< /center >}}

<span class="als-ks">L</span> or 🖱️ click `Issues` to display the `Session Log` and review the new issues.

---

# Conclusion

The main controls of ALS are no longer a mystery to you!

Next step: the `Processing` panel.