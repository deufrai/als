---
title: "RGB Balance"
description: "Detailed documentation of the Color Balance process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-10-23T16:03:39Z
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

{{% alert color="info" %}}
ℹ️ The **RGB Balance** process is only available when working with color images.
{{% /alert %}}

# Configuration

The **RGB Balance** parameters are available in the **Processing Panel**, located on the right-hand side of the 
ALS interface.

Refer to the [Processing Panel documentation](../../../../userguide/ui/processing/#balance-section) for detailed 
instructions.

# Control

The **RGB Balance** process is managed through the `Processing Panel` interface.

| Control  | Type     | Action                              |
|----------|----------|-------------------------------------|
| `Active` | checkbox | Enable or disable the process       |
| `R`      | slider   | Adjusts the red channel intensity   |
| `G`      | slider   | Adjusts the green channel intensity |
| `B`      | slider   | Adjusts the blue channel intensity  |

# Input

| Data            | Type  |
|-----------------|-------|
| stacking result | Image |

# Behavior {#behavior}

Balances the image’s color components to achieve the desired tonal balance.

# Output

The color-balanced image is sent to the **Process** pipeline.
