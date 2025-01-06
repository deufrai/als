---
title: "Suppression des pixels chauds"
description: "Documentation détaillée du traitement HotPixelRemove d'ALS"
author: "ALS Team"
lastmod: 2025-01-06T03:20:05Z
keywords: ["ALS hot pixel removal", "ALS suppression des pixels chauds"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["traitement", "pixels chauds", "calibration"]
weight: 353
---

# Présentation

Le Traitement **HotPixelRemove** supprime les pixels chauds de l'image

Sa configuration est gérée via les préférences

# Configuration

|        | Source                                                                                   | Type de donnée | Requis | Valeur par défaut |
|--------|------------------------------------------------------------------------------------------|----------------|--------|-------------------|
| ON/OFF | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#hot-remove) | ON/OFF         | ∅      | OFF               |

# Contrôle

Ce traitement est déclenché par le module **Preprocess**

# Entrée

| Donnée                                     | Type  |
|--------------------------------------------|-------|
| image fournie par le module **Preprocess** | Image |


# Comportement


```mermaid
graph LR
  A[Start Process] --> B{Is Image Available?}
  B -- No --> C[Return None]
  B -- Yes --> D[Get Hot Pixel Remover Config]
  D --> E{Is Hot Pixel Remover Enabled?}
  E -- No --> F[Return Image Unchanged]
  E -- Yes --> G{Is Image Color?}
  G -- Yes --> H[Log Skipped on Color Image]
  H --> F
  G -- No --> I[Calculate Neighbors' Mean]
  I --> J[Replace Hot Pixels with Neighbors' Mean]
  J --> K[Return Modified Image]

```

Chaque pixel de l'image dont la valeur s'écarte trop de ses voisins est considéré comme un pixel chaud 

Sa valeur est remplacée par la valeur moyenne de ses voisins.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
