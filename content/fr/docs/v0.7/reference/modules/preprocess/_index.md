---
title: "Preprocess"
description: "Documentation détaillée du module Preprocess d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: [ "ALS preprocess" ]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "calibration"]
weight: 352
---

# Présentation

Le module **Preprocess** prend en charge les traitements de **calibration** de brutes

# Configuration

Le module **Preprocess** lui-même n'a besoin d'aucune configuration.

La configuration des traitements de **calibration** est gérée par les **traitements** eux-mêmes.
Voir section [Comportement](#behavior) ci-dessous.

# Contrôle

Le module **Preprocess** est lancé en tâche de fond au démarrage d'ALS

| Source                     | Type          | Réponse              |
|----------------------------|---------------|----------------------|
| brute(s) en file d'attente | Événement     | lance la calibration |

# Entrée

| Donnée                             | Type  |
|------------------------------------|-------|
| brute en tête de la file d'attente | Image |

# Comportement {#behavior}

Applique les traitements de **calibration** à la brute :

1. [Suppression des pixels chauds](hot_remove/)
2. [Soustraction de dark](dark_remove/)
3. [Dématriçage](debayer/)

# Sortie

La brute calibrée est diffusée