---
title: "contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-28T23:45:25Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
tags: [ "GUI", "controls" ]
weight: 321
---

# Introduction

A la fin de ce chapitre, vous aurez :

- Compris l'organisation et la fonction de chaque section du panneau `Contrôles principaux`
- Approfondi vos connaissances sur les fonctionnalités d'ALS contrôlées par ces sections

---

# Présentation générale

Le panneau `Contrôles principaux` est situé à gauche de l'interface d'ALS. Il organise en sections les contrôles et
affichages les plus utilisés

<div class="row">
  <div class="col-md-8">

- [**Session**](#session-section)

  Cette section regroupe les contrôles de la session, l'affichage des informations sur la stack courante ainsi 
  que l'indicateur de statut de la session.

- [**Stack**](#stack-section)

  Cette section permet de définir le mode d'alignement et d'empilement des images. Elle propose aussi un réglage de seuil
  pour la recherche de similitudes pendant l'alignement.

- [**Serveur d'images**](#server-section)

  Permet de démarrer et arrêter le serveur d'images et affiche des informations sur le serveur lorsqu'il est actif.

- [**Enregistreur d'images**](#saver-section)

  Permet d'enregistrer à la volée l'image courante et d'activer la fonction d'enregistrement continu.

- [**Modules**](#modules-section)

  Cette section fournit des informations sur l'état d'utilisation des modules principaux d'ALS.

- [**Problèmes**](#issues-section)

  Cette section n'est visible que si le ` Journal de session` est caché. Elle affiche un indicateur de nouveaux problèmes

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="Le panneau des contrôles principaux" width="100%" alt="panneau contrôles principaux" >}}
  </div>
</div>

--- 

# Session {#session-section}

La section **session** du panneau comprend 3 zones, de haut en bas :

<div class="row">
<div class="col-md-8">

## Contrôles de session {#session-controls}

L'accessibilité de ces boutons dépend du statut de la session.

- `START` Démarre une nouvelle session ou redémarre la session mise en pause.
- `PAUSE` Met en pause la session en cours.
- `STOP` Arrête la session en cours.

  _Arrêter une session avec au moins une image dans la pile affiche une fenêtre de confirmation._

## Informations sur la stack courante

- le nombre total d'images empilées dans la stack courante.
- le temps d'exposition cumulé pour toute la session.

_Dans cet exemple, nous avons empilé 39 images pour un total de 2m 36s._

## Statut de la session

Le statut de la session en cours. Les statuts possibles sont :

- stoppée
- démarrée
- en pause

_Dans cet exemple, la session est démarrée_

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
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

# Stack {#stack-section}

La section **stack** du panneau contrôle le **module de stacking**.

L'alignement est débrayable et deux choix d'empilement sont disponibles

<div class="row">
<div class="col-md-8">

## Contrôles de la stack courante

_Ces contrôles sont accessibles uniquement quand la session est stoppée._

- Case à cocher `Aligner` : active l'**alignement** des nouvelles images sur la référence de la session.
- Liste déroulante des **modes d'empilement** : Définit le **mode d'empilement** utilisé pour cette session :
    - `moyenne` : La valeur de chaque pixel de l'image résultante est la moyenne des valeurs des pixels correspondants
      de chaque image de la stack courante.
    - `somme` : La valeur de chaque pixel de l'image résultante est la somme des valeurs des pixels correspondants de
      chaque image de la stack courante.

## Seuil de recherche de similitudes

Quand l'alignement est activé, ALS détermine les transformations à appliquer à chaque nouvelle image en se basant sur
une recherche de similitudes (**groupes de 3 étoiles**) entre celle-ci et la référence de la session.

Pour écarter les images de trop mauvaise qualité, ALS utilise un seuil de détection des similitudes : Toute image
présentant un nombre de similitudes inférieur à ce seuil sera ignorée.

Le curseur `Seuil` permet de définir ce seuil en temps réel.

- **Valeurs possibles** : 5 à 60.
- **Valeur par défaut** : 25.
- **Comportement lorsqu'une image est ignorée** :
    - L'image n'est pas ajoutée à la pile. ALS se met en attente de la prochaine image.
    - Un message est ajouté au `Journal de session`. Il porte, entre autre, le texte _Alignment matches count is lower
      than configured threshold_
    - Le bouton `Acquitter` du `Journal de session` est activé
    - Si le `journal de session` est caché, l'indicateur de nouveaux problèmes apparaît dans la section `Problèmes` du
      panneau.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="stack.png"
caption="La section stack"
width="294px"
height="92px"
alt="Section stack" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}

- `Aligner` est activé au démarrage d'ALS
- Le mode de stacking est réglé sur `moyenne` au démarrage d'ALS
- Le seuil de recherche de similitudes est conservé entre les démarrages d'ALS
  {{% /alert %}}

{{% alert title="💡 Astuce" color="light" %}}
Si le champ imagé par votre système contient peu d'étoiles, il peut être nécessaire de réduire le seuil pour éviter que
la majorité des images soient ignorées.
{{% /alert %}}

---

# Serveur d'images {#server-section}

La section **Serveur d'images** du panneau contrôle le serveur web intégré d'ALS.

<div class="row">
<div class="col-md-8">

## Contrôles du serveur

- `START` démarre le serveur
- `STOP` arrête le serveur

## Informations sur le serveur

Affiche le statut courant du serveur. Les statuts possibles sont :

- stoppé
- démarré

Quand le serveur est démarré :

- son URL est ajoutée au statut

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="server.png"
caption="La section server"
width="294px"
height="92px"
alt="Section server" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
Des paramètres supplémentaires pour le serveur web sont disponibles dans les [Préférences](../../preferences/).
Onglet **Sortie** section **Serveur web**.
{{% /alert %}}

---

# Enregistreur d'images {#saver-section}

La section **Enregistreur d'images** du panneau permet de déclencher des enregistrements supplémentaires au 
fonctionnement par défaut du module de sauvegarde

<div class="row">
<div class="col-md-8">

## Contrôles d'enregristrement

- Bouton `Enr. image courante` : Déclenche l'enregistrement de l'image de la zone centrale d'ALS dans un **nouveau**
  fichier du **dossier de travail** :
    - **nom du fichier** : Composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : En fonction du format d'enregistrement choisi dans
      les [Préférences](../../preferences/).

- Case à cocher `Enr. chaque image` : Active l'enregistrement de chaque prochain résultat de traitement dans un 
  **nouveau** fichier du **dossier de travail** :
    - **nom du fichier** : Composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : En fonction du format d'enregistrement choisi dans
      les [Préférences](../../preferences/).

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="saver.png"
caption="La section Enregistreur d'images"
width="294px"
height="69px"
alt="Section enregistreur d'images" >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
`Enr. chaque image` est désactivé au démarrage d'ALS.
{{% /alert %}}

---

# Modules {#modules-section}

La section **Modules** du panneau affiche les détails de chacun des modules principaux

- La taille de la file d'attente associée
- Le statut du module : Affiche **occupé** quand le module est en train de traiter une image

{{< center >}}
{{< figure src="modules.png"
caption="La section Modules"
width="294px"
height="153px"
alt="Section modules" >}}
{{< /center >}}

---

# Problèmes {#issues-section}

Quand un nouveau problème a été détecté par ALS **et que le `Journal de session` est caché**, un indicateur apparaît
tout en bas du panneau `contrôles principaux`

{{< center >}}
{{< figure src="problems.png"
caption="L'indicateur de nouveau problème"
width="294px"
height="44px"
alt="indicateur de nouveau problème" >}}
{{< /center >}}

Un click sur ce bouton affiche le `Journal de session` et permet de consulter les nouveaux problèmes détectés.

---

# Conclusion

Vous avez maintenant une vision claire de l'architecture d'ALS et des différentes sections du panneau
`contrôles principaux`.

Prochaine étape : le panneau `Traitements`
