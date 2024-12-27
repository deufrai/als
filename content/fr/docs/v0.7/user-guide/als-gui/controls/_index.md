---
title: "Le panneau contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-27T00:54:00Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
tags: [ "GUI", "controls" ]
weight: 321
---

# Introduction

A la fin de ce chapitre, vous aurez :

- Compris la fonction de chaque section du panneau des contrôles principaux
- Approfondi vos connaissances sur quelques concepts de base d'ALS
- Approfondi vos connaissances sur des éléments internes d'ALS : Modules stack, serveur d'images...

---

<div class="row">
  <div class="col-md-8">

# Présentation générale

Le panneau `Contrôles principaux` est situé à gauche de l'interface d'ALS. Il regroupe les contrôles et affichages
les plus utilisés en 5 sections :

## Session

Les contrôles de la session en cours se trouvent ici. Ils permettent de démarrer et d'arrêter la session, et affichent
également les informations sur la stack en cours ainsi que l'indicateur d'état de la session.

## Stack

Cette section permet de définir le mode d'alignement et d'empilement des images. Elle propose aussi un réglage de seuil
pour la recherche de similitudes pendant l'alignement.

## Serveur d'images

Permet de démarrer et arrêter le serveur d'images et affiche des informations sur le serveur lorsqu'il est actif.

## Enregistreur d'images

Permet d'enregistrer à la volée l'image courante et d'activer la fonction d'enregistrement continu.

## Modules

Cette section fournit des informations sur l'état d'utilisation de chaque module.

## Problèmes

Cette section n'est visible que si le ` Journal de session` est caché. Elle affiche un indicateur de nouveaux problèmes

  </div>
  <div class="col-md-4">
    {{< figure src="controls.png" caption="Le panneau des contrôles principaux" width="100%" alt="Menu fichier" >}}
  </div>
</div>

--- 

# Session

Avant de décrire les contrôles de session, il convient de définir ce qu'est une session dans le contexte d'ALS.

## Définition d'une session ALS

**Une session ALS** est une période pendant laquelle ALS contrôle la détection de nouvelles images et la pile
d'images actuelle.

1. **Démarrage** :
    - La session commence quand on appuie sur `START`. Cela active le module de détection de fichiers, vide la pile
      d'images actuelle et prépare la session pour de nouvelles images.
    - **Première Détection** : La première image détectée ensuite devient l'image de référence pour la session en cours.
      Toutes les images suivantes seront comparées à cette référence pour l'alignement.

2. **Traitement des Images** :
    - Pendant que la session est en cours, chaque nouvelle image détectée est comparée à l'image de référence pour
    - l'alignement, puis ajoutée à la pile, par moyenne ou somme. Les résultats successifs de cet empilement sont
      traités et affichés par l'application.
    - L'utilisateur gère la session en utilisant les contrôles `START` `PAUSE` et `STOP`.
    - Avec `PAUSE`, on arrête temporairement la détection d'images, mais la pile actuelle est conservée. Reprendre la
      session avec `START` relance la détection avec la pile existante.

3. **Arrêt** :
    - Quand on appuie sur `STOP`, la détection d'images s'arrête et la pile d'images actuelle est vidée. On peut ensuite
      démarrer une nouvelle session avec `START`.

_**Note** : ALS ne traite pas les images déjà présentes dans le **dossier scanné** avant le lancement de la session._

## Contrôle de la session

{{< center >}}
{{< figure src="session.png"
caption="La section session"
width="294px"
height="127px"
alt="Section session" >}}
{{< /center >}}

La section **session** du panneau est découpées en 3 zones :

- Boutons de contrôle de la session
- Informations sur la stack courante
- Statut de la session courante

### START

### PAUSE

### STOP

## Informations sur la stack courante

## Statut de la session courante

---

# Stack

---

# Serveur d'images

---

# Enregistreur d'images

---

# Modules

---

# Problèmes

---

# Conclusion

Vous avez maintenant une vision claire des différentes sections du panneau des contrôles principaux.
BLIBLIBLI