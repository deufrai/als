---
title: "Dématriçage"
description: "Documentation détaillée du traitement de dématriçage d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T08:41:06Z
keywords: ["ALS debayer", "ALS dépatriçage"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["traitement", "dématriçage"]
weight: 355
---

# Présentation

Le Traitement **DeBayer** est utilisé sur les images **couleur** au format **FITS** ou **Raw**.

Il consiste à générer une image couleur à partir de l'image brute et de la description de la matrice de Bayer
à utiliser.

Sa configuration est gérée via les préférences

# Configuration

| Source                                 | Paramètre                | Type de donnée           | Requis | Valeur par défaut |
|----------------------------------------|--------------------------|---------------------------| ------- | --------------- |
| [Préférences : Onglet Traitement](../../../user-guide/preferences/processing/#debayer) | Matrice de Bayer | choix :<br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR | OUI     | AUTO              |


# Contrôle

Ce traitement est ordonné par le module **Preprocess**

# Entrée

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image reçue du module parent **Preprocess** |


# Comportement

L'image brute est convertie en image couleur en utilisant la matrice de Bayer configurée.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
