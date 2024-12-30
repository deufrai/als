---
title: "Guide Utilisateur"
description: "Guide utilisateur d'ALS"
author: "ALS Team"

lastmod: 2024-12-30T08:04:04Z
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

## Glossaire {#glossary}

### brute {#sub}

Image capturée par votre système d'acquisition

### calibration {#calibration}

Ensemble de traitements appliqués aux [brutes](#sub) dans le but d'éliminer les défauts du capteur. Cela inclut
généralement la suppression des pixels chauds et la soustraction d'un [master dark](#master-dark) pour réduire le bruit
thermique.

### empilement {#stacking}

Génération d'une image contenant le résultat de la somme ou de la moyenne pixel-à-pixel d'un ensemble de [brutes](#sub)
calibrées

### livestacking {#livestacking}
Pratique consistant à traiter et afficher en temps réel l'empilement d'un ensemble de [brutes](#sub) dynamique

### master dark {#master-dark}

Image contenant le bruit thermique du capteur. Elle est soustraite des [brutes](#sub) pendant
la [calibration](#calibration) pour réduire le bruit thermique des images avant l'empilement.

### session {#session}

Cycle de vie de la [stack](#stack) actuelle, commençant par la première [brute](#sub) détectée, traitant chaque
nouvelle [brute](#sub) jusqu'à l'arrêt de la session.

### stack {#stack}

Ensemble des [brutes](#sub) empilées depuis le démarrage de la [session](#session)

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

