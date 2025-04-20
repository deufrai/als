---
title: "Traitements"
description: "Documentation du panneau Traitements de ALS"
author: "Équipe ALS"
lastmod: 2025-04-20T01:29:27Z
keywords: [ "traitements ALS", "histogramme", "auto stretch", "niveaux", "balance RVB", "curseurs", "panneaux" ]
type: "docs"
tags: [ "histogramme", "stretch", "curseurs", "traitements", "panneaux" ]
categories: [ "utilisation", "configuration" ]
weight: 322
---

# Introduction

Dans ce chapitre, vous allez apprendre à améliorer vos images en utilisant le module **Process**.

<div class="row">
<div class="col-md-8">

# Aperçu

Le panneau **Traitements** est la salle de contrôle des capacités de traitement d’image de ALS.

Situé sur le côté droit de l’interface, ce panneau regroupe les contrôles des traitements en plusieurs sections :

- [**Histogramme**](#histogramme-section)  
  Visualisation graphique de la répartition des intensités lumineuses.

- [**Auto Stretch**](#stretch-section)  
  Réglage de la force de l’étirement automatique.

- [**Niveaux**](#niveaux-section)  
  Ajustement de l’exposition globale ainsi que des écrêtages des noirs et des blancs.

- [**Balance RVB**](#balance-section)  
  Ajustement des niveaux de rouge, vert et bleu pour corriger les couleurs.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="panel.png" 
caption="Le panneau Traitements" 
width="345px"
height="670px"
alt="Le panneau Traitements de ALS, incluant les sections Histogramme, Auto Stretch, Niveaux, et Balance RVB avec leurs curseurs et contrôles associés." >}}
</div>
</div>

---

# Histogramme {#histogramme-section}

L’**Histogramme** fournit une représentation graphique de la répartition des valeurs d’intensité lumineuse dans l’image
affichée. Cet outil est essentiel pour évaluer rapidement l’équilibre des tons et des couleurs.

<div class="row">
<div class="col-md-8">

### Propriétés du Graphique

- **Axe horizontal :** Indique l’intensité lumineuse, allant des ombres à gauche (faible intensité) aux hautes lumières à
  droite (forte intensité).
- **Axe vertical :** Représente le nombre de pixels à chaque niveau d’intensité. Les pics plus élevés indiquent une plus
  grande quantité de pixels dans cette plage tonale.

Pour les images monochromes, une seule courbe blanche est affichée, représentant la répartition des pixels selon leur intensité lumineuse.

### Images en couleur

Pour les images en couleur, l’histogramme affiche des courbes distinctes pour les 3 canaux. Chaque courbe
représente la répartition des pixels selon leur intensité dans son canal respectif, offrant une vue sur la contribution
de chaque couleur dans l’image.

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="histo.png"
caption="La section Histogramme"
width="318px"
height="147px"
alt="Histogramme dynamique reflétant la répartition des valeurs d’intensité lumineuse de l’image." >}}
{{< /center >}}
</div>
</div>

---

# Contrôles des Traitements {#controls-section}

Cette section regroupe les contrôles du module **Process** et de ses 3 processeurs d’image :
- Auto Stretch
- Niveaux
- Balance RVB

Les contrôles de chaque processeur sont regroupés en sections, chacune comportant son propre ensemble de curseurs et
boutons :

## Réglages

Chaque curseur correspond à un paramètre ajustable. Aucune valeur numérique n’est affichée, pour encourager une approche
visuelle et intuitive.

{{% alert color="info" %}}
ℹ️ Tous les curseurs de ce panneau `Traitements` possèdent une fonctionnalité supplémentaire :  
🖱️ **Double-cliquer** sur la poignée d’un curseur le réinitialise à sa position par défaut.
{{% /alert %}}

## Gestion et Application des Paramètres

- **Appliquer :** Génère une nouvelle image en fonction des positions actuelles des curseurs.  
- **Défaut :** Réinitialise tous les curseurs à leurs positions par défaut sans modifier l’image affichée.
- **Recharger :** Replace les curseurs aux positions qu'ils avaient lors du dernier clic sur `Appliquer`, sans modifier
  l’image affichée.
- **Actif :** Permet d’activer ou désactiver le traitement. Une nouvelle image est générée immédiatement après ce
  changement, sans besoin de cliquer sur **Appliquer**.

---

# Ajuster l’Image

## Auto Stretch {#stretch-section}

La section **Auto Stretch** ajuste l’intensité de l’étirement automatique appliqué à l’image, essentiel pour rendre les
images empilées exploitables.

🖱️ Utilisez le curseur `Force` pour régler la quantité d’étirement.

ℹ️ Par défaut : **Un équilibre idéal magiquement défini par nous.**

## Niveaux {#niveaux-section}

<div class="row">
<div class="col-md-8">

### Noir

🖱️ Utilisez le curseur `noir` pour régler le seuil des tons sombres :

- **Analysez l’histogramme :** Observez l’extrémité gauche de l’histogramme et vérifiez la distance entre les courbes et
  le bord gauche.
- **Objectif :** Placez les courbes juste au contact du bord gauche pour optimiser les tons sombres, tout en évitant de
  les écrêter.

  *Déplacer le curseur vers la droite décale les courbes vers la gauche.*

### Blanc

🖱️ Utilisez le curseur `Blancs` pour régler le seuil des tons clairs :

- **Objectif :** Ajustez ce curseur visuellement pour équilibrer la luminosité des hautes lumières tout en conservant les
  détails.

  *Déplacer le curseur vers la gauche décale les courbes vers la droite.*

### Exposition

🖱️ Utilisez le curseur `Exposition` pour contrôler la luminosité globale :

- **Objectif :** Obtenez une exposition correcte en vous fiant à votre perception pour identifier le niveau qui met le
  mieux votre cible en valeur.

  *Déplacer le curseur vers la droite éclaircit globalement l’image.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="levels.png"
caption="Histogramme après ajustement des Niveaux"
width="318px"
height="147px"
alt="Histogramme montrant les courbes après réglages précis des niveaux noirs et blancs." >}}
</div>
</div>

## Balance RVB {#balance-section}

<div class="row">
<div class="col-md-8">

{{% alert color="info" %}}
ℹ️ Disponible uniquement pour les images en couleur.
{{% /alert %}}

### Analysez l’Histogramme

Observez le positionnement des pics principaux des trois courbes colorées sur l’axe horizontal.

### Votre Objectif

- Obtenir un équilibre neutre des couleurs en alignant verticalement les pics principaux des trois courbes est souvent
  un bon point de départ.

  Les zones où les courbes se chevauchent seront colorées selon le mélange des couleurs impliquées. Notez qu'aligner
  les pics maximise la zone blanche de l’histogramme.

- Faites également appel à votre jugement et à votre connaissance de la cible : un équilibre neutre n’est pas toujours
  souhaitable.

  Exemple : cible dominée par le H-alpha, on laissera volontiers une dominante rouge.

### Actions des Curseurs

Chaque curseur ajuste la position horizontale de la courbe correspondante.

*Déplacer le curseur vers la droite décale la courbe associée vers la droite.*

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< figure src="rgb.png"
caption="Équilibrage colorimétrique avec Balance RVB"
width="318px"
height="147px"
alt="Histogramme montrant l’alignement des pics colorés avec des curseurs RVB ajustés." >}}
</div>
</div>

---

# Conclusion

Avec ce chapitre, vous êtes désormais prêt à maîtriser le panneau **Traitements** ! Explorez ses fonctionnalités pour
améliorer vos images et en tirer le meilleur parti.

Prochaine étape : Le journal de session.
