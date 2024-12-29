---
title: "PreProcess"
description: "Documentation détaillée du module Preprocess d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T00:38:38Z
keywords: ["ALS pre-process"]
draft: false
type: "docs"
weight: 352
---

# Introduction

Le Module **Pre-Process** execute plusieurs traitements de calibration et de mise en conformité des images

# Influences

Le module **Pre-process** n'agit que comme orchestrateur de traitements.

Il est lancé au démarrage d'ALS et **ne subit plus aucune influence extérieure** à part l'arrivée des images dans 
sa file d'attente.

| Configuré par | Documentation                                                      |
|---------------|--------------------------------------------------------------------|
| Préférences   | ∅ |
| Interface     | ∅                                                                  |



| Contrôlé par | Documentation                                                                            |
|--------------|------------------------------------------------------------------------------------------|
| Interface    | ∅                |
| Menus        | ∅                                                                                        |
| Raccourcis   | ∅|

# Entrée

| Type  | Description                      |
|-------|----------------------------------|
| Image | image présente en file d'attente |


# Comportement

Effectue 4 traitements sur l'image :

  1. Suppression des pixels chauds 
  2. Soustraction du signal de thermique 
  3. Dématriçage
  4. Préparation de l'image pour les modules suivants

Les traitements 1 à 3 procèdent à la calibration de l'image

L'étape 4 est purement technique et s'efforce de ne pas modifier la qualité de l'image

# Sortie

L'image issue de l'étape 4 est transmise au module **Stack** 