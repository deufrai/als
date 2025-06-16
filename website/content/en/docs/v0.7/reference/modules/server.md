---
title: "Server"
description: "Detailed documentation of the ALS Server module"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: ["ALS server", "web"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "web", "server"]
weight: 351
---

# Overview

The **Server** module shares the **server output** of the **Save** module over the network.

It serves a minimal web page displaying the latest processing result and updates it automatically when a new image is saved.

# Configuration

|                    | Source                                                        | Data type | Required | Default value |
|--------------------|---------------------------------------------------------------|-----------|----------|---------------|
| Listening port     | Preferences: [Output Tab](../../userguide/preferences/output/#server-port) | integer  | Yes      | 8000 |

# Control

| Source | Type | Response |
|--------|------|---------|
| Interface: [Image Server](../../userguide/ui/controls/#server-section) | Command: START | Start the server |
| Interface: [Image Server](../../userguide/ui/controls/#server-section) | Command: STOP | Stop the server |

# Input

| Data | Type |
|------|------|
| Notification from the **Save** module | Event |

# Behavior

- Serve the **web folder** content on the configured port.
- Send a WebSocket notification to connected browsers each time a new image is saved.

# Output

Updated web page with the latest processing result.
