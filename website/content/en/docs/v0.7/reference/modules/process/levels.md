---
title: "Levels"
description: "Detailed documentation of the Levels process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-10-22T15:51:16Z
keywords: [ "ALS levels", "black clipping", "white clipping", "midtones", "visual processing" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "levels", "image adjustment" ]
weight: 359
---

# Overview

The **Levels** process adjusts the brightness distribution of a stacked image by setting
black and white points and tuning midtones.  
It allows precise control over image contrast and luminosity, complementing the **Auto-Stretch** process.

This process is handled by the **Process** pipeline module.

# Configuration

The **Levels** process parameters are available in the **Processing Panel**, located on the right-hand side of the ALS interface.

Refer to the [Processing Panel documentation](../../../../userguide/ui/processing/#levels-section) for detailed instructions.

# Control

The **Levels** process is managed through the `Processing Panel` interface.

| Control    | Type     | Action                                        |
|------------|----------|-----------------------------------------------|
| `Active`   | checkbox | Enable or disable the process                 |
| `Black`    | slider   | Defines the clipping threshold for shadows    |
| `Midtones` | slider   | Adjusts the image’s midtone brightness        |
| `White`    | slider   | Defines the clipping threshold for highlights |

# Input

| Data            | Type  |
|-----------------|-------|
| stacking result | Image |

# Behavior {#behavior}

Refines image brightness and contrast using user-defined thresholds.

1. Applies black clipping to remove very dark regions below the black point.  
2. Adjusts midtone gamma to enhance perceptual balance.  
3. Applies white clipping to limit overexposed regions above the white point.  
4. Outputs a balanced image ready for further processing or visualization.

# Output

The adjusted image is sent to the next process in the **Process** pipeline.
