---
title: "Scanner"
description: "Documentation détaillée du module scanner d'ALS"
author: "ALS Team"
lastmod: 2025-01-02T08:24:33Z
keywords: [ "ALS image detector", "scanner ALS" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "module", "input", "dossier scanné", "scanner" ]
weight: 350
---

# Présentation

Le module **Scanner** est le point d'entrée de vos brutes dans ALS.

Il est en charge de :
- surveiller l'**apparition** des brutes dans le **dossier scanné**
- charger les brutes détectées

{{% alert color="info" %}}
ℹ️ **Les fichiers existants sont ignorés**

Les fichiers présents dans le **dossier scanné** avant le démarrage du module **Scanner** ne sont pas détectés
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ **La détection des brutes est récursive**

Les brutes sont détectées quel que soit le niveau de sous-dossiers où elles apparaissent au sein du **dossier scanné**

Même si elles sont enregistrées dans des sous-dossiers créés après le démarrage du module **Scanner**
{{% /alert %}}

# Configuration
|                     | Source                                                                           | Type de donnée         | Requis | Valeur par défaut |
|---------------------|----------------------------------------------------------------------------------|------------------------|--------|-------------------|
| **Dossier scanné**  | Préférences : [Onglet Général](../../userguide/preferences/general/#scan-folder) | Chemin vers un dossier | Oui    | ∅                 |
| **Profil**          | Préférences : [Onglet Général](../../userguide/preferences/general/#profile)     | choix : VA / photo<br> | Oui    | VA                |
| **Gestion mémoire** | Préférences : [Onglet Général](../../userguide/preferences/general/#memory)      | mystérieux             | Oui    | "Injuste"         |
# Contrôle

| Source                                                                                  | Type                                  | Réponse                              |
|-----------------------------------------------------------------------------------------|---------------------------------------|--------------------------------------|
| Interface : [Contrôles de session](../../userguide/ui/controls/#session-controls)       | Commande : STOP                       | Surveillance du dossier scanné : OFF |
| Interface : [Contrôles de session](../../userguide/ui/controls/#session-controls)       | Commande : START                      | Surveillance du dossier scanné : ON  |
| Événement système                                                                       | brute détectée dans le dossier scanné | Charge la brute détectée             |

# Entrée

| Donnée                      | Type              |
|-----------------------------|-------------------|
| chemin de la brute détectée | Chemin de fichier |

# Comportement

## Test RAM dispo {#ram}

Attend que la quantité de RAM disponible soit supérieure à la valeur configurée :

| Gestion mémoire | Quantité de Mémoire laissée au système |
|-----------------|----------------------------------------|
| Gourmand        | 256MiB                                 |
| Injuste         | 512MiB                                 |
| Juste           | 1GiB                                   |
| Peureux         | 2GiB                                   |

## Attente fichier complet {#wait}


ℹ️ Les fichiers sont détectés dès leur **apparition** dans le **dossier scanné**

Il faut s'assurer que le fichier est complet avant de le charger en mémoire.

- Interroge en boucle la taille du fichier détecté
    - Vérifie que la taille du fichier est stable sur 2 interrogations consécutives

Le temps d'attente entre les interrogations dépend du profil configuré :

| profil         | temps d'attente entre 2 interrogations |
|----------------|----------------------------------------|
| Visuel assisté | 10ms                                   |
| Astrophoto     | 500ms                                  |

## Chargement de l'image {#load}

Le fichier est chargé en mémoire en utilisant le format correspondant à son extension :

| Extension                                                        | Format |
|------------------------------------------------------------------|--------|
| <div style="font-family: monospace;">.jpg<br>.jpeg</div>         | JPEG   |
| <span style="font-family: monospace;">.png</span>                | PNG    |
| <div style="font-family: monospace;">.tiff<br>.tif</div>         | TIFF   |
| <div style="font-family: monospace;">.fits<br>.fit<br>.fts</div> | FITS   |
| Toutes les autres extensions                                     | Raw[1] | 

## Extraction de métadonnées

Prise en charge pour les formats :
- **FITS**
- **Raw**

Métadonnées extraites du fichier et incorporées à l'image en mémoire :
- **Temps d'exposition**
- **Matrice de Bayer** (_pour les brutes issues d'un capteur couleur_)
    - fichiers FITS : entête **BAYERPAT**
    - fichiers Raw : entête Exif standard


```mermaid
flowchart LR
    START([Brute detectée])
    
    WAIT_FILE[Attend fichier<br><br>Selon profil :<br>Visuel assisté : 10ms<br>Astrophoto : 500ms]    
    WAIT_RAM[Attend 20ms]
    
    CHECK_RAM{{Teste RAM dispo<br><br>Selon préférences :<br>Gourmand : 2 GiB<br>Injuste : 1 GiB<br>Juste : 512 MiB<br>Peureux : 256MiB<br><br>OK ?}}
    CHECK_SIZE{{Teste taille fichier<br><br>OK ?}}
    TEST_FORMAT{{Teste format fichier}}
    
    FITS[Charge FITS]
    STANDARD[Charge standard]
    RAW[Charge Raw]
    
    METADATA[Extrait métadonnées]
    
    END((Fin))

    START ---> CHECK_RAM
    WAIT_RAM <-->|NON| CHECK_RAM

    CHECK_RAM --->|OUI| CHECK_SIZE
    WAIT_FILE <-->|NON| CHECK_SIZE
    CHECK_SIZE -->|OUI| TEST_FORMAT

    TEST_FORMAT -->  FITS
    TEST_FORMAT -->  STANDARD
    TEST_FORMAT -->  RAW

    RAW --> METADATA
    FITS --> METADATA

    STANDARD ---> END
    METADATA --> END

    style START fill:#333,stroke:#666,stroke-width:2px,color:#BBB,font-family:'Poppins',sans-serif
    style WAIT_RAM fill:#444,stroke:#666,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style CHECK_RAM fill:#444,stroke:#666,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style CHECK_SIZE fill:#444,stroke:#666,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style WAIT_FILE fill:#444,stroke:#666,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style TEST_FORMAT fill:#444,stroke:#666,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style FITS fill:#444,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style STANDARD fill:#444,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style RAW fill:#444,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style METADATA fill:#444,stroke:#970,stroke-width:2px,color:#c6c6c6,font-family:'Poppins',sans-serif
    style END fill:#333,stroke:#666,stroke-width:2px,color:#BBB,font-family:'Poppins',sans-serif
```



# Sortie

L'image chargée est diffusée pour qui veut bien s'en occuper.

⚙️ _ALS placera l'image dans la file d'attente du module **Preprocess** pour la calibration_

---

[1] [Liste des appareils photo pris en charge par la librairie libRaw](https://www.libraw.org/supported-cameras) 