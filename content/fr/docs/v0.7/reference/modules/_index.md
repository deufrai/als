---
title: "Modules et Traitements"
description: "Modules et Traitements ALS"
author: "ALS Team"
lastmod: 2025-01-07T00:17:54Z
keywords: [ "modules et traitements ALS" ]
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "module", "traitement" ]
weight: 345
---

# Vue d'ensemble

Ici, vous trouverez une documentation détaillée sur les modules et traitements d'ALS.

De ce qu'est un module à la façon dont fonctionne un traitement, vous trouverez tout ce que vous devez savoir sur 
les rouages d'ALS.

# Module

Un module ALS est une unité de traitement élaborée responsable d'une tâche spécifique.

- Il a son propre moteur
- Il peut être démarré et arrêté à volonté
- Il a accès aux paramètres définis dans les préférences ALS
- Son comportement peut être contrôlé via l'interface ALS

Les modules sont **simples et isolés**. Ils n'ont aucune connaissance des autres parties de l'application. Ils 
font simplement leur travail et rendent compte à l'application.

## Module utilitaire

Un module utilitaire est un module très simple qui est chargé d'une unique tâche auxiliaire à l'intérieur d'ALS.

ALS utilise 2 modules utilitaires :
- **Scanner**
- **Server**

## Module principal

Un module principal est un module spécialisé qui est chargé de **traitements d'images**.

- Il a sa propre file d'attente d'images en entrée
- Il traite chaque image qu'il prend de la file d'attente, puis diffuse le résultat à l'application.

Un module principal est démarré avec ALS et continue de sonder sa file d'attente pour de nouvelles images à traiter,
jusqu'à ce que l'application soit fermée.

```mermaid
flowchart LR
DÉMARRER((Start))
TEST{{Test:<br><br>Images dans la file d'attente ?}}
PRENDRE[Prend l'image en tête de file]
TRAITER[Traite l'image]
DIFFUSER[Diffuse le résultat]
ATTENDRE[Attend 20ms]

DÉMARRER --> TEST
TEST -- Oui --> PRENDRE
TEST -- Non --> ATTENDRE
PRENDRE --> TRAITER
TRAITER --> DIFFUSER
DIFFUSER --> ATTENDRE
ATTENDRE --> TEST

classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef wait  fill: #444, stroke: #262, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif
classDef test fill: #444, stroke: #226,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif

class DÉMARRER bounds
class TEST test
class PRENDRE step
class TRAITER step
class DIFFUSER step
class ATTENDRE wait
```

<p class="figcaption">Flux de travail du module principal</p>

ALS a 4 modules principaux :
- **Preprocess**
- **Stack**
- **Process**
- **Save**

## Pipeline

Un pipeline est un module principal spécialisé qui divise son travail en soumettant son image à une série de tâches 
simples appelées traitement.

Il gère la liste des traitements à exécuter sur les images de sa file d'attente et l'ordre dans lequel ils sont exécutés.

Il s'assure que chaque traitement est exécuté dans l'ordre, chaque traitement travaillant sur le résultat du précédent.

Une fois le dernier traitement terminé, le pipeline diffuse le résultat à l'application.


```mermaid
flowchart LR
DÉMARRER((Start))
TEST{{Test:<br><br>Images dans la file d'attente ?}}
PRENDRE[Prend l'image en tête de file]
subgraph Traitement
    A[Traitement A]
    B[Traitement B]
end
DIFFUSER[Diffuse le résultat]
ATTENDRE[Attend 20ms]

DÉMARRER --> TEST
TEST -- Oui --> PRENDRE
TEST -- Non --> ATTENDRE
PRENDRE --> A
A -.-> B
B --> DIFFUSER
DIFFUSER --> ATTENDRE
ATTENDRE --> TEST

classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
classDef process fill: #333, stroke: #622, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif
classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif

class DÉMARRER bounds
class TEST test
class PRENDRE step
class A process
class B process
class DIFFUSER step
class ATTENDRE wait
```
<p class="figcaption">Flux de travail du pipeline</p>

2 des modules principaux sont des pipelines :

- **Preprocess**
- **Process**

# Traitement

Un traitement est la plus petite unité de traitement dans ALS

Il est géré par son pipeline parent et est responsable d'une tâche spécifique à effectuer sur une image donnée.

- Il a accès aux paramètres définis dans les préférences ALS
- Il est contrôlé par son pipeline parent
- Si l'image donnée est vide, le traitement renverra une image vide.
- Si le traitement est désactivé dans les préférences, le traitement renverra simplement l'image donnée, **inchangée**.
- Si une erreur se produit pendant son travail sur l'image, le traitement signalera le problème à ALS et renverra 
  une image vide.



# Domaines

Comme indiqué précédemment, ALS est divisé en deux domaines :
- le **domaine des Brutes** : où vos brutes sont traitéés
- le **domaine des Images** : où les images d'ALS sont affichées et sauvegardées

Ci-dessous, le détail des flux à l'intérieur de chaque domaine.

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