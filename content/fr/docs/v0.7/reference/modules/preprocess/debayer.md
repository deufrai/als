---
title: "Dématriçage"
description: "Documentation détaillée du traitement de dématriçage d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: ["ALS debayer", "ALS dépatriçage"]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "traitement", "dématriçage", "calibration" ]
weight: 355
---

# Présentation

Le Traitement **DeBayer** est utilisé sur les images **couleur** au format **FITS** ou **Raw**.

Il consiste à générer une image couleur à partir de l'image brute et de la description de la matrice de Bayer
à utiliser.

Sa configuration est gérée via les préférences

# Configuration

|                  | Source                                                                                | Type de donnée                                            | Requis  | Valeur par défaut |
|------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------|---------|-------------------|
| Matrice de Bayer | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#debayer) | choix :<br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR | OUI     | AUTO              |

# Contrôle

Ce traitement est déclenché par le module **Preprocess**

# Entrée

| Donnée                                       | Type  |
|----------------------------------------------|-------|
| image fournie par le module **Preprocess**   | Image |


# Comportement

L'image brute est convertie en image couleur en utilisant la matrice de Bayer configurée.

- si la matrice configurée est définie sur **AUTO**, la matrice est extraite des métadonnées de l'image.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
