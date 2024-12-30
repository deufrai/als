---
title: "Process Tab"
description: "Documentation of the Processing tab in ALS preferences"
author: "ALS Team"
lastmod: 2024-12-30T08:41:57Z
keywords: ["ALS processing settings", "ALS processing preferences"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["preferences", "processing", "Preprocess", "debayer", "dark", "hot pixels"]
weight: 332
---

The ALS processing settings are presented in the Preferences page `Process` tab

<div class="row">
<div class="col-md-6">

# Overview

This tab contains only one section: [Pre-processing](#preprocess)

It groups the settings of the processes managed by the [**Preprocess**](../../../modules/preprocess/) module:
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
alt="Preferences page Process tab" >}}
{{< /center >}}

</div>
</div>

# Pre-processing {#preprocess}

{{% alert color="info" %}}
ℹ️ These settings are only accessible when the session is stopped
{{% /alert %}}

## Hot pixel removal {#hot-remove}

{{< center >}}
{{< figure src="hot_remove.png"
caption="Hot pixel removal settings"
width="212px"
height="75px"
alt="Hot pixel removal settings" >}}
{{< /center >}}

`Use hot pixel remover` activates the removal

## Dark subtraction {#dark-remove}

{{< center >}}
{{< figure src="dark_remove.png"
caption="Dark signal subtraction settings"
width="589px"
height="173px"
alt="Dark signal subtraction settings" >}}
{{< /center >}}

1. `Use dark subtraction` activates the subtraction
2. `Change...` allows the selection of the master dark file 
3. `Clear` empties the master dark file path

{{% alert color="warning" %}}
⚠️ The master dark **must have the same dimensions** (_width x height_) as the image to be processed

If the dimensions are different:
- a **WARNING** message is added to the session log, with the message '_Data structure inconsistency_'
- The `Acknowledge` button in the `Session Log` is activated
- If the `session log` is hidden, the new problem indicator appears in the `Issues` section of the panel.
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ It is not mandatory for the data formats of the master dark and the image to be identical.

  In case of a difference (_e.g. master dark in 32-bit floats and raw in 16-bit integers_):
  - the master dark is converted before use
  - the format difference is discreetly reported in the session log
{{% /alert %}}

## Debayering pattern {#debayer}

{{< center >}}
{{< figure src="debayer.png"
caption="Debayering settings"
width="396px"
height="196px"
alt="Debayering settings" >}}
{{< /center >}}

{{% alert title="ℹ️ AUTO mode" color="info" %}}

The bayer pattern is extracted from the sub's metadata

If the metadata does not contain any pattern information:
  - The sub will not be debayered
  - Grid or checkerboard artifacts will be visible on the generated images

<details>
<summary>Searched Metadata</summary>

- FITS image: **BAYERPAT** FITS header
- Raw image: standard Exif header
</details>
{{% /alert %}}