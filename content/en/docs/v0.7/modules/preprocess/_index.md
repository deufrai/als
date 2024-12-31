---
title: "Preprocess"
description: "Detailed documentation of the ALS Preprocess module"
author: "ALS Team"
lastmod: 2024-12-31T20:05:37Z
keywords: ["ALS preprocess"]
draft: false
type: "docs"
categories: ["detailed documentations"]
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

The **Preprocess** module is launched in the background at ALS startup

| Type      | Source                     | Shortcut | Action                                     |
|-----------|----------------------------|----------|--------------------------------------------|
| Event     | sub(s) in queue       | ∅        | trigger calibration |

# Input

| Type  | Description        |
|-------|--------------------|
| Image | sub at queue front |

# Behavior {#behavior}

Performs **calibration** processes on the sub:

1. [Hot pixel removal](hot_remove/)
2. [Dark subtraction](dark_remove/)
3. [Debayering](debayer/)

# Output

The image resulting from step 3 is transmitted to the **Stack** module.