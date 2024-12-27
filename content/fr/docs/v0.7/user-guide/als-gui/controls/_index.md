---
title: "Le panneau contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-27T01:39:16Z
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

# Présentation générale

Le panneau `Contrôles principaux` est situé à gauche de l'interface d'ALS. Il regroupe les contrôles et affichages
les plus utilisés en 5 sections

<div class="row">
  <div class="col-md-8">

## Session

Les contrôles de la session en cours se trouvent ici. Ils permettent de démarrer et d'arrêter la session, et affichent
également les informations sur la stack courante ainsi que l'indicateur d'état de la session.

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

La section **session** du panneau comprend 3 zones, de haut en bas :

<div class="row">
<div class="col-md-8">

## Contrôles de session

`START`
: Démarre une nouvelle session ou reprend la session mise en pause.

`PAUSE`
: Met en pause la session en cours.

`STOP`
: Arrête la session en cours.

L'accessibilité de ces boutons dépend du statut de la session.

## Informations sur la stack courante

Cette zone affiche le nombre total d'images empilées dans la stack courante et le temps d'exposition cumulé pour toute
la session.

_Dans cet exemple, nous avons empilé 39 images pour un total de 2m 36s._

## Statut de la session

Cette zone affiche le statut de la session en cours. Les statuts possibles sont : **stoppée**, **démarrée** et **en
pause**.

</div>
<div class="col-md-4">

{{< center >}}
{{< figure src="session.png"
caption="La section session"
width="294px"
height="127px"
alt="Section session" >}}
{{< /center >}}

</div>
</div>

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
