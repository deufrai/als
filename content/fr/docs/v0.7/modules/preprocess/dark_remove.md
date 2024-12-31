---
title: "Soustraction de dark"
description: "Documentation détaillée du traitement RemoveDark d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T20:05:37Z
keywords: ["ALS soustraction de dark"]
type: "docs"
categories: ["Documentations détaillées"] 
tags: ["traitement", "dark"]
weight: 354
---

# Présentation

Le Traitement **DarkRemove** soustrait le signal thermique de l'image en utilisant un master dark
fourni par l'utilisateur.

Sa configuration est gérée via les préférences

# Configuration


| Source                                                                         | Paramètre             | Type de donnée         | Requis | Valeur par défaut     |
|--------------------------------------------------------------------------------|-----------------------|------------------------|--------|-----------------------|
| [Préférences : Onglet Traitement](../../../userguide/preferences/processing/#dark-remove) | ON/OFF                | ON/OFF                 | ∅      | OFF                   |
| [Préférences : Onglet Traitement](../../../userguide/preferences/processing/#dark-remove) | Chemin du master dark | chemin vers un fichier | OUI    | ∅ |  

# Contrôle

Ce traitement est ordonné par le module **Preprocess**

# Entrée

| Type  | Description                               |
|-------|-------------------------------------------|
| Image | image reçue du module **Preprocess**      |
| Image | master dark lu depuis le chemin configuré |


# Comportement

Le master dark est soustrait de l'image

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
