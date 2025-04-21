---
title: "Interface"
description: "Visite détaillée de la façade d'ALS"
author: "Équipe ALS"

lastmod: 2025-04-21T12:03:47Z
keywords: ["ALS GUI", "Interface ALS"]
type: "docs"
categories: ["utilisation"]
tags: [ "interface", "panneaux" ]
weight: 320
---

# Introduction

Dans ce chapitre, vous approfondirez vos connaissances sur l'utilisation d'ALS à travers son interface.

L'interface (UI) d'ALS a été conçue pour être intuitive et conviviale, vous permettant de vous concentrer sur votre
travail sans distraction inutile.

# Éléments principaux

L'interface d'ALS est composée de six éléments majeurs, chacun jouant un rôle clé dans l'ergonomie du logiciel.

{{% center %}}
{{% figure src="6_zones.png" 
alt="ALS Interface Layout" 
caption="ALS Interface Layout" 
width="1388" 
height="666" %}}
{{% /center %}}

Voici un aperçu de ces composants :

<div class="row">
  <div class="col-md-6">

- **1 : Menu Principal**  
  Permet d'accéder à toutes les fonctionnalités et réglages d'ALS.

  *Plus de détails dans la [documentation du Menu](menu).*

- **2 : Panneau Contrôles Principaux**  
  Situé à gauche par défaut, c'est votre panneau de contrôle quotidien.

  *Approfondissez dans la [documentation du panneau Contrôles Principaux](controls).*

- **3 : Zone Centrale**  
  Affiche l'image résultante des processus d'empilement et de traitement.

  *La navigation dans l'image est expliquée dans la [page de démarrage rapide](../../quickstart#explore).*

</div>
<div class="col-md-6">

- **4 : Panneau Traitements**  
  Situé sur le côté droit, ce panneau vous permet d'affiner vos images avec divers outils de traitement.

  *Explorez les détails dans la [documentation du panneau Traitements](processing).*

- **5 : Panneau Journal de Session**  
  Placé en bas, ce panneau vous aide à surveiller l'évolution et à suivre les événements ou problèmes pendant la
  session.

  *Découvrez-en plus dans la [documentation du Journal de Session](log).*

</div>
</div>

---

- **6 : Barre d'état**

  Située en bas de l'interface, la barre d'état fournit des mises à jour en temps réel sur l'état du système.

  Elle se divise en plusieurs étiquettes :
    - **Astuces** : Affiche des conseils ou des informations utiles sur l'élément de l'interface actuellement survolé.
    - **État de la Session** : Reflète l'état d'activité de la session.
    - **Profil Actif** : Indique le nom du profil actuellement utilisé.
    - **État du Scanner** : Affiche si le scanner est actif ou arrêté et indique le chemin du dossier de scan en cours.
    - **Taille du Stack** : Indique le nombre d'images présentes dans le stack.
    - **Temps d'Exposition Total du Stack** : Affiche le temps d'exposition cumulé des images empilées.
    - **État du Serveur Web** : Affiche l'état opérationnel du serveur web intégré.
    - **Temps de Traitement Total des Images** : Fournit le temps de traitement de la dernière image.

---

# Eléments communs

Certains éléments de l'interface ont des comportements particuliers qui peuvent être utiles dans votre
travail quotidien.

## Panneaux

Les panneaux d'ALS offrent une interface flexible qui peut s'adapter à différents flux de travail.

Par défaut :

- Le panneau `Contrôles Principaux` est ancré sur le côté gauche de la fenêtre principale.
- Le panneau `Traitements` est ancré sur le côté droit.
- Le panneau `Journal de Session` est ancré en bas.

### Déplacement des Panneaux

Les panneaux peuvent être ancrés dans des zones spécifiques de la fenêtre principale ou détachés pour devenir
indépendants.

Ces panneaux indépendants peuvent être librement positionnés dans la zone d'affichage, même sur plusieurs écrans.

#### Mode ancré

- Cliquez sur la **barre de titre** du panneau et faites-le glisser vers une zone d’ancrage valide :
    - Les panneaux `Contrôles Principaux` et `Traitements` peuvent être ancrés à gauche ou à droite.
    - Le panneau `Journal de Session` peut être ancré en haut ou en bas.
  - Lorsque vous approchez une zone d’ancrage valide, des **indicateurs visuels** apparaissent pour vous guider.
  - Relâchez le clic pour fixer le panneau à l’emplacement choisi.

#### Mode flottant
  - Cliquez sur la **barre de titre** du panneau que vous souhaitez déplacer.
- Maintenez le clic et faites glisser le panneau à l’emplacement souhaité, puis relâchez le clic.
  - Le panneau reste flottant et indépendant de la fenêtre principale.

Un panneau flottant peut être ré-ancré à sa position par défaut en double-cliquant sur sa barre de titre.

---

## Curseurs

Les **curseurs** d'ALS permettent de régler divers paramètres de manière intuitive.

Voici les différentes façons d'interagir avec eux :

### Glisser la Poignée

La manière la plus simple de modifier une valeur :

- Cliquez sur la poignée du curseur avec votre souris.
- Maintenez le clic et glissez la poignée vers la gauche pour diminuer la valeur ou vers la droite pour l’augmenter.
- Relâchez le clic une fois la valeur souhaitée atteinte.

### Utiliser la Molette de la Souris

Si vous utilisez une souris avec molette, cela permet des ajustements précis :

- Placez le curseur de la souris sur la poignée ou la barre.
- Faites tourner la molette vers le haut pour augmenter la valeur ou vers le bas pour la diminuer.

### Cliquer sur la Barre

En cliquant directement sur la barre du curseur, vous pouvez ajuster la valeur associée par des incréments plus
importants comparés à l'utilisation de la molette :

- La poignée du curseur se déplace en conséquence sans se positionner directement à l'endroit du clic.

{{% alert color="info" %}}
ℹ️ Certains curseurs disposent de comportements supplémentaires expliqués dans la documentation des panneaux où ils se
trouvent.
{{% /alert %}}
