---
title: "Main Controls"
description: "documentation of ALS main controls panel"
author: "ALS Team"
lastmod: 2024-12-31T02:35:04Z
keywords: [ "ALS main controls" ]
type: "docs"
tags: [ "GUI", "controls", "stack" ]
weight: 321
---

# Introduction

By the end of this chapter, you will have:

- Understood the organization and function of each section of the `Main controls` panel
- Deepened your knowledge of the ALS features controlled by these sections

---

# General Presentation

The `Main Controls` panel is located on the left side of the ALS interface. It groups the most used controls and
displays into sections.

<div class="row">
  <div class="col-md-8">

- [**Session**](#session-section)

  The controls for the current session are found here. They allow you to start and stop the session, and also display
  information about the current stack as well as the session status indicator.

- [**Stack**](#stack-section)

  This section allows you to define the alignment and stacking modes for images. It also offers a threshold setting for
  similarity search during alignment.

- [**Image Server**](#server-section)

  Allows you to start and stop the image server and displays information about the server when it is active.

- [**Image Saver**](#saver-section)

  Allows you to save the current image on the fly and activate continuous saving.

- [**Workers**](#workers-section)

  This section provides information about the usage status of each ALS worker module.

- [**Issues**](#issues-section)

  This section is only visible if the `Session Log` is hidden. It displays an indicator of new issues.

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="The main controls panel" width="100%" alt="The main controls panel, featuring sections for Session, Stack, Image Server, Image Saver, Workers, and Issues. The Session section includes buttons labeled START, PAUSE, and STOP, with indicators for stack size (20) and stack exposure (0:01:20), and a status reading 'running'. The Stack section shows options for alignment (mean) and a threshold slider set to 19. The Image Server section has START and STOP buttons and displays the status 'running' with the URL http://10.0.2.15:8000. The Image Saver section includes a button labeled Save current and a checkbox labeled Save every frame. The Workers section provides queue sizes and status indicators for Pre-process, Stack, Process, and Save modules. The Issues section displays a red warning icon with the text 'Issues'." >}}
  </div>

</div>

--- 

# Session {#session-section}

The **session** section of the panel includes 3 areas, from top to bottom:

<div class="row">
<div class="col-md-8">

## Session Controls

The accessibility of these buttons depends on the session status.

- `START` Starts a new session or resumes paused session.
- `PAUSE` Pauses the current session.
- `STOP` Stops the current session.

  Stopping a session with at least one image in the stack triggers a confirmation window.

## Information about the current stack

- The total number of images stacked in the current stack.
- The total exposure time for the entire session.

_In this example, we have stacked 20 images for a total exposure time of 1m 20s._

## Session Status

The status of the current session. Possible statuses are:

- stopped
- running
- paused

_In this example, the session is running._

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="session.png"
caption="The session section"
width="280px"
height="127px"
alt="User interface for the session section showing the START, PAUSE, and STOP buttons. Below, information about the current session: Stack size 20, Stack exposure 0:01:20, and status running." >}}
{{< /center >}}

</div>
</div>

---

# Stack {#stack-section}

The **stack** section of the panel allows you to control the **stack** module.

<div class="row">
<div class="col-md-8">

## Aligning and Stacking mode {#controls}

{{% alert color="info" %}}
These controls are only accessible only when the session is stopped
{{% /alert %}}

- `Align` activates the **alignment** of subs on the session reference.
- The dropdown list defines the **stacking mode** used for this session:
- `mean` : The value of each pixel in the generated image is the **average value** of that pixel in all the images in
  the
  stack.
- `sum` : The value of each pixel in the generated image is the **sum** of the values of that pixel in all the images in
  the stack.

## Detection Threshold {#threshold}

Subs of poor quality are discarded using a similarities threshold:

Any sub having a number of similarities with the session reference **below** this threshold is ignored.

The `Threshold` slider allows you to set this detection threshold.

**Behavior when an image is ignored**:

- The image is not added to the stack. The **Stack** module waits for the next image.
- A **WARNING** is added to the `Session Log`. It includes the text '_Alignment matches count is lower than configured
  threshold_'.
- The `Acknowledge` button in the `Session Log` is activated.
- If the `Session Log` is hidden, the new issues indicator appears in the `Issues` section of the panel.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="stack.png"
caption="The stack section"
width="280px"
height="92px"
alt="User interface for the stack section showing a checkbox labeled Align, checked, and a dropdown menu set to mean. Below, a slider labeled Threshold set to 19, positioned towards the left end of its range." >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}

- `Align` is enabled on every ALS startup
- The stacking mode is set to `mean` on every ALS startup
- The detection threshold is global and constantly saved
  {{% /alert %}}

{{% alert title="💡 TIP" color="light" %}}
Reducing the detection threshold is useful for long focal length shots where stars are few.
{{% /alert %}}

---

# Image Server {#server-section}

The **Image Server** section of the panel allows you to control ALS's integrated web server.

This server shares the image displayed in ALS's central area on the network to which the machine running ALS is
connected.

The image displayed in the served web page is periodically refreshed by the browser.

<div class="row">
<div class="col-md-8">

## Server Controls

- `START` starts the server.
- `STOP` stops the server.

## Server Information

Displays the current status of the server. Possible statuses are:

- stopped
- running

When the server is running:

- its URL is added to the status.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="server.png"
caption="The server section"
width="280px"
height="92px"
alt="The image server section, containing the START (grayed out) and STOP buttons, the status: running, and the server URL" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
Additional parameters for the web server are available in the [ALS Preferences](../../preferences/). Tab **Output**
section **Web Server**.
{{% /alert %}}

---

# Image saver {#saver-section}

The **Image Saver** section of the panel allows you to trigger additional file saves beyond the default operation
of the **Save** module.

<div class="row">
<div class="col-md-8">

## Saving Controls {#save-controls}

- `Save current` triggers the saving of the **last** result of the **Process** module into a new timestamped file:
    - **File location**: **work folder**
    - **File name**: composed of **stack_image** and a timestamp suffix.
    - **File type and extension**: as defined [ALS Preferences](../../preferences/output/#format).

- `Save every frame` activates the saving of **each next** result of the **Process** module into a new timestamped file:
    - **File location**: **work folder**
    - **File name**: composed of **stack_image** and a timestamp suffix.
    - **File type and extension**: as defined [ALS Preferences](../../preferences/output/#format).

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="saver.png"
caption="The Image Saver section"
width="280px"
height="68px"
alt="Image Saver section of the user interface showing a button labeled Save current and a checkbox labeled Save every frame. The checkbox is unchecked." >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
`Save every frame` is disabled on ALS startup.
{{% /alert %}}

---

# Workers {#workers-section}

The **Workers** section of the panel displays the details of each main module

- The size of the associated queue
- The status of the module: Displays **busy** when the module is processing an image

{{< center >}}
{{< figure src="modules.png"
caption="The Modules section"
width="280px"
height="153px"
alt="Workers section of the user interface showing a table with three columns: Workers, Queue size, and Status. The table lists four workers: Pre-process, Stack, Process, and Save. The queue sizes for all workers are 0. The status for the Stack worker is busy, while the statuses for the other workers are indicated with a dash (-)." >}}
{{< /center >}}

---

# Issues {#issues-section}

When a new issue is detected by ALS **and the `Session Log` is hidden**, an indicator appears at the bottom of the
`main controls` panel.

{{< center >}}
{{< figure src="problems.png"
caption="New issue indicator"
width="280px"
height="44px"
alt="the Issues section with its Issues button and its red sign" >}}
{{< /center >}}

Clicking on this button displays the `Session Log` and allows you to review the newly detected issues.

---

# Conclusion

You now have a clear understanding of the architecture of ALS and the various sections of the `main controls` panel.

Next step: the `Processing` panel.
