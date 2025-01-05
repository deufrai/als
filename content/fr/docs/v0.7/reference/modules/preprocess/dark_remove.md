---
title: "Soustraction de dark"
description: "Documentation détaillée du traitement RemoveDark d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: ["ALS soustraction de dark"]
type: "docs"
categories: ["documentations détaillées"]
tags: ["traitement", "dark", "calibration"]
weight: 354
---

# Présentation

Le Traitement **DarkRemove** soustrait le signal thermique de l'image en utilisant un master dark
fourni par l'utilisateur.

Sa configuration est gérée via les préférences

# Configuration


|                       | Source                                                                                    | Type de donnée         | Requis | Valeur par défaut |
|-----------------------|-------------------------------------------------------------------------------------------|------------------------|--------|-------------------|
| ON/OFF                | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#dark-remove) | ON/OFF                 | ∅      | OFF               |
| Chemin du master dark | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#dark-remove) | chemin vers un fichier | OUI    | ∅                 |

# Contrôle

Ce traitement est déclenché par le module **Preprocess**

# Entrée

| Donnée                                     | Type  |
|--------------------------------------------|-------|
| image fournie par le module **Preprocess** | Image |
| master dark lu depuis le chemin configuré  | Image |


# Comportement

Le master dark est soustrait de l'image

- Si les types de données sont différents, le master dark est converti en le même type de données que l'image avant la soustraction.
- Si les dimensions sont différentes, le traitement est interrompu et l'image **non modifiée** est renvoyée au module **Preprocess**

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
