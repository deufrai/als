---
title: "Dark Subtraction"
description: "Detailed documentation ALS DarkRemove process"
author: "ALS Team"
lastmod: 2024-12-29T22:57:31Z
keywords: ["ALS dark current subtractor", "ALS thermal signal subtraction"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["process", "dark"]
weight: 354
---

# Overview

The **DarkRemove** process subtracts the thermal noise from the image using a user-provided master dark.

Its configuration is managed via ALS preferences page.

# Configuration

| Source                                                                         | Parameter             |
|--------------------------------------------------------------------------------|-----------------------|
| [Preferences: Processing Tab](../../../preferences/processing/#dark-remove)    | ON/OFF                |
| [Preferences: Processing Tab](../../../preferences/processing/#dark-remove)    | Master dark path      |

# Control

This process is triggered by the **Pre-Process** module.

# Input

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image received from the **Pre-Process** module |
| Image | master dark provided by the user             |

# Behavior

The master dark is subtracted from the image.

# Output

The modified image is sent back to the **Pre-Process** module.