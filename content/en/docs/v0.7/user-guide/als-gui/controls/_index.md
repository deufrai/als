---
title: "The Main Controls Panel"
description: "documentation of the ALS main controls panel"
author: "ALS Team"
lastmod: 2024-12-30T01:50:00Z
keywords: [ "ALS main controls" ]
type: "docs"
tags: [ "GUI", "controls" ]
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
    {{< figure src="controls.png" caption="The main controls panel" width="100%" alt="main controls panel" >}}
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
alt="Session section" >}}
{{< /center >}}

</div>
</div>

---

# Stack {#stack-section}

The **stack** section of the panel allows you to control the **stacking module**.

This module is responsible for aligning and stacking every detected images.
Alignment can be disabled, and two stacking modes are available.

<div class="row">
<div class="col-md-8">

## Controls of the current stack

_These controls are accessible only when the session is stopped._

- `Align` checkbox: activates the **alignment** of detected images on the session reference.
- Dropdown list of **stacking modes**: Allows you to define the **stacking mode** used for this session:
    - `mean`: each pixel of the resulting image is the average of the corresponding pixels of each image in the
      current stack.
    - `sum`: each pixel of the resulting image is the sum of the corresponding pixels of each image in the current
      stack.

## Similarity Search Threshold

When alignment is enabled, ALS determines the transformations to apply to each new image based on a similarity search
(**groups of 3 stars**) between the new image and the session reference.

To exclude images of too poor quality, ALS uses a similarity detection threshold: Any image with a number of
similarities below this threshold will be ignored.

The `Threshold` slider allows you to set this threshold in real-time.

- **Possible values**: 5 to 60.
- **Default value**: 25.
- **Behavior when an image is ignored**:
    - The image is not added to the stack. ALS waits for the next image.
    - A message is added to the `Session Log`. It contains, among other things, the text _Alignment matches count is
      lower than configured threshold_
    - The `Acknowledge` button in the `Session Log` is activated.
    - If the `Session Log` is hidden, the new issues indicator appears in the `Issues` section of the panel.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="stack.png"
caption="The stack section"
width="280px"
height="92px"
alt="Stack section" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}

- `Align` is enabled on ALS startup
- The stacking mode is set to `mean` on ALS startup
- The similarity search threshold is remembered when you exit ALS
  {{% /alert %}}

{{% alert title="💡 TIP" color="light" %}}
If the field imaged by your system contains few stars, it may be necessary to reduce the threshold in order to avoid
ignoring most images.
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
alt="Server section" >}}
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

## Saving Controls

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
caption="The Image Recorder section"
width="280px"
height="68px"
alt="Image Recorder section" >}}
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
alt="Modules section" >}}
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
alt="New issue indicator" >}}
{{< /center >}}

Clicking on this button displays the `Session Log` and allows you to review the newly detected issues.

---

# Conclusion

You now have a clear understanding of the architecture of ALS and the various sections of the `main controls` panel.

Next step: the `Processing` panel.
