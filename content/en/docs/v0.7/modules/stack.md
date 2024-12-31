---
title: "Stack"
description: "Detailed documentation of the ALS Stack module"
author: "ALS Team"
lastmod: 2024-12-31T20:05:37Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "module", "stack", "threshold" ]
weight: 356
---

# Overview

The **Stack** module handles the alignment and stacking of calibrated subs.

# Configuration

| Source                                                            | Parameter           | Data type                   | Required | Default value |
|-------------------------------------------------------------------|---------------------|-----------------------------|----------|---------------|
| [Interface: Stacking controls](../../userguide/ui/controls/#controls)  | ON/OFF              | ON/OFF                      | ∅        | ON            |
| [Interface: Stacking controls](../../userguide/ui/controls/#controls)  | Stacking mode       | choices:<br>- mean<br>- sum | YES      | mean          |
| [Interface: Stacking controls](../../userguide/ui/controls/#threshold) | Detection threshold | value range                 | YES      | 25            |

# Control

The **Stack** module is launched in the background at ALS startup

| Type      | Source                     | Shortcut | Action             |
|-----------|----------------------------|----------|--------------------|
| Event     | sub(s) in queue       | ∅        | trigger processing |

# Input

| Type  | Description                   |
|-------|-------------------------------|
| Image | calibrated sub at queue front |
| Image | session alignment reference   |

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