---
title: "Onglet Sortie"
description: "Documentation de l'onglet Sortie des préférences d'ALS"
author: "ALS Team"
lastmod: 2025-01-02T16:10:46Z
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
- [Serveur web](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Sortie des préférences"
width="622px"
height="604px"
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

ℹ️ Par défaut : JPEG

{{< center >}}
{{< figure src="formats.png"
caption="Préférences du format de fichier de la sortie principale"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

- 🖱️ utiliser Les boutons `Format` pour définir le format de fichier de la sortie principale

## Dossiers de sortie {#output-folders}

ALS utilise deux dossiers de sortie :
- **dossier de travail** 

  Destination de la **sortie principale**

- **dossier web**

  Destination de la **sortie serveur** 

### Dossier de travail {#work-folder}

- 🖱️ cliquer `Dossier de travail...` pour configurer le dossier de travail

{{< center >}}
{{< figure src="folders.png"
caption="Préférences des dossiers de sortie"
width="622px"
height="213px"
alt="" >}}
{{< /center >}}

{{% alert color="info" %}}
ℹ️ Par défaut, le **dossier web** est un alias menant au **dossier de travail**

Vous avez la possibilité de réellement séparer les deux sorties d'ALS en utilisant un **serveur web** dédié
{{% /alert %}}

### Dossier web dédié{#web-folder}

- 🖱️ cocher `Dossier web dédié` pour afficher les réglages du **dossier web** dédié
- 🖱️ cliquer `Dossier web...` pour configurer le **dossier web** dédié

## Autosave {#autosave}

`Enregistrement auto fin de session` active la sauvegarde automatique du **dernier** résultat
du module **Process** dans un nouveau fichier horodaté, à chaque arrêt de session :

- **emplacement du fichier** : **dossier de travail**
- **nom du fichier** : composé de **stack_image** et d'un suffixe d'horodatage
- **Format et extension du fichier** : en fonction du format choisi



{{< center >}}
{{< figure src="saver.png"
caption="Préférences de l'enregistreur de fichiers"
width="307px"
height="103px"
alt="Interface logicielle affichant les préférences de sauvegarde de fichiers avec des options pour sélectionner le format de fichier (TIFF, PNG, JPEG) et une case à cocher pour activer ou désactiver l'enregistrement automatique à l'arrêt." >}}
{{< /center >}}



# serveur web {#server}

Ici sont configurés les paramètres du serveur d'images



## Numéro de port {#server-port}

1. `Numéro de port serveur` configure le port sur lequel le serveur d'images est accessible

## période de rafraîchissement {#server-refresh}

2. `Période de rafraîchissement` configure la période de rafraîchissement de l'image par les navigateurs connectés



{{< center >}}
{{< figure src="web_config.png"
caption="Réglages du serveur web"
width="437px"
height="195px"
alt="Panneau de configuration des paramètres du serveur web, incluant le numéro de port du serveur réglé sur 8000, la période de rafraîchissement de la page web réglée sur 5 secondes." >}}
{{< /center >}}


## Dossier web {#web-folder}

{{< center >}}
{{< figure src="web_folder.png"
caption="Réglage du dosser web"
width="598px"
height="209px"
alt="Panneau de configuration des paramètres du serveur web, montrant des options pour utiliser un dossier web dédié" >}}
{{< /center >}}

1. Si `Utiliser un dossier spécifique` est décochée :
   - les réglages du **dossier web** sont cachés
   - le chemin du **dossier web** est celui du **dossier de travail**

   Sinon
   - les réglages du **dossier web** sont affichés

   2. `Modifier...` permet de choisir un **dossier web** spécifique.
   3. Le chemin du **dossier web** est affiché

