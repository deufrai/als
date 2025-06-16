---
title: "Levels"
description: "Detailed documentation of the Levels process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: [ "ALS levels", "visual processing" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "levels", "image adjustment" ]
weight: 359
---

# Overview

The **Levels** process adjusts black and white points as well as midtones.
It is part of the **Process** pipeline and operates automatically.

# Configuration

| Setting | Source | Data Type | Default |
|---------|------------------------------|------------------|---------|
| `Active` toggle | [Processing Panel](../ui/processing/) | ON/OFF | ON |
| `Black` slider | [Processing Panel](../ui/processing/) | integer | 0 |
| `Mids` slider | [Processing Panel](../ui/processing/) | float | 1 |
| `White` slider | [Processing Panel](../ui/processing/) | integer | 65535 |

# Control

The **Levels** process is managed through the **Processing Panel**.

# Input

| Data | Type |
|------|------|
| stacking result | Image |

# Behavior {#behavior}

Adjusts the tonal response of the image.

1. Optionally shifts the midtone level.
2. Optionally clips pixel values below `Black` and above `White`.
3. Normalizes the result to the full range.

# Output

A tone-adjusted image is forwarded to the next step.
