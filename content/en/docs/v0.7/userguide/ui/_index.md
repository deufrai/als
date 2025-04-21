---
title: "Interface"
description: "A detailed walkthrough of the ALS user interface"
author: "ALS Team"

lastmod: 2025-04-21T11:54:12Z
keywords: ["ALS GUI", "ALS Interface"]
type: "docs"
categories: ["usage"]
tags: ["interface", "panels"]
weight: 320
---

{{% center %}}
{{% figure src="6_zones.png" 
alt="ALS Interface Layout" 
caption="ALS Interface Layout" 
width="1388" 
height="666" %}}
{{% /center %}}

# Introduction

In this chapter you will get deeper knowledge about ALS use through its interface.

The ALS **U**ser **I**nterface is designed to be intuitive and user-friendly, allowing you to focus on your work without
unnecessary distractions.

# Main elements

ALS interface is composed of six major elements, each playing a key role in the software’s usability.

Below is an overview of these components:

<div class="row">
<div class="col-md-6">

- **1: Main Menu**  
  Provides access to every ALS feature and setting.

  *Learn more in the [Menu Documentation](menu).*

- **2: Main Controls Panel**  
  Located on the left by default, it's your daily control panel.

  *Dive deeper in the [Main Controls Panel Documentation](controls).*

- **3: Central Area**  
  Displays the image resulting from stacking and processing.

  *Image navigation is covered in the [Quickstart page](../../quickstart#explore).*

</div>
<div class="col-md-6">

- **4: Processing Panel**  
  Found on the right side, this panel allows you to fine-tune your images using various processing tools.

  *Explore details in the [Processing Panel Documentation](processing).*

- **5: Session Log Panel**  
  Positioned at the bottom, this panel helps you monitor progress and track events or issues during the session.

  *Find out more in the [Session Log Documentation](log).*

</div>
</div>

---

- **6: Status Bar**

  Located at the bottom of the interface, the status bar provides real-time updates on system status

  It is divided into several labels:
  - **Tips**: Displays helpful hints or information about the currently hovered UI element.
  - **Session Status**: Reflects the activity status of the session.
  - **Current Profile**: Displays the name of the currently active profile.
  - **Scanner Status**: Shows whether the scanner is running or stopped and indicates the current scan folder path.
  - **Stack Size**: Indicates the number of images currently present in the stack.
  - **Total Stack Exposure Time**: Displays the cumulative exposure time of the stacked images.
  - **Web Server Status**: Displays the operational status of the integrated web server.
  - **Total Frame Processing Time**: Provides the processing time for the most recent frame handled.

---

# Common elements

Some interface elements have specific behaviors that can be useful in your daily work.

## Panels

Panels in ALS allow for a flexible interface that can adapt to different workflows.

By default:

- The **Main Controls** panel is docked on the left side of the main window.
- The **Processing** panel is docked on the right side.
- The **Session Log** panel is docked at the bottom.

### Moving Panels

Panels can be docked to specific zones in the main window or detached to become independent floating elements.

These floating panels can be freely positioned anywhere in the display area, even across multiple screens.

#### Docked Mode
  - Click on the **title bar** of a panel and drag it towards a valid docking area:
    - The **Main Controls** and **Processing** panels can be docked to the left or right sides.
    - The **Session Log** panel can be docked to the top or bottom.
  - As you approach a valid docking zone, **visual indicators** appear to guide you.
  - Release the click to anchor the panel at the chosen location.

#### Floating Mode
  - Click on the **title bar** of the panel you want to move.
  - Hold the click and drag the panel anywhere in the display area, then release the click.
  - The panel will remain floating and detached from the main window.

A floating panel can be re-docked to its default position by double-clicking on its title bar.

---

## Sliders

The **sliders** in ALS allow users to adjust various parameters in an intuitive way.

Here are the different methods of interacting with them:

### Dragging the Handle
The most straightforward way to change a value:
- Click on the slider handle with your mouse.
- Hold the click and drag the handle to the left to decrease the value or to the right to increase it.
- Release the click once the desired value is reached.

### Using the Mouse Wheel
If you’re using a mouse with a scroll wheel, this can provide fine-tuned adjustments:
- Hover the mouse pointer over the slider handle or bar.
- Scroll the wheel upwards to increase the value or downwards to decrease it.

### Clicking on the Bar
Clicking directly on the slider bar adjusts the associated value in larger increments compared to using the mouse wheel:
- The slider handle moves accordingly but does not jump directly to the click position.

{{% alert color="info" %}}
ℹ️ Certain sliders feature additional behaviors that are explained in the documentation of the specific panels where they are located.
{{% /alert %}}


