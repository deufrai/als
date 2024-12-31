---
title: "Save"
description: "Documentation détaillée du module Save d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T14:11:00Z
keywords: ["module Save d'ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module", "output", "dossier web", "dossier de travail" ]
weight: 362
---

# Présentation

Le module **save** prend en charge tous les enregistrements de fichiers images générés par ALS.

Sa configuration est gérée via les préférences

# Configuration

| Source                        | Paramètre                    | Type de donnée                       | Requis | Valeur par défaut    |
|-------------------------------|------------------------------|--------------------------------------| ------- |----------------------|
| [Préf. : Onglet Général](../../userguide/preferences/general/#work-folder) | dossier de travail           | chemin vers un dossier               | Oui     | ∅                    |
| [Préf. : Onglet Sortie](../../userguide/preferences/output/#web-folder) | dossier web                  | chemin vers un dossier               | Oui     | = dossier de travail |
| [Préf. : Onglet Sortie](../../userguide/preferences/output/#format) | format de fichier            | choix :<br>- TIFF<br>- PNG<br>- JPEG | Oui     | JPEG                 |

# Contrôle

Le module **Save** est lancé en tâche de fond au démarrage d'ALS

# Entrée

| Type  | Description                     |
|-------|---------------------------------|
| Image | image en tête de file d'attente |

# Comportement

Enregistre les deux sorties sur disque :

| Type de sortie    | Nom de Fichier                        | Emplacement du fichier | Format de fichier |
|-------------------|---------------------------------------|------------------------|-------------------|
| Principale        | stack_image (+ horodatage si demandé) | dossier de travail     | Tel que configuré |
| Serveur           | web_image                             | dosser web             | JPEG              |     

# Sortie

Fichiers images enregistrés sur disque