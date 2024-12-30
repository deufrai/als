---
title: "User Guide"
description: "ALS User Guide"
author: "ALS Team"

lastmod: 2024-12-30T01:09:14Z
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

## Glossary

calibration
: Set of processes applied to subs to eliminate sensor defects. This generally includes hot pixel removal and the
subtraction of a master dark to reduce thermal noise.

master dark
: Calibration image containing the sensor's thermal noise. It is subtracted from the subs during calibration to reduce
thermal noise in the images before stacking.

session
: the lifecycle of the current stack, starting with the first detected sub, processing each new sub until the session is
stopped.

stack
: Set of subs stacked since the start of the session

sub
: Image captured by your acquisition system

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

