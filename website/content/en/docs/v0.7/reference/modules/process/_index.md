---
title: "Process"
description: "Detailed documentation of the ALS Process module"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: ["ALS process"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module"]
weight: 357
---

# Overview

The **Process** pipeline handles **visual processing** tasks applied to the stacking results.

# Configuration

The **Process** pipeline itself requires no configuration.

The configuration of the **visual processing** tasks is managed by the **processes** themselves.
See the [Behavior](#behavior) section below.

# Control

The **Process** module is launched in the background at ALS startup.

| Source                | Type      | Response           |
|-----------------------|-----------|--------------------|
| sub(s) in queue       | Event     | trigger processing |

# Input

| Data               | Type  |
|--------------------|-------|
| sub at queue front | Image |

# Behavior {#behavior}

Performs **visual processing** tasks on the stacking result:

1. [Auto-stretch](autostretch/)
2. [Levels](levels/)
3. [RGB Balance](rgb_balance/)

# Output

Visually processed image is broadcast.
