---
title: "Scanner"
description: "Detailed documentation of the ALS scanner module"
author: "ALS Team"
lastmod: 2025-01-01T00:18:50Z
keywords: ["ALS image detector", "ALS scanner"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "input", "scan folder", "scanner"]
weight: 350
---

# Overview

The **Scanner** module is the entry point for your subs in ALS.

- Monitors the **scan folder**
- Loads detected subs
- Transmits subs to the **Preprocess** module

# Configuration

Its configuration is managed via preferences.

| Source                                                                           | Parameter   | Data Type                        | Required | Default Value |
|----------------------------------------------------------------------------------|-------------|----------------------------------|----------|---------------|
| [Preferences: General Tab](../../userguide/preferences/general/#scan-folder)     | scan folder | Path to a folder                 | Yes      | ∅             |
| [Preferences: General Tab](../../userguide/preferences/general/#profile)         | Profile     | Choice: <br>- EAA<br>- photo<br> | Yes      | EAA           |
| [Preferences: General Tab](../../userguide/preferences/general/#memory)          | Memory Use  | fuzzy                            | Yes      | "Unfair"      |

# Control

| Source                                                                       | Type        | Action                              |
|------------------------------------------------------------------------------|-------------|-------------------------------------|
| [Interface: Session Controls](../../userguide/ui/controls/#session-controls) | Events      | Scan folder monitoring: ON/OFF      |
| A sub has been detected in the scan folder                                   | Event       | Load the detected sub               |

{{% alert color="info" %}}
ℹ️ Detection works regardless of the subfolder structure inside the **scan folder**.
{{% /alert %}}

# Input

| Type              | Description                 |
|-------------------|-----------------------------|
| File path         | Path to the detected sub    |

# Behavior

## Wait for complete file {#wait}

Files are detected as soon as they **appear** in the **scan folder**

To avoid loading incomplete files, the **Scanner** module waits for the file to be fully written before loading it:

- Continuously checks the size of the detected file
- Waits for the file size to stabilize over 2 consecutive checks

  The waiting time between checks depends on the configured profile:

  - **Electronically Assisted Astronomy** profile: 10ms
  - **Astrophoto** profile: 500ms

## Image Loading {#load}

### Compatible Formats

- Common image file formats
- **FITS** files
- **Raw** files from cameras supported by the libRaw library [1]

### Memory Management

It may happen that subs are detected more frequently than ALS can process and save images.

In this case, it is necessary to ensure that the system memory is not filled up by continuously detected subs 

- Wait until the available RAM is greater than the configured value for the Memory Use configuration parameter :

    | Memory Management | Amount of Memory left for the system |
    |-------------------|--------------------------------------|
    | Greedy            | 256MiB                               |
    | Unfair            | 512MiB                               |
    | Fair              | 1GiB                                 |
    | Scared            | 2GiB                                 |

### File Reading

The file is read and loaded into memory.

## Metadata Extraction

Metadata extraction is supported for **FITS** and **Raw** formats.

The following metadata are extracted from the file and incorporated into the image in memory:
- **Exposure time**
- **Bayer pattern** (_for subs from a color sensor_)
  - FITS files: **BAYERPAT** header
  - Raw files: Standard Exif header

# Output

The loaded image is transmitted to the **Preprocess** module.

---

[1] [List of cameras supported by the libRaw library](https://www.libraw.org/supported-cameras)