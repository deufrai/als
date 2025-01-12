---
title: "Dark Subtraction"
description: "Detailed documentation ALS DarkRemove process"
author: "ALS Team"
lastmod: 2025-01-12T11:46:35Z
keywords: ["ALS dark current subtractor", "ALS thermal signal subtraction"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["process", "dark", "calibration"]
weight: 354
---

# Overview

The **DarkRemove** process subtracts the thermal noise from the image using a user-provided master dark.

Its configuration is managed via ALS preferences page.

# Configuration

|                  | Source                                                                                | Data type | Required  | Default value  |
|------------------|---------------------------------------------------------------------------------------|-----------|-----------|----------------|
| ON/OFF           | Preferences: [Processing Tab](../../../userguide/preferences/processing/#dark-remove) | ON/OFF    | ∅         | OFF            |
| Master dark path | Preferences: [Processing Tab](../../../userguide/preferences/processing/#dark-remove) | File path | Yes       | ∅              |

# Control

This process is triggered by the **Preprocess** pipeline.

# Input

| Data                                            | Type  |
|-------------------------------------------------|-------|
| image received from the **Preprocess** pipeline | Image |
| master dark read from configured path           | Image |

# Behavior

```mermaid
graph LR

START([START])

TEST_ENABLED{{Processing enabled?}}
TEST_SIZE{{Identical dimensions?}}
TEST_TYPE{{Identical data types?}}

CONVERT[Convert master dark]
SUBTRACT[Subtract master dark from image]

RETURN[Return modified image]
UNCHANGED[Return unchanged image]

END([END])

START --> TEST_ENABLED

TEST_ENABLED ----->|No| UNCHANGED
TEST_ENABLED -->|Yes| TEST_SIZE

TEST_SIZE ----->|No| UNCHANGED
TEST_SIZE -->|Yes| TEST_TYPE

TEST_TYPE -->|No| CONVERT
TEST_TYPE -->|Yes| SUBTRACT

CONVERT --> SUBTRACT
SUBTRACT --> RETURN

RETURN --> END
UNCHANGED --> END

classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class TEST_ENABLED,TEST_SIZE,TEST_TYPE test
class START,END bounds
class RETURN,UNCHANGED,CONVERT,SUBTRACT step
```

The master dark is subtracted from the image.

- If data types are different, the master dark is converted to the same data type as the image before subtraction.
- If dimensions are different, the process is aborted and the **unmodified** image is sent back to the **Preprocess** module.

# Output

The modified image is sent back to the **Preprocess** pipeline.