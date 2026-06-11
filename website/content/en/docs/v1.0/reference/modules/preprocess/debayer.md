---
title: "Debayering"
description: "Detailed documentation of the ALS Debayer process"
author: "ALS Team"
lastmod: 2026-06-11T22:56:10Z
keywords: [ "ALS debayer", "ALS debayering" ]
draft: false
type: "docs"
categories: [ "detailed documentation" ]
tags: [ "processing", "debayer", "calibration" ]
weight: 100356
---

# Overview

The **Debayer** process is used on **color** images in **FITS** or **Raw** format.

It generates a color image from the raw image and the description of the Bayer pattern installed on the sensor that
generated the image.

Its configuration is managed via ALS preferences page.

# Configuration

|               | Source                                                                            | Data Type                                                  | Required | Default Value |
|---------------|-----------------------------------------------------------------------------------|------------------------------------------------------------|----------|---------------|
| Bayer pattern | Preferences: [Processing Tab](../../../userguide/preferences/processing/#debayer) | choice: <br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR | YES      | AUTO          |

# Control

This process is triggered by the **Preprocess** module.

# Input

| Data                                          | Type  |
|-----------------------------------------------|-------|
| image received from the **Preprocess** module | Image |

# Behavior

```mermaid
graph LR

START([START])

TEST_AUTO{{Preferences = AUTO?}}
TEST_NEEDED{{Debayering needed?}}
TEST_DATA_TYPE{{8-bit or 16-bit<br>unsigned integer data?}}

READ_META[Pattern = Read metadata]
READ_PREF[Pattern = Read preferences]

DEBAYER[Debayering]
UNCHANGED[Return unchanged image]
IGNORED[Skip sub]

RETURN[Return modified image]

END([END])

START --> TEST_AUTO

TEST_AUTO -- YES --> TEST_NEEDED
TEST_NEEDED -- YES --> READ_META
TEST_AUTO -- NO --> READ_PREF

READ_META --> TEST_DATA_TYPE
READ_PREF --> TEST_DATA_TYPE

TEST_DATA_TYPE -- YES --> DEBAYER
TEST_DATA_TYPE -- NO --> IGNORED

TEST_NEEDED -- NO --> UNCHANGED

DEBAYER --> RETURN

UNCHANGED --> END
IGNORED --> END
RETURN --> END


classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class TEST_AUTO,TEST_NEEDED,TEST_DATA_TYPE test
class START,END bounds
class RETURN,UNCHANGED,IGNORED,DEBAYER,READ_META,READ_PREF step
```


The raw image is converted to a color image using the configured Bayer pattern.

- if configured pattern is set to **AUTO**, the pattern is taken from the image metadata.

{{% alert color="warning" %}}
Subs requiring debayering must contain 8-bit or 16-bit unsigned integer data. Subs using another data type cannot be
debayered and are skipped.
{{% /alert %}}

# Output

- Subs successfully debayered are sent back to the **Preprocess** module as modified color images.
- When the Bayer pattern preference is set to **AUTO**, mono subs and already-debayered color subs are sent back
  unchanged.
- Subs that cannot be debayered are skipped and produce no output.
