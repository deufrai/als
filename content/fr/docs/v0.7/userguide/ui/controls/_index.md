---
title: "contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T02:35:04Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "interface", "contrôles", "stack", "session", "module" ]
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
    {{< figure src="controls.png" caption="Le panneau des contrôles principaux" width="100%" alt="Le panneau des contrôles principaux d'ALS, avec plusieurs sections : Contrôles de session avec les boutons START, PAUSE et STOP, Taille Stack 39, Exposition Stack 0:02:36, Statut démarrée ; Paramètres de la stack avec Aligner, moyenne, et curseur de seuil à 19 ; Serveur d'images avec les boutons START et STOP, Statut démarré avec l'URL http://10.0.2.15:8000 ; Enregistreur d'images avec les options Enr. image courante et Enr. chaque image ; Modules avec les statuts Taille file d'attente et Statut occupé ; Problèmes avec une icône d'avertissement et le label Problèmes." >}}
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
alt="Interface utilisateur de la section session montrant les boutons START, PAUSE et STOP. En dessous, des informations sur la session actuelle : Taille Stack 39, Exposition Stack 0:02:36, et statut démarrée." >}}
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
    - `moyenne` : La valeur de chaque pixel de l'empilement généré est la **valeur moyenne** de ce pixel dans toutes
      les images de la stack.
    - `somme` : La valeur de chaque pixel de l'empilement généré est la **somme** des valeurs de ce pixel dans toutes
      les images de la stack.

## Seuil de détection {#threshold}

Les images de mauvaise qualité sont écartées en utilisant un seuil de similitudes :

Toute image présentant un nombre de similitudes avec la référence de la session **inférieur** à ce seuil est ignorée.

Le curseur `Seuil` permet de définir ce seuil de détection.

**Comportement lorsqu'une image est ignorée** :

- L'image n'est pas ajoutée à la pile. Le module **Stack** se met en attente de la prochaine image.
- Un message **WARNING** est ajouté au `Journal de session`. Il porte, entre autre, le texte '_Alignment matches count
  is
  lower than configured threshold_'
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
alt="Interface utilisateur de la section stack montrant une case à cocher intitulée Aligner, cochée, et un menu déroulant avec l'option moyenne sélectionnée. En dessous, un curseur intitulé Seuil réglé à 19, positionné vers le côté gauche de sa plage." >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}

- `Aligner` est activé à chaque démarrage d'ALS
- Le mode de stacking est réglé sur `moyenne` à chaque démarrage d'ALS
- Le seuil de détection est global et sauvegardé en permanence
  {{% /alert %}}

{{% alert title="💡 Astuce" color="light" %}}
Réduire le seuil d'empilement est utile sur les prises de vues à longue focale où les étoiles sont peu nombreuses.
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
alt="La section serveur d'images, contenant les 2 boutons START (grisé) et STOP, le statut : démarré et l'URL du serveur" >}}
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

## Contrôles d'enregristrement {#save-controls}

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
alt="Section Enregistreur d'images de l'interface utilisateur montrant un bouton intitulé Enr. image courante et une case à cocher intitulée Enr. chaque image. La case à cocher est décochée." >}}
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
alt="Section Modules de l'interface utilisateur montrant un tableau avec trois colonnes : Modules, Taille file d'attente et Statut. Le tableau liste quatre modules : Pre-process, Stack, Process et Sauvegarde. La taille des files d'attente pour tous les modules est 0. Le statut du module Stack est occupé, tandis que les statuts des autres modules sont indiqués par un tiret (-)." >}}
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
alt="La session problèmes avec le bouton et son panneau rouge" >}}
{{< /center >}}

Un click sur ce bouton affiche le `Journal de session` et permet de consulter les nouveaux problèmes détectés.

---

# Conclusion

Vous avez maintenant une vision claire de l'architecture d'ALS et des différentes sections du panneau
`contrôles principaux`.

Prochaine étape : le panneau `Traitements`
