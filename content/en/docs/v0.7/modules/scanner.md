---
title: "Scanner"
description: "Detailed documentation of the ALS scanner module"
author: "ALS Team"
lastmod: 2024-12-30T09:00:23Z
keywords: ["ALS scanner"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["module", "scanned folder"]
weight: 350
---

# Overview

The **Scanner** module is your subs' entry point to ALS.

It monitors the **scan folder** and provides the detected subs to the **Preprocess** module.

Its configuration is managed via ALS preferences

It is controlled by the interface and keyboard shortcuts.

# Configuration

| Source                            | Parameter                | data type | Required    | Default value |
|-----------------------------------|--------------------------|-|-------------|---------------|
| [Preferences: General Tab](../../user-guide/preferences/general/#scan-folder) | Path to the scan folder | Folder path | Yes           | ∅              |  




# Control

| Source                                                                       | Action                                                                                                                         |
|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| [Interface: Session Controls](../../user-guide/ui/controls/#session-controls) | ON/OFF                                                                                                                         |
| Shortcuts                                                                   | - <span class="als-ks">R</span> ON/OFF toggle within current session<br> - <span class="als-ks">X</span> OFF + session closure |

# Input

| Type      | Description                                        |
|-----------|----------------------------------------------------|
| Event     | A new sub has been detected in the **scan folder** |


# Behavior

1. Loads the detected image into memory, with all its metadata

{{% alert color="info" %}}
ℹ️ Detection works regardless of the subfolder structure inside the **scan folder**.
{{% /alert %}}

# Output

The loaded image is transmitted to the **Preprocess** module