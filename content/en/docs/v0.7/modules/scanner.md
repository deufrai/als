---
title: "Scanner"
description: "Detailed documentation of the ALS scanner module"
author: "ALS Team"
lastmod: 2025-01-01T22:17:04Z
keywords: ["ALS image detector", "ALS scanner"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "input", "scan folder", "scanner"]
weight: 350
---

# Overview

The **Scanner** module is the entry point for your subs in ALS.

It is responsible for:
- Monitoring the appearance of subs in the **scan folder**
- Loading the detected subs

{{% alert color="info" %}}
ℹ️ **Existing files are ignored**

Files present in the **scan folder** before the **Scanner** module is started are not detected
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ **Detection of subs is recursive**

Subs are detected regardless of the level of subfolders where they appear within the **scan folder**

Even if they are saved in subfolders created after the **Scanner** module is started
{{% /alert %}}

# Configuration

|                     | Source                                                                           | Data Type                        | Required | Default Value |
|---------------------|----------------------------------------------------------------------------------|----------------------------------|----------|---------------|
| **Scan Folder**     | Preferences: [General Tab](../../userguide/preferences/general/#scan-folder)     | Path to a folder                 | Yes      | ∅             |
| **Profile**         | Preferences: [General Tab](../../userguide/preferences/general/#profile)         | Choice: <br>- EAA<br>- photo<br> | Yes      | EAA           |
| **Memory Use**      | Preferences: [General Tab](../../userguide/preferences/general/#memory)          | fuzzy                            | Yes      | "Unfair"      |
# Control

| Source                                                                       | Type        | Response                       |
|------------------------------------------------------------------------------|-------------|--------------------------------|
| Interface: [Session Controls](../../userguide/ui/controls/#session-controls) | Events      | Scan folder monitoring: ON/OFF |
| A sub has been detected in the scan folder                                   | Event       | Load the detected sub          |


# Input

| Data                     | Type              |
|--------------------------|-------------------|
| Path to the detected sub | File path         |

# Behavior

## RAM Test {#ram}

It may happen that subs are detected more frequently than ALS can process and save the images.

To avoid saturating the system memory by loading subs uncontrollably:

- Wait until the available RAM is greater than the value configured for memory management:

  | Memory Management | Amount of Memory Left for the System |
  |-------------------|--------------------------------------|
  | Greedy            | 256MiB                               |
  | Unfair            | 512MiB                               |
  | Fair              | 1GiB                                 |
  | Cautious          | 2GiB                                 |

## Wait for Complete File {#wait}

Files are detected as soon as they **appear** in the **scan folder**.

To avoid loading incomplete files, the **Scanner** module waits until the file is completely written before loading it:

- Poll the size of the detected file in a loop
    - Verify that the file size is stable over 2 consecutive polls

The polling interval depends on the configured profile:

| Profile        | Polling Interval |
|----------------|------------------|
| EAA            | 10ms             |
| Astrophoto     | 500ms            |

## Image Loading {#load}

### Compatible Formats {#input-formats}

ALS determines the image format based on its file extension:

The file is loaded into memory using the format determined by its extension.

| Extension                                                        | Format |
|------------------------------------------------------------------|--------|
| <div style="font-family: monospace;">.jpg<br>.jpeg</div>         | JPEG   |
| <span style="font-family: monospace;">.png</span>                | PNG    |
| <div style="font-family: monospace;">.tiff<br>.tif</div>         | TIFF   |
| <div style="font-family: monospace;">.fits<br>.fit<br>.fts</div> | FITS   |
| All other extensions                                             | Raw    |

## Metadata Extraction

Supported for:
- **FITS**
- **Raw**

Metadata extracted from file and incorporated into the loaded image:
- **Exposure Time**
- **Bayer Matrix** (_for subs from a color sensor_)
    - FITS files: **BAYERPAT** header
    - Raw files: standard Exif header

```mermaid
flowchart TB
    START([Sub detected])
    WAIT_RAM[Wait for RAM]
    CHECK_RAM{{TEST: Available RAM<br>According to profile<br><br>OK?}}
    CHECK_SIZE{{TEST: File size<br>OK?}}
    WAIT_FILE[Wait for file<br>According to profile]
    TEST_FORMAT{{TEST: File format}}
    FITS[Load FITS file]
    STANDARD[Load standard file]
    RAW[Load Raw file]
    METADATA[Extract metadata]
    END((End))
    
    START ---> CHECK_RAM   
    WAIT_RAM <-->|NO| CHECK_RAM
 
    
    CHECK_RAM --->|YES| CHECK_SIZE
    WAIT_FILE <-->|NO| CHECK_SIZE   
    CHECK_SIZE -->|YES| TEST_FORMAT

    TEST_FORMAT -->  FITS
    TEST_FORMAT -->  STANDARD
    TEST_FORMAT -->  RAW
    

    RAW --> METADATA
    FITS --> METADATA
    
    STANDARD ---> END
    METADATA --> END
```

# Output

The loaded image is broadcast to whoever listens.

⚙️ _ALS will pass the image to the **Preprocess** module for calibration_

---

[1] [List of cameras supported by the libRaw library](https://www.libraw.org/supported-cameras)