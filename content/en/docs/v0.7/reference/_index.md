---
title: "Reference documentation"
description: "ALS Modules and Processes"
author: "ALS Team"
lastmod: 2025-01-06T08:27:40Z
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

ALS has four **main modules**:
- **Preprocess**
- **Stacker**
- **Process**
- **Save**

## Utility modules

Utility modules are responsible for auxiliary tasks

They don't have an input queue and can be started and stopped at will

ALS has two **utility modules**:
- **Scanner**
- **Server**

## Pipelines

A **pipeline** is a special **main module** that **splits its work** into a series of tasks called **processes**.

The pipeline is responsible for hosting its processes

The only duty of a **pipeline** on **each image** it picks up from its queue is :
- make sure it is processed by each process in order
  - each process working on the result of the previous one
- broadcast the result of the last process

ALS has two **pipelines**:
- **Preprocess**

  Orders the following processes:
  - Hot pixel removal
  - Dark subtraction
  - Debayering

- **Process**

  Orders the following processes:
    - Autostretch
    - Levels
    - Color balance

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
    
    classDef module fill:#333,stroke:darkred,stroke-width:2px
    classDef main_module fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif
    classDef process fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    classDef folder fill:#555,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    classDef display fill:#555,stroke:#222,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    
    class SCANNER_ENGINE module
    class PREPROCESS_ENGINE main_module
    class STACK_ENGINE main_module
    class HOT_PIXEL process
    class DARK_SUB process
    class DEBAYER process
    class SCAN_FOLDER folder
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
    
    classDef module fill:#333,stroke:darkred,stroke-width:2px
    classDef main_module fill:#333,stroke:darkred,stroke-width:4px,color:#c6c6c6,font-family:'Poppins',sans-serif
    classDef process fill:#262626,stroke:darkred,stroke-width:1px,color:#c3c3c3,font-family:'Poppins',sans-serif
    classDef folder fill:#555,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    classDef display fill:#555,stroke:#222,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    
    class STACK_ENGINE main_module
    class PROCESS_ENGINE main_module
    class SAVE_ENGINE main_module
    class SERVER_ENGINE module
    class SCREEN display
    class HISTOGRAM display
    class STRETCH process
    class LEVELS process
    class COLOR_BAL process
    class WEB_FOLDER folder
    class WORK_FOLDER folder
```

<p class="figcaption">Flow inside the images realm</p>