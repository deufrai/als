---
title: Installation on a Mac Intel
description: Installing ALS on Mac Intel
author: ALZ Team
lastmod: 2024-12-15T10:17:33Z
keywords: ["installation", "mac", "intel", "astro live stacker", "guide"]
weight: 24
tags: ['install', 'Mac', 'Intel']
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
   - Look for the disk image whose name starts with `als` and ends with `-amd64.dmg`. For example, it might be `als-v0.7-beta7-amd64.dmg`.

3. **Mount the disk image**
   - Double-click on the `als-v0.7-beta7-amd64.dmg` disk image. This will mount the disk image.
   - A new Finder window will display the contents of the disk image. You will see the `ALS` application icon on the left and a shortcut to the system `Applications` folder on the right.

4. **Copy the application to the Applications folder**
   - Drag the `ALS` application icon from the Finder window to the `Applications` shortcut in the same window.
   - If prompted, enter your administrator password to authorize this operation.

5. **Manage the app permissions**
   - macOS versions prior to Catalina (10.15)
     - A dialog will appear indicating that the application is from an unidentified developer. Click "Open" to confirm.
     - Once the application is authorized, double-click the `ALS` application in the `Applications` folder to launch it.
   - macOS Catalina (10.15) to Sonoma (14.x.x)
     - A dialog will appear indicating that the application cannot be opened because it is from an unidentified developer. Click "Cancel".
     - Go to "System Preferences" > "Security & Privacy" > "General", then click "Open Anyway" next to the message about `ALS`.
     - Confirm by clicking "Open" again in the new dialog that appears.
     - Once the application is authorized, double-click the `ALS` application in the `Applications` folder to launch it.
   - macOS Sequoia (15.x.x)
     - Open Finder and go to the `Applications` folder.
     - Then, go to the `Utilities` subfolder.
     - In this subfolder, double-click the `Terminal` application to open it.
     - In the Terminal window, type the following command:
       ```bash
       sudo xattr -r -d com.apple.quarantine /Applications/als.app
       ```
     - Press `Enter`. Enter your administrator password if prompted and press `Enter` again.

6. **Launch ALS**
     - Go to the `Applications` folder, then double-click the `ALS` application to run it.

Continue to our [user guide](../user-guide/). We are here to assist you during this first start-up.

Enjoy using ALS! 🔭
