---
title: "Quick Start"
description: "Everything you need to know to get started with ALS."
author: "ALS Team"
lastmod: 2024-12-31T21:07:16Z
keywords: [ "Quick start with ALS" ]
draft: false
type: "docs"
categories: [ "beginner's guide" ]
tags: [ "linux", "scan folder", "session", "work folder"  ]
weight: 280
---

# Introduction

By the end of this chapter, you will have:

- Configured the only required settings for a quick start with ALS's default settings.
- Started your first stacking session and obtained your first results.

# In the shoes of the character... {#character}

Throughout this journey, you will embody a new ALS user:

- **Username**: Your username is **astrogeek**
- **System used**: You use ALS on a Linux system
- **Organization of subs**: Your acquisition system saves the subs in the **astroshots** folder of your home
  directory, organized by target with subs in **Light** subfolders.

  Example: Session on Messier 27, the subs are saved in the **astroshots/M_27/Light** folder.

{{< center >}}
{{< figure
src="lights_placement.png"
width="889px" height="479px"
caption="Placement of raw images"
alt="File manager window displaying the Light subfolder within the directory astroshots/M_27/Light, showing eight FITS files" >}}
{{< /center >}}

# Initial Configuration

On the first start, ALS welcomes you and asks you to define two essential settings:

- **Scan folder**: The folder where ALS monitors the arrival of new subs.
- **Work folder**: The folder where ALS saves the produced images.

{{< center >}}
{{< figure src="welcome.png"
caption="Welcome message"
width="382px"
height="172px"
alt="Welcome dialog box for ALS with text indicating it's the user's first use and instructions to set paths for the Scan and Work folders. An OK button is at the bottom right." >}}
{{< /center >}}

🖱️ Click `OK` to access the preferences.

---

## Configure Critical Folders

The critical folders are defined in the **Paths** section of the **General** tab.

### Scan Folder

ALS monitors the arrival of new subs in this folder.

{{% alert color="info" %}}
ℹ️ Detection works regardless of the subfolder structure inside the **scan folder**.
{{% /alert %}}

Configure ALS to monitor the **astroshots** folder:

{{< center >}}
{{< figure src="prefs_01.png"
caption="Button to set the **scan folder**"
width="622px"
height="226px"
alt="Screenshot of ALS preferences showing the General tab. A red arrow highlights the Scan folder button." >}}
{{< /center >}}

🖱️ Click `Scan folder...`. A folder selector appears...

---

{{< center >}}
{{< figure src="prefs_02.png"
caption="The **scan folder** selector"
width="635px"
height="443px"
alt="File selection dialog box titled 'Select scan folder' with the astroshots folder highlighted under the user astrogeek directory. The Choose button is highlighted, indicating the user is about to confirm the selection." >}}
{{< /center >}}

1. 🖱️ Select the **astroshots** folder.
2. 🖱️ Click `Choose`.

---

### Work Folder

Create a subfolder for ALS named **als_output** in your home directory:

{{< center >}}
{{< figure src="prefs_03.png"
caption="The file output settings"
width="622px"
height="328px"
alt="Screenshot of ALS preferences showing the Output tab. The Work folder field is highlighted." >}}
{{< /center >}}

1. Switch to the **Output** tab
2. 🖱️ Click `Work folder...`. A folder selector appears...

---

{{< center >}}
{{< figure src="prefs_04.png"
caption="Button to create a new folder"
width="730px"
height="455px"
alt="File selection dialog box titled 'Select work folder' displaying the contents of the directory /home/astrogeek, showing various folders and a log file. A red arrow points to the 'Create New Folder' button, indicating the option to create a new folder." >}}
{{< /center >}}

🖱️ Click `Create new folder`.

---

{{< center >}}
{{< figure src="prefs_05.png"
caption="New folder ready to be renamed"
width="635px"
height="443px"
alt="File selection dialog box titled 'Select work folder' displaying the contents of the directory /home/astrogeek. A newly created folder named 'New Folder' is highlighted in blue, ready to be renamed. The bottom part of the dialog box has fields for Directory and Files of type, with buttons labeled Choose and Cancel." >}}
{{< /center >}}

A new folder appears, ready to be renamed.

---

{{< center >}}
{{< figure src="prefs_06.png"
caption="New folder renamed and confirmed"
width="635px"
height="443px"
alt="File selection dialog box titled 'Select work folder' displaying the contents of the directory /home/astrogeek, including several folders and a log file. The newly created folder named als_output is highlighted, and the Choose button is highlighted, indicating the user is about to confirm the selection." >}}
{{< /center >}}

1. ⌨️ Name it **als_output**.
2. 🖱️ Click `Choose`.

🖱️ Switch back to the `General` tab.

{{% alert color="warning" %}}
**⚠️ Do not confirm the preferences yet**, there is one important point left:
{{% /alert %}}

## Usage Statistics

It is very useful for us to know which versions of ALS are being used and on which platform.

{{< center >}}
{{< figure src="prefs_07.png"
caption="Checkbox indicating the choice to send usage statistics"
width="622px"
height="660px"
alt="Screenshot of ALS preferences showing the General tab. The Data section with Usage statistics is highlighted." >}}
{{< /center >}}

We would be very grateful if you allow ALS to send us usage statistics, but we also understand that you may be reluctant
to enable such a feature.

Please note that:

- ALS will **only** send the following information at each startup:
    - ALS version.
    - Processor type.
    - Operating system type.
- We do not seek to identify or geolocate the source of this information.

<details>
    <summary>Click here to see how you can verify these claims yourself</summary>

ALS and our tracking tools are **opensource** software, their source code is publicly available.

- <a href="https://github.com/deufrai/als/blob/release/0.7/src/als/main.py#L46" target="_blank">code for sending
  statistics by ALS</a> <i class="fa-brands fa-square-github"></i>
- <a href="https://github.com/deufrai/als-stats-receiver/blob/master/listen.py#L35" target="_blank">code for recording
  received statistics by our servers</a> <i class="fa-brands fa-square-github"></i>

</details>

---

🖱️ Once you have made your choice, click `OK` to confirm the preferences.

---

# Your Very First Session

{{< center >}}
{{< figure src="ready.png"
caption="ALS ready to start its very first session"
width="1920px"
height="1053px"
alt="ALS main window showing a software interface for stacking astronomical images in real-time. The interface includes sections for main controls (start, pause, stop), stack settings (align, threshold), image server (start, stop), image saver (save current, save every frame), workers (queue size, status), processing (histogram, auto stretch, levels, RGB balance), and session log." >}}
{{< /center >}}

## Starting the Session

{{< center >}}
{{< figure src="start.png"
caption="The session start button"
width="297px"
height="162px"
alt="ALS main controls section with the Session subsection, showing the START, PAUSE, and STOP buttons. The START button is highlighted with a red arrow pointing to it. Below, indicators for Stack size (0) and Stack exposure (n/a) are displayed. The status reads 'stopped'." >}}
{{< /center >}}

🖱️ Click `START` in the **session** section at the top left

---

ALS confirms the successful session start:

{{< center >}}
{{< figure src="started.png"
caption="The session control buttons and session status are updated"
width="297px"
height="162px"
alt="ALS main controls section with the Session subsection, showing the START, PAUSE, and STOP buttons. Below these buttons, indicators for Stack size (0) and Stack exposure (n/a) are displayed. The status reads 'running' with a red arrow pointing to it." >}}
{{< /center >}}

{{< center >}}
{{< figure src="status.png"
caption="The **session log** displays the latest events and the **status bar** is updated"
width="964px"
height="166px"
alt="Session log showing informational messages with timestamps. The entries include 'Starting new session,' 'Input scanner started,' and 'Session running in mode mean with alignment True.' Buttons labeled Acknowledge, issues only, follow. Statusbar item reads : session running" >}}
{{< /center >}}

---

🎛️ Now start the acquisitions with your usual system. ALS detects and processes each new sub.

As an example, we will illustrate the following sections with a session on Messier 27: ZWO ASI224MC camera, 200 x 4 sec.
subs

{{< center >}}
{{< figure src="stacked_01.png"
caption="ALS after processing the 1<sup>st</sup> sub"
width="1920px"
height="1053px"
alt="ALS main window after processing the first sub, displaying an initial, slightly noisy image of Messier 27 nebula with scattered stars. The session log shows successful processing messages. The processing panel on the right provides histogram and level adjustments, RGB balance, and auto stretch settings." >}}
{{< /center >}}

{{% alert color="info" %}}
ℹ️ The first detected sub serves as the **alignment reference** for the entire session
{{% /alert %}}

---

All new subs are first aligned to this reference and then stacked by averaging with all previously processed
subs.

{{< center >}}
{{< figure src="stacked_15.png"
caption="ALS after processing the 15<sup>th</sup> image. Contrast and noise improve"
width="1920px"
height="1053px"
alt="ALS main window after processing the 15th sub, displaying a less noisy and more detailed image of Messier 27 nebula with scattered stars. The session log shows successful processing messages. The processing panel on the right provides histogram and level adjustments, RGB balance, and auto stretch settings." >}}
{{< /center >}}

After each alignment and stacking of a new sub, ALS automatically adjusts the brightness and color balance before
displaying the result in the **central area**.

As you stack more subs, you will see the result gain in contrast and detail. The grainy appearance of the sky background
will gradually fade away.

---

## Explore

Let ALS work on the subs that keep coming in and lose yourself a bit in the **central area**:

- 🖱️ Zoom in and out using your mouse wheel
- 🖱️ Navigate the image by dragging it, like with any other viewing software
- 🖱️ Reset the zoom by right-clicking in the image

The image in the **central area** is instantly updated after each sub is processed, with no impact on navigation.

---

{{< center >}}
{{< figure src="stacked_200.png"
caption="ALS after processing the 200<sup>th</sup> image. A beautiful, detailed, and smoothed image"
width="1920px"
height="1053px"
alt="The Astro Live Stacker (ALS) main window after processing the 200th sub, displaying a smooth, detailed, and high-contrast image of the Messier 27 nebula with numerous stars. The session log at the bottom shows successful processing messages and the image saver panel on the left indicates that the images have been saved successfully. The right panel includes processing options such as histogram adjustments, auto stretch, levels, and RGB balance." >}}
{{< /center >}}

This quick start guide does not cover the other features and settings of ALS. However, ALS has been designed to be very
intuitive. Feel free to explore and experiment with the various controls located on the right side of the screen in the
**Processing** section.

---

## Stopping the Session

Our express guided tour is coming to an end, stop the current session.

{{< center >}}
{{< figure src="stopping.png"
caption="The session stop button"
width="305px"
height="165px"
alt="Main controls section in ALS software interface, specifically the Session area showing START, PAUSE, and STOP buttons. The STOP button is highlighted with a red arrow pointing to it. Below the buttons are Stack size (200) and Stack exposure (0:13:20). The status shows 'running'." >}}
{{< /center >}}

🖱️ Click `STOP` in the **session** section at the top left. A confirmation window appears...

---

{{< center >}}
{{< figure src="stop.png"
caption="Session stop confirmation window"
width="612px"
height="151px"
alt="Dialog box titled 'Session stop,' asking for confirmation to stop the current session with a message: 'Stopping the current session will reset the stack and all image enhancements. Are you sure you want to stop the current session?' Below the message are a checkbox labeled 'Save result before stop' and two buttons labeled 'No' and 'Yes.' The 'No' button is highlighted in red, and the 'Yes' button is highlighted in green." >}}
{{< /center >}}

🖱️ Click `Yes`

You will find the final result of this session in the file named **stack_image.jpg** saved in the **work folder**

---

{{% alert title="ℹ️ Linux Systems" color="info" %}}
This section is exclusively for ALS users on Linux, whether on PC or Raspberry Pi
<details>
<summary>Creating a system launcher for ALS</summary>

{{< center >}}
{{< figure src="launcher_menu.png"
caption="Launcher creation menu"
width="491px"
height="197px"
alt="The image shows a screenshot of a software interface with a dark theme. The top menu bar includes options such as File, Session, Edit, Image, View, Utilities, and Help. The Utilities menu is expanded, revealing two options: QR Code and Create launcher, with the latter highlighted in blue and a cursor pointing to it" >}}
{{< /center >}}

🖱️ Open the **Utilities** menu and select the **Create launcher** item. A file selector appears...

{{< center >}}
<div style="display: flex; justify-content: center; gap: 1rem;">
{{< figure src="exe_picker.png"
caption="File selector for **PC**"
width="635px"
height="443px"
alt="File selection dialog box titled 'Select your ALS executable.' The directory path is set to /home/astrogeek/Applications/ALS. The file als-v0.7-beta7.run is selected, with a size of 255.47 MiB, indicating it is a run File. The Open button is highlighted, suggesting the user is about to open the selected file. Three numbered arrows point to the directory path, the selected file, and the Open button." >}}
{{< figure src="exe_picker_rpi.png"
caption="File selector for **Raspberry PI**"
width="661px"
height="463px"
alt="File selection dialog box titled 'Select your ALS executable.' The dialog box is used to navigate through directories and select a specific file. The directory path shown is /home/astrogeek/Applications/ALS/als-v0.7-beta7. The file als-v0.7-beta7 is highlighted and selected. The dialog box has three main labeled elements: 1. The 'Look in:' field showing the current directory path. 2. The file list area where the 'als-v0.7-beta7' file is selected. 3. The 'Open' button to confirm the selection and the 'Cancel' button to cancel the operation." >}}
</div>
{{< /center >}}

1. 🖱️ Browse to the folder where ALS is located
    - **PC**: Browse to `/home/astrogeek/Applications/ALS`
    - **Raspberry PI**: Browse to `/home/astrogeek/Applications/ALS/als-v0.7-beta8`
2. 🖱️ Select the executable
    - **PC**: Select the file `als-v0.7-beta8.run`
    - **Raspberry PI**: Select the file `als-v0.7-beta8`
3. 🖱️ Click `Open`

ALS confirms the successful creation of the launcher
{{< center >}}
{{< figure src="launcher_created.png"
caption="Launcher creation confirmation window"
width="305px"
height="129px"
alt="Notification window with the title 'ALS launcher created / updated.' The notification contains an icon of a lightbulb and the text 'You'll find ALS with the graphics apps.' There is an 'OK' button at the bottom right of the window." >}}
{{< /center >}}

You can now easily start ALS using your system menu
{{< center >}}
{{< figure src="launcher_ok.png"
caption="ALS in the **Graphics** section of the system menu"
width="536px"
height="374px"
alt="The image shows a section of a computer screen displaying the 'Applications' menu, specifically highlighting the 'Graphics' category. The menu lists various graphics-related applications available on the system, including Astro Live Stacker - Live Stacking Made in France." >}}
{{< /center >}}

</details>
{{% /alert %}}

---

# Conclusion

ALS is now properly configured and ready to process your subs with its defaults settings.

You have just completed your first stacking session and obtained your first result.

Next step: diving in our user guide