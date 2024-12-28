---
title: "Détecteur d'images"
description: "Documentation détaillée du module détecteur d'images d'ALS"
author: "ALS Team"
lastmod: 2024-12-28T23:45:25Z
keywords: ["ALS image detector", "détecteur d'images ALS"]
draft: false
type: "docs"
weight: 350
---

Le module **détecteur d'images** est le point d'entrée de vos brutes dans ALS.

Il surveille le **dossier scanné** et fournit les images détectées aux autres modules. 

{{% alert color="info" %}}
ℹ️ La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

# Influences


| Configuré par | Documentation                                                      |
|---------------|--------------------------------------------------------------------|
| Préférences   | [Chemin du dossier scanné](../../preferences/general/#scan-folder) |
| Interface     | ∅                                                                  |



| Contrôlé par | Documentation                                                                            |
|--------------|------------------------------------------------------------------------------------------|
| Interface    | [Contrôles de session](../../als-gui/controls/#session-controls)                         |
| Menus        | ∅                                                                                        |
| Raccourcis   | - `R` bascule marche/arrêt dans la session courante<br> - `X` arrêt + clôture de session |

# Entrée

| Type      | Description |
|-----------|-------------|
| Événement | Nouvelle image détectée dans le **dossier scanné** |


# Comportement

1. Charge l'image en mémoire, avec toutes les métadonnées disponibles

# Sortie

L'image chargée est transmise au module **Pre-Process** 