---
title: "The Main Controls Panel"
description: "documentation of the ALS main controls panel"
author: "ALS Team"
lastmod: 2024-12-27T09:52:30Z
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

- **Session**

The controls for the current session are found here. They allow you to start and stop the session, and also display
information about the current stack as well as the session status indicator.

- **Stack**

This section allows you to define the alignment and stacking modes for images. It also offers a threshold setting for
similarity search during alignment.

- **Image Server**

Allows you to start and stop the image server and displays information about the server when it is active.

- **Image Saver**

Allows you to save the current image on the fly and activate continuous saving.

- **Workers**

This section provides information about the usage status of each ALS worker module.

- **Issues**

This section is only visible if the `Session Log` is hidden. It displays an indicator of new issues.

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="The main controls panel" width="100%" alt="main controls panel" >}}
  </div>
</div>

--- 

# Session

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

# Stack

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
If the field imaged by your system contains few stars, it may be necessary to reduce the threshold in order to avoid
ignoring most images.
{{% /alert %}}

---

# Image Server

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

# Image saver

The **Image saver** section of the panel allows you to control the saving of images produced by ALS.

After the complete processing of each new image, ALS saves the image from the central area in a file in the **work
folder**:

- **File name**: **stack_image**

  The file is overwritten with each new image.

- **File type and extension**: according to the saving format chosen in the [ALS Preferences](../../preferences/).

  By default: **JPEG** format and **.jpg** extension.

The saving controls allow you to trigger additional saves.

<div class="row">
<div class="col-md-8">

## Saving Controls

- `Save current` button: Triggers the recording of the image from the central area into a new file in the
  **work folder**:
    - **File name**: composed of **stack_image** and a timestamp suffix.
    - **File type and extension**: according to the saving format chosen in
      the [ALS Preferences](../../preferences/).

- `Save every frame` checkbox: Activates the recording of each next processing result into a new file in the **work
  folder**:
    - **File name**: composed of **stack_image** and a timestamp suffix.
    - **File type and extension**: according to the saving format chosen in
      the [ALS Preferences](../../preferences/).

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
An example of a timestamped file name: **stack_image-2024-12-27-06-20-24-091899.jpg**.
{{% /alert %}}

---

# Workers

This section provides an opportunity to better describe the architecture of ALS and the flow of images through the
application.

## ALS Architecture and worker modules

All image processing tasks are distributed across four main modules.

Each module is assigned a queue and processes all images in its queue sequentially.

Each module places its successive processing results in the queue of the next module.

The modules are organized in the following order:

### Pre-process

As soon as a new image is detected in the **scan folder**, it is added to the queue of this module.

The **pre-process** module applies the usual astrophotography preprocessing in order :

- **Hot pixel removal**: Replaces the value of hot pixels with the average value of neighboring pixels.
  This processing can be disabled in the [ALS Preferences](../../preferences/).
- **Dark frame subtraction**: Uses a dark frame provided by the user to subtract the thermal noise from the image. The
  path to the dark frame and the activation of this processing are defined in the
  [ALS Preferences](../../preferences/).

  If the data format of the provided dark frame is not the same as that of the image to be processed, ALS performs a
  conversion on-the-fly of the dark frame before subtraction.

- **Demosaicing**: In the case of a color image saved in a FITS or Raw file, converts the image to RGB color using the
  Bayer matrix described in the file headers.

  <details>
    <summary>Click here for details on the headers used</summary>

    - FITS file: Standard FITS header **BAYERPAT**
    - Raw file: Standard EXIF header

  </details>

  An option in the [ALS Preferences](../../preferences/) allows you to either let ALS decide or explicitly define the
  Bayer matrix to be used. This option is useful if ALS does not correctly detect the matrix or if the file
  does not contain the expected header.

### Stack

Handles the alignment and stacking of images.

- **Alignment**
    - Calculates the transformations to be applied to the current image to align it with the session reference
    - Applies the transformations to the current image
- **Stacking**
    - Adds the current image to the current stack
    - Calculates the resulting image based on the chosen stacking mode

The detailed operation of these processes was covered in the **Stack** section.

### Process

Post-processing module. It includes the following processes:

- **Auto-stretch**: Automatically adjusts the image levels to maximize contrast
- **Exposure settings**: Allows adjustment of the black levels, white levels, and mid-gray level of the image
- **RGB balance**: Allows adjustment of the color balance of the image

The details of these processes will be covered on the page dedicated to the **Processing** panel.

### Save

Image saver module.

The detailed operation of the image saver was described in the **Image Recorder** section.

## Modules display

The **Modules** section of the panel displays, for each module:

- The size of the associated queue
- The usage status of the module

  Displays **busy** when the module is processing an image

{{< center >}}
{{< figure src="modules.png"
caption="The Modules section"
width="280px"
height="153px"
alt="Modules section" >}}
{{< /center >}}

---

# Issues

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
