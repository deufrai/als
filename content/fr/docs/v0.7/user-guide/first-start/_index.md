---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"

lastmod: 2024-12-07T15:45:57Z
keywords: ["Premier démarrage d'ALS"]
draft: false
type: "docs"
tags: ['preferences']
weight: 31
---

A la fin de chapitre, vous aurez :
- Effectué la configuration minimale requise pour le fonctionnement d'ALS
- Lancé votre toute première session d'empilement et obtenu vos premiers résultats

# Configuration minimale

À votre tout premier démarrage, ALS vous souhaite la bienvenue et vous demande de définir les 2 réglages 
indispensables à son fonctionnement :

- **Dossier scanné** : Le dossier de votre système dans lequel ALS surveille l'arrivée des nouvelles brutes
- **Dossier de travail** : Le dossier de votre système dans lequel ALS enregistre les images produites

{{< center >}}
{{< figure src="welcome.png" >}}
{{< /center >}}

Un click sur `OK` et ALS vous présente la fenêtre des préférences

---

## Configurer les dossiers critiques

Les deux dossiers critiques d'ALS sont définis dans la section **Chemins** de l'onglet **Général** de la fenêtre des préférences.

### Dossier scanné

Nous allons indiquer à ALS de surveiller le contenu du dossier **astroshots** 

{{< center >}}
{{< figure src="prefs_01.png" >}}
{{< /center >}}

Cliquez sur le bouton `Modifier...` en regard de **Dossier scanné**. Un sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_02.png" >}}
{{< /center >}}

  1. Selectionnez le dossier **astroshots**
  2. Cliquez sur le bouton `Choisir` 

--- 

### Dossier de travail

Nous allons créer un sous-dossier spécifique à ALS, nommé **sorties_als**, dans notre dossier personnel


{{< center >}}
{{< figure src="prefs_03.png" >}}
{{< /center >}}

Cliquez sur le bouton `Modifier...` en regard de **Dossier de travail**. Un autre sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_04.png" >}}
{{< /center >}}

Cliquez sur le bouton `Créer un nouveau dossier`

---

{{< center >}}
{{< figure src="prefs_05.png" >}}
{{< /center >}}

Un nouveau dossier apparaît et son nom est prêt à être modifié 

---

{{< center >}}
{{< figure src="prefs_06.png" >}}
{{< /center >}}

1. Saisissez directement **sorties_als**
2. Cliquez sur le bouton `Choisir` 

---

**ℹ️ Ne validez pas encore les préférences**, il reste un point important à aborder

---

## Statistiques d'utilisation

{{< center >}}
{{< figure src="prefs_07.png" >}}
{{< /center >}}

Il nous est très utile de savoir quelles versions d'ALS sont utilisées, et surtout sur quelle plateforme et quel
système d'exploitation.

C'est pourquoi nous vous demandons de bien vouloir autoriser ALS à nous envoyer les informations suivantes à chaque 
démarrage :
- Version d'ALS
- Type de processeur
- Type de système d'exploitation

Nous comprenons que vous puissiez être réticent à autoriser une telle fonctionnalité. Après tout, quelle garantie
avez-vous qu'ALS envoie bien uniquement les informations listées ci-dessus ? ALS est un **logiciel opensource** : Son code
est disponible publiquement. Vous pouvez vérifier par vous-même la nature des informations envoyées par ALS en 
consultant le
<a href="https://github.com/deufrai/als/blob/release/0.7/src/als/main.py#L46" target="_blank">code source de cette fonctionnalité</a>

Une fois votre choix fait en toute connaissance de cause, validez les préférences en cliquant le bouton `OK`

---

# Votre toute première session 

{{< center >}}
{{< figure src="ready.png" >}}
{{< /center >}}

bliblobliblo lorem etc... Et aussi... pecat ! On peut vagement en faire quelque chose.