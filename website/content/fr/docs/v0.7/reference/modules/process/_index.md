---
title: "Process"
description: "Documentation détaillée du module Process d'ALS"
author: "ALS Team"
lastmod: 2025-10-21T16:10:05Z
keywords: [ "ALS process" ]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module"]
weight: 357
---

# Présentation

Le pipeline **Process** prend en charge les traitements **visuels** appliqués aux résultats d’empilement.

# Configuration

Le pipeline **Process** lui-même n'a besoin d'aucune configuration.

La configuration des traitements **visuels** est gérée par les **traitements** eux-mêmes.  
Voir section [Comportement](#behavior) ci-dessous.

# Contrôle

Le module **Process** est lancé en tâche de fond au démarrage d'ALS

| Source                     | Type        | Réponse                |
|-----------------------------|-------------|------------------------|
| brute(s) en file d’attente  | Événement   | lance le traitement visuel |

# Entrée

| Donnée                            | Type  |
|-----------------------------------|-------|
| brute en tête de la file d’attente | Image |

# Comportement {#behavior}

Applique les traitements **visuels** au résultat d’empilement :

1. [Auto-étirement](autostretch/)
2. [Niveaux](levels/)
3. [Balance RVB](rgb_balance/)

# Sortie

L’image traitée visuellement est diffusée.
