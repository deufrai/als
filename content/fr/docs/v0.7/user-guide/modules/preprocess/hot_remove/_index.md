---
title: "Suppression des pixels chauds"
description: "Documentation détaillée du traitement HotPixelRemove d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T02:17:04Z
keywords: ["ALS hot pixel removal", "ALS suppression des pixels chauds"]
draft: false
type: "docs"
weight: 353
---

# Introduction

Le Traitement **HotPixelRemove** supprime les pixels chauds de l'image

# Influences

| Configuré par | Documentation                                              |
|---------------|------------------------------------------------------------|
| Préférences   | [Traitements](../../../preferences/processing/#hot-remove) |
| Interface     | ∅                                                          |



| Contrôlé par | Documentation                                                                            |
|--------------|------------------------------------------------------------------------------------------|
| Interface    | ∅                |
| Menus        | ∅                                                                                        |
| Raccourcis   | ∅|

# Entrée

| Type  | Description                                    |
|-------|------------------------------------------------|
| Image | image reçue du module parent : **Pre-process** |


# Comportement

Chaque pixel de l'image dont la valeur s'écarte trop de ses voisins est considéré comme un pixel chaud 

Sa valeur est remplacée par la valeur moyenne de ses voisins.

# Sortie

L'image est rendue au module **Pre-Process** pour la suite du traitement
