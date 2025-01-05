---
title: "Preprocess"
description: "Detailed documentation of the ALS Preprocess module"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: ["ALS preprocess"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "calibration"]
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

| Source                | Type      | Response            |
|-----------------------|-----------|---------------------|
| sub(s) in queue       | Event     | trigger calibration |

# Input

| Data               | Type  |
|--------------------|-------|
| sub at queue front | Image |

# Behavior {#behavior}

Performs **calibration** processes on the sub:

1. [Hot pixel removal](hot_remove/)
2. [Dark subtraction](dark_remove/)
3. [Debayering](debayer/)

# Output

Calibrated sub is broadcast
