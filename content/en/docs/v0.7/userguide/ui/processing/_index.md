---
title: "Processing"
description: "Documentation for the ALS Processing Panel"
author: "ALS Team"
lastmod: 2025-04-20T23:01:34Z
keywords: [ "ALS processing", "histogram", "auto stretch", "levels", "RGB balance", "sliders", "panels" ]
type: "docs"
tags: [ "histogram", "stretch", "sliders", "processing", "panels" ]
categories: [ "usage", "configuration" ]
weight: 322
---

# Introduction

In this chapter, you will learn how to improve your images using the `Processing` panel.

<div class="row">
<div class="col-md-8">

# Overview

The `Processing` panel is the control room for the **Process** module in ALS.

Located on the right side of the interface, it organizes image processing controls into several sections:

- [**Histogram**](#histogram-section)  
  A graphical representation of pixel intensity distribution.

- [**Auto Stretch**](#stretch-section)  
  Adjust the strength of the automatic stretch.

- [**Levels**](#levels-section)  
  Fine-tune overall exposure and adjust black and white clipping.

- [**RGB Balance**](#rgb-balance-section)  
  Adjust the red, green, and blue levels to correct color balance.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="panel.png" 
caption="The Processing Panel" 
width="345px"
height="670px"
alt="The ALS Processing Panel, including the Histogram, Auto Stretch, Levels, and RGB Balance sections with their respective sliders and controls." >}}
</div>
</div>

---

# Histogram {#histogram-section}

The **Histogram** provides a graphical representation of the intensity distribution of pixels within the currently displayed image.

This tool is essential for quickly evaluating tonal and color balance.

<div class="row">
<div class="col-md-8">

## Graph Properties

- **Horizontal Axis:** Indicates pixel intensity, ranging from shadows on the left (low intensity) to highlights on the right (high intensity).
- **Vertical Axis:** Represents the number of pixels at each intensity level. Higher peaks indicate more pixels within that tonal range.

## Monochrome Mode

For monochrome images, a single white curve is displayed, showing the intensity distribution of all pixels in the image.

## Color Mode

For color images, the histogram displays separate curves for the three channels: red, green, and blue. 

Each curve represents the intensity distribution for its respective channel, giving insight into each color’s contribution to the image.

Overlapping regions of the curves are colored to reflect the resulting mix of hues.

</div>

<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="histo.png"
caption="The Histogram Section"
width="318px"
height="147px"
alt="Dynamic histogram reflecting the distribution of intensity values in the image." >}}
{{< /center >}}
</div>
</div>

---

# Processing Controls {#controls-section}

This section consolidates the controls for the **Process** module and its three image processors:
- Auto Stretch
- Levels
- RGB Balance

The controls for each processor are grouped into sections, each with its own sliders and buttons:

## Adjustments

Each slider corresponds to an adjustable parameter. No numerical values are displayed, encouraging an intuitive and visual workflow.

{{% alert color="info" %}}
ℹ️ All sliders in this `Processing` panel feature an additional action:  
🖱️ **Double-click** the slider handle to reset it to its default position.
{{% /alert %}}

## Managing and Applying Settings

- `Apply` Generates a new image based on the current slider positions.  
  The central view and histogram update automatically once processing completes.
- `Default` Resets all sliders to their default positions without altering the currently displayed image.
- `Reload` Resets the sliders to their positions when `Apply` was last clicked, without modifying the currently displayed image.
- `Active` Enables or disables the processor. Changing this toggle generates a new image immediately, without needing to click `Apply`.

---

# Image Adjustments

## Auto Stretch {#stretch-section}

The **Auto Stretch** section adjusts the intensity of the automatic stretch applied to the image, making stacked images visually usable.

🖱️ Adjust the stretch intensity using the `Strength` slider.

ℹ️ Default: **An ideal balance, defined by us.**

## Levels {#levels-section}

<div class="row">
<div class="col-md-8">

### Black

🖱️ Adjust the `Black` slider to set the threshold for dark tones.

ℹ️ Default: Leftmost position.

- **Analyze the histogram:** Observe the far left of the histogram and check the distance between the curves and the left edge.
- **Goal:** Position the curves just touching the left edge to optimize dark tones without clipping.

*Moving the slider to the right shifts the curves to the left.*

### White

🖱️ Adjust the `White` slider to set the threshold for bright tones.

ℹ️ Default: Rightmost position.

- **Goal:** Visually balance the brightness of highlights while preserving details.

*Moving the slider to the left shifts the curves to the right.*

### Exposure

🖱️ Adjust the `Exposure` slider to control overall brightness.

ℹ️ Default: Center position.

- **Goal:** Find the brightness level that best highlights your target by trusting your eyes.

*Moving the slider to the right brightens the image.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="levels.png"
caption="Histogram after Levels adjustment"
width="318px"
height="147px"
alt="Histogram showing optimized tonal ranges after adjusting black and white points." >}}
</div>
</div>

## RGB Balance {#rgb-balance-section}

<div class="row">
<div class="col-md-12">
  {{% alert color="info" %}}
  ℹ️ Available only for color images.
  {{% /alert %}}

  The **RGB Balance** section adjusts the red, green, and blue levels for improved overall color balance.

  ### Analyze the Histogram

  Observe the relative positions of the main peaks of the three curves
</div>
</div>

<div class="row">
<div class="col-md-8">

  ### Your Goal

  Achieving a neutral color balance by vertically aligning the main peaks of the three curves is often a good starting point. 

  Aligning the peaks typically maximizes the white area in the histogram.

</div>

<div class="col-md-4 d-flex align-items-center justify-content-center flex-column">

  <div class="mb-3">
    {{< figure src="rgb.png"
    caption="Histogram of a color-neutral image"
    width="320px"
    height="146px"
    alt="Histogram showing aligned peaks for RGB curves in a color-neutral image." >}}
  </div>

</div>
</div>

<div class="row">
<div class="col-md-8">

{{% alert color="light" %}}
💡 Depending on your target and equipment, the histogram curves might not display distinct peaks.

For example, a target rich in H-alpha will show a flattened red curve without a clear peak.

The blended colors in the histogram effectively show the red dominance of the processed image.
{{% /alert %}}
</div>

<div class="col-md-4 d-flex align-items-center justify-content-center flex-column">

  <div>
    {{< figure src="h-alpha.png"
    caption="Histogram of an H-alpha target"
    width="320px"
    height="146px"
    alt="Histogram showing the red dominance of a correctly adjusted H-alpha image." >}}
  </div>

</div>
</div>

### Slider Actions

Each slider adjusts the horizontal position of its respective color curve.

*Moving the slider to the right shifts the curve to the right.*
