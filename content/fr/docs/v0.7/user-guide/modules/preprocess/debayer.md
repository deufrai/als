---
title: "Dématriçage"
description: "Documentation détaillée du traitement de dématriçage d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T05:45:18Z
keywords: ["ALS debayer", "ALS dépatriçage"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["traitement", "dématriçage"]
weight: 355
---

# Présentation

Le Traitement **DeBayer** est utilisé sur les images **couleur** au **format FITS ou Raw**.

Il consiste à générer une image couleur à partir de l'image brute et de la description de la matrice de Bayer
installée sur le capteur qui a généré l'image.

# Configuration

| Source                                                                         | Paramètre                |
|--------------------------------------------------------------------------------|--------------------------|
| [Préférences : Onglet Traitement](../../../preferences/processing/#demosaic) | Matrice de Bayer |  

# Contrôle

Ce traitement est appliqué par le module **Pre-Process** sur chaque image reçue

# Entrée

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image reçue du module parent **Pre-process** |


# Comportement

L'image brute est convertie en image couleur en utilisant la matrice de Bayer configurée.

- Si le paramètre de configuration **Matrice de Bayer** vaut **AUTO**

  La matrice utilisée et celle décrite dans les métadonnées de l'image.
  - ⚠️ Si les métadonnées ne contiennent aucune matrice
    - L'image n'est pas convertie
    - Des défauts en forme de grille ou de damiers seront visibles sur l'image

  <details>
  <summary>Métadonnées recherchées</summary>

  - Image au format FITS : entête FITS **BAYERPAT**
  - Image au format Raw : entête Exif standard
  </details>


# Sortie

L'image est rendue au module **Pre-Process** pour la suite du traitement
