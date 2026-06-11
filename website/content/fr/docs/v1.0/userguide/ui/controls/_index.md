---
title: "contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2026-06-11T00:33:39Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
categories: ["utilisation", "configuration"]
tags: [ "module", "stack", "session", "serveur d’images", "sorties", "correspondances minimales", "rejet sigma", "save", "problèmes", "panneaux" ]
weight: 100321
---

# Introduction

Au cours de ce chapitre, vous allez :
- vous familiariser avec les contrôles principaux d'ALS
- approfondir vos connaissances sur les fonctionnalités clés

# Vue d'ensemble

<div class="row">
  <div class="col-md-8">

Le poste de commande d'ALS est le panneau d'interface `Contrôles principaux`

Situé à gauche de l'interface d'ALS, il organise les contrôles et affichages les plus utilisés en sections :

- [**Session**](#session-section)

  Contrôles et statut de la session

- [**Stack**](#stack-section)

  Contrôles du stacking et informations sur la stack

- [**Serveur d'images**](#server-section)

  Contrôles et statut du serveur d'images

- [**Enregistreur d'images**](#saver-section)

  Outils d'enregistrement d'images

- [**Modules**](#modules-section)

  Informations sur l'état d'utilisation des modules principaux

- [**Mise à jour disponible**](#available-update)

  Notification lorsqu'une nouvelle version d'ALS est disponible

- [**Problèmes**](#issues-section)

  Indicateur de problèmes

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
  
{{< figure src="controls.png" 
caption="Le panneau des contrôles principaux" 
width="313px"
height="684px"
alt="Le panneau des contrôles principaux d'ALS, avec plusieurs sections : contrôles de session avec les boutons START, PAUSE et STOP et le statut démarrée ; paramètres de la stack avec Aligner, moyenne et Corresp. min. réglé à 25 ; taille de la stack 42 et exposition 2:06:00 ; serveur d'images démarré ; enregistreur d'images ; modules ; disponibilité d'ALS 1.0 et bouton Problèmes." >}}
</div>

</div>

--- 

# Session {#session-section}

La section **session** du panneau comprend 2 zones :

<div class="row">
<div class="col-md-8">

## Contrôles de session {#session-controls}

- {{< als-ks >}}R{{< /als-ks >}} ou 🖱️ cliquez `START` pour :
  - **démarrer** une nouvelle session
  - **reprendre** une session mise en **pause**
- {{< als-ks >}}R{{< /als-ks >}} ou 🖱️ cliquez `PAUSE` pour mettre en **pause** une session **démarrée**.
- {{< als-ks >}}X{{< /als-ks >}} ou 🖱️ cliquez `STOP` pour **arrêter** une session **démarrée**.

{{% alert color="info" %}}
ℹ️ Arrêter une session avec au moins une brute dans la **stack** affiche une demande de confirmation
{{% /alert %}}


## Statut de la session

Enfin, Le statut de la session en cours

_Dans cet exemple, la session est démarrée_

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="session.png"
caption="La section session"
width="313px"
height="101px"
alt="Interface utilisateur de la section session montrant les boutons START, PAUSE et STOP et le statut démarrée." >}}
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
- {{< als-ks >}}A{{< /als-ks >}} ou 🖱️ cochez `Aligner` pour activer l'**alignement** des brutes

- Utilisez la liste déroulante pour définir le **mode d'empilement** à utiliser :
    - `moyenne`

      Utilisé pour le visuel assisté ou la surveillance d'une série d'acquisitions

      ⚙️ _La valeur de chaque pixel de l'empilement généré est la **valeur moyenne** de ce pixel sur toutes
      les brutes de la **stack**_.

      ℹ️ _Les valeurs aberrantes sont rejetées automatiquement dès que au moins **5** brutes sont présentes dans la stack
      et le profil **Astrophoto** est utilisé._

    - `somme`

      Utilisé pour réaliser des filés d'étoiles ou des images circum-polaires

      ⚙️ _La valeur de chaque pixel de l'empilement généré est la **somme des valeurs** de ce pixel sur toutes
      les brutes de la **stack**_.

## Correspondances minimales {#threshold}

L'alignement fonctionne en comparant chaque brute avec la **référence d'alignement**, à la recherche de groupes
d'étoiles correspondants.

Les brutes de mauvaise qualité, présentant des étoiles trop peu nombreuses ou déformées, peuvent ne pas produire assez
de correspondances pour être alignées de manière fiable.

Toute brute présentant moins de correspondances que le minimum configuré est abandonnée.

- 🖱️ Utilisez le curseur `Corresp. min.` pour modifier le **nombre minimal de correspondances** requis.

**Quand une brute est abandonnée** :

- L'image n'est pas ajoutée à la pile et le module **Stacker** se met en attente de la prochaine brute.
- Un **WARNING** est ajouté au **Journal de session**. Il porte le texte '_Alignment match count
  is lower than configured minimum_'
- Le bouton `Acquitter` du panneau `Journal de session` est activé
  
  _Si le panneau_ `journal de session` _est caché, l'indicateur de problèmes apparaît dans la section_ **Problèmes**

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="stack.png"
caption="La section stack"
width="313px"
height="169px"
alt="Interface utilisateur de la section stack montrant la case Aligner cochée, le mode moyenne, le curseur Corresp. min. réglé à 25, une taille de stack de 42 et une exposition de 2:06:00." >}}
{{< /center >}}

</div>
</div>

{{% alert title="💡" color="light" %}}
- Cherchez à régler le nombre minimal de correspondances le plus haut possible, sans provoquer d'abandons de brutes
- Réduire le nombre minimal de correspondances est utile sur les prises de vues à longue focale où les étoiles sont peu
  nombreuses
{{% /alert %}}

{{% alert title="ℹ️" color="info" %}}
- L'alignement est activé à chaque démarrage d'ALS
- Le mode de stacking est réglé sur **moyenne** à chaque démarrage d'ALS
- Le nombre minimal de correspondances est global et sauvegardé en permanence
{{% /alert %}}

## Informations sur la stack

À droite des contrôles d'alignement et des correspondances minimales, vous trouverez les informations sur la **stack** :

- le nombre de brutes actuellement dans la **stack**
- le cumul des temps d'expositions des brutes de la **stack**.

_Dans cet exemple, nous avons empilé 42 brutes pour un total de 2 h 6 min._


---

# Serveur d'images {#server-section}

La section **Serveur d'images** du panneau contrôle le module **Server**

<div class="row">
<div class="col-md-8">

## Contrôles du serveur

- {{< als-ks >}}W{{< /als-ks >}} ou 🖱️ cliquez `START` pour démarrer le serveur
- {{< als-ks >}}W{{< /als-ks >}} ou 🖱️ cliquez `STOP` pour arrêter le serveur

## Informations sur le serveur

Sous les contrôles du serveur, vous trouverez l'affichage de son statut

Quand le serveur est **démarré** :
- l'URL construite à partir de l'adresse affichée et du port configurés dans les
  [Préférences](../../preferences/output/#server) est ajoutée au statut
- {{< als-ks >}}Q{{< /als-ks >}} bascule l'affichaque du QR code pour l'URL du serveur 

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="server.png"
caption="La section server"
width="313px"
height="100px"
alt="La section serveur d'images, contenant les 2 boutons START (grisé) et STOP, le statut : démarré et l'URL du serveur" >}}
{{< /center >}}

</div>
</div>

---

# Enregistreur d'images {#saver-section}

La section **Enregistreur d'images** du panneau permet de déclencher des enregistrements supplémentaires au
fonctionnement par défaut du module **Save**

<div class="row">
<div class="col-md-8">

## Contrôles d'enregristrement {#save-controls}

- {{< als-ks >}}S{{< /als-ks >}} ou 🖱️ cliquez `Enr. image courante` pour enregistrer le **dernier** 
  résultat de traitement avec horodatage
- {{< als-ks >}}F{{< /als-ks >}} ou 🖱️ cochez `Enr. chaque image` pour activer l'enregistrement de **chaque prochain** 
  résultat de traitement avec horodatage

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="saver.png"
caption="La section Enregistreur d'images"
width="313px"
height="79px"
alt="Section Enregistreur d'images de l'interface utilisateur montrant un bouton intitulé Enr. image courante et une case à cocher intitulée Enr. chaque image. La case à cocher est décochée." >}}
{{< /center >}}

</div>
</div>

{{% alert title="ℹ️ INFO" color="info" %}}
`Enr. chaque image` est désactivée au démarrage d'ALS.
{{% /alert %}}

---

<div class="row">
  <div class="col-md-8">

# Modules {#modules-section}

La section **Modules** du panneau affiche les détails de chacun des modules principaux

- La taille de la file d'attente associée
- Le statut du module : Affiche **occupé** quand le module est en train de traiter une image

---

# Mise à jour disponible {#available-update}

Quand `Rechercher les mises à jour au démarrage` est activé dans les
[préférences générales](../../preferences/general/), ALS recherche une nouvelle version disponible après son démarrage.

Si une nouvelle version est disponible, le label `ALS version est disponible` apparaît sous la section **Modules**,
où `version` est le numéro de la version disponible.

---

# Problèmes {#issues-section}

Quand un nouveau problème a été détecté **et que le `Journal de session` est caché**, le bouton `Problèmes`
apparaît dans cette section.

{{< als-ks >}}L{{< /als-ks >}} ou 🖱️ cliquez `Problèmes` pour afficher le `Journal de session` et consulter
les nouveaux problèmes détectés.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">

{{< center >}}
{{< figure src="modules_and_below.png"
caption="Modules, mise à jour disponible et problèmes"
width="313px"
height="230px"
alt="Les sections Modules, Mise à jour disponible et Problèmes. Les files d'attente sont vides, le module Process est occupé, ALS 1.0 est disponible et le bouton Problèmes est affiché." >}}
{{< /center >}}

  </div>
</div>

---

# Conclusion

Les contrôles principaux d'ALS n'ont plus de secret pour vous ! 

Prochaine étape : Le panneau Traitements
