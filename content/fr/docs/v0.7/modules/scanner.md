---
title: "Scanner"
description: "Documentation détaillée du module scanner d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T02:48:28Z
keywords: ["ALS image detector", "scanner ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module", "dossier scanné" ]
weight: 350
---

# Présentation

Le module **Scanner** est le point d'entrée de vos brutes dans ALS.

Il surveille le **dossier scanné** et fournit les images détectées au module **Preprocess**.

Sa configuration est gérée via les préférences.

# Configuration

| Source                                                                            | Paramètre                | Type de donnée           | Requis | Valeur par défaut |
|-----------------------------------------------------------------------------------|--------------------------|---------------------------| ------- | --------------- |
| [Préférences : Onglet Général](../../userguide/preferences/general/#scan-folder) | Chemin du dossier scanné | Chemin vers un dossier | Oui     | ∅              |  


# Contrôle

| Type   | Source                                                                   | Raccourci                                                                                                                                      | Action      |
|--------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Événements | [Interface : Contrôles de session](../../userguide/ui/controls/#session-controls) | - <span class="als-ks">R</span> Bascule ON/OFF dans la session en cours<br> - <span class="als-ks">X</span> OFF + fermeture de session | ON/OFF      |
| Événement  | brute détectée dans le dossier scanné                                   | ∅                                                                                                                                              | Charge l'image  |

# Entrée

| Type              | Description                 |
|-------------------|-----------------------------|
| Chemin de fichier | chemin de la brute détectée |


# Comportement

1. Charge en mémoire la brute détectée, avec toutes ses métadonnées

{{% alert color="info" %}}
ℹ️ La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

# Sortie

L'image chargée est transmise au module **Preprocess** 