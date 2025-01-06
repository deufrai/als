---
title: "Hot Pixel Removal"
description: "Detailed documentation of the ALS HotPixelRemove process"
author: "ALS Team"
lastmod: 2025-01-06T03:20:05Z
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

This process is triggered by the **Preprocess** module.

# Input

| Data                                        | Type  |
|---------------------------------------------|-------|
| image provided by the **Preprocess** module | Image |

# Behavior

```mermaid
graph LR
  A[Start Process] --> B{Is Image Available?}
  B -- No --> C[Return None]
  B -- Yes --> D[Get Hot Pixel Remover Config]
  D --> E{Is Hot Pixel Remover Enabled?}
  E -- No --> F[Return Image Unchanged]
  E -- Yes --> G{Is Image Color?}
  G -- Yes --> H[Log Skipped on Color Image]
  H --> F
  G -- No --> I[Calculate Neighbors' Mean]
  I --> J[Replace Hot Pixels with Neighbors' Mean]
  J --> K[Return Modified Image]

```

Each pixel in the image whose value deviates too much from its neighbors is considered a hot pixel.

Its value is replaced by the average value of its neighbors.

# Output

The modified image is sent back to the **Preprocess** module.