---
title: "Suppression des pixels chauds"
description: "Documentation détaillée du traitement HotPixelRemove d'ALS"
author: "ALS Team"
lastmod: 2025-01-12T13:03:24Z
keywords: ["ALS hot pixel removal", "ALS suppression des pixels chauds"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["traitement", "pixels chauds", "calibration"]
weight: 353
---

# Présentation

Le Traitement **HotPixelRemove** supprime les pixels chauds de l'image

Sa configuration est gérée via les préférences

# Configuration

|        | Source                                                                                   | Type de donnée | Requis | Valeur par défaut |
|--------|------------------------------------------------------------------------------------------|----------------|--------|-------------------|
| ON/OFF | Préférences : [Onglet Traitement](../../../userguide/preferences/processing/#hot-remove) | ON/OFF         | ∅      | OFF               |

# Contrôle

Ce traitement est contrôlé par le pipeline **Preprocess**

# Entrée

| Donnée                                       | Type  |
|----------------------------------------------|-------|
| image fournie par le pipeline **Preprocess** | Image |


# Comportement


```mermaid
graph LR

    START([START])
    
    TEST_ENABLED{{Ttaitement activé ?}}
    TEST_COLOR{{Image couleur ?}}
    
    COMPUTE[Calculer valeurs moyennes des voisins de chaque pixel]
    REPLACE[Remplacer la valeur des pixels chauds par la moyenne des voisins]
    
    RETURN[Renvoyer image modifiée]
    UNCHANGED[Renvoyer image inchangée]
    
    END([END])
    
    START --> TEST_ENABLED
    TEST_ENABLED -->|Oui| TEST_COLOR
    TEST_COLOR ---->|Oui| UNCHANGED
    TEST_ENABLED ---->|Non| UNCHANGED
    TEST_COLOR -->|Non| COMPUTE
    COMPUTE --> REPLACE
    REPLACE --> RETURN
    RETURN --> END
    UNCHANGED --> END
    
    classDef bounds fill: #333, stroke: #666, stroke-width: 2px, color: #BBB, font-family: 'Poppins', sans-serif
    classDef step fill: #444, stroke: #622, stroke-width:2px, color: #c6c6c6, font-family: 'Poppins',sans-serif
    classDef wait  fill: #444, stroke: #262,stroke-width: 2px, color: #c6c6c6, font-family:'Poppins', sans-serif
    classDef test fill: #444, stroke: #226, stroke-width: 2px, color: #c6c6c6, font-family: 'Poppins', sans-serif
    
    class START bounds
    class TEST_ENABLED test
    class TEST_COLOR test
    class COMPUTE step
    class UNCHANGED step
    class REPLACE step
    class RETURN step
    class END bounds
```

Chaque pixel de l'image dont la valeur s'écarte trop de ses voisins est considéré comme un pixel chaud 

Sa valeur est remplacée par la valeur moyenne de ses voisins.

# Sortie

L'image modifiée est renvoyée au pipeline **Preprocess**
