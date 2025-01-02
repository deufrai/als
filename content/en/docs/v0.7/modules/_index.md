---
title: "Modules and Processes"
description: "ALS Modules and Processes"
author: "ALS Team"
lastmod: 2025-01-02T02:48:31Z
keywords: ["ALS modules and processes", "ALS modules and processes"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "process"]
weight: 345
---

This section contains detailed documentation for each ALS module.

Modules can perform one or more processes on the images they receive.

If a module performs multiple processes, it hosts a list of processes that will be applied sequentially to the current image.

```mermaid
flowchart LR

    SCAN_FOLDER[Scan Folder] 
    
    subgraph Scanner 
        SCANNER_BRAIN[Module Brain]
    end
           
    subgraph Preprocess
        direction TB
        PREPROCESS_BRAIN[Module Brain]
        HOT_PIXEL[Hot Pixel Removal]
        DARK_SUB[Dark Subtraction]
        DEBAYER[DeBayer]
    end  
    
    subgraph Stack
        direction TB
        STACK_BRAIN[Module Brain]
    end
    
    subgraph Process
        direction TB
        PROCESS_BRAIN[Module Brain]
        STRETCH[Autostretch]
        LEVELS[Levels]
        COLOR_BAL[Color Balance]
    end 
    
    subgraph Save
        direction TB
        SAVE_BRAIN[Module Brain]
    end

    WEB_FOLDER[Web Folder]
    WORK_FOLDER[Work Folder]
    
    subgraph Server
        direction TB
        SERVER_BRAIN[Module Brain]
    end

    SCAN_FOLDER -.-> SCANNER_BRAIN
    
    SCANNER_BRAIN -.-> PREPROCESS_BRAIN
    PREPROCESS_BRAIN -.-> STACK_BRAIN
    
    STACK_BRAIN --> PROCESS_BRAIN
    PROCESS_BRAIN --> SAVE_BRAIN
    
    SAVE_BRAIN --> WEB_FOLDER
    SAVE_BRAIN --> WORK_FOLDER
    
    WEB_FOLDER --> SERVER_BRAIN

```

Below you will find the list of documented modules.