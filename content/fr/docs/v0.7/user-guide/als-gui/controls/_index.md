---
title: "Le panneau contrôles principaux"
description: "documentation du panneau des contrôles principaux d'ALS"
author: "ALS Team"
lastmod: 2024-12-27T08:26:24Z
keywords: [ "controles principaux d'ALS" ]
type: "docs"
tags: [ "GUI", "controls" ]
weight: 321
---

# Introduction

A la fin de ce chapitre, vous aurez :

- Compris l'organisation et la fonction de chaque section du panneau des contrôles principaux
- Approfondi vos connaissances sur les fonctionnalités d'ALS contrôlées par ces sections

---

# Présentation générale

Le panneau `Contrôles principaux` est situé à gauche de l'interface d'ALS. Il regroupe les contrôles et affichages
les plus utilisés en sections

<div class="row">
  <div class="col-md-8">

- **Session**

Les contrôles de la session en cours se trouvent ici. Ils permettent de démarrer et d'arrêter la session, et affichent
également les informations sur la stack courante ainsi que l'indicateur d'état de la session.

- **Stack**

Cette section permet de définir le mode d'alignement et d'empilement des images. Elle propose aussi un réglage de seuil
pour la recherche de similitudes pendant l'alignement.

- **Serveur d'images**

Permet de démarrer et arrêter le serveur d'images et affiche des informations sur le serveur lorsqu'il est actif.

- **Enregistreur d'images**

Permet d'enregistrer à la volée l'image courante et d'activer la fonction d'enregistrement continu.

- **Modules**

Cette section fournit des informations sur l'état d'utilisation de chaque module.

- **Problèmes**

Cette section n'est visible que si le ` Journal de session` est caché. Elle affiche un indicateur de nouveaux problèmes

  </div>
  <div class="col-md-4 d-flex align-items-center justify-content-center">
    {{< figure src="controls.png" caption="Le panneau des contrôles principaux" width="100%" alt="Menu fichier" >}}
  </div>
</div>

--- 

# Session

La section **session** du panneau comprend 3 zones, de haut en bas :

<div class="row">
<div class="col-md-8">

## Contrôles de session

L'accessibilité de ces boutons dépend du statut de la session.

- `START` Démarre une nouvelle session ou reprend la session mise en pause.
- `PAUSE` Met en pause la session en cours.
- `STOP` Arrête la session en cours.

  Arrêter une session avec au moins une image dans la pile déclenche une fenêtre de confirmation.

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

# Stack

La section **stack** du panneau permet de contrôler le **module de stacking**.

Ce module est en charge de l'alignement et de l'empilement des images brutes.
L'alignement est débrayable et deux choix d'empilement sont disponibles

<div class="row">
<div class="col-md-8">

## Contrôles de la stack courante

_Ces contrôles sont accessibles uniquement quand la session est stoppée._

- Case à cocher `Aligner` : active l'**alignement** des images sur la référence de la session.
- Liste déroulante des **modes d'empilement** : Permet de définir le **mode d'empilement** utilisé pour cette session :
    - `moyenne` : chaque pixel de l'image résultante est la moyenne des pixels correspondants de chaque image de la
      stack courante.
    - `somme` : chaque pixel de l'image résultante est la somme des pixels correspondants de chaque image de la stack
      courante.

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
Si le champ imagé par votre système contient peu d'étoiles, il peut être nécessaire de réduire le seuil pour éviter que
la majorité des images soient ignorées.
{{% /alert %}}

---

# Serveur d'images

La section **Serveur d'images** du panneau permet de contrôler le serveur web intégré d'ALS.

Ce serveur partage l'image affichée dans la zone centrale d'ALS sur le réseau auquel la machine qui exécute
ALS est connectée.

L'image affichée dans la page web servie est rafraîchie périodiquement par le navigateur.

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
Des paramètres supplémentaires pour le serveur web sont disponibles dans les [Préférences d'ALS](../../preferences/).
Onglet **Sortie** section **Serveur web**.
{{% /alert %}}

---

# Enregistreur d'images

La section **Enregistreur d'images** du panneau permet de contrôler l'enregistrement des images prduites par ALS.

Après le traitement complet de chaque nouvelle image, ALS enregistre l'image de la zone centrale dans un fichier du
**dossier de travail** :

- **nom du fichier** : **stack_image**

  Le fichier est écrasé à chaque nouvelle image.

- **Type et extension du fichier** : en fonction du format d'enregistrement choisi dans
  les [Préférences d'ALS](../../preferences/).

  Par défaut : format **JPEG** et extension **.jpg**.

Les contrôles d'enregistrement permettent de déclencher d'autres enregistrements

<div class="row">
<div class="col-md-8">

## Contrôles d'enregristrement

- Bouton `Enr. image courante` : Déclenche l'enregistrement de l'image de la zone centrale d'ALS dans un nouveau
  fichier du **dossier de travail** :
    - **nom du fichier** : composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : en fonction du format d'enregistrement choisi dans
      les [Préférences d'ALS](../../preferences/).

- Case à cocher `Enr. chaque image` : Active l'enregistrement de chaque prochain résultat de traitement dans un nouveau
  fichier du **dossier de travail** :
    - **nom du fichier** : composé de **stack_image** et d'un suffixe d'horodatage
    - **Type et extension du fichier** : en fonction du format d'enregistrement choisi dans
      les [Préférences d'ALS](../../preferences/).

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
Un exemple de nom de fichier horodaté : **stack_image-2024-12-27-06-20-24-091899.jpg**.
{{% /alert %}}

---

# Modules

Cette section est l'occasion de mieux décrire l'architecture d'ALS et le cheminement des images dans l'application.

## Architecture des modules

Tous les traitements appliqués aux images sont répartis dans 4 modules principaux.

Chaque module se voit assigner une file d'attente et traite séquentiellement toutes les images dans sa file d'attente.

Chaque module place ses résultats de traitement successifs dans la file d'attente du module suivant.

Les modules sont organisés dans cet ordre :

### Pre-process

Dès qu'une nouvelle image est détectée dans le **dossier scanné**, elle est ajoutée à la file d'attente de ce module.

Le module de **pre-process** applique sur chaque image les pré-traitements habituels en astrophoto :
- **Suppression des pixels chauds** : Remplace la valeur des pixels chauds par la valeur moyenne des pixels voisins.
  Ce traitement est debrayable dans les [Préférences d'ALS](../../preferences/).
- **Soustraction de master dark** : Utilise un master dark fourni par l'utilisateur pour soustraire le bruit thermique
  de l'image. Le chemin du master dark et l'activation de ce traitement sont définis dans les
  [Préférences d'ALS](../../preferences/).

  Si le format de données du master dark fourni n'est pas le même que celui de l'image à traiter, ALS effectue une
  conversion automatique du master dark avant la soustraction.

- **Dématriçage** : Dans le cas d'une image couleur enregistrée dans un fichier FITS ou Raw, convertit l'image en
  couleur RVB en utilisant la matrice de Bayer décrite dans les entêtes du fichier.

  <details>
    <summary>Cliquer ici pour des détails sur les entêtes utilisés</summary>

    - Fichier FITS : Entête FITS standard **BAYERPAT**
    - Fichier Raw : Entête EXIF standard

  </details>

  Une option des [Préférences d'ALS](../../preferences/) permet de laisser ALS choisir ou de définir explicitement
  la matrice de Bayer à utiliser. Cette option est utile si ALS ne détecte pas correctement la matrice à utiliser
  ou si le fichier ne contient pas l'entête recherché.

### Stack

Prend en charge l'alignement et l'empilement des images

- **Alignement**
    - calcul des transformations à appliquer à l'image courante pour l'aligner sur la référence de la session
    - application des transformations à l'image courante
- **Empilement**
    - Ajout de l'image courante à la stack courante
    - calcul de l'image résultante en fonction du mode d'empilement choisi

Le fonctionnement détaillé de ces traitements a été abordé dans la section **Stack**.

### Process

Module de post-traitement. Il comprend les traitements suivants :

- **Auto-stretch** : Ajuste automatiquement les niveaux de l'image pour maximiser le contraste
- **Réglages d'exposition** : Permet de régler les niveaux de noir, de blanc et le niveau de gris moyen de l'image
- **Balance RVB** : Permet de régler la balance des couleurs de l'image

Les détails de ces traitements seront abordés dans la page consacrée au panneau **Traitements**.

### Sauvegarde

Module d'enregistrement des images.

Le fonctionnement détaillé de l'enregistreur d'images a été décrit dans la section **Enregistreur d'images**.

## Affichage des modules

La section **Modules** du panneau affiche pour chaque module :

- La taille de la file d'attente associée
- L'état d'utilisation du module

  Affiche **occupé** quand le module est en train de traiter une image

{{< center >}}
{{< figure src="modules.png"
caption="La section Modules"
width="294px"
height="153px"
alt="Section modules" >}}
{{< /center >}}

---

# Problèmes

Quand un nouveau problème a été détecté par ALS **et que le `Journal de session` est caché**, un indicateur apparaît tout
en bas du panneau `contrôles principaux`

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
