---
title: "Onglet Sortie"
description: "Documentation de l'onglet Sortie des préférences d'ALS"
author: "ALS Team"
lastmod: 2025-01-07T14:26:57Z
keywords: [ "ALS output settings", "préférences Sortie  d'ALS" ]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["output", "serveur", "dossier web", "dossier de travail", "save"]
weight: 333
---

Les réglages régissant les sorties d'ALS présentés dans l'onglet `Sortie`.

<div class="row">
<div class="col-md-4">

# Vue d'ensemble

Cet onglet est divisé en 2 sections :

- [Enregistreur de fichiers](#save)
- [Serveur d'images](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Sortie des préférences"
width="622px"
height="660px"
alt="Fenêtre de préférences ALS avec l'onglet Sortie sélectionné, affichant les paramètres pour les options de format de sauvegarde de fichier, l'enregistrement automatique à l'arrêt, la configuration du numéro de port du serveur, la période de rafraîchissement de la page web et une case à cocher pour le dossier dédié." >}}
{{< /center >}}

</div>
</div>

# Save {#save}

Ici sont configurés le format des images sauvegardées, les dossiers de sortie et la fonction d'autosave


## Format {#format}

ALS enregistre les images de la sortie principale dans l'un des formats suivants :
- **TIFF**
- **PNG**
- **JPEG**

{{< center >}}
{{< figure src="formats.png"
caption="Préférences du format de fichier de la sortie principale"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

- 🖱️ utilisez Les boutons `Format` pour définir le format de fichier de la sortie principale

ℹ️ Par défaut : JPEG

## Dossiers de sortie {#output-folders}

ALS utilise deux dossiers de sortie :
- **dossier de travail** 

  Destination de la **sortie principale**

- **dossier web**

  Destination de la **sortie serveur** 

### Dossier de travail {#work-folder}

- 🖱️ cliquez `Dossier de travail...` pour configurer le dossier de travail

ℹ️ Par défaut : ∅

{{< center >}}
{{< figure src="folders.png"
caption="Préférences des dossiers de sortie"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

### Dossier web{#web-folder}

{{% alert color="info" %}}
ℹ️ Par défaut, le **dossier web** est un alias menant au **dossier de travail**

Vous avez la possibilité de réellement séparer les deux sorties d'ALS en utilisant un **dossier web** dédié
{{% /alert %}}

### Dossier web dédié{#web-dedicated}

- 🖱️ cochez `Dossier web dédié` pour afficher les réglages du **dossier web** dédié
- 🖱️ cliquez `Dossier web...` pour configurer le **dossier web** dédié

ℹ️ Par défaut : OFF

## Autosave {#autosave}

### Résutlat horodaté à l'arrêt de session {#autosave-stop}

Active la sauvegarde, à **chaque arrêt de session**, du **dernier** résultat de traitement :

- **sortie** : sortie principale
- **nom** : composé de **stack_image** + **_final** + _suffixe d'horodatage_
- **Format** : Format de sortie configuré

{{% alert title="💡" color="light" %}}
Cette fonction est utile quand vous enchaînez les sessions sur des cibles différentes

A chaque arrêt de session, la meilleure version de l'image pour cette cible est sauvegardée dans un fichier qui
ne risque pas d'être écrasé
{{% /alert %}}

{{< center >}}
{{< figure src="autosave.png"
caption="Préférences de l'autosave"
width="622px"
height="417px"
alt="" >}}
{{< /center >}}

- 🖱️ cochez `Résutlat horodaté à l'arrêt de session` pour activer la fonction d'autosave

ℹ️ Par défaut : ON

# Server {#server}

Ici sont configurés le port d'écoute du serveur d'images et la période de rafraîchissement des images

## Numéro de port {#server-port}

Le port d'écoute du serveur d'images est configuré ici

Valeurs autorisées : 1024 à 65535

- ⌨️ Saisissez le `numéro de port` sur lequel le serveur d'images d'ALS sera accessible

ℹ️ Par défaut : 8000

{{< center >}}
{{< figure src="web_config.png"
caption="Réglages du serveur web"
width="622px"
height="175px"
alt="" >}}
{{< /center >}}



