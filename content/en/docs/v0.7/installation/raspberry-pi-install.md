---
title: Installation on Raspberry Pi
description: Installing ALS on Raspberry Pi
author: ALZ Team
lastmod: 2024-12-26T21:11:22Z
keywords: [ "installation", "raspberry pi", "linux", "astro live stacker", "guide" ]
weight: 220
tags: ['install', 'Linux', 'Raspberry Pi']
---

# 🖥️ Minimum System Requirements

## 64-bit GNU/Linux Distribution*
- Raspberry Pi OS - Bullseye (Version 11)
- Raspberry Pi OS - Bookworm
- any other distribution offering GLIBC 2.31 or higher

## Hardware Requirements
|                    | Minimum      |
|--------------------|--------------|
| **Model**          | Pi 4 Model B | 
| **RAM**            | 4 GB         |
| **Free Storage**   | 650 MB       | 

*_The ALS versions available for download for Raspberry Pi are intended for 64-bit systems.
However, you can easily adapt this [build script](https://github.com/deufrai/als/blob/release/0.7/ci/builds/build_dist_arm64_linux.sh)
to package a 32-bit version of ALS from the source. The only strict requirement is to use Python version 3.6.x. 
Feel free to [contact us](mailto://support@als-app.org) 
if you need assistance._

# 📦 Installation


1. **Open the Downloads folder**
    - Access your Downloads folder. You can usually find it by clicking on the icon of your file manager (for example, PCManFM) and selecting "Downloads" in the navigation menu on the left.

2. **Identify the ALS archive**
    - Look for the archive whose name starts with `als` and ends with `.tgz`. For example, it might be `als-v0.7-beta8.tgz`.

3. **Extract the archive**
    - To extract the archive, you can use a file manager:
        - Right-click on the `als-v0.7-beta8.tgz` archive.
        - Select "Extract Here" or a similar option.

4. **Move ALS to a permanent location**

   **Why move ALS out of the Downloads folder?**

   Moving ALS to a dedicated directory helps organize your files better and ensures the application is installed in a stable and permanent location. The Downloads folder is often used for temporary files and can be cleaned up regularly, leading to the accidental deletion of important files. By creating a specific folder for ALS, you ensure the application remains accessible and safe.

    - Open your file manager (for example, PCManFM).
    - Go to your home directory (`/home/username`).
    - Right-click in the directory and select "Create New Folder".
    - Name the folder `Applications` and press "Enter".
    - Double-click the `Applications` folder to open it.
    - Create another folder inside it called `ALS` and press "Enter".
    - Navigate to the Downloads folder (`Downloads`) in another window of your file manager. It's important to have two distinct and visible windows to easily drag and drop files.
    - Find the `als-v0.7-beta8` folder in the Downloads folder, then drag this folder into the `ALS` folder (`/home/username/Applications/ALS`).

5. **Run the executable**
    - Navigate to the `als-v0.7-beta8` folder in the file manager.
    - Double-click on the `als-v0.7-beta8` file.
    - If a dialog box appears asking you to confirm the execution, choose the option to run or open the file.

Continue to our [user guide](../user-guide/). We are here to assist you during this first start-up.

Enjoy using ALS! 🔭
