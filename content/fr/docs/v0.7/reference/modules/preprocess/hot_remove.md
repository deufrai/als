---
title: "Suppression des pixels chauds"
description: "Documentation détaillée du traitement HotPixelRemove d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
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

Chaque pixel de l'image dont la valeur s'écarte trop de ses voisins est considéré comme un pixel chaud 

Sa valeur est remplacée par la valeur moyenne de ses voisins.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
