---
title: "Scanner"
description: "Detailed documentation of the ALS scanner module"
author: "ALS Team"
lastmod: 2025-01-02T01:53:20Z
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
- Monitoring the **appearance** of subs in the **scan folder**
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

|                     | Source                                                                           | Data Type           | Required | Default Value |
|---------------------|----------------------------------------------------------------------------------|---------------------|----------|---------------|
| **Scan Folder**     | Preferences: [General Tab](../../userguide/preferences/general/#scan-folder)     | Path to a folder    | Yes      | ∅             |
| **Profile**         | Preferences: [General Tab](../../userguide/preferences/general/#profile)         | Choice: EAA / photo | Yes      | EAA           |
| **Memory Use**      | Preferences: [General Tab](../../userguide/preferences/general/#memory)          | fuzzy               | Yes      | "Unfair"      |

# Control

| Source                                                                          | Type                            | Response                    |
|---------------------------------------------------------------------------------|---------------------------------|-----------------------------|
| Interface: [Session Controls](../../userguide/ui/controls/#session-controls)    | Command: STOP                   | Scan folder monitoring: OFF |
| Interface: [Session Controls](../../userguide/ui/controls/#session-controls)    | Command: START                  | Scan folder monitoring: ON  |
| System event                                                                    | sub detected in the scan folder | Load the detected sub       |


# Input

| Data                     | Type              |
|--------------------------|-------------------|
| Path to the detected sub | File path         |

# Behavior

## RAM Test {#ram}

Wait until the available RAM is greater than the configured value:

| Memory Use | Amount of Memory Left for the System |
|------------|--------------------------------------|
| Greedy     | 256MiB                               |
| Unfair     | 512MiB                               |
| Fair       | 1GiB                                 |
| Cautious   | 2GiB                                 |

## Wait for Complete File {#wait}

ℹ️ Files are detected as soon as they **appear** in the **scan folder**.

To ensure file is complete before loading it:

- Poll the size of the detected file in a loop
    - Verify that the file size is stable over 2 consecutive polls

The polling interval depends on the configured profile:

| Profile        | Polling Interval |
|----------------|------------------|
| EAA            | 10ms             |
| Astrophoto     | 500ms            |

## Image Loading {#load}

### Compatible Formats {#input-formats}

The file is loaded into memory using the format matching its filename extension.

| Extension                                                        | Format |
|------------------------------------------------------------------|--------|
| <div style="font-family: monospace;">.jpg<br>.jpeg</div>         | JPEG   |
| <span style="font-family: monospace;">.png</span>                | PNG    |
| <div style="font-family: monospace;">.tiff<br>.tif</div>         | TIFF   |
| <div style="font-family: monospace;">.fits<br>.fit<br>.fts</div> | FITS   |
| All other extensions                                             | Raw[1] |

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
flowchart LR
    START([Sub detected])
    
    WAIT_FILE[Wait for file<br><br>According to profile:<br>EAA: 10ms<br>Astrophoto: 500ms]    
    WAIT_RAM[Wait 20ms]
    
    CHECK_RAM{{Check available RAM<br><br>According to preferences:<br>Greedy: 2 GiB<br>Unfair: 1 GiB<br>Fair: 512 MiB<br>Cautious: 256MiB<br><br>OK?}}
    CHECK_SIZE{{Check file size<br><br>OK?}}
    TEST_FORMAT{{Check file format}}
    
    FITS[Load FITS]
    STANDARD[Load standard]
    RAW[Load Raw]
    
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