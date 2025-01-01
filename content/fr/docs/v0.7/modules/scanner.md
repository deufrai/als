---
title: "Scanner"
description: "Documentation détaillée du module scanner d'ALS"
author: "ALS Team"
lastmod: 2025-01-01T22:17:04Z
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
- surveiller l'apparition des brutes dans le **dossier scanné**
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
|                     | Source                                                                           | Type de donnée                 | Requis | Valeur par défaut |
|---------------------|----------------------------------------------------------------------------------|--------------------------------|--------|-------------------|
| **Dossier scanné**  | Préférences : [Onglet Général](../../userguide/preferences/general/#scan-folder) | Chemin vers un dossier         | Oui    | ∅                 |
| **Profil**          | Préférences : [Onglet Général](../../userguide/preferences/general/#profile)     | choix :<br>- VA<br>- photo<br> | Oui    | VA                |
| **Gestion mémoire** | Préférences : [Onglet Général](../../userguide/preferences/general/#memory)      | mystérieux                     | Oui    | "Injuste"         |
# Contrôle

| Source                                                                            | Type       | Réponse                              |
|-----------------------------------------------------------------------------------|------------|--------------------------------------|
| Interface : [Contrôles de session](../../userguide/ui/controls/#session-controls) | Évenements | Surveillance dossier scanné : ON/OFF |
| une brute a été détectée dans le dossier scanné                                   | Évenement  | Charge la brute détectée             |

# Entrée

| Donnée                      | Type              |
|-----------------------------|-------------------|
| chemin de la brute détectée | Chemin de fichier |

# Comportement

## Test RAM dispo {#ram}

Il peut arriver que les brutes soient détectées plus fréquemment qu'ALS ne peut traiter et
enregistrer les images.

Il faut éviter de saturer la mémoire du système en chargeant sans contrôle les brutes qui se présentent

- Attend que la quantité de RAM disponible soit supérieure à la valeur configurée pour la gestion de la mémoire :

  | Gestion de la mémoire | Quantité de Mémoire laissée au système |
  |-----------------------|----------------------------------------|
  | Gourmand              | 256MiB                                 |
  | Injuste               | 512MiB                                 |
  | Juste                 | 1GiB                                   |
  | Peureux               | 2GiB                                   |

## Attente fichier complet {#wait}

Les fichiers sont détectés dès leur **apparition** dans le **dossier scanné**

Pour éviter de charger des fichiers incomplets, le module **Scanner** attend que le fichier soit complètement
écrit avant de le charger :

- Interroge en boucle la taille du fichier détecté
    - Vérifie que la taille du fichier est stable sur 2 interrogations consécutives

Le temps d'attente entre les interrogations dépend du profil configuré :

| profil         | temps d'attente entre 2 interrogations |
|----------------|----------------------------------------|
| Visuel assisté | 10ms                                   |
| Astrophoto     | 500ms                                  |

## Chargement de l'image {#load}

### Formats compatibles {#input-formats}

ALS détermine le format de l'image à partir de son extension de fichier

Le fichier est chargé en mémoire en utilisant le format déterminé par son extension : 

| Extension                                                        | Format |
|------------------------------------------------------------------|--------|
| <div style="font-family: monospace;">.jpg<br>.jpeg</div>         | JPEG   |
| <span style="font-family: monospace;">.png</span>                | PNG    |
| <div style="font-family: monospace;">.tiff<br>.tif</div>         | TIFF   |
| <div style="font-family: monospace;">.fits<br>.fit<br>.fts</div> | FITS   |
| Toutes les autres extensions                                     | Raw    | 

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
flowchart TB
    START([Brute detectée])
    WAIT_RAM[Attend RAM]
    CHECK_RAM{{TEST : RAM dispo<br>Selon profil<br><br>OK ?}}
    CHECK_SIZE{{TEST : taille fichier<br>OK ?}}
    WAIT_FILE[Attend fichier<br>Selon profil]
    TEST_FORMAT{{TEST : format fichier}}
    FITS[Charge fichier FITS]
    STANDARD[Charge fichier standard]
    RAW[Charge fichie Raw]
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
```

# Sortie

L'image chargée est diffusée pour qui veut bien s'en occuper.

⚙️ _ALS passera l'image au module **Prétraitement** pour la calibration_

---

[1] [Liste des appareils photo pris en charge par la librairie libRaw](https://www.libraw.org/supported-cameras) 