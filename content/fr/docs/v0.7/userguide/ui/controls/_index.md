---
title: "contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T21:07:16Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
categories: ["configuration", "utilisation"]
tags: [ "stack", "session", "serveur", "sortie", "seuil", "enregistrement", "problèmes" ]
weight: 321
---

# Introduction

A la fin de ce chapitre, vous aurez :

- Compris l'organisation et la fonction de chaque section du panneau `Contrôles principaux`
- Approfondi vos connaissances sur les fonctionnalités d'ALS contrôlées par ces sections

<div class="row">
  <div class="col-md-8">

# Présentation

Le panneau `Contrôles principaux` est situé à gauche de l'interface d'ALS

Il organise en sections les contrôles et affichages les plus utilisés

- [**Session**](#session-section)

  Contrôles de session, informations sur la stack et le statut de la session

- [**Stack**](#stack-section)

  Réglages du stacking : Alignement, mode d'empilement et seuil de détection

- [**Serveur d'images**](#server-section)

  Contrôles et statut du serveur d'images

- [**Enregistreur d'images**](#saver-section)

  Outils d'enregistrement d'images

- [**Modules**](#modules-section)

  Informations sur l'état d'utilisation des modules principaux

- [**Problèmes**](#issues-section)

  Indicateur de problèmes

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="Le panneau des contrôles principaux" width="100%" alt="Le panneau des contrôles principaux d'ALS, avec plusieurs sections : Contrôles de session avec les boutons START, PAUSE et STOP, Taille Stack 39, Exposition Stack 0:02:36, Statut démarrée ; Paramètres de la stack avec Aligner, moyenne, et curseur de seuil à 19 ; Serveur d'images avec les boutons START et STOP, Statut démarré avec l'URL http://10.0.2.15:8000 ; Enregistreur d'images avec les options Enr. image courante et Enr. chaque image ; Modules avec les statuts Taille file d'attente et Statut occupé ; Problèmes avec une icône d'avertissement et le label Problèmes." >}}
  </div>

</div>

--- 

# Session {#session-section}

La section **session** du panneau comprend 3 zones :

<div class="row">
<div class="col-md-8">

## Contrôles de session {#session-controls}

- <span class="als-ks">R</span> ou 🖱️ cliquez `START` pour démarrer une nouvelle session ou reprendre 
  une session mise en pause.
- <span class="als-ks">R</span> ou 🖱️ cliquez `PAUSE` pour mettre en pause la session en cours.
- <span class="als-ks">X</span> ou 🖱️ cliquez `STOP` pour arrêter la session en cours.

{{% alert color="info" %}}
ℹ️ Arrêter une session avec au moins une brute dans la **stack** affiche une demande de confirmation
{{% /alert %}}

## Informations sur la stack

Sous les contrôles de session, vous trouverez les informations sur la **stack** :

- le nombre de brutes actuellement dans la **stack**
- le cumul des temps d'expositions des brutes de la **stack**.

_Dans cet exemple, nous avons empilé 39 brutes pour un total de 2m 36s._

## Statut de la session

Enfin, Le statut de la session en cours

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

La section **stack** du panneau contrôle le module **Stacker**.

<div class="row">
<div class="col-md-8">

## Alignement et mode d'empilement {#controls}

{{% alert color="info" %}}
ℹ️ Ces contrôles sont accessibles uniquement quand la session est stoppée.
{{% /alert %}}
- <span class="als-ks">A</span> ou 🖱️ cochez `Aligner` pour activer l'**alignement** des brutes

- Utilisez la liste déroulante pour définir le **mode d'empilement** à utiliser :
    - `moyenne`

      Utilisé pour le visuel assisté ou la surveillance d'une série d'acquisitions 

      ⚙️ _La valeur de chaque pixel de l'empilement généré est la **valeur moyenne** de ce pixel sur toutes
      les brutes de la **stack**_.

    - `somme`

      Utilisé pour réaliser des filés d'étoiles ou des images circum-polaires

      ⚙️ _La valeur de chaque pixel de l'empilement généré est la **somme** des valeurs de ce pixel sur toutes
      les brutes de la **stack**_.

## Seuil de détection {#threshold}

L'alignement fonctionne en comparant les brutes avec la **référence d'alignement**, à la recherche de groupes 
d'étoiles similaires. 

Les brutes de mauvaise qualité, présentant des étoiles top peu nombreuses ou déformées, sont écartées en utilisant un 
seuil :

Toute brute présentant un nombre de similitudes **inférieur** à ce seuil est abandonnée.

🖱️ Utilisez le curseur `Seuil` pour modifier la valeur de ce **seuil de détection**

**Quand une brute est abandonnée** :

- L'image n'est pas ajoutée à la pile et le module **Stacker** se met en attente de la prochaine brute.
- Un **WARNING** est ajouté au **Journal de session**. Il porte le texte '_Alignment matches count
  is lower than configured threshold_'
- Le bouton `Acquitter` du panneau `Journal de session` est activé
  
  _Si le panneau_ `journal de session` _est caché, l'indicateur de problèmes apparaît dans la section_ **Problèmes**

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

{{% alert title="💡" color="light" %}}
- Cherchez à régler le seuil de détection le plus haut possible, sans provoquer d'abandons de brutes
- Réduire le seuil d'empilement est utile sur les prises de vues à longue focale où les étoiles sont peu nombreuses
{{% /alert %}}

{{% alert title="ℹ️" color="info" %}}
- L'alignement est activé à chaque démarrage d'ALS
- Le mode de stacking est réglé sur **moyenne** à chaque démarrage d'ALS
- Le seuil de détection est global et sauvegardé en permanence
{{% /alert %}}


---

# Serveur d'images {#server-section}

La section **Serveur d'images** du panneau contrôle le module **Server**

<div class="row">
<div class="col-md-8">

## Contrôles du serveur

- <span class="als-ks">W</span> ou 🖱️ cliquez `START` pour démarrer le serveur
- <span class="als-ks">W</span> ou 🖱️ cliquez `STOP` pour arrêter le serveur

## Informations sur le serveur

Sous les contrôles du serveur, vous trouverez l'affichage de son statut

Quand le serveur est **démarré** :
- son URL est ajoutée au statut
- <span class="als-ks">Q</span> bascule l'affichaque du QR code pour l'URL du serveur 

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

{{% alert title="ℹ️" color="info" %}}
Des paramètres supplémentaires pour le serveur web sont disponibles dans les [Préférences](../../preferences/).
{{% /alert %}}

---

# Enregistreur d'images {#saver-section}

La section **Enregistreur d'images** du panneau permet de déclencher des enregistrements supplémentaires au
fonctionnement par défaut du module **Save**

<div class="row">
<div class="col-md-8">

## Contrôles d'enregristrement {#save-controls}

- <span class="als-ks">S</span> ou 🖱️ cliquez `Enr. image courante` pour enregistrer le **dernier** 
  résultat de traitement avec horodatage
- <span class="als-ks">F</span> ou 🖱️ cochez `Enr. chaque image` pour activer l'enregistrement de **chaque prochain** 
  résultat de traitement avec horodatage

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

Quand un nouveau problème a été détecté **et que le `Journal de session` est caché**, le bouton `Problèmes`
apparaît dans cette section.

{{< center >}}
{{< figure src="problems.png"
caption="L'indicateur de problème"
width="294px"
height="44px"
alt="La section problèmes avec le bouton problèmes et son panneau rouge" >}}
{{< /center >}}

<span class="als-ks">L</span> ou 🖱️ cliquez `Problèmes` pour afficher le `Journal de session` et consulter 
les nouveaux problèmes détectés.

---

# Conclusion

Les contrôles principaux d'ALS n'ont plus de secret pour vous ! 

Prochaine étape : le panneau `Traitements`
