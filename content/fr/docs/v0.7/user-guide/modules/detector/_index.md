---
title: "Détecteur d'images"
description: "Documentation détaillée du module détecteur d'images d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T05:45:18Z
keywords: ["ALS image detector", "détecteur d'images ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module" ]
weight: 350
---

# Présentation

Le module **détecteur d'images** est le point d'entrée de vos brutes dans ALS.

Il surveille le **dossier scanné** et fournit les images détectées aux autres modules.

# Configuration

| Source                                                                      | Paramètre                |
|-----------------------------------------------------------------------------|--------------------------|
| [Préférences : Onglet Général](../../preferences/general/#scan-folder) | Chemin du dossier scanné |  


# Contrôle

| Source                                                                       | Action                                                                                   |
|------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| [Interface : Contrôles de session](../../als-gui/controls/#session-controls) | marche/arrêt                                                                             |
| Raccourcis                                                                   | - `R` bascule marche/arrêt dans la session courante<br> - `X` arrêt + clôture de session |

# Entrée

| Type      | Description |
|-----------|-------------|
| Événement | Nouvelle image détectée dans le **dossier scanné** |


# Comportement

1. Charge en mémoire l'image détectée, avec toutes ses métadonnées

{{% alert color="info" %}}
ℹ️ La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

# Sortie

L'image chargée est transmise au module **Pre-Process** 