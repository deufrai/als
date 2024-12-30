---
title: "User Guide"
description: "ALS User Guide"
author: "ALS Team"

lastmod: 2024-12-30T08:04:04Z
keywords: [ "ALS user guide" ]
draft: false
type: "docs"
categories: [ "user guide" ]
tags: [ "conventions" , "glossary" , "typography" ]
weight: 300
---

**Let yourself be guided!** We will show you everything you need to know about ALS for smooth and optimal use, tailored
to **your** needs.

# Conventions

First, let's define the terms and formatting we will use throughout this guide.

## Glossary {#glossary}

### calibration {#calibration}

Set of processes applied to subs to eliminate sensor defects. This generally includes hot pixel removal and the
subtraction of a [master dark](#master-dark) to reduce thermal noise.

### livestacking {#livestacking}

Real-time processing and display of the stacking of a dynamic set of [subs](#sub)

### master dark {#master-dark}

Image containing the sensor's thermal noise. It is subtracted from the subs during [calibration](#calibration) to reduce
thermal noise in the images before stacking.

### session {#session}

The lifecycle of the current [stack](#stack), starting with the first detected [sub](#sub), processing each new [sub](#sub) until the
session is
stopped.

### stack {#stack}

Set of subs stacked since the start of the [session](#session)

### stacking {#stacking}

Generation of an image containing the result of the pixel-to-pixel sum or average of a set of calibrated [subs](#sub)

### sub {#sub}

Image captured by your acquisition system

## Typography

- This is a `graphical interface element`
- this is a <span class="als-ks">keyboard shortcut</span>
- This is an **important information**
- This is a ⚠️ Warning
- This is an ℹ️ Information
- This is a 💡 Tip
- This is a 🧠 Reminder
- 🖱️ a mouse action is required
- ⌨️ a keyboard action is required
- 🎛️ an action outside of ALS is required

