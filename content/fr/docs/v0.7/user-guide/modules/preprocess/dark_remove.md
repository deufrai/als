---
title: "Soustraction du signal thermique"
description: "Documentation détaillée du traitement RemoveDark d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T20:11:36Z
keywords: ["ALS dark current subtractor", "ALS soustraction de signal thermique"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["traitement", "dark"]
weight: 354
---

# Présentation

Le Traitement **DarkRemove** opère la soustraction du signal thermique de l'image en utilisant un master dark
fourni par l'utilisateur.

Sa configuration est gérée via les préférences

# Configuration


| Source                                                                         | Paramètre             |
|--------------------------------------------------------------------------------|-----------------------|
| [Préférences : Onglet Traitement](../../../preferences/processing/#dark-remove) | ON/OFF                |  
| [Préférences : Onglet Traitement](../../../preferences/processing/#dark-remove) | Chemin du master dark |  

# Contrôle

Ce traitement est ordonné par le module **Pre-Process**

# Entrée

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image reçue du module **Pre-process** |
| Image | master dark fourni par l'utilisateur          |


# Comportement

Le master dark est soustrait de l'image

# Sortie

L'image modifiée est renvoyée au module **Pre-Process**
