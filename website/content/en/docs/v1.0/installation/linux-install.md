---
title: Installation on PC/Linux
description: Installing ALS on Linux PC
author: ALZ Team
lastmod: 2026-06-11T00:08:20Z
keywords: [ "installation", "linux", "astro live stacker", "guide" ]
weight: 100210
tags: ['linux', 'PC']
categories : ['installation procedures']
---

# 🖥️ Minimum System Requirements

## 64-bit GNU/Linux Distribution
- Ubuntu 22.04 or higher
- Fedora 34 or higher
- Debian 11 (Bullseye) or higher
- openSUSE Leap 15.3 or higher
- Linux Mint 21 or higher
- any other distribution offering GLIBC 2.35 or higher

## Hardware Requirements
|                    | Minimum |
|--------------------|---------|
| **RAM**            | 4 GB    |
| **Free Storage**   | 950 MB  | 

# 📦 Installation

1. **Open the Downloads folder**
    - Access your Downloads folder. You can usually find it by clicking on the icon of your file manager (for example, Nautilus, Dolphin, or Thunar) and selecting "Downloads" in the navigation menu on the left.

2. **Identify the ALS file**
    - Look for the file whose name starts with {{< als-code >}}als{{< /als-code >}} and ends with {{< als-code >}}.run{{< /als-code >}}. For example, it might be {{< als-code >}}als-v1.0.run{{< /als-code >}}.

3. **Make the file executable**
    - To make the file executable, you need to change its permissions. This can be done directly from the file manager:
        - Right-click on the {{< als-code >}}als-v1.0.run{{< /als-code >}} file.
        - Select "Properties".
        - Go to the "Permissions" tab.
        - Check the "Allow executing file as program" option.

4. **Move ALS to a permanent location**

   **Why move ALS out of the Downloads folder?**

   Moving ALS to a dedicated directory helps organize your files better and ensures the application is installed in a stable and permanent location. The Downloads folder is often used for temporary files and can be cleaned up regularly, leading to the accidental deletion of important files. By creating a specific folder for ALS, you ensure the application remains accessible and safe.

    - Open your file manager (for example, Nautilus).
    - Go to your home directory ({{< als-code >}}/home/username{{< /als-code >}}).
    - Right-click in the directory and select "Create New Folder".
    - Name the folder {{< als-code >}}Applications{{< /als-code >}} and press "Enter".
    - Double-click the {{< als-code >}}Applications{{< /als-code >}} folder to open it.
    - Create another folder inside it called {{< als-code >}}ALS{{< /als-code >}} and press "Enter".
    - Navigate to the Downloads folder ({{< als-code >}}Downloads{{< /als-code >}}) in another window of your file manager. It's important to have two distinct and visible windows to easily drag and drop files.
    - Find the {{< als-code >}}als-v1.0.run{{< /als-code >}} file in the Downloads folder, then drag this file into the {{< als-code >}}ALS{{< /als-code >}} folder ({{< als-code >}}/home/username/Applications/ALS{{< /als-code >}}).

5. **Run the executable file**
    - Double-click on the {{< als-code >}}als-v1.0.run{{< /als-code >}} file.
    - If a dialog box appears asking you to confirm running the file, choose the option to execute or open the file.

Next step : Our [Quickstart](../quickstart/) guide
