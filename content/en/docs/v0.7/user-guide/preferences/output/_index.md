---
title: "Output Tab"
description: "Documentation of the Output tab in ALS preferences"
author: "ALS Team"
lastmod: 2024-12-30T12:16:23Z
keywords: ["ALS output settings", "ALS Output preferences"]
draft: false
type: "docs"
categories: ["user guide"]
tags: ["preferences", "output", "formats", "server", "web folder"]
weight: 333
---

The settings governing ALS produced results are presented in the `Output` tab of the preferences.

<div class="row">
<div class="col-md-4">

# Overview

This tab is divided into 2 sections:

- [File Saving](#save)
- [Web Server](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The Output tab of the preferences"
width="622px"
height="604px"
alt="The Output tab of the preferences" >}}
{{< /center >}}

</div>
</div>

# File Saving {#save}

Here are the settings for the output file format and the **autosave on stop** feature

<div class="row">
<div class="col-md-8">

## Format

The `Format` buttons define the output file format

## Autosave on stop

`Autosave on stop` activates the automatic saving of the **last** result of te **Process** module into a new 
timestamped file, on every session stop:

- **file location**: **working directory**
- **file name**: composed of **stack_image** and a timestamp suffix
- **File format and extension**: according to the chosen format

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">

{{< center >}}
{{< figure src="saver.png"
caption="File saving preferences"
width="252px"
height="107px"
alt="File saving preferences" >}}
{{< /center >}}

</div>
</div>


# Web Server {#server}

Here are the settings for the image server

<div class="row">
<div class="col-md-8">

## Server Port {#server-port}

1. `Server port number` configures the port on which the image server is accessible

## Refresh Period {#server-refresh}

2. `Web page refresh period` configures the image refresh period used by connected browsers

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="web_config.png"
caption="Web server settings"
width="480px"
height="201px"
alt="Web server settings" >}}
{{< /center >}}

</div>
</div>

## Web Folder {#web-folder}

{{< center >}}
{{< figure src="web_folder.png"
caption="Web folder settings"
width="595px"
height="211px"
alt="Web folder settings" >}}
{{< /center >}}

1. If `Use dedicated folder` is unchecked:
   - the **web folder** settings are hidden
   - the **web folder** path is the same as the **work folder**

   Otherwise
   - the **web folder** settings are displayed

   2. `Change...` allows choosing a dedicated **web folder**
   3. The **web folder** path is displayed