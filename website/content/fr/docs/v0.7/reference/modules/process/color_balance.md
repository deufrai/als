---
title: "Color Balance"
description: "Documentation détaillée du traitement Color Balance dans le module Process d'ALS"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: [ "ALS color balance", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "traitement", "rgb", "ajustement d'image" ]
weight: 360
---

# Présentation

Le traitement **Color Balance** permet d'ajuster séparément les canaux rouge, vert et bleu.
Il appartient au pipeline **Process**.

# Configuration

| Réglage          | Source                               | Type de donnée | Valeur par défaut |
|------------------|--------------------------------------|----------------|-------------------|
| Bascule `Active` | [Panneau de traitement](../ui/processing/) | ON/OFF         | ON                |
| Curseur `Red`    | [Panneau de traitement](../ui/processing/) | flottant       | 1                 |
| Curseur `Green`  | [Panneau de traitement](../ui/processing/) | flottant       | 1                 |
| Curseur `Blue`   | [Panneau de traitement](../ui/processing/) | flottant       | 1                 |

# Contrôle

Ce traitement se gère depuis le **panneau de traitement**.

# Entrée

| Donnée            | Type  |
|-------------------|-------|
| résultat d'empilement | Image |

# Comportement {#behavior}

Ajuste la balance des couleurs de l'image.

1. Multiplie chaque canal par la valeur du curseur associé.
2. Limite les résultats à la plage supportée.

# Sortie

L'image équilibrée en couleurs est transmise à l'étape suivante.
