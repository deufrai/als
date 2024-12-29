---
title: "Process Tab"
description: "Documentation of the Processing tab in ALS preferences"
author: "ALS Team"
lastmod: 2024-12-29T22:57:32Z
keywords: ["ALS processing settings", "ALS processing preferences"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["preferences", "processing", "Pre-process", "debayer", "dark", "hot pixels"]
weight: 332
---

The ALS processing settings are presented in the Preferences page `Process` tab

<div class="row">
<div class="col-md-6">

# Overview

This tab contains only one section: [Pre-processing](#preprocess)

It groups the settings of the processes managed by the [**Pre-process**](../../modules/preprocess/) module:
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

## Hot pixel remover {#hot-remove}

- Activation

    |           |          |
    |-----------|----------|
    |Data type  | ON / OFF |
    | Required  | ∅        |
    | Default value | OFF  |

{{< center >}}
{{< figure src="hot_remove.png"
caption="Hot pixel removal settings"
width="212px"
height="75px"
alt="Hot pixel removal settings" >}}
{{< /center >}}

The `Use hot pixel remover` checkbox allows you to enable or disable hot pixel removal.

## Dark subtraction {#dark-remove}

- Activation

    |           |          |
    |-----------|----------|
    |Data type  | ON / OFF |
    | Required  | ∅        |
    | Default value | OFF  |

- Master dark file path

    |           |                            |
    |-----------|----------------------------|
    |Data type  | Path to a file             |
    | Required  | When the process is ON     |
    | Default value | ∅                      |

{{< center >}}
{{< figure src="dark_remove.png"
caption="Dark signal subtraction settings"
width="589px"
height="173px"
alt="Dark signal subtraction settings" >}}
{{< /center >}}

1. Activate subtraction with the `Use dark subtraction` checkbox.
2. Click the `Change...` button to pick the master dark file to use for the subtraction. 
3. The `Clear` button allows you to empty the master dark file path.

{{% alert color="warning" %}}
⚠️ The master dark **must have the same dimensions** (_width x height_) as the image to be processed
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ It is not mandatory for the data formats of the master dark and the image to be identical.

  In case of a difference (_e.g. master dark in 32-bit floats and raw in 16-bit integers_):
  - the master dark is converted before use
  - the format difference is discreetly reported in the session log
{{% /alert %}}

## Debayering {#debayer}

- Debayering pattern
    
    |           |                                                                   |
    |-----------|-------------------------------------------------------------------|
    |Data type  | choice:<br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR         |
    | Required  | YES                                                               |
    | Default value | AUTO                                                          |
    

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