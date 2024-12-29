---
title: "Onglet Traitement"
description: "Documentation de l'onglet Traitement des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T05:45:18Z
keywords: ["ALS processing settings", "préférences traitement ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["preferences", "traitement" ]
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


## Suppression des pixels chauds {#hot-remove}

Un seul réglage : l'activation du traitement

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

2 réglages : 

- l'activation du traitement

    |           |          |
    |-----------|----------|
    |Type de donnée       | ON / OFF |
    | Requis | ∅        |
    | Valeur par défaut | OFF      |

- le chemin du fichier master dark

    |           |                                |
    |-----------|--------------------------------|
    |Type de donnée       | Chemin vers un fichier         |
    | Requis | Quand le traitement est activé |
    | Valeur par défaut | ∅                              |

{{< center >}}
{{< figure src="dark_remove.png"
caption="Réglages de soustraction du signal thermique"
width="588px"
height="139px"
alt="Réglages de soustraction du signal thermique" >}}
{{< /center >}}

1. La case à cocher `soustraction de dark` permet d'activer ou de désactiver le traitement. 
2. Le bouton `Modifier...` permet de choisir le fichier master dark
3. Le bouton `Vider` permet de vider le chemin du fichier master dark

## Dématriçage {#demosaic}

Un seul réglage : la matrice de Bayer à utiliser

|           |                |
|-----------|----------------|
|Type de donnée       | Liste de choix |
| Requis | OUI            |
| Valeur par défaut | AUTO           |

Les choix possibles sont :

- **AUTO** : Utilise la matrice décrite dans les métadonnées des images
- **GRBG**
- **RGGB**
- **GBRG**
- **BGGR**

{{< center >}}
{{< figure src="debayer.png"
caption="Réglages de dématriçage"
width="588px"
height="139px"
alt="Réglages de dématriçage" >}}
{{< /center >}}

