---
title: "Guide Utilisateur"
description: "Guide utilisateur d'ALS"
author: "ALS Team"

lastmod: 2026-06-03T20:47:13Z
keywords: [ "guide utilisateur d'ALS" ]
draft: false
type: "docs"
tags: [ "glossaire" , "typographie" ]
weight: 100300
---

**Laissez-vous guider !** Nous allons vous montrer tout ce qu'il y a à savoir sur ALS pour une utilisation fluide et
optimale, adaptée à **vos** besoins.

Le guide utilisateur vous accompagne dans ALS après le premier lancement : concepts de base, déroulement d'une session,
interface principale, préférences et interactions courantes.

# Conventions

Ce guide utilise les conventions de mise en forme et les termes suivants.

## Typographie {#typography}

<div class="row">
<div class="col-md-5">

### Texte
- un `élémént d'interface graphique`
- un {{< als-ks >}}raccourci clavier{{< /als-ks >}}
- une {{< als-code >}}commande{{< /als-code >}} ou un {{< als-code >}}extrait de code{{< /als-code >}}
- une **information importante**
- ⚙️ Détail technique

</div>
<div class="col-md-3">

### Paragraphes
- ⚠️ Avertissement
- ℹ️ Information
- 💡 Astuce
- 🧠 Rappel
- 🐛 Bug connu

</div>
<div class="col-md-4">

### Actions utilisateur
- 🖱️ une action à la souris est requise
- ⌨️ une action au clavier est requise
- 🎛️ une action en dehors d'ALS est requise

</div>
</div>

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
