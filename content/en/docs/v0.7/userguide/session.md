---
title: "Typical Session"
description: "Step-by-step guide to running an ALS session"
author: "ALS Team"

lastmod: 2025-04-21T15:48:04Z
keywords: [ "ALS typical session", "session workflow", "astrophotography guide" ]
draft: false
type: "docs"
categories: [ "session workflow guide" ]
tags: [ "module", "stack", "process", "session", "output", "scan folder", "work folder", "web folder", "server", "scanner", "save", "calibration", "profile", "alignment" ]
weight: 317
---

# Typical Session

This chapter guides you through the ALS session workflow, tailored to your activity type and goals. Whether you aim to
produce a final image during your session or monitor a photo session for later processing, ALS adapts seamlessly to your
needs.

---

## Setup

### Preferences Review

#### Profile

Begin by choosing the profile that matches your current activity:

- **Electronically Assisted Astronomy (EEA)**: Perfect for live imaging with short exposures (a few seconds). ALS
  processes subs rapidly, producing vibrant, viewable images in real time.
- **Astrophoto Session**: Ideal for long exposures (several minutes). ALS acts as a diagnostic tool, offering a preview
  of your session’s results while you prepare for detailed post-processing elsewhere.

The selected profile ensures ALS adapts to your imaging workflow.

---

#### Master Dark

Think about this: do you have a master dark for your current setup—same sensor, same temperature? If yes, enable **Dark
Subtraction** to clean up thermal noise and ensure it matches the dimensions of your subs. If not, no problem—ALS will
perform perfectly without it.

---

### Stacking Settings

Using the main ALS interface, configure session-specific stacking parameters to align with your objectives:

- **Alignment**: Enable for deep-sky object imaging to register stars consistently, or disable for creative workflows.
- **Stacking Mode**: Choose Mean for noise-free, smooth results when stacking deep-sky images, or Sum for amplified
  brightness effects.

---

## Session in Motion

As your session unfolds, ALS offers various tools and controls to keep things running smoothly, refine your results, and
interact with the evolving image. Here’s how to make the most of the session:

### Monitor and Optimize Processing

Stay on top of processing by using the available feedback tools:

- **Session Log**: Refer to the log for detailed information about potential issues, such as alignment failures or
  calibration inconsistencies. It’s your go-to resource for understanding and troubleshooting problems during the
  session.
- **Modules Panel**: View queue sizes and module statuses to ensure subs are flowing through ALS efficiently.
- **Alignment Threshold Management**: When alignment is ON, aim for the highest possible threshold. Use the session log
  to strike the right balance—raise the threshold gradually without causing subs to drop unnecessarily.

---

### Fine-Tune Your Image as It Develops

Use the **Processing Panel** to shape your image in real time. This is where you achieve optimal brightness, contrast,
and color adjustments, tailoring the evolving stack to match your goals. These dynamic tweaks help bring your image
closer to its full potential during the session.

---

### Explore the Evolving Image

Interacting with the stacked image makes the session more immersive:

- Zoom in and out to inspect finer details.
- Pan across the frame to explore specific regions.
- Reset the view with a right-click for a fresh perspective.

Enjoy the satisfaction of seeing your image grow and evolve as ALS processes incoming subs.

---

### Share Your Session with Ease

Looking to engage others in your session? ALS’s live sharing feature is designed for collaboration and outreach, making
it ideal for use in astronomy clubs or public stargazing events.

- **Outreach**: Share your session results in real-time with the public during events, offering them a firsthand look at
  the sky’s wonders as your image evolves.
- **Collaboration**: Let club members or remote collaborators follow along with your imaging session, enhancing group
  discussions or team-based observations.

ALS generates a **QR Code** for easy access—participants can scan it to view live updates on their devices. This feature
transforms your session into an interactive, shared experience, bringing astrophotography to life for audiences and
collaborators alike.

---

## Session Stop

End your session by clicking `STOP`. The final result is saved in your work folder (e.g., `stack_image.jpg`) or
autosaved based on your settings. ALS clears the stack, ready for the next session.

---

## Conclusion

ALS bridges the gap between live imaging and session monitoring, offering both immediate results and diagnostic
previews. Whether producing vibrant deep-sky images or creative workflows, its intuitive features empower all
astrophotography workflows.

