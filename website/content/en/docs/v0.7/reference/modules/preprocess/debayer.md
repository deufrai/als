---
title: "Debayering"
description: "Detailed documentation of the ALS Debayer process"
author: "ALS Team"
lastmod: 2025-01-12T13:54:13Z
keywords: [ "ALS debayer", "ALS debayering" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "debayer", "calibration" ]
weight: 355
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

READ_META[Pattern = Read metadata]
READ_PREF[Pattern = Read preferences]

DEBAYER[Debayering]
UNCHANGED[Return unchanged image]

RETURN[Return modified image]

END([END])

START --> TEST_AUTO

TEST_AUTO -- YES --> TEST_NEEDED
TEST_NEEDED -- YES --> READ_META
TEST_AUTO -- NO --> READ_PREF

READ_META --> DEBAYER
READ_PREF --> DEBAYER

TEST_NEEDED -- NO --> UNCHANGED

DEBAYER --> RETURN

UNCHANGED --> END
RETURN --> END


classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class TEST_AUTO,TEST_NEEDED test
class START,END bounds
class RETURN,UNCHANGED,DEBAYER,READ_META,READ_PREF step
```


The raw image is converted to a color image using the configured Bayer pattern.

- if configured pattern is set to **AUTO**, the pattern is taken from the image metadata.

# Output

The modified image is sent back to the **Preprocess** module.