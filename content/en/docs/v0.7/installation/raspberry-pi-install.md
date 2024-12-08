---
title: Installation on Raspberry Pi
description: Installing ALS on Raspberry Pi
author: ALZ Team
lastmod: 2024-12-08T16:40:58Z
keywords: [ "installation", "raspberry pi", "linux", "astro live stacker", "guide" ]
weight: 22
tags: ['install', 'Linux', 'Raspberry Pi']
---

1. **Open the Downloads folder**
    - Access your Downloads folder. You can usually find it by clicking on the icon of your file manager (for example, PCManFM) and selecting "Downloads" in the navigation menu on the left.

2. **Identify the ALS archive**
    - Look for the archive whose name starts with `als` and ends with `.tgz`. For example, it might be `als-v0.7-beta7.tgz`.

3. **Extract the archive**
    - To extract the archive, you can use a file manager:
        - Right-click on the `als-v0.7-beta7.tgz` archive.
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
    - Find the `als-v0.7-beta7` folder in the Downloads folder, then drag this folder into the `ALS` folder (`/home/username/Applications/ALS`).

5. **Run the executable**
    - Navigate to the `als-v0.7-beta7` folder in the file manager.
    - Double-click on the `als-v0.7-beta7` file.
    - If a dialog box appears asking you to confirm the execution, choose the option to run or open the file.

Continue to our [user guide](../user-guide/). We are here to assist you during this first start-up.

Enjoy using ALS! 🔭
