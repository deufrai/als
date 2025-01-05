---
title: "Output Tab"
description: "ALS Preferences Output Tab Documentation"
author: "ALS Team"
lastmod: 2025-01-05T10:44:51Z
keywords: ["ALS output settings", "ALS Output preferences"]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["output", "server", "web folder", "work folder", "save"]
weight: 333
---

The settings governing ALS outputs are presented in the `Output` tab.

<div class="row">
<div class="col-md-4">

# Overview

This tab is divided into 2 sections:

- [File Saver](#save)
- [Image Server](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The Output tab in preferences"
width="622px"
height="604px"
alt="" >}}
{{< /center >}}

</div>
</div>

# Save {#save}

Here are the output file format, output folders, and autosave function settings 

## Format {#format}

ALS saves the main output images in one of the following formats:
- **TIFF**
- **PNG**
- **JPEG**

{{< center >}}
{{< figure src="formats.png"
caption="Main output file format preferences"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

- 🖱️ use the `Format` buttons to set the main output file format

ℹ️ Default: JPEG

## Output Folders {#output-folders}

ALS uses two output folders:
- **work folder**

  Destination of the **main output**

- **web folder**

  Destination of the **server output**

### Work Folder {#work-folder}

- 🖱️ click `Work Folder...` to configure the work folder

{{< center >}}
{{< figure src="folders.png"
caption="Output folders preferences"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

ℹ️ Default: ∅

### Web Folder {#web-folder}

{{% alert color="info" %}}
ℹ️ By default, the **web folder** is an alias leading to the **work folder**

You have the option to actually separate the two ALS outputs by using a dedicated **web folder**
{{% /alert %}}

### Dedicated Web Folder {#web-dedicated}

- 🖱️ check `Dedicated Web Folder` to display the dedicated **web folder** settings
- 🖱️ click `Web Folder...` to configure the dedicated **web folder**

ℹ️ Default: OFF

## Autosave {#autosave}

### Timestamped Result on Session Stop {#autosave-stop}

Activates the saving, on **each session stop**, of the **last** processing result:

- **output**: main output
- **name**: composed of **stack_image** + **_final** + _timestamp suffix_
- **Format**: Configured output format

{{% alert title="💡" color="light" %}}
This function is useful when you chain sessions on different targets

At each session stop, the best image for that target is saved in a file that is not at risk 
of being overwritten
{{% /alert %}}

{{< center >}}
{{< figure src="autosave.png"
caption="Autosave preferences"
width="622px"
height="417px"
alt="" >}}
{{< /center >}}

- 🖱️ check `Timestamped Result on Session Stop` to activate the autosave function

ℹ️ Default: OFF

# Server {#server}

Here, the image server listening port and the image refresh period are configured.

## Port Number {#server-port}

The image server listening port is configured here

Allowed values: 1024 to 65535

- ⌨️ Enter the `port number` on which the ALS image server will be accessible

{{< center >}}
{{< figure src="web_config.png"
caption="Web server settings"
width="622px"
height="215px"
alt="" >}}
{{< /center >}}

ℹ️ Default: 8000

## Refresh Period {#server-refresh}

Period, in sec., used in the web page served by ALS to force connected browsers to refresh the image

`Refresh Period` configures the refresh period

You can:
- ⌨️ enter the value via keyboard
- 🖱️ use the arrow buttons
- 🖱️ use the mouse wheel

ℹ️ Default: 5 sec.
