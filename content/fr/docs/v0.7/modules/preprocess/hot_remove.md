---
title: "Suppression des pixels chauds"
description: "Documentation détaillée du traitement HotPixelRemove d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T08:41:06Z
keywords: ["ALS hot pixel removal", "ALS suppression des pixels chauds"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["traitement", "pixels chauds"]
weight: 353
---

# Présentation

Le Traitement **HotPixelRemove** supprime les pixels chauds de l'image

Sa configuration est gérée via les préférences

# Configuration

| Source                                                                         | Paramètre | Type de donnée | Requis | Valeur par défaut |
|--------------------------------------------------------------------------------|-----------|----------------|----| --------------- |
| [Préférences : Onglet Traitement](../../../user-guide/preferences/processing/#hot-remove) | ON/OFF    | ON/OFF         |  ∅  | OFF             |

# Contrôle

Ce traitement est ordonné par le module **Preprocess**

# Entrée

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image reçue du module **Preprocess** |


# Comportement

Chaque pixel de l'image dont la valeur s'écarte trop de ses voisins est considéré comme un pixel chaud 

Sa valeur est remplacée par la valeur moyenne de ses voisins.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
