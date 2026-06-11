---
title: "Quick Start"
description: "Everything you need to know to get started with ALS."
author: "ALS Team"
lastmod: 2026-06-11T00:33:39Z
keywords: [ "Quick start with ALS" ]
draft: false
type: "docs"
categories: [ "beginner's guide" ]
tags: [ "linux", "scan folder", "session", "stack", "processing", "output", "save", "work folder" ]
weight: 100280
---

# Introduction {#introduction}

By the end of this chapter, you will have:

- Configured the only required settings for a quick start
- Started your first stacking session and obtained your first results.

# Initial configuration {#initial-configuration}

On the first start, ALS introduces the configuration steps required to get started:

ALS needs to know the paths of two **critical folders**:

- The **Scan folder**: The folder where ALS monitors the arrival of new subs.
- The **Work folder**: The folder where ALS saves the produced images.

{{< center >}}
{{< figure src="welcome.png"
caption="ALS welcome screen with setup options"
width="787px"
height="461px"
alt="ALS welcome screen with setup options" >}}
{{< /center >}}

You have two options: 

## Default configuration {#default-configuration}

- 🖱️ Click the left button to let ALS create the 2 folders on **your desktop** then start the application

## Custom configuration {#custom-configuration}

- 🖱️ Click the right button to choose custom folders

{{< center >}}
{{< figure src="custom_config.png"
caption="ALS custom folder setup screen"
width="787px"
height="461px"
alt="ALS custom folder setup screen" >}}
{{< /center >}}

- 🖱️ Click both buttons to select the **Scan folder** and the **Work folder** ALS will use

ALS also monitors subfolders, so if your acquisition system organizes subs into folders by date, target name, frame type,
or similar criteria, select their common parent folder as ALS's **Scan folder**.

You can select or create any folder on your system, but we recommend using folders on a fast drive

- 🖱️ Once both folders are set, click `GO !` to start the application


# Your Very First Session {#your-very-first-session}

To save your sight until the end if this guide, we switch ALS to **dark mode**, using either :
- the `View > Dark theme` menu
- the {{< als-ks >}}T{{< /als-ks >}} keyboard sgortcut

{{< center >}}
{{< figure src="ready.png"
caption="ALS ready to start its very first session"
width="1920px"
height="1080px"
alt="ALS main window showing a software interface for stacking astronomical images in real-time. The interface includes sections for main controls (start, pause, stop), stack settings (align, minimum matches), image server (start, stop), image saver (save current, save every frame), workers (queue size, status), processing (histogram, auto stretch, levels, RGB balance), and session log." >}}
{{< /center >}}

## Starting the Session {#starting-the-session}

{{< center >}}
{{< figure src="start.png"
caption="The session start button"
width="319px"
height="130px"
alt="ALS main controls section with the Session subsection, showing the START, PAUSE, and STOP buttons. The START button is highlighted with a red arrow pointing to it. Below, indicators for Stack size (0) and Stack exposure (n/a) are displayed. The status reads 'stopped'." >}}
{{< /center >}}

🖱️ Click `START` in the **session** section at the top left

---

ALS confirms the successful session start:

{{< center >}}
{{< figure src="started.png"
caption="The session control buttons and session status are updated"
width="319px"
height="130px"
alt="ALS main controls section with the Session subsection, showing the START, PAUSE, and STOP buttons. Below these buttons, indicators for Stack size (0) and Stack exposure (n/a) are displayed. The status reads 'running' with a red arrow pointing to it." >}}
{{< /center >}}

{{< center >}}
{{< figure src="status.png"
caption="The **session log** displays the latest events and the **status bar** is updated"
width="959px"
height="163px"
alt="Session log showing informational messages with timestamps. The entries include 'Starting new session,' 'Input scanner started,' and 'Session running in mode mean with alignment True.' Buttons labeled Acknowledge, issues only, follow. Statusbar item reads : session running" >}}
{{< /center >}}

---

🎛️ Before starting your acquisitions, make sure that new subs will be saved in the **Scan folder** configured in ALS, or
any of its subfolders.

🎛️ Now start the acquisitions with your usual system. ALS detects and processes each new sub.

As an example, we will illustrate the following sections with a session on Messier 27: ZWO ASI224MC camera, 200 x 4 sec. subs

{{< center >}}
{{< figure src="stacked_01.png"
caption="ALS after processing the 1<sup>st</sup> sub"
width="1920px"
height="1080px"
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
height="1080px"
alt="ALS main window after processing the 15th sub, displaying a less noisy and more detailed image of Messier 27 nebula with scattered stars. The session log shows successful processing messages. The processing panel on the right provides histogram and level adjustments, RGB balance, and auto stretch settings." >}}
{{< /center >}}

After each alignment and stacking of a new sub, ALS automatically adjusts the brightness and color balance before
displaying the result in the **central area**.

As you stack more subs, you will see the result gain in contrast and detail. The grainy appearance of the sky background
will gradually fade away.

---

## Explore {#explore}

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
height="1080px"
alt="The Astro Live Stacker (ALS) main window after processing the 200th sub, displaying a smooth, detailed, and high-contrast image of the Messier 27 nebula with numerous stars. The session log at the bottom shows successful processing messages and the image saver panel on the left indicates that the images have been saved successfully. The right panel includes processing options such as histogram adjustments, auto stretch, levels, and RGB balance." >}}
{{< /center >}}

This quick start guide does not cover the other features and settings of ALS. However, ALS has been designed to be very
intuitive. Feel free to explore and experiment with the various controls located on the right side of the screen in the
**Processing** section.

---

## Stopping the Session {#stopping-the-session}

Our express guided tour is coming to an end, stop the current session.

{{< center >}}
{{< figure src="stopping.png"
caption="The session stop button"
width="319px"
height="130px"
alt="Main controls section in ALS software interface, specifically the Session area showing START, PAUSE, and STOP buttons. The STOP button is highlighted with a red arrow pointing to it. Below the buttons are Stack size (200) and Stack exposure (0:13:20). The status shows 'running'." >}}
{{< /center >}}

🖱️ Click `STOP` in the **session** section at the top left. A confirmation window appears...

---

{{< center >}}
{{< figure src="stop.png"
caption="Session stop confirmation window"
width="604px"
height="153px"
alt="Dialog box titled 'Session stop,' asking for confirmation to stop the current session with a message: 'Stopping the current session will reset the stack and all image enhancements. Are you sure you want to stop the current session?' Below the message are a checkbox labeled 'Save result before stop' and two buttons labeled 'No' and 'Yes.' The 'No' button is highlighted in red, and the 'Yes' button is highlighted in green." >}}
{{< /center >}}

🖱️ Click `Yes`

You will find the final result of this session in the file named **stack_image.jpg** saved in the **work folder**

---

{{% alert title="ℹ️ Linux Systems" color="info" %}}
This section is exclusively for ALS users on Linux, whether on PC or Raspberry Pi
<details>
<summary>Creating a system launcher for ALS</summary>

This optional step creates a launcher in your system application menu, so you can start ALS without browsing to the
installation folder each time.

🖱️ Open the **Utilities** menu and select **Create launcher**. A file selector appears.

1. 🖱️ Browse to the folder where ALS is located
    - **PC**: Browse to {{< als-code >}}/home/astrogeek/Applications/ALS{{< /als-code >}}
    - **Raspberry Pi**: Browse to {{< als-code >}}/home/astrogeek/Applications/ALS/als-v1.0{{< /als-code >}}
2. 🖱️ Select the executable
    - **PC**: Select the file {{< als-code >}}als-v1.0.run{{< /als-code >}}
    - **Raspberry Pi**: Select the file {{< als-code >}}als-v1.0{{< /als-code >}}
3. 🖱️ Click `Open`

ALS confirms the successful creation of the launcher

ALS is now accessible from your system menu, in the Graphics section

</details>
{{% /alert %}}

---

# Conclusion {#conclusion}

ALS is now properly configured and ready to process your subs with its default settings.

You have just completed your first stacking session and obtained your first result.

Next step: diving in our [user guide](../userguide/)
