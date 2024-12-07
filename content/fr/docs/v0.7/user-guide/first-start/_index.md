---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"
lastmod: 2024-12-07T16:32:23Z
keywords: ["Premier démarrage d'ALS"]
draft: false
type: "docs"
tags: ['preferences']
weight: 31
---

# Introduction

À la fin de ce chapitre, vous aurez :
- Configuré les paramètres essentiels pour ALS.
- Lancé votre première session d'empilement et obtenu vos premiers résultats.


# Configuration minimale

Lors du premier démarrage, ALS vous accueille et vous demande de définir deux réglages essentiels :

- **Dossier scanné** : Le dossier où ALS surveille l'arrivée de nouvelles brutes.
- **Dossier de travail** : Le dossier où ALS enregistre les images produites.

{{< center >}}
{{< figure src="welcome.png" >}}
{{< /center >}}

Cliquez sur `OK` pour accéder aux préférences.

---

## Configurer les dossiers critiques

Définissez les dossiers critiques dans la section **Chemins** de l'onglet **Général**.

### Dossier scanné

Configurez ALS pour surveiller le dossier **astroshots** :

{{< center >}}
{{< figure src="prefs_01.png" >}}
{{< /center >}}

Cliquez sur `Modifier...` à côté de **Dossier scanné**. Un sélecteur de dossier apparaît.

---

{{< center >}}
{{< figure src="prefs_02.png" >}}
{{< /center >}}

1. Sélectionnez le dossier **astroshots**.
2. Cliquez sur `Choisir`.

---

### Dossier de travail

Créez un sous-dossier pour ALS nommé **sorties_als** dans votre dossier personnel :

{{< center >}}
{{< figure src="prefs_03.png" >}}
{{< /center >}}

Cliquez sur `Modifier...` à côté de **Dossier de travail**. Un sélecteur de dossier apparaît.

---

{{< center >}}
{{< figure src="prefs_04.png" >}}
{{< /center >}}

Cliquez sur `Créer un nouveau dossier`.

---

{{< center >}}
{{< figure src="prefs_05.png" >}}
{{< /center >}}

Un nouveau dossier apparaît, prêt à être renommé.

---

{{< center >}}
{{< figure src="prefs_06.png" >}}
{{< /center >}}

1. Nommez-le **sorties_als**.
2. Cliquez sur `Choisir`.

---

**ℹ️ Ne validez pas encore les préférences**, il reste un point important à aborder

---

## Statistiques d'utilisation

Il nous est très utile de savoir quelles versions d'ALS sont utilisées et sur quelle plateforme.

{{< center >}}
{{< figure src="prefs_07.png" >}}
{{< /center >}}

Nous vous serions très reconnaissants d'autoriser ALS à nous envoyer des statistiques d'utilisation, mais nous comprenons
également que vous puissiez être réticent à autoriser une telle fonctionnalité.

Sachez qu'ALS nous enverra **uniquement** les informations suivantes à chaque démarrage :
- Version d'ALS.
- Type de processeur.
- Type de système d'exploitation.

ALS étant un logiciel **opensource**, son code est disponible publiquement. Vous pouvez ainsi vérifier par vous-même 
la nature des informations envoyées en consultant le
<a href="https://github.com/deufrai/als/blob/release/0.7/src/als/main.py#L46" target="_blank">
code source de cette fonctionnalité</a> <i class="fa-brands fa-square-github"></i>

Cliquez ensuite sur `OK` pour valider les préférences.

---

# Votre toute première session

ALS est maintenant prêt à vous servir. Lancez une session avec les paramètres par défaut.

{{< center >}}
{{< figure src="ready.png" >}}
{{< /center >}}

1. Cliquez sur `START` dans la section **session** en haut à gauche
2. Lancer vos acquisitions avec votre système habituel

La première image détectée par ALS sert de référence.

Toutes les suivantes sont d'abord alignées avec cette référence puis empilées par moyenne sur toutes les précédentes.

Le résultat de ces traitements est présenté dans la zone centrale d'ALS. 

Laissez ALS travailler sur les images qui continuent à arriver et perdez-vous donc un peu dans la zone centrale :

- Zoomez avec la molette de votre souris
- Déplacez-vous dans l'image avec des glisser/déposer comme vous le feriez avec n'importe quel logiciel de visualisation
- Remettez le zoom à sa valeur d'origine avec un clic droit

À mesure que les images arrivent dans le dossier scanné, vous verrez l'image centrale gagner en contraste et en 
qualité.
