---
title: "Onglet Traitement"
description: "Documentation de l'onglet Traitement des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T20:11:36Z
keywords: ["ALS processing settings", "préférences traitement ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["preferences", "traitement", "Pre-process", "dématriçage", "dark", "pixels chauds"]
weight: 332
---

Les réglages des traitements d'ALS sont présentés dans l'onglet `Traitement` des préférences.

<div class="row">
<div class="col-md-6">

# Vue d'ensemble

Cet onglet ne contient qu'une seule section : [Pre-processing](#preprocess)

Elle regroupe les réglages des traitements gérés par le module [**Pre-process**](../../modules/preprocess/) :
- [Suppression des pixels chauds](#hot-remove)
- [Soustraction de dark](#dark-remove)
- [Dématriçage](#demosaic)

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

- Activation

    |           |          |
    |-----------|----------|
    |Type de donnée       | ON / OFF |
    | Requis | ∅        |
    | Valeur par défaut | OFF      |

{{< center >}}
{{< figure src="hot_remove.png"
caption="Réglages de suppression des pixels chauds"
width="259px"
height="75px"
alt="Réglages de suppression des pixels chauds" >}}
{{< /center >}}

La case à cocher `suppression des pixels chauds` permet d'activer ou de désactiver le traitement.

## Soustraction de dark {#dark-remove}

- Activation

    |           |          |
    |-----------|----------|
    |Type de donnée       | ON / OFF |
    | Requis | ∅        |
    | Valeur par défaut | OFF      |

- Chemin du fichier master dark

    |           |                            |
    |-----------|----------------------------|
    |Type de donnée       | Chemin vers un fichier     |
    | Requis | Quand le traitement est ON |
    | Valeur par défaut | ∅                          |

{{< center >}}
{{< figure src="dark_remove.png"
caption="Réglages de soustraction du signal thermique"
width="588px"
height="139px"
alt="Réglages de soustraction du signal thermique" >}}
{{< /center >}}

1. La case à cocher `soustraction de dark` permet d'activer la soustraction. 
2. Le bouton `Modifier...` permet de désigner le fichier master dark à utiliser pour la soustraction.
3. Le bouton `Vider` permet de vider le chemin du fichier master dark.

{{% alert color="warning" %}}
⚠️ Le master dark **doit avoir les mêmes dimensions** (_largeur x hauteur_) que l'image à traiter
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ Il n'est pas obligatoire que les formats de données du master dark et de l'image soient identiques.

  En cas de différence (_ex. master dark en flottants 32bits et brute en entiers 16bits_) : 
  - une conversion du master dark est opérée avant la soustraction
  - la différence de format est signalée discrètement dans le journal de session
{{% /alert %}}

## Dématriçage {#demosaic}

- Matrice de Bayer à utiliser
    
    |           |                                                                   |
    |-----------|-------------------------------------------------------------------|
    |Type de donnée       | choix :<br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR |
    | Requis | OUI                                                               |
    | Valeur par défaut | AUTO                                                              |
    

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
