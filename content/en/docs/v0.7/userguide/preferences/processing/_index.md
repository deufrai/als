---
title: "Process Tab"
description: "ALS Preferences Process Tab Documentation"
author: "ALS Team"
lastmod: 2025-01-05T10:44:51Z
keywords: ["ALS processing settings", "ALS processing preferences"]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["process", "debayer", "dark", "hot pixels", "calibration"]
weight: 332
---

The ALS processing settings are presented in the Preferences page `Process` tab

<div class="row">
<div class="col-md-6">

# Overview

This tab contains only one section: [Preprocess](#preprocess)

It gathers the settings for all **calibration** tasks:
- [Hot pixel removal](#hot-remove)
- [Dark subtraction](#dark-remove)
- [Debayering](#debayer)

</div>
<div class="col-md-6 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="Preferences page Process tab"
width="622px"
height="604px"
alt="ALS preferences window with Process tab selected, showing settings for pre-processing images, including hot pixel remover, dark subtraction, and debayering pattern options, with paths specified and Change and Clear buttons." >}}
{{< /center >}}

</div>
</div>

# Preprocess {#preprocess}

{{% alert color="info" %}}
ℹ️ These settings are only accessible when the session is stopped
{{% /alert %}}

## Hot pixel removal {#hot-remove}

{{< center >}}
{{< figure src="hot_remove.png"
caption="Hot pixel removal settings"
width="622px"
height="224px"
alt="Software interface showing the Pre-Processing category with an option to Use hot pixel remover checked." >}}
{{< /center >}}

- 🖱️ Check `Remove` to activate the hot pixel removal

ℹ️ Default : OFF

## Dark subtraction {#dark-remove}

{{< center >}}
{{< figure src="dark_remove.png"
caption="Dark subtraction settings"
width="622px"
height="213px"
alt="Software interface showing options to use dark subtraction, change the specified master dark path, and clear the path." >}}
{{< /center >}}

- 🖱️ Check `Active` to enable dark subtraction
- 🖱️ Click `Master dark...` to choose the master dark file to use for subtraction

  The configured master dark path is displayed to the right of the button
- 🖱️ Click `Clear` to clear the master dark file path

{{% alert color="warning" %}}
⚠️ The master dark **must have the same dimensions** (_width x height_) as the image to be processed

If the dimensions are different:
- Each subtraction attempt will add a **WARNING** message to the session log:

  _data structure inconsistency - dark subtraction is IGNORED_
- The `Acknowledge` button in the `Session log` is activated
- If the `session log` is hidden, the new issues indicator appears in the `Issues` section of the panel.
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ It is not mandatory for the master dark and  sub data formats to be identical

  In case of a difference (_e.g., master dark in 32-bit floats and raw in 16-bit integers_):
  - The master dark is converted before use
  - The format difference is discreetly noted in the session log
{{% /alert %}}

ℹ️ Default : OFF

## Debayering pattern {#debayer}

{{< center >}}
{{< figure src="debayer.png"
caption="Debayering settings"
width="622px"
height="293px"
alt="Software interface showing image processing preferences with options for setting Dark path and selecting Debayering pattern, including AUTO and various color filter array patterns." >}}
{{< /center >}}

{{% alert title="ℹ️ AUTO mode recommended" color="info" %}}

The bayer pattern is extracted from the sub's metadata and **works most of the time.**

If the metadata does not contain any pattern information:
  - The sub will not be debayered
  - Grid or checkerboard artifacts will be visible on the generated images

<details>
<summary>Searched Metadata</summary>

- FITS image: **BAYERPAT** FITS header
- Raw image: standard Exif header
</details>
{{% /alert %}}

{{% alert color="light" %}} 
💡 Manual Bayer pattern selection is useful in the following cases:
- Image metadata does not contain the Bayer pattern
- AUTO mode does not provide the expected result (_i.e. grid or checkerboard on the debayered image_)
{{% /alert %}}

ℹ️ Default : AUTO
