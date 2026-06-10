---
title: "Onglet Sortie"
description: "Documentation de l'onglet Sortie des préférences d'ALS"
author: "ALS Team"
lastmod: 2026-06-10T17:50:29Z
keywords: [ "ALS output settings", "préférences Sortie d'ALS" ]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["output", "serveur", "dossier web", "dossier de travail", "save"]
weight: 100333
---

Les réglages régissant les sorties d'ALS sont présentés dans l'onglet `Sortie`.

# Vue d'ensemble {#overview}

<div class="row">
<div class="col-md-4">

Cet onglet est divisé en 2 sections :

- [Enregistreur de fichiers](#save)
- [Serveur d'images](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Sortie des préférences"
width="577px"
height="546px"
alt="Fenêtre des préférences ALS avec l'onglet Sortie sélectionné, affichant les options de format, les dossiers de sortie, l'enregistrement auto, l'adresse affichée et le numéro de port du serveur." >}}
{{< /center >}}

</div>
</div>

# Save {#save}

Ici sont configurés le format des images sauvegardées, les dossiers de sortie et la fonction d'autosave.


## Format {#format}

ALS enregistre les images de la sortie principale dans l'un des formats suivants :
- **TIFF**
- **PNG**
- **JPEG**

{{< center >}}
{{< figure src="formats.png"
caption="Préférences du format de fichier de la sortie principale"
width="577px"
height="212px"
alt="" >}}
{{< /center >}}

- 🖱️ utilisez les boutons `Format` pour définir le format de fichier de la sortie principale

ℹ️ Par défaut : JPEG

## Dossiers de sortie {#output-folders}

ALS utilise deux dossiers de sortie :
- **dossier de travail**

  Destination de la **sortie principale**

- **dossier web**

  Destination de la **sortie serveur**

### Dossier de travail {#work-folder}

- 🖱️ cliquez sur `Dossier de travail...` pour configurer le dossier de travail

ℹ️ Par défaut : ∅

{{< center >}}
{{< figure src="folders.png"
caption="Préférences des dossiers de sortie"
width="577px"
height="199px"
alt="" >}}
{{< /center >}}

### Dossier web {#web-folder}

{{% alert color="info" %}}
ℹ️ Par défaut, le **dossier web** est un alias menant au **dossier de travail**

Vous avez la possibilité de réellement séparer les deux sorties d'ALS en utilisant un **dossier web** dédié
{{% /alert %}}

### Dossier web dédié {#web-dedicated}

- 🖱️ cochez `Dossier web dédié` pour afficher les réglages du **dossier web** dédié
- 🖱️ cliquez sur `Dossier web...` pour configurer le **dossier web** dédié

ℹ️ Par défaut : OFF

## Autosave {#autosave}

### Résultat horodaté à l'arrêt de session {#autosave-stop}

Active la sauvegarde, à **chaque arrêt de session**, du **dernier** résultat de traitement :

- **sortie** : sortie principale
- **nom** : composé de **stack_image** + **_final** + _suffixe d'horodatage_
- **Format** : Format de sortie configuré

{{% alert title="💡" color="light" %}}
Cette fonction est utile quand vous enchaînez les sessions sur des cibles différentes

À chaque arrêt de session, le dernier résultat est sauvegardé dans un fichier qui ne risque pas d'être écrasé
{{% /alert %}}

{{< center >}}
{{< figure src="autosave.png"
caption="Préférences de l'autosave"
width="577px"
height="154px"
alt="" >}}
{{< /center >}}

- 🖱️ cochez `Résultat horodaté à l'arrêt de session` pour activer la fonction d'autosave

ℹ️ Par défaut : ON

# Server {#server}

Ici sont configurés l'adresse affichée et le port d'écoute du serveur d'images.

{{< center >}}
{{< figure src="web_config.png"
caption="Réglages du serveur d'images"
width="577px"
height="187px"
alt="Réglages du serveur d'images affichant la liste Adresse affichée réglée sur Auto - recommandé et le numéro de port réglé sur 8000." >}}
{{< /center >}}

## Adresse affichée {#server-address}

Définit l'adresse réseau affichée dans le panneau `Contrôles principaux`, la barre de statut et la fenêtre QR code
lorsque le serveur d'images fonctionne.

La liste contient `Auto - recommandé`, puis les adresses réseau découvertes sur le système qui exécute ALS. Chaque
adresse listée appartient à un adaptateur réseau détecté.

Les adresses listées sont ordonnées selon leur utilité probable :

1. Adresses probablement accessibles depuis un autre appareil du réseau local.
2. Adresses d'adaptateurs Wi-Fi ou Ethernet courants.
3. Adresses d'autres adaptateurs, y compris point d'accès, partage de connexion, bridge, virtuels, Docker, VPN et tunnel.
4. Adresses link-local, lorsqu'aucune meilleure adresse locale n'est disponible.
5. Adresses de loopback, en dernier recours pour un accès local uniquement.

- 🖱️ choisissez `Auto - recommandé` pour utiliser la première adresse de la liste ordonnée
- 🖱️ choisissez une adresse spécifique lorsqu'un autre appareil doit se connecter par un réseau particulier, par exemple
  un point d'accès Wi-Fi ou un réseau local dédié

ℹ️ Par défaut : Auto - recommandé

{{% alert title="Dépannage" color="warning" %}}
Si un autre appareil ne peut pas naviguer vers le serveur d'images pendant qu'il fonctionne, ouvrez les préférences
Sortie et sélectionnez une autre **Adresse affichée**. Choisissez une adresse appartenant au même réseau que l'appareil qui
utilise le navigateur, cliquez `OK`, puis réessayez l'URL ou le QR code.

L'adresse affichée peut être modifiée sans arrêter le serveur d'images.
{{% /alert %}}

## Numéro de port {#server-port}

Le port d'écoute du serveur d'images est configuré ici

Valeurs autorisées : 1024 à 65535

- ⌨️ Saisissez le `numéro de port` sur lequel le serveur d'images sera accessible

ℹ️ Par défaut : 8000

{{% alert color="info" %}}
Changer le numéro de port nécessite d'abord d'arrêter le serveur d'images.
{{% /alert %}}
