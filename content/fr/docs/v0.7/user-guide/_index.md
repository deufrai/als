---
title: "Guide Utilisateur"
description: "Guide utilisateur d'ALS"
author: "ALS Team"

lastmod: 2024-12-29T18:10:20Z
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

session
: Cycle de vie de la stack actuelle, commençant par la première brute détectée, traitant chaque nouvelle brute jusqu'à
  l'arrêt de la session.

stack
: Ensemble des brutes empilées depuis le démarrage de la session

## Typographie

- Ceci est un `élémént   d'interface graphique`
- Ceci est une **information importante**
- Ceci est un ⚠️ Avertissement
- Ceci est une ℹ️ Information
- Ceci est une 💡 Astuce
- Ceci eset un 🧠 Rappel
- 🖱️ une action à la souris est requise
- ⌨️ une action au clavier est requise
- 🎛️ une action en dehors d'ALS est requise

# Dans la peau du personnage... {#character}

Tout au long de ce voyage, vous incarnerez un nouvel utilisateur d'ALS :

- **Nom d'utilisateur**&nbsp;: Votre nom d'utilisateur est **astrogeek**
- **Système utilisé**&nbsp;: Vous utilisez ALS sur un système Linux
- **Organisation des brutes**&nbsp;: votre système d'acquisition enregistre les brutes dans le dossier **astroshots** de
  votre dossier personnel, organisées par cible avec les brutes dans des sous-dossiers **Light**.

  Exemple : Session sur Messier 27, les brutes sont enregistrées dans le dossier **astroshots/M_27/Light**.

{{< center >}}
{{< figure
src="lights_placement.png"
width="888px" height="484px"
caption="Emplacement des brutes"
alt="Emplacement des brutes" >}}
{{< /center >}}
