---
title: "Pre-process"
description: "Documentation détaillée du module Preprocess d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T05:01:25Z
keywords: ["ALS pre-process"]
draft: false
type: "docs"
weight: 352
---

# Introduction

Le Module **Pre-Process** execute plusieurs traitements de calibration d'image

# Configuration

Le module **Pre-process** n'a besoin d'aucune configuration

# Contrôle

Le module **Pre-process** n'agit que comme orchestrateur de traitements.

Il est lancé au démarrage d'ALS et **ne subit plus aucune influence extérieure** à part l'arrivée des images dans 
sa file d'attente.

# Entrée

| Type  | Description                      |
|-------|----------------------------------|
| Image | image présente en file d'attente |


# Comportement

Applique ces traitements sur l'image :
  1. [Suppression des pixels chauds](hot_remove/)
  2. [Soustraction du signal thermique](dark_remove/) 
  3. [Dématriçage](debayer/)

# Sortie

L'image issue de l'étape 3 est transmise au module **Stack** 