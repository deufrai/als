---
title: "Reference documentation"
description: "ALS Modules and Processes"
author: "ALS Team"
lastmod: 2025-01-02T07:23:46Z
keywords: ["ALS reference documentation"]
draft: false
type: "docs"
categories: ["detailed documentations"]
tags: ["module", "process"]
weight: 340
---

# Overview

This section contains detailed documentation about ALS bits and bolts

{{% alert color="info" %}}
🧠 It elaborates on the [concepts](/docs/v0.7/userguide/concepts) introduced at the beginning of the user guide

{{% /alert %}}

# ALS Modules

ALS modules have their own engine and are responsible for a specific task.

## Main modules

Main modules are in charge of **image processing**

- start with ALS
- work endlessly on the content of **their own image queue**
  1. take the image at the head of the queue
  2. process it
  3. broadcast the result

    -  ⚙️ a hidden entity is responsible for listening to these broadcasts and sending the images to the right place: other queues, displays, etc...

  4. go back to step as soon as the queue is not empty

## Utility modules

Utility modules are responsible for auxiliary tasks

They don't have an input queue and can be started and stopped at will

ALS has two **utility modules**:
- the **Scanner** module
- the **Server** module

## Pipelines

A **pipeline** is a special **main module** that **splits its work** into a series of tasks called **processes**.

The pipeline is responsible for hosting its processes

The only duty of a **pipeline** on **each image** it picks up from its queue is :
- make sure it is processed by each process in order
  - each process working on the result of the previous one
- broadcast the result of the last process

ALS has two **pipelines**:
- the **PreProcess** module
- the **Process** module

# Realms

As implied earlier, ALS is split into two realms:
- the **Subs realm**: where your subs are processed
- the **Images realm**: where ALS's images are displayed and saved

## Subs realm

From the file system to the **Stacker** module

```mermaid
flowchart LR

    subgraph Filesystem
        SCAN_FOLDER@{ shape: lin-cyl, label: "Scan Folder" }
    end
        
    subgraph Scanner Module 
        SCANNER_ENGINE[Engine]
    end
           
    subgraph Preprocess Module
        direction TB
        PREPROCESS_ENGINE[Engine]
        HOT_PIXEL[Hot Pixel Removal]
        DARK_SUB[Dark Subtraction]
        DEBAYER[DeBayer]
    end  

    subgraph Stacker Module
        direction TB
        STACK_ENGINE[Engine]
    end

    SCAN_FOLDER -.-> SCANNER_ENGINE
    SCANNER_ENGINE -.-> PREPROCESS_ENGINE
    PREPROCESS_ENGINE -.-> STACK_ENGINE
    


    style SCANNER_ENGINE fill:#333,stroke:darkred,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    
    style PREPROCESS_ENGINE fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style STACK_ENGINE fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif


    style HOT_PIXEL  fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    style DARK_SUB fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    style DEBAYER fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif

    style SCAN_FOLDER fill:#555,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
```

<p class="figcaption">Flow inside the subs realm</p>

## Images realm

From the **Stacker** module to the displays and output filesystem


```mermaid
flowchart LR

    subgraph Stacker Module
        direction TB
        STACK_ENGINE[Engine]
    end
    
    subgraph Process Module
        direction TB
        PROCESS_ENGINE[Engine]
        STRETCH[Autostretch]
        LEVELS[Levels]
        COLOR_BAL[Color Balance]
    end 
    
    subgraph Saver Module
        direction TB
        SAVE_ENGINE[Engine]
    end

    subgraph Filesystem
        direction TB
        
        WEB_FOLDER@{ shape: lin-cyl, label: "Web Folder" }
        WORK_FOLDER@{ shape: lin-cyl, label: "Work Folder" }
    end
    
    subgraph Server Module
        direction TB
        SERVER_ENGINE[Engine]
    end
    
    subgraph GUI
        direction TB
        SCREEN@{ shape: curv-trap, label: "Central zone" }
        HISTOGRAM@{ shape: curv-trap, label: "Histogram" }
    end
    
    STACK_ENGINE --> PROCESS_ENGINE
    
    PROCESS_ENGINE --> SAVE_ENGINE
    PROCESS_ENGINE ---> SCREEN
    PROCESS_ENGINE ---> HISTOGRAM
    
    SAVE_ENGINE --> WEB_FOLDER
    SAVE_ENGINE --> WORK_FOLDER

    WEB_FOLDER --> SERVER_ENGINE
    
    style SERVER_ENGINE fill:#333,stroke:darkred,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    
    style STACK_ENGINE fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style PROCESS_ENGINE fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style SAVE_ENGINE fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif

    style STRETCH fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    style LEVELS fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    style COLOR_BAL fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif


    style WEB_FOLDER fill:#555,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style WORK_FOLDER fill:#555,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    
    style SCREEN fill:#555,stroke:#222,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style HISTOGRAM fill:#555,stroke:#222,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
```

<p class="figcaption">Flow inside the images realm</p>