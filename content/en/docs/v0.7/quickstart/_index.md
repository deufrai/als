---
title: "Quick Start"
description: "Everything you need to know to get started with ALS."
author: "ALS Team"
lastmod: 2024-12-29T23:29:11Z
keywords: [ "Quick start with ALS" ]
draft: false
type: "docs"
categories: [ "user guide" ]
tags: [ "basics", "linux", "scan folder", "session", "work folder" ]
weight: 280
---

# Introduction

By the end of this chapter, you will have:

- Configured the only required settings for a quick start with ALS's default settings.
- Started your first stacking session and obtained your first results.

{{% alert color="info" %}}
🧠 Don't forget to put yourself [in the shoes of the character](../#character) before following this quick start guide 🌝
{{% /alert %}}

# Minimal Configuration

On the first start, ALS welcomes you and asks you to define two essential settings:

- **Scan folder**: The folder where ALS monitors the arrival of new subs.
- **Work folder**: The folder where ALS saves the produced images.

{{< center >}}
{{< figure src="welcome.png"
caption="Welcome message"
width="382px"
height="172px"
alt="Welcome message" >}}
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
width="628px"
height="250px"
alt="Preferences paths section" >}}
{{< /center >}}

🖱️ Click `Change...` next to **Scan folder**. A folder selector appears...

---

{{< center >}}
{{< figure src="prefs_02.png"
caption="The **scan folder** selector"
width="635px"
height="443px"
alt="Scan folder selector" >}}
{{< /center >}}

1. 🖱️ Select the **astroshots** folder.
2. 🖱️ Click `Choose`.

---

### Work Folder

Create a subfolder for ALS named **als_output** in your home directory:

{{< center >}}
{{< figure src="prefs_03.png"
caption="Button to set the **work folder**"
width="628px"
height="252px"
alt="Preferences paths section" >}}
{{< /center >}}

🖱️ Click `Change...` next to **Work folder**. A folder selector appears...

---

{{< center >}}
{{< figure src="prefs_04.png"
caption="Button to create a new folder"
width="730px"
height="455px"
alt="Create new folder button" >}}
{{< /center >}}

🖱️ Click `Create new folder`.

---

{{< center >}}
{{< figure src="prefs_05.png"
caption="New folder ready to be renamed"
width="635px"
height="443px"
alt="Renaming the new folder - step 1" >}}
{{< /center >}}

A new folder appears, ready to be renamed.

---

{{< center >}}
{{< figure src="prefs_06.png"
caption="New folder renamed and confirmed"
width="635px"
height="443px"
alt="Renaming the new folder - step 2" >}}
{{< /center >}}

- ⌨️ Name it **als_output**.
- 🖱️ Click `Choose`.

{{% alert color="warning" %}}
**⚠️ Do not confirm the preferences yet**, there is one important point left:
{{% /alert %}}

## Usage Statistics

It is very useful for us to know which versions of ALS are being used and on which platform.

{{< center >}}
{{< figure src="prefs_07.png"
caption="Checkbox indicating the choice to send usage statistics"
width="628px"
height="607px"
alt="Preferences screen - General tab" >}}
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
alt="ALS main window" >}}
{{< /center >}}

## Starting the Session

{{< center >}}
{{< figure src="start.png"
caption="The session start button"
width="297px"
height="162px"
alt="Session control panel before start" >}}
{{< /center >}}

🖱️ Click `START` in the **session** section at the top left

---

ALS confirms the successful session start:

{{< center >}}
{{< figure src="started.png"
caption="The session control buttons and session status are updated"
width="297px"
height="162px"
alt="Session control panel after start" >}}
{{< /center >}}

{{< center >}}
{{< figure src="status.png"
caption="The **session log** displays the latest events and the **status bar** is updated"
width="964px"
height="166px"
alt="Session log" >}}
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
alt="ALS main window - Stack 1" >}}
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
alt="ALS main window - Stack 15" >}}
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
alt="ALS main window - Stack 200" >}}
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
alt="Session control panel before stop" >}}
{{< /center >}}

🖱️ Click `STOP` in the **session** section at the top left. A confirmation window appears...

---

{{< center >}}
{{< figure src="stop.png"
caption="Session stop confirmation window"
width="612px"
height="151px"
alt="Session stop confirmation" >}}
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
alt="Menu entry for launcher creation" >}}
{{< /center >}}

🖱️ Open the **Utilities** menu and select the **Create launcher** item. A file selector appears...

{{< center >}}
<div style="display: flex; justify-content: center; gap: 1rem;">
{{< figure src="exe_picker.png"
caption="File selector for **PC**"
width="635px"
height="443px"
alt="PC file selector" >}}
{{< figure src="exe_picker_rpi.png"
caption="File selector for **Raspberry PI**"
width="661px"
height="463px"
alt="Raspberry Pi file selector" >}}
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
alt="Launcher creation confirmation window" >}}
{{< /center >}}

You can now easily start ALS using your system menu
{{< center >}}
{{< figure src="launcher_ok.png"
caption="ALS in the **Graphics** section of the system menu"
width="536px"
height="374px"
alt="System menu" >}}
{{< /center >}}

</details>
{{% /alert %}}

---

# Conclusion

ALS is now properly configured and ready to process your subs with its defaults settings.

You have just completed your first stacking session and obtained your first result.

Next step: diving in our user guide