---
title: "Dark Subtraction"
description: "Detailed documentation ALS DarkRemove process"
author: "ALS Team"
lastmod: 2024-12-31T02:48:28Z
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

| Source                                                                         | Parameter             | Data type             | Required              | Default value         |
|--------------------------------------------------------------------------------|-----------------------|-|-----------------------|-----------------------|
| [Preferences: Processing Tab](../../../userguide/preferences/processing/#dark-remove)    | ON/OFF                | ON/OFF                | ∅                     | OFF                   |
| [Preferences: Processing Tab](../../../userguide/preferences/processing/#dark-remove)    | Master dark path      | File path             | Yes                   | ∅                     |

# Control

This process is triggered by the **Preprocess** module.

# Input

| Type  | Description                                   |
|-------|-----------------------------------------------|
| Image | image received from the **Preprocess** module |
| Image | master dark read from configured path         |

# Behavior

The master dark is subtracted from the image.

# Output

The modified image is sent back to the **Preprocess** module.