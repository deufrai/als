---
title: "Niveaux"
description: "Documentation détaillée du processus Niveaux dans le module Process d’ALS"
author: "Équipe ALS"
lastmod: 2025-10-22T15:32:52Z
keywords: [ "ALS niveaux", "écrêtage noir", "écrêtage blanc", "tons moyens", "traitement visuel" ]
draft: false
type: "docs"
categories: [ "documentations détaillées" ]
tags: [ "processus", "niveaux", "ajustement d’image" ]
weight: 359
---

# Vue d’ensemble

Le processus **Niveaux** ajuste la répartition de la luminosité d’une image empilée en définissant les
points noir et blanc, et en réglant les tons moyens.  
Il permet un contrôle précis du contraste et de la luminosité de l’image, en complément du processus **Auto-Stretch**.

Ce processus est géré par le module **Process** de la chaîne de traitement.

# Configuration

Les paramètres du processus **Niveaux** sont accessibles depuis le **Panneau de traitement**, situé sur le côté droit de l’interface d’ALS.

Consultez la [documentation du Panneau de traitement](../../../../userguide/ui/processing/#niveaux-section)
pour des instructions détaillées.

# Commandes

Le processus **Niveaux** est contrôlé via l’interface du `Panneau de traitement`.

| Commande      | Type       | Action                                               |
|---------------|------------|------------------------------------------------------|
| `Noir`        | curseur    | Définit le seuil d’écrêtage pour les zones sombres   |
| `Exposition`  | curseur    | Ajuste la luminosité des tons moyens                 |
| `Blanc`       | curseur    | Définit le seuil d’écrêtage pour les hautes lumières |

# Entrée

| Donnée                | Type  |
|-----------------------|-------|
| résultat d’empilement | Image |

# Comportement {#behavior}

Affine la luminosité et le contraste de l’image selon les seuils définis par l’utilisateur.

1. Applique un écrêtage noir pour supprimer les zones très sombres situées sous le point noir.  
2. Ajuste le gamma des tons moyens pour améliorer l’équilibre visuel.  
3. Applique un écrêtage blanc pour limiter les zones surexposées au-dessus du point blanc.  
4. Produit une image équilibrée, prête pour un traitement ou une visualisation ultérieure.

# Sortie

L’image ajustée est transmise au processus suivant dans la chaîne **Process**.
