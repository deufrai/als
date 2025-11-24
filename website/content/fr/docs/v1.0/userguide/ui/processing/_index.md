---
title: "Traitements"
description: "Documentation du panneau Traitements de ALS"
author: "Équipe ALS"
lastmod: 2025-11-24T18:20:31Z
keywords: [ "traitements ALS", "histogramme", "auto stretch", "niveaux", "balance RVB", "curseurs", "panneaux" ]
type: "docs"
tags: [ "histogramme", "stretch", "curseurs", "traitements", "panneaux" ]
categories: [ "utilisation", "configuration" ]
weight: 100322
---

# Introduction

Dans ce chapitre, vous allez apprendre à améliorer vos images en utilisant le panneau `Traitements`

<div class="row">
<div class="col-md-8">

# Aperçu

Le panneau `Traitements` est la salle de contrôle du module **Process** 

Situé sur le côté droit de l’interface, ce panneau regroupe les contrôles des traitements en plusieurs sections :

- [**Histogramme**](#histogramme-section)  
  Visualisation graphique de la répartition des intensités lumineuses.

- [**Auto Stretch**](#stretch-section)  
  Réglage de la force de l’étirement automatique.

- [**Niveaux**](#niveaux-section)  
  Ajustement de l’exposition globale ainsi que des écrêtages des noirs et des blancs.

- [**Balance RVB**](#balance-section)  
  Ajustement des niveaux de rouge, vert et bleu pour corriger les couleurs.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="panel.png" 
caption="Le panneau Traitements" 
width="297px"
height="675px"
alt="Le panneau Traitements de ALS, incluant les sections Histogramme, Auto Stretch, Niveaux, et Balance RVB avec leurs curseurs et contrôles associés." >}}
</div>
</div>

---

# Histogramme {#histogramme-section}

L’**Histogramme** fournit une représentation graphique de la répartition des valeurs d’intensité lumineuse dans l’image
affichée. 

Cet outil est essentiel pour évaluer rapidement l’équilibre des tons et des couleurs.

## Propriétés du Graphique

- **Axe horizontal :** Indique l’intensité lumineuse, allant des ombres à gauche (faible intensité) aux hautes lumières à
  droite (forte intensité).
- **Axe vertical :** Représente le nombre de pixels à chaque niveau d’intensité. Les pics plus élevés indiquent une plus
  grande quantité de pixels dans cette plage tonale.

<div class="row">
<div class="col-md-8">

## Mode monochrome

Pour des brutes monochromes, une seule courbe est affichée, représentant la répartition des intensités lumineuses des
pixels de l’image.

</div>

<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="histo_mono.png"
caption="Histogramme monochrome"
width="321px"
height="148px"
alt="Histogramme dynamique reflétant la répartition des valeurs d’intensité lumineuse d'une image monochrome" >}}
{{< /center >}}
</div>
</div>

## Mode couleurs

<div class="row">
<div class="col-md-8">

Pour des brutes en couleur, l’histogramme affiche des courbes distinctes pour les 3 canaux : rouge, vert & bleu. 

Chaque courbe représente la répartition des pixels selon leur intensité dans son canal respectif, offrant une vue 
sur la contribution de chaque couleur dans l’image.

Les zones où les courbes se chevauchent sont colorées selon le mélange des couleurs impliquées.
</div>

<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="histo.png"
caption="Histogramme couleur"
width="318px"
height="147px"
alt="Histogramme dynamique reflétant la répartition des valeurs d’intensité lumineuse d'une image en couleurs" >}}
{{< /center >}}
</div>
</div>

---

# Contrôles des Traitements {#controls-section}

Cette section regroupe les contrôles du module **Process** et de ses 3 processeurs d’image :
- Auto Stretch
- Niveaux
- Balance RVB

Les contrôles de chaque processeur sont regroupés en sections, chacune comportant son propre ensemble de curseurs et
boutons :

## Réglages

Chaque curseur correspond à un paramètre ajustable. Aucune valeur numérique n’est affichée, pour encourager une approche
visuelle et intuitive.

{{% alert color="info" %}}
ℹ️ Tous les curseurs de ce panneau `Traitements` possèdent une fonctionnalité supplémentaire :  
🖱️ **Double-cliquer** sur la poignée d’un curseur le réinitialise à sa position par défaut.
{{% /alert %}}

## Gestion et Application des Paramètres

- `Appliquer` Génère une nouvelle image en fonction des positions actuelles des curseurs.  
  La vue centrale et l’histogramme seront mis à jour une fois le traitement terminé.
- `Défaut` Réinitialise tous les curseurs à leurs positions par défaut sans modifier l’image affichée.
- `Recharger` Replace les curseurs aux positions qu'ils avaient lors du dernier clic sur `Appliquer`, sans modifier
  l’image affichée.
- `Actif` Permet d’activer ou désactiver le traitement. Une nouvelle image est générée immédiatement après ce
  changement, sans besoin de cliquer sur `Appliquer`.

---

# Ajuster l’Image

## Auto Stretch {#stretch-section}

La section **Auto Stretch** ajuste l’intensité de l’étirement automatique appliqué à l’image, essentiel pour rendre les
images empilées exploitables.

🖱️ Utilisez le curseur `Force` pour régler la quantité d’étirement.

ℹ️ Par défaut : Un équilibre idéal magiquement défini par nous.

## Niveaux {#niveaux-section}

<div class="row">
<div class="col-md-8">

### Noir

🖱️ Utilisez le curseur `Noir` pour régler le seuil des tons sombres.

ℹ️ Par défaut : Gauche

- **Analysez l’histogramme :** Observez l’extrémité gauche de l’histogramme et vérifiez la distance entre les courbes et
  le bord gauche.
- **Objectif :** Placez les courbes juste au contact du bord gauche pour optimiser les tons sombres, tout en évitant de
  les écrêter.

*Déplacer le curseur vers la droite décale les courbes vers la gauche.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="levels.png"
caption="Histogramme après ajustement du noir"
width="318px"
height="147px"
alt="Histogramme montrant les courbes après réglages précis des niveaux noirs" >}}
</div>
</div>

### Blanc

🖱️ Utilisez le curseur `Blanc` pour régler le seuil des tons clairs

ℹ️ Par défaut : Droite

- **Objectif :** Ajustez ce curseur visuellement pour équilibrer la luminosité des hautes lumières tout en conservant les
  détails.

*Déplacer le curseur vers la gauche décale les courbes vers la droite.*

### Exposition

🖱️ Utilisez le curseur `Exposition` pour contrôler la luminosité globale

ℹ️ Par défaut : Centre

- **Objectif :** Obtenez une exposition correcte en vous fiant à votre perception pour identifier le niveau qui met le
  mieux votre cible en valeur.

*Déplacer le curseur vers la droite éclaircit globalement l’image.*

## Balance RVB {#balance-section}

<div class="row">
<div class="col-md-12">
  {{% alert color="info" %}}
  ℹ️ Disponible uniquement pour les images en couleur.
  {{% /alert %}}

  La section **Balance RVB** ajuste les niveaux de rouge, vert et bleu pour améliorer l’équilibre global des couleurs de l’image.

  ### Analysez l’Histogramme

  Observez les positions relatives des pics des trois courbes colorées
</div>
</div>

<div class="row">
<div class="col-md-8">

  ### Votre Objectif

  Obtenir un équilibre neutre des couleurs en alignant verticalement les pics principaux des trois courbes est 
  généralement un bon point de départ. 

  L'alignement des pics maximise souvent la zone blanche de l’histogramme.

</div>

<div class="col-md-4 d-flex align-items-center justify-content-center flex-column">

  <div class="mb-3">
    {{< figure src="rgb.png"
    caption="Histogramme d'une image neutre"
    width="320px"
    height="146px"
    alt="Histogramme montrant des pics alignés pour une image colorimétriquement neutre." >}}
  </div>

</div>
</div>

<div class="row">
<div class="col-md-8">

{{% alert color="light" %}}
💡 En fonction de la cible et de votre équipement, certaines courbes peuvent ne pas présenter de pics principaux.

Par exemple, une cible riche en H-alpha présentera une courbe rouge aplatie sans pic marqué.

Le mélange des couleurs de l'histogramme rend bien compte de la dominante rouge de l'image produite.
{{% /alert %}}
</div>

<div class="col-md-4 d-flex align-items-center justify-content-center flex-column">

  <div>
    {{< figure src="h-alpha.png"
    caption="Histogramme d'une cible H-alpha"
    width="320px"
    height="146px"
    alt="Histogramme montrant la dominance rouge d'une image H-alpha correctement ajustée." >}}
  </div>

</div>
</div>

### Actions des Curseurs

- Les curseurs **R**, **V** et **B** ajustent la position horizontale de leurs courbes respectives.
  *Déplacer le curseur vers la droite décale la courbe vers la droite.*
- Le curseur de **saturation** contrôle l'éloignement des canaux par rapport au gris neutre :
  - À gauche = désaturer jusqu'au monochrome.
  - Au centre = neutre (pas de changement).
  - À droite = renforcer l'intensité des couleurs sans modifier l'exposition.
  {{% alert color="info" %}}
  ⚙️ L'augmentation de la saturation n'affecte que les zones dont la luminosité dépasse le niveau du fond de ciel, en préservant les zones sombres.
  {{% /alert %}}