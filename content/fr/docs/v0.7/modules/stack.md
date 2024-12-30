---
title: "Stack"
description: "Documentation détaillée du module Stack d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T13:56:14Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "module", "stack" ]
weight: 356
---

# Présentation

Le module **Stack** prend en charge l'alignement et l'empilement des brutes calibrées

# Configuration

| Source                                                                 | Paramètre                  | Type de donnée                  | Requis | Valeur par défaut |
|------------------------------------------------------------------------|----------------------------|---------------------------------|--------|-------------------|
| [Interface : Contrôles de stacking](../../user-guide/ui/controls/#controls)  | Activation de l'alignement | ON/OFF                          | ∅      | ON                |
| [Interface : Contrôles de stacking](../../user-guide/ui/controls/#controls)  | Mode d'empilement          | choix :<br>- moyenne<br>- somme | OUI    | moyenne           |
| [Interface : Contrôles de stacking](../../user-guide/ui/controls/#threshold) | Seuil de détection         | page de valeurs                 | OUI    | 25                |

# Contrôle

Le module **Stack** est lancé en tâche de fond au démarrage d'ALS

| Type          | Source                     | Raccourci         | Action              |
|---------------|----------------------------|-------------------|---------------------|
| Événement     | brute(s) en file d'attente | ∅                 | lance le traitement |

# Entrée

| Type  | Description                                       |
|-------|---------------------------------------------------|
| Image | brute calibrée en tête de file d'attente |
| Image | référence d'alignement de la session              |

# Comportement {#behavior}

## Alignement

**Si l'alignement est activé**

1. recherche des similitudes entre la brute calibrée et la **référence d'alignement** de la session.

   {{% alert color="info" %}}
   Si la brute calibrée présente un nombre de similitudes **inférieur** au seuil de détection configuré, elle est
   **abandonnée** et le module **Stack** se remet à l'écoute de sa file d'attente.
   {{% /alert %}}

2. calcul des transformations nécessaires pour que la brute calibrée soit alignée sur la référence
    - translations
    - rotation
    - redimensionnements

3. application des transformations à la brute calibrée

## Empilement

1. Ajout de la brute calibrée et alignée (si demandé) à la pile
2. Génération d'une nouvelle image contenant le résultat de l'empilement selon le mode configuré

# Sortie

L'image générée est transmise au module **Process** 