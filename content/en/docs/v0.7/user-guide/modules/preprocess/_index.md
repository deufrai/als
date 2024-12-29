---
title: "Pre-process"
description: "Detailed documentation of the ALS Preprocess module"
author: "ALS Team"
lastmod: 2024-12-29T22:57:31Z
keywords: ["ALS pre-process"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["module", "Pre-process"]
weight: 352
---

# Introduction

The **Pre-Process** module handles image **calibration** processing.

# Configuration

The **Pre-process** module itself requires no configuration.

The configuration of the **calibration** processes is managed by the **processes** themselves.
See the [Behavior](#behavior) section below.

# Control

The **Pre-process** module is started when ALS launches and **is not influenced by any external factors** except for the arrival of images in its queue.

# Input

| Type  | Description                      |
|-------|----------------------------------|
| Image | image present in the queue       |

# Behavior {#behavior}

Applies these processes to the image:

1. [Hot pixel removal](hot_remove/)
2. [Dark subtraction](dark_remove/)
3. [Debayering](debayer/)

# Output

The image resulting from step 3 is transmitted to the **Stack** module.