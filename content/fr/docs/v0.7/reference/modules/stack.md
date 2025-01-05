---
title: "Stacker"
description: "Documentation détaillée du module Stack d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: [ "ALS stack" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "module", "traitement", "stack", "seuil" ]
weight: 356
---

# Présentation

Le module **Stacker** prend en charge l'alignement et l'empilement des brutes calibrées

# Configuration

|                            | Source                                                                      | Type de donnée                  | Requis | Valeur par défaut |
|----------------------------|-----------------------------------------------------------------------------|---------------------------------|--------|-------------------|
| Activation de l'alignement | Interface : [Contrôles de stacking](../../userguide/ui/controls/#controls)  | ON/OFF                          | ∅      | ON                |
| Mode d'empilement          | Interface : [Contrôles de stacking](../../userguide/ui/controls/#controls)  | choix :<br>- moyenne<br>- somme | OUI    | moyenne           |
| Seuil de détection         | Interface : [Contrôles de stacking](../../userguide/ui/controls/#threshold) | entier                          | OUI    | 25                |

# Contrôle

Le module **Stack** est lancé en tâche de fond au démarrage d'ALS

| Source                     | Type          | Réponse             |
|----------------------------|---------------|---------------------|
| brute(s) en file d'attente | Événement     | lance le traitement |

# Entrée

| Description                          | Type  |
|--------------------------------------|-------|
| brute en tête de file d'attente      | Image |
| référence d'alignement de la session | Image |

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

1. Ajout de la brute alignée (si demandé) à la pile
2. Génération d'une nouvelle image contenant le résultat de l'empilement selon le mode configuré

# Sortie

L'image générée est diffusée