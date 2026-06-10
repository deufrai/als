---
title: Installation on a Mac Apple Silicon
description: Installing ALS on Mac Apple Silicon
author: ALZ Team
lastmod: 2026-06-10T23:53:27Z
keywords: ["installation", "mac", "m1", "m2", "astro live stacker", "guide"]
weight: 100240
tags: ['install', 'Mac', 'Apple Silicon Mac']
categories : ['procedures']
---

# 🖥️ Minimum System Requirements

## System Version

macOS 10.13 (High Sierra) or later

## Hardware Requirements
|                    | Minimum |
|--------------------|---------|
| **RAM**            | 4 GB    |
| **Free Storage**   | 400 MB  | 

# 📦 Installation


1. **Open the Downloads folder**
   - When the download is complete, open Finder by clicking on its icon in the Dock.
   - Access your Downloads folder by selecting "Downloads" in the navigation menu on the left.

2. **Identify the ALS disk image**
   - Look for the disk image whose name starts with {{< als-code >}}als{{< /als-code >}} and ends with {{< als-code >}}-arm64.dmg{{< /als-code >}}. For example, it might be {{< als-code >}}als-v1.0-arm64.dmg{{< /als-code >}}.

3. **Mount the disk image**
   - Double-click on the {{< als-code >}}als-v1.0-arm64.dmg{{< /als-code >}} disk image. This will mount the disk image.
   - A new Finder window will display the contents of the disk image. You will see the {{< als-code >}}ALS{{< /als-code >}} application icon on the left and a shortcut to the system {{< als-code >}}Applications{{< /als-code >}} folder on the right.

4. **Copy the application to the Applications folder**
   - Drag the {{< als-code >}}ALS{{< /als-code >}} application icon from the Finder window to the {{< als-code >}}Applications{{< /als-code >}} shortcut in the same window.
   - If prompted, enter your administrator password to authorize this operation.

5. **Manage the app permissions**
   - macOS versions prior to Catalina (10.15)
     - A dialog will appear indicating that the application is from an unidentified developer. Click "Open" to confirm.
     - Once the application is authorized, double-click the {{< als-code >}}ALS{{< /als-code >}} application in the {{< als-code >}}Applications{{< /als-code >}} folder to launch it.
   - macOS Catalina (10.15) to Sonoma (14.x.x)
     - A dialog will appear indicating that the application cannot be opened because it is from an unidentified developer. Click "Cancel".
     - Go to "System Preferences" > "Security & Privacy" > "General", then click "Open Anyway" next to the message about {{< als-code >}}ALS{{< /als-code >}}.
     - Confirm by clicking "Open" again in the new dialog that appears.
     - Once the application is authorized, double-click the {{< als-code >}}ALS{{< /als-code >}} application in the {{< als-code >}}Applications{{< /als-code >}} folder to launch it.
   - macOS Sequoia (15.x.x)
     - Open Finder and go to the {{< als-code >}}Applications{{< /als-code >}} folder.
     - Then, go to the {{< als-code >}}Utilities{{< /als-code >}} subfolder.
     - In this subfolder, double-click the {{< als-code >}}Terminal{{< /als-code >}} application to open it.
     - In the Terminal window, type the following command:
       
       {{< als-code >}}sudo xattr -r -d com.apple.quarantine /Applications/als.app{{< /als-code >}}
     - Press {{< als-ks >}}Enter{{< /als-ks >}}. Enter your password if prompted and press {{< als-ks >}}Enter{{< /als-ks >}} again.

6. **Launch ALS**
     - Go to the {{< als-code >}}Applications{{< /als-code >}} folder, then double-click the {{< als-code >}}ALS{{< /als-code >}} application to run it.

Next step : Our [Quickstart](../quickstart/) guide 
