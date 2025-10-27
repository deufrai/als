---
title: "Auto-Stretch"
description: "Detailed documentation of the Auto-Stretch process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-10-21T18:18:46Z
keywords: [ "ALS auto stretch", "visual processing" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "stretch", "image adjustment" ]
weight: 358
---

# Overview

The **Auto-Stretch** process optimizes the intensity levels of stacked images, making them visually usable without
manual adjustments.

This process is handled by the **Process** pipeline module.

# Configuration

Adjustments can be made through the **Processing Panel**, located on the right-hand side of the ALS
interface.


| Control    | Type     | Action                        |
|------------|----------|-------------------------------|
| `Active`   | checkbox | Enable or disable the process |
| `Strength` | slider   | Adjust stretch intensity      |

Refer to the [Processing Panel documentation](../../../../userguide/ui/processing/#stretch-section) for detailed instructions

# Control

The **Auto-Stretch** process is managed by the **Process** pipeline

# Input

| Data            | Type  |
|-----------------|-------|
| stacking result | Image |

# Behavior {#behavior}

Adjusts intensity levels for optimal viewing.

1. Evaluates pixel distribution based on the stacking result.
2. Applies stretch parameters configured by the user.
3. Generates a visually optimized image.

# Output

Stretched image is sent to the next process in the **Process** pipeline
