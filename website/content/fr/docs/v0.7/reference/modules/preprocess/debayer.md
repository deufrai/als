---
title: "Dématriçage"
description: "Documentation détaillée du traitement de dématriçage d'ALS"
author: "ALS Team"
lastmod: 2025-06-17T10:36:33Z
keywords: ["ALS debayer", "ALS dépatriçage"]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "traitement", "dématriçage", "calibration" ]
weight: 355
---

# Présentation

Le Traitement **DeBayer** est utilisé sur les images **couleur** au format **FITS** ou **Raw**.

Il consiste à générer une image couleur à partir de l'image brute et de la description de la matrice de Bayer
à utiliser.

Sa configuration est gérée via les préférences

# Configuration

|                  | Source                                                                                | Type de donnée                                            | Requis  | Valeur par défaut |
|------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------|---------|-------------------|
| Matrice de Bayer | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#debayer) | choix :<br>- AUTO<br>- GRBG<br>- RGGB<br>- GBRG<br>- BGGR | OUI     | AUTO              |

# Contrôle

Ce traitement est contrôlé par le module **Preprocess**

# Entrée

| Donnée                                       | Type  |
|----------------------------------------------|-------|
| image fournie par le module **Preprocess**   | Image |


# Comportement

```mermaid
graph LR

    START([START])
    
    TEST_AUTO{{Préférences = AUTO ?}}
    TEST_NEEDED{{Dématriçage nécessaire ?}}
    
    READ_META[Matrice = Lecture des métadonnées]
    READ_PREF[Matrice = Lecture des préférences]
    
    DEBAYER[Dématriçage]
    UNCHANGED[Renvoyer image inchangée]
    
    RETURN[Renvoyer image modifiée]
    
    END([END])
    
    START --> TEST_AUTO
    
    TEST_AUTO -- OUI --> TEST_NEEDED
    TEST_NEEDED -- OUI ---> READ_META
    TEST_AUTO -- NON ---> READ_PREF
    
    READ_META --> DEBAYER
    READ_PREF --> DEBAYER
    
    TEST_NEEDED -- NON --> UNCHANGED
    
    DEBAYER --> RETURN
    
    UNCHANGED --> END
    RETURN --> END

    
    classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
    classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
    classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
    classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif
    
    class TEST_AUTO,TEST_NEEDED test
    class START,END bounds
    class RETURN,UNCHANGED,DEBAYER,READ_META,READ_PREF step
```

L'image brute est convertie en image couleur en utilisant la matrice de Bayer configurée.

- si la matrice configurée est définie sur **AUTO**, la matrice est extraite des métadonnées de l'image.

# Sortie

L'image modifiée est renvoyée au module **Preprocess**
