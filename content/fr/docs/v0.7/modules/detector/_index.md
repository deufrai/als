---
title: "Détecteur d'images"
description: "Documentation détaillée du module détecteur d'images d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T08:41:06Z
keywords: ["ALS image detector", "détecteur d'images ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module", "dossier scanné" ]
weight: 350
---

# Présentation

Le module **détecteur d'images** est le point d'entrée de vos brutes dans ALS.

Il surveille le **dossier scanné** et fournit les images détectées au module **Preprocess**.

Sa configuration est gérée via les préférences.

Il est contrôlé par l'interface et les raccourcis clavier.

# Configuration

| Source                                                                            | Paramètre                | Type de donnée           | Requis | Valeur par défaut |
|-----------------------------------------------------------------------------------|--------------------------|---------------------------| ------- | --------------- |
| [Préférences : Onglet Général](../../user-guide/preferences/general/#scan-folder) | Chemin du dossier scanné | Chemin vers un dossier | Oui     | ∅              |  


# Contrôle

| Source                                                                       | Action                                                                                                                               |
|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| [Interface : Contrôles de session](../../user-guide/ui/controls/#session-controls) | ON/OFF                                                                                                                               |
| Raccourcis                                                                   | - <span class="als-ks">R</span> bascule ON/OFF dans la session courante<br> - <span class="als-ks">X</span> OFF + clôture de session |

# Entrée

| Type      | Description                                                  |
|-----------|--------------------------------------------------------------|
| Événement | Une nouvelle brute a été détectée dans le **dossier scanné** |


# Comportement

1. Charge en mémoire l'image détectée, avec toutes ses métadonnées

{{% alert color="info" %}}
ℹ️ La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

# Sortie

L'image chargée est transmise au module **Preprocess** 