---
title: Install on an Intel Mac
description: Installing ALS on an Intel Mac
author: ALZ Team

lastmod: 2024-12-08T13:29:09Z
keywords: ["installation", "mac", "intel", "astro live stacker", "guide"]
weight: 25
---

1. **Open the Downloads Folder**:
   - When the download is complete, open Finder by clicking its icon in the Dock.
   - Navigate to your downloads folder by selecting "Downloads" from the navigation menu on the left.

2. **Identify the ALS Disk Image**:
   - Look for the disk image that starts with `als` and ends with `-amd64.dmg`. For example, it might be `als-v0.7-beta7-amd64.dmg`.

3. **Mount the Disk Image**:
   - Double-click on the `als-v0.7-beta7-amd64.dmg` disk image. This will mount the disk image.
   - A new Finder window will show the contents of the disk image. You will see the `ALS` application icon on the left and a shortcut to the system's `Applications` folder on the right.

4. **Copy the Application to the Applications Folder**:
   - Drag the `ALS` application icon from the Finder window to the `Applications` shortcut in the same window.
   - If prompted, enter your administrator password to authorize this operation.

5. **Manage App Permissions**:
   - macOS versions prior to Catalina (10.15):
     - A dialog box will appear stating the application is from an unknown developer. Click "Open" to confirm.
     - Once the application is authorized, double-click the `ALS` application in the `Applications` folder to launch it.
   - macOS Catalina (10.15) up to Sonoma (14.x.x):
     - A dialog box will appear stating the application cannot be opened because it is from an unknown developer. Click "Cancel".
     - Go to "System Preferences" > "Security & Privacy" > "General" and click "Open Anyway" next to the message about `ALS`.
     - Confirm by clicking "Open" again in the new dialog that appears.
     - Once the application is authorized, double-click the `ALS` application in the `Applications` folder to launch it.
   - macOS Sequoia (15.x.x):
     - Open Finder and go to the `Applications` folder.
     - Then, go to the `Utilities` subfolder.
     - In this subfolder, double-click the `Terminal` application to open it.
     - In the Terminal window, type the following command:
       ```bash
       sudo xattr -r -d com.apple.quarantine /Applications/als.app
       ```
     - Press `Enter`. Enter your administrator password if prompted and press `Enter` again.
     - Navigate to the `Applications` folder and double-click the `ALS` application to run it.

Enjoy using ALS! 🚀✨
