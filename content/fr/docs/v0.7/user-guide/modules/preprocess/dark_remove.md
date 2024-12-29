---
title: "Soustraction du signal thermique"
description: "Documentation détaillée du traitement RemoveDark d'ALS"
author: "ALS Team"
lastmod: 2024-12-29T05:01:25Z
keywords: ["ALS dark current subtractor", "ALS soustraction de signal thermique"]
draft: false
type: "docs"
weight: 354
---

# Présentation

Le Traitement **DarkRemove** opère la soustraction du signal thermique de l'image en utilisant un master dark
fourni par l'utilisateur.

# Configuration


| Source                                                                         | Paramètre                |
|--------------------------------------------------------------------------------|--------------------------|
| [Préférences : Onglet Traitement](../../../preferences/processing/#dark-remove) | Activation du traitement |  
| [Préférences : Onglet Traitement](../../../preferences/processing/#dark-remove) | Chemin du master dark    |  

# Contrôle

Ce traitement est appliqué par le module **Pre-Process** sur chaque image reçue

# Entrée

| Type  | Description                                  |
|-------|----------------------------------------------|
| Image | image reçue du module parent **Pre-process** |
| Image | master dark fourni par l'utilisateur          |


# Comportement

le master dark est soustrait de l'image


{{% alert color="warning" %}}
⚠️ Le master dark **doit avoir les mêmes dimensions** (_largeur x hauteur_) que l'image à traiter
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ Il n'est pas obligatoire que les formats de données du master dark et de l'image soient identiques.

  En cas de différence : 
  - une conversion du master dark est opérée avant la soustraction
  - la différence de format est signalée discrètement dans le journal de session
{{% /alert %}}

# Sortie

L'image est rendue au module **Pre-Process** pour la suite du traitement
