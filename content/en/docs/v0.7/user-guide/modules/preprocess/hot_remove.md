---
title: "Hot Pixel Removal"
description: "Detailed documentation of the ALS HotPixelRemove process"
author: "ALS Team"
lastmod: 2024-12-30T03:29:59Z
keywords: ["ALS hot pixel removal", "ALS hot pixel suppression"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["process", "hot pixels"]
weight: 353
---

# Overview

The **HotPixelRemove** process removes hot pixels from the image.

Its configuration is managed via ALS preferences.

# Configuration

| Source                             | Parameter | Data Type | Required | Default   |
|------------------------------------|-----------|-----------|---------|-----------|
| [Preferences: Processing Tab](../../../preferences/processing/#hot-remove) | ON/OFF    | ON/OFF    | ∅         | OFF       |

# Control

This process is triggered by the **Preprocess** module.

# Input

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image received from the **Preprocess** module |

# Behavior

Each pixel in the image whose value deviates too much from its neighbors is considered a hot pixel.

Its value is replaced by the average value of its neighbors.

# Output

The modified image is sent back to the **Preprocess** module.