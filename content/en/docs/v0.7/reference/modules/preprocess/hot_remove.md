---
title: "Hot Pixel Removal"
description: "Detailed documentation of the ALS HotPixelRemove process"
author: "ALS Team"
lastmod: 2025-01-07T17:57:43Z
keywords: ["ALS hot pixel removal", "ALS hot pixel suppression"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["process", "hot pixels", "calibration"]
weight: 353
---

# Overview

The **HotPixelRemove** process removes hot pixels from the image.

Its configuration is managed via ALS preferences.

# Configuration

|        | Source                                                                                | Data Type | Required | Default   |
|--------|---------------------------------------------------------------------------------------|-----------|----------|-----------|
| ON/OFF | Preferences: [Processing Tab](../../../userguide/preferences/processing/#hot-remove)  | ON/OFF    | ∅        | OFF       |

# Control

This process is controlled by the **Preprocess** pipeline.

# Input

| Data                                          | Type  |
|-----------------------------------------------|-------|
| image provided by the **Preprocess** pipeline | Image |

# Behavior

```mermaid
graph LR

START([START])

TEST_ENABLED{{TEST:<br><br>Process enabled?}}
TEST_COLOR{{TEST:<br><br>Color image?}}

COMPUTE[Compute average value of neighbors of each pixel]
REPLACE[Replace hot pixel value with the average of its neighbors]

RETURN[Return modified image]
UNCHANGED[Return unchanged image]

END([END])

START --> TEST_ENABLED
TEST_ENABLED -->|Yes| TEST_COLOR
TEST_COLOR ---->|Yes| UNCHANGED
TEST_ENABLED ---->|No| UNCHANGED
TEST_COLOR -->|No| COMPUTE
COMPUTE --> REPLACE
REPLACE --> RETURN
RETURN --> END
UNCHANGED --> END

classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2 px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class START bounds
class TEST_ENABLED test
class TEST_COLOR test
class COMPUTE step
class UNCHANGED step
class REPLACE step
class RETURN step
class END bounds
```

Each pixel in the image whose value deviates too much from its neighbors is considered a hot pixel.

Its value is replaced by the average value of its neighbors.

# Output

The modified image is sent back to the **Preprocess** pipeline.