---
title: "Scanner"
description: "Documentation détaillée du module scanner d'ALS"
author: "ALS Team"
lastmod: 2025-01-01T00:18:50Z
keywords: ["ALS image detector", "scanner ALS"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "input", "dossier scanné", "scanner"]
weight: 350
---

# Présentation

Le module **Scanner** est le point d'entrée de vos brutes dans ALS.

- surveille le **dossier scanné**
- charge les brutes détectées
- transmet les brutes au module **Preprocess**

# Configuration

Sa configuration est gérée via les préférences.

| Source                                                                           | Paramètre             | Type de donnée                 | Requis   | Valeur par défaut |
|----------------------------------------------------------------------------------|-----------------------|--------------------------------|----------|-------------------|
| [Préférences : Onglet Général](../../userguide/preferences/general/#scan-folder) | dossier scanné        | Chemin vers un dossier         | Oui      | ∅                 |
| [Préférences : Onglet Général](../../userguide/preferences/general/#profile)     | Profil                | choix :<br>- VA<br>- photo<br> | Oui      | VA                |
| [Préférences : Onglet Général](../../userguide/preferences/general/#memory)      | Gestion de la mémoire | flou                           | Oui      | "Injuste"         |

# Contrôle

| Source                                                                            | Type        | Action                               |
|-----------------------------------------------------------------------------------|-------------|--------------------------------------|
| [Interface : Contrôles de session](../../userguide/ui/controls/#session-controls) | Évenements  | Surveillance dossier scanné : ON/OFF |
| une brute a été détectée dans le dossier scanné                                   | Évenement   | Charge la brute détectée             |

{{% alert color="info" %}}
ℹ️ La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

# Entrée

| Type              | Description                 |
|-------------------|-----------------------------|
| Chemin de fichier | chemin de la brute détectée |

# Comportement

## Attente fichier complet {#wait}

Les fichiers sont détectés dès leur **apparition** dans le **dossier scanné**

Pour éviter de charger des fichiers incomplets, le module **Scanner** attend que le fichier soit complètement 
écrit avant de le charger :

- Interroge en boucle la taille du fichier détecté
- Attend que la taille du fichier soit stable sur 2 interrogations consécutives

  Le délai d'attente entre les interrogations dépend du profil configuré :

  - Profil **Visuel assisté** : 10ms
  - Profil **astrophoto** : 500ms

## Chargement de l'image {#load}

### Formats compatibles

- Les formats de fichiers image courants
- Les fichiers **FITS**
- Les fichiers **Raw** des appareils photo pris en charge par la librairie libRaw [1]

### Gestion de la mémoire

Il peut arriver que les brutes soient détectées plus fréquemment qu'ALS ne peut traiter et 
enregistrer les images. 

Dans ce cas, il faut s'assurer de ne pas saturer la mémoire du système en continuant indéfiniment à charger les brutes
qui se présentent

- Attend que la quantité de RAM disponible soit supérieure à la valeur configurée pour la gestion de la mémoire :
        
    | Gestion de la mémoire | Quantité de Mémoire laissée au système |
    |-----------------------|----------------------------------------|
    | Gourmand              | 256MiB                                 |
    | Injuste               | 512MiB                                 |
    | Juste                 | 1GiB                                   |
    | Peureux               | 2GiB                                   |

### Lecture du fichier

Le fichier est lu et chargé en mémoire.

## Extraction de métadonnées

L'extraction de métadonnées est prise en charge pour les formats **FITS** et **Raw**

Les métadonnées suivantes sont extraites du fichier et incorporées à l'image en mémoire
- **Temps d'exposition**
- **Matrice de Bayer** (_pour les brutes issues d'un capteur couleur_)
  - fichiers FITS : entête **BAYERPAT**
  - fichiers Raw : entête Exif standard

# Sortie

L'image chargée est transmise au module **Preprocess** 

---

[1] [Liste des appareils photo pris en charge par la librairie libRaw](https://www.libraw.org/supported-cameras) 