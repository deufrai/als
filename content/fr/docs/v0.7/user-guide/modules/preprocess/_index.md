---
title: "Pre-process"
description: "Documentation détaillée du module Preprocess d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T20:11:36Z
keywords: [ "ALS pre-process" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "module", "Pre-process" ]
weight: 352
---

# Introduction

Le module **Pre-Process** prend en charge les traitements de **calibration** d'image

# Configuration

Le module **Pre-process** lui-même n'a besoin d'aucune configuration.

La configuration des traitements de **calibration** est gérée par les **traitements** eux-mêmes.
Voir section [Comportement](#behavior) ci-dessous.

# Contrôle

Le module **Pre-process** est lancé au démarrage d'ALS et **ne subit plus aucune influence extérieure** à part l'arrivée
des images dans sa file d'attente.

# Entrée

| Type  | Description                      |
|-------|----------------------------------|
| Image | image présente en file d'attente |

# Comportement {#behavior}

Applique ces traitements sur l'image :

1. [Suppression des pixels chauds](hot_remove/)
2. [Soustraction du signal thermique](dark_remove/)
3. [Dématriçage](debayer/)

# Sortie

L'image issue de l'étape 3 est transmise au module **Stack** 