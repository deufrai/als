---
title: "contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T05:21:00Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "interface", "contrôles", "session", "module" ]
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

  Cette section permet de définir le mode d'alignement et d'empilement des images. Elle propose aussi un réglage de
  seuil
  pour la recherche de similitudes pendant l'alignement.

- [**Serveur d'images**](#server-section)

  Permet de démarrer et arrêter le serveur d'images et affiche des informations sur le serveur lorsqu'il est actif.

- [**Enregistreur d'images**](#saver-section)

  Permet d'enregistrer à la volée l'image courante et d'activer la fonction d'enregistrement continu.

- [**Modules**](#modules-section)

  Cette section fournit des informations sur l'état d'utilisation des modules principaux d'ALS.

- [**Problèmes**](#issues-section)

  Cette section n'est visible que si le ` Journal de session` est caché. Elle affiche un indicateur de nouveaux
  problèmes

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

La section **stack** du panneau contrôle le module **Stack**.

<div class="row">
<div class="col-md-8">

## Alignement et mode d'empilement {#controls}

{{% alert color="info" %}}
ℹ️ Ces contrôles sont accessibles uniquement quand la session est stoppée.
{{% /alert %}}

- `Aligner` active l'**alignement** des brutes sur la référence de la session.
- La liste déroulante définit le **mode d'empilement** utilisé pour cette session :
    - `moyenne` : La valeur de chaque pixel de l'image résultante est la moyenne des valeurs des pixels correspondants
      de chaque image de la stack courante.
    - `somme` : La valeur de chaque pixel de l'image résultante est la somme des valeurs des pixels correspondants de
      chaque image de la stack courante.

## Seuil de détection {#threshold}

Pour procéder à l'alignement, ALS recherche les similitudes (**groupes de 3 étoiles**) entre la brute
et la référence de la session.

Les images de trop mauvaise qualité sont écartés en utilisant un seuil : Toute image présentant un nombre de similitudes
**inférieur** à ce seuil sera ignorée.

Le curseur `Seuil` permet de définir ce seuil en temps réel.

**Comportement lorsqu'une image est ignorée** :

- L'image n'est pas ajoutée à la pile. Le module **Stack** se met en attente de la prochaine image.
- Un message **WARNING** est ajouté au `Journal de session`. Il porte, entre autre, le texte _Alignment matches count is
  lower than configured threshold_
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

- `Aligner` est activé à chaque démarrage d'ALS
- Le mode de stacking est réglé sur `moyenne` à chaque démarrage d'ALS
- Le seuil de détection est global et sauvegardé en permanence
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
fonctionnement par défaut du module **Save**

<div class="row">
<div class="col-md-8">

## Contrôles d'enregristrement

- `Enr. image courante` déclenche l'enregistrement de la **dernière image** sortie du module **Process** dans
  un nouveau fichier horodaté :
    - **emplacement du fichier** : **dossier de travail**
    - **nom du fichier** : Composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : Tel que défini dans les [Préférences](../../preferences/output/#format).

- `Enr. chaque image` active l'enregistrement de **chaque image** sortie du module **Process** dans un
  nouveau fichier horodaté :
    - **emplacement du fichier** : **dossier de travail**
    - **nom du fichier** : Composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : Tel que défini dans les [Préférences](../../preferences/output/#format).

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
`Enr. chaque image` est désactivée au démarrage d'ALS.
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
