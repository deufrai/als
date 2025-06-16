---
title: "Save"
description: "Documentation détaillée du module Save d'ALS"
author: "ALS Team"
lastmod: 2025-01-05T13:36:11Z
keywords: ["module Save d'ALS"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "output", "dossier web", "dossier de travail", "save"]
weight: 362
---

# Présentation

Le module **save** prend en charge tous les enregistrements sur disque des images générés par ALS.

Sa configuration est gérée via les préférences

# Configuration

|                    | Source                                                                    | Type de donnée                       | Requis | Valeur par défaut    |
|--------------------|---------------------------------------------------------------------------|--------------------------------------|--------|----------------------|
| dossier de travail | [Préf. : Onglet Sortie](../../userguide/preferences/output/#work-folder)  | chemin vers un dossier               | Oui    | ∅                    |
| dossier web        | [Préf. : Onglet Sortie](../../userguide/preferences/output/#web-folder)   | chemin vers un dossier               | Oui    | = dossier de travail |
| format de fichier  | [Préf. : Onglet Sortie](../../userguide/preferences/output/#format)       | choix :<br>- TIFF<br>- PNG<br>- JPEG | Oui    | JPEG                 |

# Contrôle

Le module **Save** est lancé en tâche de fond au démarrage d'ALS

# Entrée

| Donnée                          | Type  |
|---------------------------------|-------|
| image en tête de file d'attente | Image |

# Comportement

Enregistre les deux sorties sur disque :

| Type de sortie    | Nom de Fichier                        | Emplacement du fichier | Format de fichier |
|-------------------|---------------------------------------|------------------------|-------------------|
| Principale        | stack_image (+ horodatage si demandé) | dossier de travail     | Tel que configuré |
| Serveur           | web_image                             | dosser web             | JPEG              |     

# Sortie

Fichiers images enregistrés sur disque