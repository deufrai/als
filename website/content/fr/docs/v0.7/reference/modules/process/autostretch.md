---
title: "Auto-Stretch"
description: "Documentation détaillée du traitement Auto-Stretch dans le module Process d'ALS"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: [ "ALS auto stretch", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "traitement", "stretch", "ajustement d'image" ]
weight: 358
---

# Présentation

Le traitement **Auto-Stretch** optimise automatiquement les niveaux d'intensité des images empilées afin de les rendre directement exploitables.

Ce traitement fait partie du pipeline **Process** et fonctionne en tâche de fond.

# Configuration

Le traitement **Auto-Stretch** ne nécessite aucune configuration.
Ses paramètres sont accessibles via le **panneau de traitement**.

# Contrôle

Le traitement est piloté depuis le **panneau de traitement**.

| Réglage           | Action                                      |
|-------------------|----------------------------------------------|
| Curseur `Strength`| Ajuste la force de l'étirement               |
| Bascule `Active`  | Active ou désactive le traitement            |

# Entrée

| Donnée           | Type  |
|------------------|-------|
| résultat d'empilement | Image |

# Comportement {#behavior}

Ajuste les niveaux pour une visualisation optimale.

1. Analyse la distribution des pixels.
2. Applique les paramètres définis dans ALS.
3. Génère une image optimisée.

# Sortie

L'image étirée est transmise à l'étape suivante ou affichée dans la zone centrale d'ALS.
