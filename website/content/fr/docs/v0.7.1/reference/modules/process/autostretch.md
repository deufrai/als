---
title: "Auto-Stretch"
description: "Documentation détaillée du processus Auto-Stretch dans le module Process d’ALS"
author: "Équipe ALS"
lastmod: 2026-06-10T23:25:50Z
keywords: [ "ALS auto stretch", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentation détaillée" ]
tags: [ "processus", "étirement", "ajustement d’image" ]
weight: 71358
---

# Présentation

Le processus **Auto-Stretch** optimise les niveaux d’intensité des images empilées afin de les rendre
visuellement exploitables sans ajustement manuel.

Ce processus est géré par le module **Process** de la chaîne de traitement.

# Configuration

Les réglages peuvent être effectués depuis le Panneau **Traitements**, situé sur le côté droit de
l’interface d’ALS.

| Contrôle | Type           | Action                              |
|----------|----------------|-------------------------------------|
| `Actif`  | case à cocher  | Active ou désactiver le processus   |
| `Force`  | curseur        | Ajuste l’intensité de l’étirement   |

Consultez la [documentation du Panneau de traitement](../../../../userguide/ui/processing/#stretch-section)
pour des instructions détaillées.

# Contrôle

Le processus **Auto-Stretch** est contrôlé par le pipeline **Process**

# Entrée

| Donnée                | Type  |
|-----------------------|-------|
| résultat d’empilement | Image |

# Comportement {#behavior}

Ajuste les niveaux d’intensité pour un rendu visuel optimal.

1. Évalue la distribution des pixels à partir du résultat d’empilement.  
2. Applique les paramètres d’étirement configurés par l’utilisateur.  
3. Génère une image visuellement optimisée.

# Sortie

L’image étirée est transmise au processus suivant dans le pipeline **Process**.
