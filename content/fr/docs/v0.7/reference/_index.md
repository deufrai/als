---
title: "Documentation de référence"
description: "Documentation détaillée d'ALS"
author: "Équipe ALS"
lastmod: 2025-01-06T08:27:40Z
keywords: ["documentation de référence ALS"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "processus"]
weight: 340
---

# Vue d'ensemble

Cette section contient une documentation détaillée sur les rouages d'ALS

{{% alert color="info" %}}
🧠 Elle développe les [concepts](/docs/v0.7/userguide/concepts) introduits au début du guide de l'utilisateur

{{% /alert %}}

# Modules ALS

Les modules ALS ont leur propre moteur et sont responsables d'une tâche spécifique.

## Modules principaux

Les modules principaux sont en charge du **traitement des images**

- démarrent avec l'ALS
- travaillent sans fin sur le contenu de **leur propre file d'attente d'images**
  1. prendre l'image en tête de la file d'attente
  2. la traiter
  3. diffuser le résultat

    -  ⚙️ une entité cachée se charge d'écouter ces diffusions et d'envoyer les images au bon endroit : d'autres 
       files d'attente, des affichages, etc...

  4. reprendre à l'étape 1 dès que file d'attente n'est pas vide

ALS a quatre **modules principaux** :
- **Preprocess**
- **Stacker**
- **Process**
- **Save**

## Modules utilitaires

Les modules utilitaires sont responsables des tâches auxiliaires

Ils n'ont pas de file d'attente d'entrée et peuvent être démarrés et arrêtés à volonté

ALS a deux **modules utilitaires** :
- **Scanner**
- **Server**

## Pipelines

Un **pipeline** est un **module principal** spécial qui **divise son travail** en une série de tâches appelées **traitements**.

Le pipeline est responsable de l'hébergement de ses traitements

La seule tâche d'un **pipeline** sur **chaque image** qu'il prend dans sa file d'attente est :
  - s'assurer qu'elle est traitée par chaque traitement dans l'ordre
    - chaque traitement travaillant sur le résultat du précédent
  - diffuser le résultat du dernier traitement

ALS a deux **pipelines** :
- **Preprocess**

  Ordonne les traitements suivants :
  - Suppresion des pixels chauds
  - Soustraction de dark
  - Dématriçage

- **Process**

  Ordonne les traitements suivants :
    - Autostretch
    - Niveaux
    - Balance des couleurs

# Domaines

Comme indiqué précédemment, ALS est divisé en deux domaines :
- le **domaine des Brutes** : où vos brutes sont traitéés
- le **domaine des Images** : où les images d'ALS sont affichées et sauvegardées

## Domaine des Brutes

Du système de fichiers au module **Stacker**

```mermaid
flowchart LR

    subgraph Filesystem
        SCAN_FOLDER@{ shape: lin-cyl, label: "Dossier Scanné" }
    end
        
    subgraph Scanner Module 
        SCANNER_ENGINE[Moteur]
    end
           
    subgraph Preprocess Module
        direction TB
        PREPROCESS_ENGINE[Moteur]
        HOT_PIXEL[Suppression Pixels Chauds]
        DARK_SUB[Soustraction de Dark]
        DEBAYER[Dématriçage]
    end  

    subgraph Stacker Module
        direction TB
        STACK_ENGINE[Moteur]
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

<p class="figcaption">Flux à l'intérieur du domaine des subs</p>

## Domaine des Images

Du module **Stacker** aux affichages et au système de fichiers de sortie

```mermaid
flowchart LR

subgraph Module Stacker
    direction TB
    STACK_ENGINE[Moteur]
end

subgraph Module Process
    direction TB
    PROCESS_ENGINE[Moteur]
    STRETCH[Autostretch]
    LEVELS[Niveaux]
    COLOR_BAL[Balance des couleurs]
end 

subgraph Module Saver
    direction TB
    SAVE_ENGINE[Moteur]
end

subgraph Système de fichiers
    direction TB
    
    WEB_FOLDER@{ shape: lin-cyl, label: "Dossier Web" }
    WORK_FOLDER@{ shape: lin-cyl, label: "Dossier de travail" }
end

subgraph Module Server
    direction TB
    SERVER_ENGINE[Moteur]
end

subgraph Interface
    direction TB
    SCREEN@{ shape: curv-trap, label: "Zone centrale" }
    HISTOGRAM@{ shape: curv-trap, label: "Histogramme" }
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
class WEB_FOLDER folder
class WORK_FOLDER folder
class STRETCH process
class LEVELS process
class COLOR_BAL process
```


<p class="figcaption">Flux à l'intérieur du domaine des images</p>