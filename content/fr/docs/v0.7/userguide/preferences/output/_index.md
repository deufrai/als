---
title: "Onglet Sortie"
description: "Documentation de l'onglet Sortie des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T20:05:38Z
keywords: [ "ALS outout settings", "préférences Sortie  d'ALS" ]
draft: false
type: "docs"
categories: ["configuration"]
tags: [ "preferences", "output", "formats", "serveur", "dossier web" ]
weight: 333
---

Les réglages régissant les résultats produits sont présentés dans l'onglet `Sortie`.

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

# Enregistreur de fichiers {#save}

Ici sont configurés le format des images sauvegardées et la fonction de sauvegarde auto à l'arrêt de la session.

<div class="row">
<div class="col-md-8">

## Format {#format}

Les boutons `Format` définissent le format des fichiers enregistrés

## Enregistrement auto fin de session {#session-stop-save}

`Enregistrement auto fin de session` active la sauvegarde automatique du **dernier** résultat
du module **Process** dans un nouveau fichier horodaté, à chaque arrêt de session :

- **emplacement du fichier** : **dossier de travail**
- **nom du fichier** : composé de **stack_image** et d'un suffixe d'horodatage
- **Format et extension du fichier** : en fonction du format choisi

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">

{{< center >}}
{{< figure src="saver.png"
caption="Préférences de l'enregistreur de fichiers"
width="307px"
height="103px"
alt="Interface logicielle affichant les préférences de sauvegarde de fichiers avec des options pour sélectionner le format de fichier (TIFF, PNG, JPEG) et une case à cocher pour activer ou désactiver l'enregistrement automatique à l'arrêt." >}}
{{< /center >}}

</div>
</div>


# serveur web {#server}

Ici sont configurés les paramètres du serveur d'images

<div class="row">
<div class="col-md-8">

## Numéro de port {#server-port}

1. `Numéro de port serveur` configure le port sur lequel le serveur d'images est accessible

## période de rafraîchissement {#server-refresh}

2. `Période de rafraîchissement` configure la période de rafraîchissement de l'image par les navigateurs connectés


</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="web_config.png"
caption="Réglages du serveur web"
width="437px"
height="195px"
alt="Panneau de configuration des paramètres du serveur web, incluant le numéro de port du serveur réglé sur 8000, la période de rafraîchissement de la page web réglée sur 5 secondes." >}}
{{< /center >}}

</div>
</div>

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

