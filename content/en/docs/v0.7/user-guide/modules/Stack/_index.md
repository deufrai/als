---
title: "Stack"
description: "Detailed documentation of the Stack module in ALS"
author: "ALS Team"
lastmod: 2024-12-30T07:18:00Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "user guide" ]
tags: [ "module", "stack" ]
weight: 354
---

# Introduction

The **Stack** module handles the alignment and stacking of calibrated subs.

# Configuration

| Source                                                            | Parameter           | Data type                   | Required | Default value |
|-------------------------------------------------------------------|---------------------|-----------------------------|----------|---------------|
| [Interface: Stacking controls](../../als-gui/controls/#controls)  | ON/OFF              | ON/OFF                      | ∅        | ON            |
| [Interface: Stacking controls](../../als-gui/controls/#controls)  | Stacking mode       | choices:<br>- mean<br>- sum | YES      | mean          |
| [Interface: Stacking controls](../../als-gui/controls/#threshold) | Detection threshold | value range                 | YES      | 25            |

# Control

The **Stack** module is started when ALS launches and **is not influenced by any external factors** except for the
arrival of images in its queue.

# Input

| Type  | Description                 |
|-------|-----------------------------|
| Image | calibrated sub in queue     |
| Image | session alignment reference |

# Behavior {#behavior}

## Alignment

**If alignment is ON**

1. Search for similarities between the calibrated sub and the session **alignment reference**.

   {{% alert color="info" %}}
   If the calibrated sub has similarities count **below** the configured detection threshold, it is **discarded** and
   the **Stack** module resumes listening to its queue.
   {{% /alert %}}

2. Compute required transformations for the calibrated sub to align with the reference:
    - translations
    - rotation
    - resizing

3. Apply the transformations to the calibrated sub.

## Stacking

1. Add the calibrated and aligned (if requested) sub to the stack.
2. Generate a new image containing the stacking result according to the configured mode.

# Output

The generated image is passed to the **Process** module.