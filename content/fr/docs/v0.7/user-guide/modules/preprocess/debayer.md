---
title: "Dématriçage"
description: "Documentation détaillée du traitement de dématriçage d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T02:26:36Z
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
installée sur le capteur qui a généré l'image.

Sa configuration est gérée via les préférences

# Configuration

| Source                                                                         | Paramètre                |
|--------------------------------------------------------------------------------|--------------------------|
| [Préférences : Onglet Traitement](../../../preferences/processing/#debayer) | Matrice de Bayer |  

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
