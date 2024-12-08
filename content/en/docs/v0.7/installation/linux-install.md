---
title: Install on a Linux PC
description: Installing ALS on a Linux PC
author: ALZ Team

lastmod: 2024-12-08T10:07:10Z
keywords: ["installation", "linux", "astro live stacker", "guide"]
weight: 21
---

1. **Open the Downloads Folder**:
   - Navigate to your downloads folder. You can usually find it by clicking on your file manager's icon (such as Nautilus, Dolphin, or Thunar) and selecting "Downloads" from the navigation menu on the left.
   - Alternatively, you can open a terminal and enter the following command to go directly to the downloads folder:
     ```bash
     cd ~/Downloads
     ```

2. **Identify the ALS File**:
   - Look for the file that starts with `als` and ends with `.run`. For example, it might be `als-v0.7-beta6.run`.

3. **Make the File Executable**:
   - To make the file executable, you need to change its permissions. This can be done directly from the file manager or via the terminal.
   
   **Via the File Manager**:
     - Right-click on the `als-v0.7-beta6.run` file.
     - Select "Properties".
     - Go to the "Permissions" tab.
     - Check the option "Allow executing file as a program".

   **Via the Terminal**:
     - Open a terminal and make sure you are in the downloads folder:
       ```bash
       cd ~/Downloads
       ```
     - Run the following command to make the file executable:
       ```bash
       chmod +x als-v0.7-beta6.run
       ```

4. **Run the Executable File**:
   - **Via the Terminal**:
     - Still in the terminal, run the following command:
       ```bash
       ./als-v0.7-beta6.run
       ```
   - **Via the File Manager**:
     - Double-click on the `als-v0.7-beta6.run` file.
     - If a dialog box appears asking you to confirm the execution of the file, choose the option to execute or open the file.

Enjoy using ALS! 🚀✨

