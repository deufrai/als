---
title: "Save"
description: "Documentation détaillée du module Save d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T02:48:28Z
keywords: ["module Save d'ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module", "output", "dossier web", "dossier de travail" ]
weight: 362
---

# Présentation

Le module **save** prend en charge tous les enregistrements de fichiers images générés par ALS.

Sa configuration est gérée via les préférences et l'interface.

# Configuration

| Source                        | Paramètre                    | Type de donnée                       | Requis | Valeur par défaut    |
|-------------------------------|------------------------------|--------------------------------------| ------- |----------------------|
| [Préf. : Onglet Général](../../userguide/preferences/general/#work-folder) | dossier de travail           | chemin vers un dossier               | Oui     | ∅                    |
| [Préf. : Onglet Sortie](../../userguide/preferences/output/#web-folder) | dossier web                  | chemin vers un dossier               | Oui     | = dossier de travail |
| [Préf. : Onglet Sortie](../../userguide/preferences/output/#format) | format de fichier            | choix :<br>- TIFF<br>- PNG<br>- JPEG | Oui     | JPEG                 |
| [Préf. : Onglet Sortie](../../userguide/preferences/output/#session-stop-save) | enreg. auto (fin de session) | ON/OFF                               | ∅     | OFF                  |
| [Interf. : Contrôles d'enreg.](../../userguide/ui/controls/#save-controls) | enreg. auto (chaque image)   | ON/OFF                               | ∅     | OFF                  |

# Contrôle

Le module **Save** est lancé en tâche de fond au démarrage d'ALS

| Type      | Source                                                                        | Raccourci                     | Action                                         |
|-----------|-------------------------------------------------------------------------------|-------------------------------|------------------------------------------------|
| Événement | [Interface : Contrôles d'enreg.](../../userguide/ui/controls/#save-controls) | <span class="als-ks">S</span> | enreg. auto ON pour le prochain enregistrement |
| Événement | empilement(s) traité(s) en file d'attente                                     | ∅                            | Enregsitre l'image                             |


# Entrée

| Type  | Description                                            |
|-------|--------------------------------------------------------|
| Image | Sortie du module **Process** en tête de file d'attente |

# Comportement

Enregistre l'image dans un fichier image :

| Type de sortie | Nom de Fichier                          | Emplacement du fichier | Format de fichier |
|-------------|-----------------------------------------|------------------------|-------------------|
| Principale  | stack_image + horodatage si enreg. auto | dossier de travail     | Tel que configuré |
| Serveur     | web_image                               | dosser web             | JPEG              |     

# Sortie

Fichier image enregistré sur disque