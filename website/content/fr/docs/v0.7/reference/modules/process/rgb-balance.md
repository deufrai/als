---
title: "Balance RVB"
description: "Documentation détaillée du processus d’équilibrage des couleurs (Color Balance) dans le module Process d’ALS"
author: "Équipe ALS"
lastmod: 2025-10-22T19:07:25Z
keywords: [ "ALS balance des couleurs", "ajustement rvb", "correction colorimétrique", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "processus", "balance rvb", "ajustement d’image" ]
weight: 360
---

# Vue d’ensemble

Le processus **Balance RVB** ajuste l’intensité relative des trois couleurs primaires — rouge, vert et bleu — afin de corriger ou d’affiner la tonalité globale d’une image empilée.  
Il offre un contrôle précis de la balance chromatique, en complément des processus **Niveaux** et **Auto-Stretch**.

Ce processus est géré par le module **Process** de la chaîne de traitement.

# Configuration

Les paramètres de la **Balance RVB** sont accessibles depuis le **Panneau de traitement**, situé sur le côté droit de l’interface d’ALS.

Consultez la [documentation du Panneau de traitement](../../../../userguide/ui/processing/#balance-section)
pour des instructions détaillées.

# Contrôle

Le processus **Balance RVB** est contrôlé via l’interface du panneau `traitements`.

| Contrôle   | Type          | Action                               |
|------------|---------------|--------------------------------------|
| `Actif`    | case à cocher | Active ou désactiver le processus    |
| `R`        | curseur       | Ajuste l’intensité du canal rouge    |
| `V`        | curseur       | Ajuste l’intensité du canal vert     |
| `B`        | curseur       | Ajuste l’intensité du canal bleu     |

# Entrée

| Donnée                | Type  |
|-----------------------|-------|
| résultat d’empilement | Image |

# Comportement {#behavior}

Balance les composantes colorimétriques de l’image pour obtenir la tonalité souhaitée.

# Sortie

L’image équilibrée est transmise à la chaîne **Process**.
