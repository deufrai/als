---
title: "General Tab"
description: "Documentation of the General tab in ALS preferences"
author: "ALS Team"
lastmod: 2024-12-31T21:07:16Z
keywords: [ "ALS general settings", "ALS general preferences" ]
draft: false
type: "docs"
categories: ["configuration", "troubleshooting"]
tags: [ "scan folder", "memory", "profile", "language" ]
weight: 331
---

Most critical settings are presented in the Preferences page `General` tab.

<div class="row">
<div class="col-md-4">

# Overview

This tab is divided into 4 sections:

- [Paths](#paths)
- [Profile](#profile)
- [Memory Management](#memory)
- [General](#general)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The General tab of the preferences"
width="622px"
height="604px"
alt="ALS preferences window with General tab selected, showing sections for Paths, Profile, Memory Management, and Core settings, including paths for Scan and Work folders, profile options, memory slider, language setting, debug logs, and usage stats." >}}
{{< /center >}}

</div>
</div>

# Paths {#paths}

{{% alert color="info" %}}
ℹ️ These settings are only accessible when the session is stopped
{{% /alert %}}

## Scan Folder {#scan-folder}

Defines the path of the folder monitored by ALS to detect subs recorded by your acquisition system.

{{% alert color="light" %}}
💡 Detection works regardless of the subfolder structure within the **scan folder**.

If your acquisition system records subs in subfolders organized by target or date, set the **scan folder** to the parent
folder of these subfolders.
{{% /alert %}}

{{< center >}}
{{< figure src="scan_folder_01.png"
caption="Scan folder preferences"
width="622px"
height="168px"
alt="Software interface showing settings for Scan folder with the path set to /home/astrogeek/astroshots, and a Change button for configuring this path." >}}
{{< /center >}}

1. `Change...` allows you to configure the **scan folder**.
2. The configured path is displayed to the right of the button

## Work Folder {#work-folder}

Sets the path of the **work folder**

{{< center >}}
{{< figure src="work_folder.png"
caption="Work folder preferences"
width="610px"
height="160px"
alt="Software interface showing settings for Work folder with the path set to /home/astrogeek/sorties_als, and a Change button for configuring this path." >}}
{{< /center >}}

1. `Change...` allows you to configure the **work folder**.
2. The configured path is displayed to the right of the button

# Profile {#profile}

# Memory Management {#memory}

# General {#general}

Oops, twice general. 🫡