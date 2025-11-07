---
title: "Guide Utilisateur"
description: "Guide utilisateur d'ALS"
author: "ALS Team"

lastmod: 2025-11-07T14:26:25Z
keywords: [ "guide utilisateur d'ALS" ]
draft: false
type: "docs"
tags: [ "glossaire" , "typographie" ]
weight: 100300
---

**Laissez-vous guider !** Nous allons vous montrer tout ce qu'il y a à savoir sur ALS pour une utilisation fluide et
optimale, adaptée à **vos** besoins.

# Conventions

Définissons tout d'abord les termes et mises en forme que nous utiliserons tout au long de ce guide.

## Glossaire {#glossary}

### brute {#sub}

Image capturée par votre système d'acquisition

### calibration {#calibration}

Ensemble de traitements appliqués aux brutes dans le but d'éliminer les défauts du capteur du système optique

### master dark {#master-dark}

Image contenant le bruit thermique du capteur. Elle est soustraite des brutes pendant la calibration

### master flat {#master-flat}

Image représentant le motif d'illumination du système optique et les non-uniformités de réponse du capteur. Elle est
utilisée pour corriger les brutes du vignettage et des ombres de poussières pendant la calibration.

Les brutes sont divisées par le master flat après la soustraction du master dark pendant la calibration

## Typographie

### Texte
- un `élémént d'interface graphique`
- un <span class="als-ks">raccourci clavier</span>
- une {{< als-code >}}commande{{< /als-code >}} ou un {{< als-code >}}extrait de code{{< /als-code >}}
- une **information importante**
- ⚙️ Détail technique

### Paragraphes
- ⚠️ Avertissement
- ℹ️ Information
- 💡 Astuce
- 🧠 Rappel
- 🐛 Bug connu

### Actions utilisateur
- 🖱️ une action à la souris est requise
- ⌨️ une action au clavier est requise
- 🎛️ une action en dehors d'ALS est requise

