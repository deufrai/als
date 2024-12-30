---
title: "Stack"
description: "Documentation détaillée du module Stack d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T05:21:00Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "module", "stack" ]
weight: 354
---

# Introduction

Le module **Stack** prend en charge l'alignement et l'empilement des brutes

# Configuration

| Source                                                                           | Paramètre                  | Type de donnée                  | Requis | Valeur par défaut |
|----------------------------------------------------------------------------------|----------------------------|---------------------------------|--------|-------------------|
| [Interface : Contrôles de stacking](../../../preferences/processing/#dark-remove) | Activation de l'alignement | ON/OFF                          | ∅      | ON                |
| [Interface : Contrôles de stacking](../../../preferences/processing/#dark-remov) | Mode de stacking           | choix :<br>- moyenne<br>- somme | OUI    | moyenne           |
 | [Interface : Contrôles de stacking](TODO)                                        | Seuil de détection         | page de valeur : min=5 max=60   | OUI    | 25                |

# Contrôle

Le module **Stack** est lancé au démarrage d'ALS et **ne subit plus aucune influence extérieure** à part l'arrivée
des images dans sa file d'attente.

# Entrée

| Type  | Description                      |
|-------|----------------------------------|
| Image | image présente en file d'attente |

# Comportement {#behavior}

## Alignement

## Empilement

# Sortie

L'image issue de l'étape 3 est transmise au module **Process** 