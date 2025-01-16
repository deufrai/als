---
title: "Stacker"
description: "Detailed documentation of the ALS Stack module"
author: "ALS Team"
lastmod: 2025-01-16T07:31:46Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "detailed documentations" ]
tags: [ "module", "process", "stack", "threshold" ]
weight: 356
---

# Overview

The **Stacker** module handles the alignment and stacking of calibrated subs.

# Configuration

|                     | Source                                                                 | Data type                   | Required | Default value |
|---------------------|------------------------------------------------------------------------|-----------------------------|----------|---------------|
| Alignment ON/OFF    | Interface: [Stacking controls](../../userguide/ui/controls/#controls)  | ON/OFF                      | ∅        | ON            |
| Stacking mode       | Interface: [Stacking controls](../../userguide/ui/controls/#controls)  | choices:<br>- mean<br>- sum | YES      | mean          |
| Detection threshold | Interface: [Stacking controls](../../userguide/ui/controls/#threshold) | integer                     | YES      | 25            |

# Control

The **Stack** module is launched in the background at ALS startup

| Source                     | Type      | Response           |
|----------------------------|-----------|--------------------|
| sub(s) in queue            | Event     | trigger processing |

# Input

| Data                        | Type  |
|-----------------------------|-------|
| sub at queue front          | Image |
| session alignment reference | Image |

# Behavior {#behavior}

```mermaid
flowchart LR
Start([START])
FirstSub{{First sub of the session?}}
SetAlignReference[Set sub as alignment reference]
CheckShape{{Sub same dimensions as previous result?}}
CheckAlign{{Alignment ON?}}
AlignImage[Align sub]
StackImage[Add sub to Stack]
ComputeStacking[Compute stacking]
PublishReference[Return alignment reference]
PublishResult[Return generated image]
End([END])

Start --> FirstSub
FirstSub -- YES --> SetAlignReference
SetAlignReference --> PublishReference
FirstSub -- NO --> CheckShape
CheckShape -- YES --> CheckAlign
CheckAlign -- YES --> AlignImage
AlignImage --> StackImage
CheckAlign -- NO --> StackImage
StackImage --> ComputeStacking
ComputeStacking --> PublishResult
CheckShape -- NO --> End
PublishReference --> End
PublishResult --> End

classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class Start,End bounds
class SetAlignReference,AlignImage,StackImage,PublishResult,ComputeStacking,PublishReference step
class CheckShape,CheckAlign,FirstSub test
```

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

1. Add the aligned (if requested) sub to the stack.
2. Generate a new image containing the stacking result according to the configured mode.

# Output

The generated image is broadcast