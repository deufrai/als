---
title: "Scanner"
description: "Detailed documentation of the ALS scanner module"
author: "ALS Team"
lastmod: 2024-12-31T21:07:16Z
keywords: ["ALS scanner"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "input", "scan folder", "scanner"]
weight: 350
---

# Overview

The **Scanner** module is your subs' entry point to ALS.

It monitors the **scan folder** and provides the detected subs to the **Preprocess** module.

Its configuration is managed via ALS preferences

# Configuration

| Source                            | Parameter                | data type | Required    | Default value |
|-----------------------------------|--------------------------|-|-------------|---------------|
| [Preferences: General Tab](../../userguide/preferences/general/#scan-folder) | Path to the scan folder | Folder path | Yes           | ∅              |  


# Control

| Type   | Source                                          | Action                          |
|--------|-------------------------------------------------|---------------------------------|
| Events | [Interface: Session Controls](../../userguide/ui/controls/#session-controls) | Scan folder monitoring : ON/OFF |
| Event  | A new sub has been detected in the scan folder   | Load detected sub               |


# Input

| Type      | Description              |
|-----------|--------------------------|
| File path | path of the detected sub |


# Behavior

1. Loads detected sub into memory, with all its metadata

{{% alert color="info" %}}
ℹ️ Detection works regardless of the subfolder structure inside the **scan folder**.
{{% /alert %}}

# Output

The loaded image is transmitted to the **Preprocess** module