---
title: "Preprocess"
description: "Detailed documentation of the ALS Preprocess module"
author: "ALS Team"
lastmod: 2024-12-30T08:47:09Z
keywords: ["ALS preprocess"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["module", "Preprocess"]
weight: 352
---

# Overview

The **Preprocess** module handles sub **calibration**

# Configuration

The **Preprocess** module itself requires no configuration.

The configuration of the **calibration** processes is managed by the **processes** themselves.
See the [Behavior](#behavior) section below.

# Control

The **Preprocess** module is started when ALS launches and **is not influenced by any external factors** except for the arrival of images in its queue.

# Input

| Type  | Description          |
|-------|----------------------|
| Image | sub present in queue |

# Behavior {#behavior}

Performs **calibration** processes on the sub:

1. [Hot pixel removal](hot_remove/)
2. [Dark subtraction](dark_remove/)
3. [Debayering](debayer/)

# Output

The image resulting from step 3 is transmitted to the **Stack** module.