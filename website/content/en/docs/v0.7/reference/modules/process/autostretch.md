---
title: "Auto-Stretch"
description: "Detailed documentation of the Auto-Stretch process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
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

This process is part of the **Process Module** pipeline and operates automatically in the background.

# Configuration

The **Auto-Stretch** process requires no configuration from the user.

Adjustments to its behavior can be made through the **Processing Panel**, located on the right-hand side of the ALS
interface.

Refer to the [Processing Panel documentation](../ui/processing/) for detailed instructions on managing the stretch
intensity slider.

# Control

The **Auto-Stretch** process is managed through the `Processing Panel` interface.

| Setting           | Action                         |
|-------------------|--------------------------------|
| `Strength` slider | Adjust the stretch level.      |
| `Active` toggle   | Enable or disable the process. |

## Default Actions

- **Double-click** the slider handle to reset it to its default position.
- Changes to the **Active** toggle generate a new image immediately.

# Input

| Data            | Type  |
|-----------------|-------|
| stacking result | Image |

# Behavior {#behavior}

Adjusts intensity levels for optimal viewing.

1. Evaluates pixel distribution based on the stacking result.
2. Applies default stretch parameters configured by ALS.
3. Generates a visually optimized image.

# Output

A stretched image is sent to the next process in the **Process Module pipeline** or directly displayed in the central
area of ALS.

# Notes

- Auto-Stretch is typically used to improve the visibility of faint details in stacked images.
- Default parameters aim to balance intensity across various imaging scenarios.

---
