---
title: "General Tab"
description: "ALS Preferences General Tab Documentation"
author: "ALS Team"
lastmod: 2026-06-11T00:46:48Z
keywords: [ "ALS general settings", "ALS general preferences" ]
draft: false
type: "docs"
categories: ["configuration", "troubleshooting"]
tags: [ "scanner", "input", "scan folder", "memory", "profile", "outlier rejection", "log" ]
weight: 100331
---

The most critical ALS settings are presented in the `General` tab.

# Overview

<div class="row">
<div class="col-md-4">

This tab is divided into 3 sections:

- [Scanner](#scanner)
- [Memory use](#memory)
- [Core](#core)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The General tab in ALS preferences"
width="551px"
height="546px"
alt="ALS preferences window with the General tab selected, displaying Scanner, Memory use, Core, Profile, Language, Network and Data settings." >}}
{{< /center >}}

</div>
</div>

# Scanner {#scanner}

## Scan folder {#scan-folder}

{{% alert color="info" %}}
ℹ️ This setting can only be modified when the session is stopped.
{{% /alert %}}

Defines the path of the folder monitored by ALS to detect subs recorded by your acquisition system.

{{% alert color="light" %}}
💡 Detection works regardless of the subfolder structure inside the **scan folder**.

If your acquisition system saves subs in subfolders organized by target or date, monitor the parent folder of these subfolders.
{{% /alert %}}

{{< center >}}
{{< figure src="scan_folder_01.png"
caption="Scan folder preferences"
width="551px"
height="215px"
alt="Scanner settings showing the Scan folder... button and the configured path /home/astrogeek/astroshots." >}}
{{< /center >}}

- 🖱️ click `Scan folder...` to configure the **scan folder**
- The configured path is displayed to the right of the button

ℹ️ Default: ∅

# Memory use {#memory}

Defines ALS's behavior regarding the amount of memory it leaves to other applications.

{{< center >}}
{{< figure src="memory.png"
caption="Memory use preferences"
width="551px"
height="189px"
alt="Memory use settings with a slider ranging from Greedy to Scared and set to Unfair." >}}
{{< /center >}}

The names associated with these slider steps are as vague as memory management can be.

We advise you to experiment with an open and joyful mind...

⚙️ Or consult the **Scanner** module's [detailed documentation](../../../reference/modules/scanner#ram)

ℹ️ Default: **Unfair**

---

# Core {#core}

{{% alert color="info" %}}
ℹ️ Changes made to core settings require a restart of ALS to take effect.
{{% /alert %}}

## Profile {#profile}

ALS offers two different operating modes, called **profiles**.

Profiles optimize ALS's behavior for specific uses:

| Profile                            | Scanner Responsiveness | Processing Priority    | Sigma Clipping |
|------------------------------------|------------------------|------------------------|----------------|
| Electronically Assisted Astronomy  | High                   | Calibration + stacking | OFF            |
| Astrophoto Session Monitoring      | Normal                 | Image processing       | ON             |

`Electronically Assisted Astronomy` keeps detection, calibration, and stacking responsive so new subs can be integrated
quickly during a live observing session.

`Astrophoto Session Monitoring` gives more priority to image processing, which is commonly used between
low-paced incoming subs. It also enables sigma clipping in **mean** stacking mode to remove transient bright artifacts
such as satellite trails.

- 🖱️ Select the profile matching the activity you want ALS to support.

⚙️ You will find details on how profiles impact the **Scanner** in the [detailed documentation](../../../reference/modules/scanner#wait).

ℹ️ Default: **Electronically Assisted Astronomy**

{{< center >}}
{{< figure src="proflang.png"
caption="Profile and language preferences"
width="551px"
height="205px"
alt="Core settings showing the Electronically Assisted Astronomy and Astrophoto Session Monitoring profiles and the interface language selection." >}}
{{< /center >}}

## Language {#language}

Defines the language of the ALS user interface.

- 🖱️ The following choices are available:

  - **System**: ALS follows the system language
  - **French**
  - **English**
  - **Russian**

ℹ️ Default: **System**

{{% alert color="info" %}}
If you chose **system** and your system is using a language not supported by ALS, the interface will be displayed in English.
{{% /alert %}}

---

## Network {#network}

### Send usage statistics on startup {#usage-stats}

It is very useful for us to know which versions of ALS are being used and on which platform.

We would be very grateful if you allow ALS to send us usage statistics, but we also understand that you may be reluctant
to enable such a feature.

Please note that:

- ALS will **only** send the following information at each startup:
  - ALS version.
  - Machine architecture.
  - Operating system type.
- We do not seek to identify or geolocate the source of this information.

<details>
    <summary>Click here to see how you can verify these claims yourself</summary>

ALS and our tracking tools are **opensource** software, their source code is publicly available.

- <a href="https://github.com/deufrai/als/blob/v1.0/src/als/main.py#L51" target="_blank">code for sending
  statistics by ALS</a> <i class="fa-brands fa-square-github"></i>
- <a href="https://github.com/deufrai/als-stats-receiver/blob/master/listen.py#L42" target="_blank">code for recording
  received statistics by our servers</a> <i class="fa-brands fa-square-github"></i>

</details>

- 🖱️ Check `Send usage statistics on startup` to enable the collection of ALS usage data.

ℹ️ Default: **OFF**

### Check for updates on startup {#check-updates}

ALS can check if a new version is available at each startup.

If a new version is available, a message will be displayed below the `Modules` group on the Main controls panel.

- 🖱️ Check `Check for updates on startup` to enable the new version check.

ℹ️ Default: **OFF**

{{< center >}}
{{< figure src="net_data.png"
caption="Network and Data preferences"
width="551px"
height="198px"
alt="TODO" >}}
{{< /center >}}

## Data {#data}

### Detailed logs {#logs}

Manages the level of detail in the messages written to the log file.

The log file is named **als.log**. It is located in your home folder:

{{< tabpane text=true >}}
  {{% tab header="Linux" %}}
  <span style="font-family: monospace;">/home/astrogeek/als.log</span>
  {{% /tab %}}
  {{% tab header="Windows" %}}
  <span style="font-family: monospace;">C:\Users\astrogeek\als.log</span>
  {{% /tab %}}
  {{% tab header="macOS"  %}}
  <span style="font-family: monospace;">/Users/astrogeek/als.log</span>
  {{% /tab %}}
{{< /tabpane >}}

- 🖱️ Check `Detailed logs` to enable detailed message logging.

Detailed logs can slow down the application. Use this option when you need to analyze a malfunction
or plan to [report an issue](https://github.com/deufrai/als/issues) and provide us with as much information as possible.

Detailed logs include:

- application startup configuration
- your system's characteristics
- application-specific metrics
- communications between all modules
- detailed processing steps

ℹ️ Default: **OFF**
