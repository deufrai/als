---
title: "RGB Balance"
description: "Detailed documentation of the RGB Balance process in the ALS Process module"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: [ "ALS color balance", "visual processing" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "process", "rgb", "image adjustment" ]
weight: 360
---

# Overview

The **RGB Balance** process tweaks the intensity of red, green and blue channels.
It runs as part of the **Process** pipeline.

# Configuration

| Setting | Source | Data Type | Default |
|---------|------------------------------|------------------|---------|
| `Active` toggle | [Processing Panel](../ui/processing/) | ON/OFF | ON |
| `Red` slider | [Processing Panel](../ui/processing/) | float | 1 |
| `Green` slider | [Processing Panel](../ui/processing/) | float | 1 |
| `Blue` slider | [Processing Panel](../ui/processing/) | float | 1 |

# Control

The **RGB Balance** process is managed through the **Processing Panel**.

# Input

| Data | Type |
|------|------|
| stacking result | Image |

# Behavior {#behavior}

Adjusts color balance for better visual appearance.

1. Scales each channel according to the sliders.
2. Clips values to the supported range.

# Output

A color-balanced image is passed to the next step.
