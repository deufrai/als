---
title: "A successful session"
description: "Step-by-step guide to running an ALS session"
author: "ALS Team"

lastmod: 2026-06-11T00:33:39Z
keywords: [ "ALS typical session", "session workflow", "astrophotography guide" ]
draft: false
type: "docs"
categories: [ "usage", "configuration" ]
tags: [ "session", "stack", "processing", "calibration", "dark", "flat", "minimum matches", "image server", "output", "save", "work folder", "profile" ]
weight: 100317
---

# 📘 Introduction

This chapter is your roadmap for running a successful ALS session and monitoring its progress.

It wraps up the presentation of ALS main concepts before you dive into the user interface guide.

---

# ⚡ Startup

ALS can be launched either from its graphical interface or directly from the command line, depending on your workflow or
automation needs.

- **Graphical launch**:  
  Simply start ALS as any other application. You’ll land in the main window, ready to configure your session.

- **Command-line launch**:  
  ALS supports two optional startup parameters that can automate session initialization or live sharing.

  | Parameter                           | Description                                                                                                                        |
  |-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
  | {{< als-code >}}-s{{< /als-code >}} | Start a stacking session immediately after ALS launches. The session begins with **alignment enabled** and **mean stacking mode**. |
  | {{< als-code >}}-w{{< /als-code >}} | Start the integrated web server automatically, allowing remote and live viewing right after startup.                               |

  These parameters can be combined if you want ALS to begin processing and broadcasting the stacked image right away.

---

# ⚙️ Setup

Whether you’re shooting DSO live, preparing data for detailed post-processing, or diving into something more artistic, 
these steps will help you get the best out of ALS every time.

## ✔️ Choose Your Profile

<div class="row">
<div class="col-md-6">

- **EAA**: For live imaging

  ALS processes subs rapidly, producing colorful, viewable images in real time.

</div>

<div class="col-md-6">

- **Astrophoto**: For monitoring an astrophoto session

  ALS acts as an acquisition and data diagnostic tool, giving you a high-quality preview of your fully processed image.

</div>
</div>

## ✔️ Prep Your Calibration

- Do you have a master dark that matches your sensor and temperature?  

  If yes, use **Dark Subtraction** to clean up thermal noise.

- Do you have a master flat that matches your optical setup?  

  If yes, use **Flat Calibration** to correct for vignetting and dust motes.

## ✔️ Adjust Stacking Settings

- Enable **Alignment** for Deep Sky Objects imaging, or disable it for artistic shots such as star trails or time-lapses.

- Set **Stacking Mode**:
    - **Mean** for smooth and noise-free results.
    - **Sum** for amplified brightness and a creative twist.

---

# 🚀 Progress

Start the session and let ALS do its thing... 

Here’s how to keep everything running smoothly and eventually enjoy the results:

## 📊 Stay on Top of Things

Keep track of your session by reviewing ALS feedback on performance and potential issues during subs processing.

## 🌦️ Adapt to Conditions

Adapt the minimum matches setting to changing weather conditions or specific acquisition setups.

## 🎨 Tweak Your Image

Tweak ALS image processing settings to adjust the image as it develops with each new sub.

## 🔍 Dive Into Your Image

Zoom in/out and pan across the image to find areas that deserve attention or just to enjoy the view.

## 🌐 Share Your Progress

Perfect for public outreach or collaborative discussions :

Let others follow your session live by activating the image server and sharing the generated QR code. 

Viewers can explore your evolving image with the same image browsing features as the main ALS app, optimized for both 
desktop and mobile devices. 

---

# 📦 Wrap Up

Stop your session and find the final result image in your **work folder**.

{{< alert color="info" >}}
To end a session started **via the command line**, use {{< als-ks >}}Ctrl+C{{< /als-ks >}} in the terminal where ALS is running.
This will also **quit the whole application**.
{{< /alert >}}

---

# 🎯 Conclusion

It is now time for **you** to take control of ALS by diving into the next chapter: ALS user interface.
