---
title: "User Guide"
description: "ALS User Guide"
author: "ALS Team"

lastmod: 2026-06-11T00:46:48Z
keywords: [ "ALS user guide" ]
draft: false
type: "docs"
weight: 100300
---

**Let yourself be guided!** We will show you everything you need to know about ALS for smooth and optimal use, tailored
to **your** needs.

The user guide walks through ALS after first launch: core concepts, session workflow, main interface, preferences, and
common interactions.

# Conventions

This guide uses the following formatting conventions and terms.

## Typography {#typography}

<div class="row">
<div class="col-md-5">

### Text
- a `graphical user interface element`
- a {{< als-ks >}}keyboard shortcut{{< /als-ks >}}
- a {{< als-code >}}command{{< /als-code >}} or {{< als-code >}}code extract{{< /als-code >}}
- an **important information**
- ⚙️ Technical detail

</div>
<div class="col-md-3">

### Paragraphs
- ⚠️ Warning
- ℹ️ Information
- 💡 Tip
- 🧠 Reminder
- 🐛 Known bug

</div>
<div class="col-md-4">

### User Actions
- 🖱️ mouse action required
- ⌨️ keyboard action required
- 🎛️ action outside of ALS required

</div>
</div>

## Glossary {#glossary}

### sub {#sub}

Image captured by your acquisition system

### calibration {#calibration}

Set of processes applied to subs to eliminate sensor and optical train defects.

### master dark {#master-dark}

Image containing the sensor's thermal noise. It is subtracted from the subs during calibration

### master flat {#master-flat}

Image representing the optical system’s illumination pattern and sensor response non-uniformities. It is used to correct
the subs for vignetting and dust shadows during calibration.

Subs are divided by the master flat after dark subtraction during calibration
