---
title: "RGB Balance"
description: "Detailed documentation of the Color Balance process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-10-22T15:45:01Z
keywords: [ "ALS color balance", "rgb adjustment", "color correction", "visual processing" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "color balance", "image adjustment" ]
weight: 360
---

# Overview

The **RGB Balance** process adjusts the relative intensity of the three primary colors — red, green, and blue — to correct or refine the overall color tone of a stacked image.  
It allows fine control of image chromatic balance, complementing the **Levels** and **Auto-Stretch** processes.

This process is handled by the **Process** pipeline module.

# Configuration

The **RGB Balance** parameters are available in the **Processing Panel**, located on the right-hand side of the 
ALS interface.

Refer to the [Processing Panel documentation](../../../../userguide/ui/processing/#balance-section) for detailed 
instructions.

# Control

The **RGB Balance** process is managed through the `Processing Panel` interface.

| Control | Type     | Action                                   |
|---------|----------|------------------------------------------|
| `R`     | slider   | Adjusts the red channel intensity        |
| `G`     | slider   | Adjusts the green channel intensity      |
| `B`     | slider   | Adjusts the blue channel intensity       |

# Input

| Data            | Type  |
|-----------------|-------|
| stacking result | Image |

# Behavior {#behavior}

Balances the image’s color components to achieve the desired tonal balance.

1. Applies user-defined scaling to each RGB channel.  
2. Recalculates color ratios for consistent white balance.  
3. Outputs a color-balanced image with corrected chromatic tones.

# Output

The color-balanced image is sent to the **Process** pipeline.
