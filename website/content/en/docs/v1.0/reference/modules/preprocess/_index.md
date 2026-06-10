---
title: "Preprocess"
description: "Detailed documentation of the ALS Preprocess module"
author: "ALS Team"
lastmod: 2026-06-10T23:25:49Z
keywords: ["ALS preprocess"]
draft: false
type: "docs"
categories: ["detailed documentation"]
tags: ["module", "calibration"]
weight: 100352
---

# Overview

The **Preprocess** pipeline handles **calibration** processes

# Configuration

The **Preprocess** pipeline itself requires no configuration.

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
3. [Flat calibration](flat_calibrate/)
4. [Debayering](debayer/)

# Output

Calibrated sub is broadcast
