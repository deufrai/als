---
title: "Guide Utilisateur"
description: "Guide utilisateur d'ALS"
author: "ALS Team"

lastmod: 2024-12-30T07:34:28Z
keywords: [ "guide utilisateur d'ALS" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "conventions" , "glossaire" , "typographie" ]
weight: 300
---

**Laissez-vous guider !** Nous allons vous montrer tout ce qu'il y a à savoir sur ALS pour une utilisation fluide et
optimale, adaptée à **vos** besoins.

# Conventions

Définissons tout d'abord les termes et mises en forme que nous utiliserons tout au long de ce guide.

## Glossaire

brute
: Image capturée par votre système d'acquisition

calibration
: Ensemble de traitements appliqués aux brutes dans le but d'éliminer les défauts du capteur. Cela inclut généralement
la suppression des pixels chauds et la soustraction d'un master dark pour réduire le bruit thermique.

empilement
: Génération d'une image contenant le résultat de la somme ou de la moyenne pixel-à-pixel d'un ensemble de brutes calibrées

master dark
: Image de calibration contenant le bruit thermique du capteur. Elle est soustraite des brutes pendant la calibration
pour réduire le bruit thermique des images avant l'empilement.

session
: Cycle de vie de la stack actuelle, commençant par la première brute détectée, traitant chaque nouvelle brute jusqu'à
l'arrêt de la session.

stack
: Ensemble des brutes empilées depuis le démarrage de la session

## Typographie

- Ceci est un `élémént   d'interface graphique`
- Cece est un <span class="als-ks">raccourci clavier</span>
- Ceci est une **information importante**
- Ceci est un ⚠️ Avertissement
- Ceci est une ℹ️ Information
- Ceci est une 💡 Astuce
- Ceci eset un 🧠 Rappel
- 🖱️ une action à la souris est requise
- ⌨️ une action au clavier est requise
- 🎛️ une action en dehors d'ALS est requise

