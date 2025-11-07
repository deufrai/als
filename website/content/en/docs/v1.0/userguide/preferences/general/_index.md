---
title: "General Tab"
description: "ALS Preferences General Tab Documentation"
author: "ALS Team"
lastmod: 2025-11-07T20:28:45Z
keywords: [ "ALS general settings", "ALS general preferences" ]
draft: false
type: "docs"
categories: ["configuration", "troubleshooting"]
tags: [ "scan folder", "memory", "profile", "language" ]
weight: 100331
---

The most critical ALS settings are presented in the `General` tab.

<div class="row">
<div class="col-md-4">

# Overview

This tab is divided into 3 sections:

- [Scanner](#scanner)
- [Memory](#memory)
- [Core](#core)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The General tab in ALS preferences"
width="622px"
height="660px"
alt="ALS preferences window with the General tab selected, displaying the Paths, Profile, Memory Management, and Basic Settings sections, including scan and work folder paths, profile options, memory slider, language setting, debug logs, and usage statistics." >}}
{{< /center >}}

</div>
</div>

# Scanner {#scanner}

## Scan Folder {#scan-folder}

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
width="622px"
height="244px"
alt="Software interface showing scan folder settings with the path set to /home/astrogeek/astroshots, and a Modify button to configure this path." >}}
{{< /center >}}

- 🖱️ click `Scan Folder...` to configure the **scan folder**
- The configured path is displayed to the right of the button

ℹ️ Defaut : ∅

# Memory Usage {#memory}

Defines ALS's behavior regarding the amount of memory it leaves to other applications.

{{< center >}}
{{< figure src="memory.png"
caption="Memory management preferences"
width="600px"
height="209px"
alt="" >}}
{{< /center >}}

The names associated with these slider steps are as vague as memory management can be.

We advise you to experiment with an open and joyful mind...

⚙️ Or consult the **Scanner** module's [detailed documentation](../../../reference/modules/scanner#memory-management)

ℹ️ Default: **Unfair**

---

# Core {#core}

{{% alert color="info" %}}
ℹ️ Changes made to core settings require a restart of ALS to take effect.
{{% /alert %}}

## Profile {#profile}

ALS offers two different operating modes, called **profiles**.

Profiles optimize ALS's behavior for specific uses:

| Profile                            | Scanner<br>Responsiveness | Similarity<br>Search Optimization |
|------------------------------------|---------------------------|-----------------------------------|
| Electronically Assisted Astronomy  | High                      | ON                                |
| Astrophoto                         | Normal                    | OFF                               |


- 🖱️ The `Electronically Assisted Astronomy` profile enforces application responsiveness.

   Recommended for medium-sized subs arriving at a high rate: a few seconds between each sub.

- 🖱️ The `Astrophoto Session Monitoring` profile enforces processing reliability.

   Recommended for large subs arriving at a slow rate: up to several minutes between each sub.

⚙️ You will find details on how profiles impact the **Scanner** in the [detailed documentation](../../../reference/modules/scanner#wait).

{{% alert title="🐛 Known Bug" color="danger" %}}
Using the **Electronically Assisted Astronomy** profile with square 1:1 subs causes alignment errors.

The subs stack up forming nested squares of decreasing sizes.
{{% /alert %}}

ℹ️ Default: **Electronically Assisted Astronomy**

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

{{< center >}}
{{< figure src="proflang.png"
caption="Profile and language preferences"
width="609px"
height="153px"
alt="Software interface showing work folder settings with the path set to /home/astrogeek/sorties_als, and a Modify button to configure this path." >}}
{{< /center >}}

---

## Data {#data}

### Detailed Logs {#logs}

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

- 🖱️ Check `Detailed Logs` to enable detailed message logging.

Detailed logs can slow down the application. Use this option when you need to analyze a malfunction
or plan to [report an issue](https://github.com/deufrai/als/issues) and provide us with as much information as possible.

Detailed logs include:
<div class="row">
<div class="col-md-6">

- application startup configuration

- your system's characteristics

- application-specific metrics

</div>
<div class="col-md-6">

- communications between all modules

- detailed processing steps
</div>
</div>

ℹ️ Default: **OFF**

{{< center >}}
{{< figure src="data.png"
caption="Data preferences"
width="622px"
height="198px"
alt="" >}}
{{< /center >}}

### Usage Stats

- 🖱️ Check `Usage stats` to enable the collection of ALS usage data.

The collected data is anonymous and used to improve the application.

You will find details on data collection in the [quick start guide](../../../quickstart#usage-stats).

ℹ️ Default: **OFF**