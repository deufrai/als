---
title: "Enregistreur d'images"
description: "Documentation détaillée de l'enregistreur d'images d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T13:01:03Z
keywords: ["enregistreur d'images d'ALS"]
draft: false
type: "docs"
categories: ["guide utilisateur"] 
tags: ["module", "output", "dossier web", "server" ]
weight: 362
---

# Présentation

Le module **enregistreur d'images** prend en charge tous les enregistrements de fichiers images générés par ALS.

Sa configuration est gérée via les préférences et l'interface.

# Configuration

| Source                                                                          | Paramètre                                  | Type de donnée                       | Requis | Valeur par défaut    |
|---------------------------------------------------------------------------------|--------------------------------------------|--------------------------------------| ------- |----------------------|
| [Préf. : Onglet Général](../../user-guide/preferences/general/#work-folder)     | dossier de travail                         | chemin vers un dossier               | Oui     | ∅                    |
| [Préf. : Onglet Sortie](../../user-guide/preferences/output/#web-folder)        | dossier web                                | chemin vers un dossier               | Oui     | = dossier de travail |
| [Préf. : Onglet Sortie](../../user-guide/preferences/output/#format)            | format de fichier                          | choix :<br>- TIFF<br>- PNG<br>- JPEG | Oui     | JPEG                 |
| [Préf. : Onglet Sortie](../../user-guide/preferences/output/#session-stop-save) | enreg. auto en fin de session              | ON/OFF                               | ∅     | OFF                  |
| [Interf. : Contrôles d'enreg.](../../user-guide/ui/controls/#save-controls)     | enreg. auto chaque resultats de traitement | ON/OFF                               | ∅     | OFF                  |

# Contrôle

Le module **Save** est lancé en tâche de fond au démarrage d'ALS

| Type      | Source                                | Raccourci                         | Action                                                    |
|-----------|---------------------------------------|-----------------------------------|-----------------------------------------------------------|
| Événement | [Interface : Contrôles d'enreg.](../../user-guide/ui/controls/#save-controls) |  <span class="als-ks">S</span>    | déclenche l'enreg. auto du dernier résutlat de traitement |


# Entrée

| Type  | Description                                    |
|-------|------------------------------------------------|
| Image | Sortie du module **Process** en file d'attente |

# Comportement

Enregistre l'image dans un fichier image :

| Type de sortie | Nom de Fichier                          | Emplacement du fichier | Format de fichier |
|-------------|-----------------------------------------|------------------------|-------------------|
| Principale  | stack_image + horodatage si enreg. auto | dossier de travail     | Tel que configuré |
| Serveur     | web_image                               | dosser web             | JPEG              |     

# Sortie

Fichier image enregistré sur disque