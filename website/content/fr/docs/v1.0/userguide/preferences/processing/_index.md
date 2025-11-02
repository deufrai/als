---
title: "Onglet Traitement"
description: "Documentation de l'onglet Traitement des préférences d'ALS"
author: "ALS Team"
lastmod: 2025-11-02T19:02:52Z
keywords: ["ALS processing settings", "préférences traitement ALS"]
draft: false
type: "docs"
categories: ["configuration"]
tags: ["traitement", "dématriçage", "dark", "pixels chauds", "calibration"]
weight: 332
---

Les réglages des traitements d'ALS sont présentés dans l'onglet `Traitement`

<div class="row">
<div class="col-md-6">

# Vue d'ensemble

Cet onglet ne contient qu'une seule section : [Preprocess](#preprocess)

Elle regroupe les réglages des tâches de **calibration** :
- [Suppression des pixels chauds](#hot-remove)
- [Soustraction de dark](#dark-remove)
- [Dématriçage](#debayer)

</div>
<div class="col-md-6 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Traitement des préférences"
width="622px"
height="604px"
alt="Fenêtre de préférences ALS avec l'onglet Traitement sélectionné, affichant les paramètres de prétraitement des images, y compris les options de suppression des pixels chauds, de soustraction dark et de motif de dématriçage, avec chemins spécifiés et boutons Modifier et Effacer." >}}
{{< /center >}}

</div>
</div>

# Preprocess {#preprocess}

{{% alert color="info" %}}
ℹ️ Ces paramètres ne sont accessibles que quand la session est stoppée
{{% /alert %}}

## Suppression des pixels chauds {#hot-remove}

{{< center >}}
{{< figure src="hot_remove.png"
caption="Réglages de suppression des pixels chauds"
width="622px"
height="217px"
alt="" >}}
{{< /center >}}

- 🖱️ Cochez `Supprimer` pour activer la suppression des pixels chauds

ℹ️ Par défaut : OFF

## Soustraction de dark {#dark-remove}

{{< center >}}
{{< figure src="dark_remove.png"
caption="Réglages de soustraction de dark"
width="622px"
height="196px"
alt="Interface logicielle affichant les options pour utiliser la soustraction de dark, changer le chemin du master dark spécifié et effacer le chemin." >}}
{{< /center >}}

- 🖱️ Cochez `Active` pour activer la soustraction de dark
- 🖱️ Cliquez `Master dark...` pour choisir le fichier master dark à utiliser pour la soustraction

  le chemin du master dark configuré est affiché à droite du bouton
- 🖱️ Cliquez `Vider` pour vider le chemin du fichier master dark

{{% alert color="warning" %}}
⚠️ Le master dark **doit avoir les mêmes dimensions** (_largeur x hauteur_) que l'image à traiter

Si les dimensions sont différentes :
- chaque tentative de soustraction provoque l'ajout au journal de session d'un **WARNING** portant le message :

  _incohérence de la structure des données - la soustraction de dark est IGNOREE_
- Le bouton `Acquitter` du `Journal de session` est activé
- Si le `journal de session` est caché, l'indicateur de nouveaux problèmes apparaît dans la section `Problèmes` du
  panneau.
{{% /alert %}}

{{% alert color="info" %}}
ℹ️ Il n'est pas obligatoire que les formats de données du master dark et de l'image soient identiques.

  En cas de différence (_ex. master dark en flottants 32bits et brute en entiers 16bits_) : 
  - le master dark est converti avant son utilisation
  - la différence de format est signalée discrètement dans le journal de session
{{% /alert %}}

ℹ️ Par défaut : OFF

## Dématriçage {#debayer}


{{< center >}}
{{< figure src="debayer.png"
caption="Réglage du dématriçage"
width="622px"
height="286px"
alt="Interface logicielle affichant les préférences de traitement d'image avec des options pour définir le chemin de signal noir et sélectionner le motif de dématriçage, y compris AUTO et divers motifs de filtres de couleur." >}}
{{< /center >}}

{{% alert title="ℹ️ mode AUTO recommandé" color="info" %}}

La matrice utilisée est extraite des métadonnées des brutes et fonctionne **la grande majorité du temps.**

Si les métadonnées ne contiennent aucune matrice
  - Les brutes ne seront pas dématricées
  - Des défauts en forme de grille ou de damiers seront visibles sur les images générées
  - Utilisez la sélection manuelle pour corriger ce problème

<details>
<summary>Métadonnées recherchées</summary>

- Image au format FITS : entête FITS **BAYERPAT**
- Image au format Raw : entête Exif standard
</details>
{{% /alert %}}

{{% alert color="light" %}}
💡 La sélection manuelle de la matrice de Bayer est utile dans les cas suivants :
- Les métadonnées de l'image ne contiennent pas la matrice de Bayer
- Le mode AUTO ne donne pas le résultat attendu (_ex. grille ou damiers sur l'image dématricée_)
{{% /alert %}}

ℹ️ Par défaut : AUTO