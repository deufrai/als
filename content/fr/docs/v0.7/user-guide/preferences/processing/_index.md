---
title: "Onglet Traitement"
description: "Documentation de l'onglet Traitement des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T05:45:30Z
keywords: ["ALS processing settings", "préférences traitement ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["preferences", "traitement", "Preprocess", "dématriçage", "dark", "pixels chauds"]
weight: 332
---

Les réglages des traitements d'ALS sont présentés dans l'onglet `Traitement` des préférences.

<div class="row">
<div class="col-md-6">

# Vue d'ensemble

Cet onglet ne contient qu'une seule section : [Pre-processing](#preprocess)

Elle regroupe les réglages des traitements gérés par le module [**Preprocess**](../../modules/preprocess/) :
- [Suppression des pixels chauds](#hot-remove)
- [Soustraction de dark](#dark-remove)
- [Dématriçage](#debayer)

</div>
<div class="col-md-6 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Traitement des préférences"
width="622px"
height="604px"
alt="L'onglet Traitement des préférences" >}}
{{< /center >}}

</div>
</div>

# Pre-processing {#preprocess}

{{% alert color="info" %}}
ℹ️ Ces paramètres ne sont accessibles que quand la session est stoppée
{{% /alert %}}

## Suppression des pixels chauds {#hot-remove}

{{< center >}}
{{< figure src="hot_remove.png"
caption="Réglages de suppression des pixels chauds"
width="259px"
height="75px"
alt="Réglages de suppression des pixels chauds" >}}
{{< /center >}}

`suppression des pixels chauds` active la suppression

## Soustraction de dark {#dark-remove}

{{< center >}}
{{< figure src="dark_remove.png"
caption="Réglages de soustraction du signal thermique"
width="588px"
height="139px"
alt="Réglages de soustraction du signal thermique" >}}
{{< /center >}}

1. `soustraction de dark` active la soustraction
2. `Modifier...` permet de choisir le fichier master dark à utiliser pour la soustraction. 
3. `Vider` permet de vider le chemin du fichier master dark.

{{% alert color="warning" %}}
⚠️ Le master dark **doit avoir les mêmes dimensions** (_largeur x hauteur_) que l'image à traiter

Si les dimensions sont différentes :
- un message **WARNING** est ajouté au journal de session, portant le message '_incohérence de la structure des données_'
- Le bouton `Acquitter` du `Journal de session` est activé
- Si le `journal de session` est caché, l'indicateur de nouveaux problèmes apparaît dans la section `Problèmes` du
  panneau.
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ Il n'est pas obligatoire que les formats de données du master dark et de l'image soient identiques.

  En cas de différence (_ex. master dark en flottants 32bits et brute en entiers 16bits_) : 
  - le master dark est converti avant son utilisation
  - la différence de format est signalée discrètement dans le journal de session
{{% /alert %}}

## Dématriçage {#debayer}

{{< center >}}
{{< figure src="debayer.png"
caption="Réglage du dématriçage"
width="588px"
height="139px"
alt="Réglage du dématriçage" >}}
{{< /center >}}

{{% alert title="ℹ️ mode AUTO" color="info" %}}

La matrice utilisée est extraite des métadonnées des brutes

Si les métadonnées ne contiennent aucune matrice
  - Les brutes ne seront pas dématricées
  - Des défauts en forme de grille ou de damiers seront visibles sur les images générées

<details>
<summary>Métadonnées recherchées</summary>

- Image au format FITS : entête FITS **BAYERPAT**
- Image au format Raw : entête Exif standard
</details>
{{% /alert %}}
