---
title: "Output Tab"
description: "ALS Preferences Output Tab Documentation"
author: "ALS Team"
lastmod: 2026-06-07T15:53:25Z
keywords: ["ALS output settings", "ALS Output preferences"]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["output", "server", "web folder", "work folder", "save"]
weight: 100333
---

The settings governing ALS outputs are presented in the `Output` tab.

<div class="row">
<div class="col-md-4">

# Overview {#overview}

This tab is divided into 2 sections:

- [File Saver](#save)
- [image server](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="The Output tab in preferences"
width="628px"
height="663px"
alt="ALS preferences window with the Output tab selected, showing save format options, output folder settings, autosave, displayed address, and port number settings." >}}
{{< /center >}}

</div>
</div>

# Save {#save}

Here are the output file format, output folders, and autosave function settings.

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
height="179px"
alt="" >}}
{{< /center >}}

- 🖱️ check `Timestamped Result on Session Stop` to activate the autosave function

ℹ️ Default: ON

# Server {#server}

Here are the settings for the ALS image server.

{{< center >}}
{{< figure src="web_config.png"
caption="Image server settings"
width="628px"
height="187px"
alt="Image server settings showing the Displayed address dropdown set to Auto - recommended and the port number set to 8000." >}}
{{< /center >}}

## Displayed Address {#server-address}

Defines the network address shown in the `Main controls` panel, the status bar, and the QR code window
when the image server is running.

The list contains `Auto - recommended`, followed by the network addresses discovered on the system running ALS. Each
listed address belongs to one detected network adapter.

Listed addresses are ordered by likely usefulness:

1. Addresses likely to be reachable from another device on a local network.
2. Addresses from common Wi-Fi or Ethernet adapters.
3. Addresses from other adapters, including hotspot, sharing, bridge, virtual, Docker, VPN, and tunnel adapters.
4. Link-local addresses, when no better local address is available.
5. Loopback addresses, as a last fallback for local-only access.

- 🖱️ Choose `Auto - recommended` to use the first address in the ordered list
- 🖱️ Choose a specific address when another device must connect through a particular network, such as a Wi-Fi hotspot
  or a dedicated local network

ℹ️ Default: Auto - recommended

{{% alert title="Troubleshooting" color="warning" %}}
If another device cannot browse the image server while it is running, open the Output preferences and
select another **Displayed address**. Choose an address that belongs to the same network as the browser device, click
`OK`, then retry the URL or QR code.

The displayed address can be changed without stopping the image server.
{{% /alert %}}

## Port Number {#server-port}

The image server listening port is configured here

Allowed values: 1024 to 65535

- ⌨️ Enter the `port number` on which the ALS image server will be accessible

ℹ️ Default: 8000

{{% alert color="info" %}}
Changing the port number requires stopping the image server first.
{{% /alert %}}
