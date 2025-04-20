---
title: "Processing"
description: "Documentation for the ALS Processing Panel"
author: "ALS Team"
lastmod: 2025-04-20T01:29:27Z
keywords: [ "ALS processing", "histogram", "auto stretch", "levels", "RGB balance", "sliders", "panels" ]
type: "docs"
tags: [ "histogram", "stretch", "sliders", "processing", "panels" ]
categories: [ "usage", "configuration" ]
weight: 322
---

# Introduction

In this chapter, you will learn how to improve your images using the **Process** Module.

<div class="row">
<div class="col-md-8">

# Overview

The **Processing** panel is the control room of ALS's image processing capabilities.

Located on the right side of the interface, it groups the image processing controls into several sections:

- [**Histogram**](#histogram-section)  
  A visual representation of pixel intensity distribution.

- [**Auto Stretch**](#stretch-section)  
  Adjusts the strength of the automatic stretch.

- [**Levels**](#levels-section)  
  Fine-tunes global exposure as well as black and white clipping.

- [**RGB Balance**](#rgb-balance-section)  
  Adjusts the red, green, and blue levels for color correction.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="panel.png" 
caption="The Processing Panel" 
width="346px"
height="660px"
alt="The ALS Processing Panel, including the Histogram, Auto Stretch, Levels, and RGB Balance sections with their respective sliders and controls." >}}
</div>
</div>

---

# Histogram {#histogram-section}

The Histogram provides a graphical representation of the distribution of pixel intensity values within the image
displayed in the central area. This tool is essential for quickly assessing the balance of tones and colors.

<div class="row">
<div class="col-md-8">

### Graph properties

- **Horizontal Axis:** Indicates pixel intensity, ranging from shadows on the left (low intensity) to highlights on the
  right (high intensity).
- **Vertical Axis:** Represents the number of pixels at each intensity level. Higher peaks mean more pixels in that tonal
  range.

For monochrome images, a single white curve is displayed, showing the pixel intensity distribution across the entire image.

### Color Images

For color images, the histogram displays separate curves for the 3 color channels. Each curve represents the
pixel intensity distribution for its respective channel, providing insights into how each color contributes to the image.

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

This section provides controls for the **Process** module and its 3 image processors:
- Auto Stretch
- Levels
- RGB Balance

Controls for each processor are grouped into sections, each with its own set of sliders and buttons:

## Adjustments

Each slider corresponds to an adjustable parameter. No numerical values are displayed—this encourages a more intuitive
and visual approach.

{{% alert color="info" %}}
ℹ️ All sliders in this `Processing` panel have an additional feature:  
🖱️ **Double-click** the slider handle to reset it to its default position.
{{% /alert %}}

## Managing and Applying Settings

- `Apply` Generates a new image based on the current slider positions.  
  The central view and histogram will update once the processing is complete.
- `Default` Resets all sliders to their default positions without changing the currently displayed image.
- `Reload` Resets the sliders to the position they were in when `Apply` was last clicked, without changing the currently
  displayed image.
- `Active` Enables or disables the processor. A new image is immediately generated after changing this toggle,
  without needing to click `Apply`.

---

# Tweaking the Image

## Auto Stretch {#stretch-section}

The **Auto Stretch** section adjusts the intensity of the automatic stretch applied to the image, which is essential for
making stacked images visually usable.

🖱️ Use the `Strength` slider to adjust the amount of stretching.

ℹ️ Default: **An ideal balance magically defined by us.**

## Levels {#levels-section}

<div class="row">
<div class="col-md-8">

The **Levels** section allows you to adjust black and white points, as well as the overall image exposure.

### Black

🖱️ Use the `Black` slider to set the threshold for dark tones:

- **Analyze the histogram:** Look at the far left of the histogram and observe the distance between the curves and the
  left edge.
- **Objective:** Move the curves to just touch the left edge to optimize dark tones without clipping them.

  *Sliding to the right moves the curves to the left.*

### White Point

🖱️ Use the `White` slider to set the threshold for bright tones:

- **Objective:** Adjust this slider visually to balance the brightness of the highlights while preserving details and
  maintaining the overall aesthetic.

  *Sliding to the left moves the curves to the right.*

### Exposure

🖱️ Use the `Exposure` slider to control overall image brightness:

- **Objective:** Aim for proper exposure. Trust your eyes to find the brightness level that best highlights your target.

  *Sliding to the right brightens the entire image.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="levels.png"
caption="Histogram after Levels adjustment"
width="320px"
height="146px"
alt="Histogram showing optimized tonal ranges after precise adjustments to black and white points." >}}
</div>
</div>

## RGB Balance {#rgb-balance-section}

<div class="row">
<div class="col-md-8">

{{% alert color="info" %}}
ℹ️ Only available for color images.
{{% /alert %}}

The **RGB Balance** section adjusts the red, green, and blue levels to improve the overall color balance of the image.

### Analyze the Histogram

Observe the placement of the main peaks of the three color curves on the horizontal axis.

### Your Objective

- Achieving a neutral color balance by vertically aligning the main peaks of the three curves is often a good starting
  point.

  Areas where the curves overlap are colored according to the actual blending of the overlapping colors. Aligning peaks
  often maximizes the white area of the histogram.

- Use your judgment and knowledge of your target and setup: a neutral balance is not always desirable.

  Example: For a target dominated by H-alpha, keeping the global red tint is often preferred.

### Slider Actions

Each slider adjusts the horizontal position of the corresponding color curve.

*Sliding to the right shifts the associated curve to the right.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="rgb.png"
caption="Color balancing with RGB Balance"
width="320px"
height="146px"
alt="Histogram showing aligned peaks for RGB curves after precise adjustments." >}}
</div>
</div>

---

# Conclusion

With this chapter, you're now fully equipped to master the **Processing** panel! Use these features to refine your
images and bring out the best in them.

Next step: The Session Log.
