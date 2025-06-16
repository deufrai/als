---
title: "Levels"
description: "Documentation détaillée du traitement Levels dans le module Process d'ALS"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: [ "ALS levels", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "traitement", "levels", "ajustement d'image" ]
weight: 359
---

# Présentation

Le traitement **Levels** ajuste les points noir et blanc ainsi que le niveau des tons moyens.
Il est exécuté automatiquement dans le pipeline **Process**.

# Configuration

| Réglage          | Source                               | Type de donnée | Valeur par défaut |
|------------------|--------------------------------------|----------------|-------------------|
| Bascule `Active` | [Panneau de traitement](../ui/processing/) | ON/OFF         | ON                |
| Curseur `Black`  | [Panneau de traitement](../ui/processing/) | entier         | 0                 |
| Curseur `Mids`   | [Panneau de traitement](../ui/processing/) | flottant       | 1                 |
| Curseur `White`  | [Panneau de traitement](../ui/processing/) | entier         | 65535             |

# Contrôle

Le traitement se pilote depuis le **panneau de traitement**.

# Entrée

| Donnée            | Type  |
|-------------------|-------|
| résultat d'empilement | Image |

# Comportement {#behavior}

Ajuste la tonalité de l'image.

1. Décale éventuellement le niveau des tons moyens.
2. Écrête éventuellement les valeurs en dehors de `Black` et `White`.
3. Normalise le résultat sur toute la plage.

# Sortie

Une image au ton corrigé est transmise à l'étape suivante.
