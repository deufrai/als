---
title: "Onglet général"
description: "Documentation de l'onglet Général des préférences d'ALS"
author: "ALS Team"
lastmod: 2025-01-01T03:59:57Z
keywords: [ "ALS general settings", "préférences générales ALS" ]
draft: false
type: "docs"
categories: ["configuration", "dépannage"]
tags: [ "dossier scanné", "memoire", "profil", "langue" ]
weight: 331
---

Les réglages les plus critiques d'ALS sont présentés dans l'onglet `Général`

<div class="row">
<div class="col-md-4">

# Vue d'ensemble

Cet onglet est divisé en 3 sections :

- [Scanner](#scanner)
- [Mémoire](#memory)
- [Moteur](#engine)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Général des préférences"
width="622px"
height="660px"
alt="Fenêtre de préférences ALS avec l'onglet Général sélectionné, affichant les sections Chemins, Profil, Gestion de la mémoire et Paramètres de base, y compris les chemins des dossiers de numérisation et de travail, les options de profil, le curseur de mémoire, le paramètre de langue, les journaux de débogage et les statistiques d'utilisation." >}}
{{< /center >}}

</div>
</div>

# Scanner {#scanner}

## Dossier scanné {#scan-folder}

{{% alert color="info" %}}
ℹ️ Ce paramètre n'est modifiable que quand la session est stoppée
{{% /alert %}}

Définit le chemin du dossier surveillé par ALS pour détecter les brutes enregistrées par votre système d'acquisition 

{{% alert color="light" %}}
💡 La détection fonctionne quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.

Si votre système d'acquisition enregistre les brutes dans des sous-dossiers organisés par cible ou date, configurez
le **dossier scanné** sur le dossier parent de ces sous-dossiers.
{{% /alert %}}

{{< center >}}
{{< figure src="scan_folder_01.png"
caption="Préférences du dossier scanné"
width="622px"
height="311px"
alt="Interface logicielle affichant les paramètres du dossier scanné avec le chemin défini sur /home/astrogeek/astroshots, et un bouton Modifier pour configurer ce chemin." >}}
{{< /center >}}

- 🖱️ cliquez `Dossier scanné...` pour configurer le **dossier scanné**
- Le chemin configuré est affiché à droite du bouton

# Utilisation Mémoire {#memory}

Défini le comportement d'ALS concernant la quantité de mémoire à laisser à la disposition des autres applications

{{< center >}}
{{< figure src="memory.png"
caption="Préférences de gestion de la mémoire"
width="600px"
height="209px"
alt="" >}}
{{< /center >}}

Les noms associés aux valeurs de ce curseur sont aussi flous que la gestion de la mémoire peut l'être.

Nous vous conseillons d'expérimenter avec un esprit ouvert et joyeux... 

⚙️ Ou allez consulter la [documentation détaillée](../../../modules/scanner#memory-management) du module **Scanner**

# Moteur {#engine}

{{% alert color="info" %}}
ℹ️ Les modifications faites aux paramètres moteur nécessitent un redémarrage d'ALS pour être pris en compte
{{% /alert %}}

<div class="row">
<div class="col-md-6">

## Profil {#profile}

ALS propose deux modes de fonctionnement différents, appelés **profils**

Les profils optimisent le comportement d'ALS pour des usages particuliers :

| Profil                  | Réactivité<br>Scanner | Optimisation<br>recherche de similitudes | 
|-------------------------|-----------------------|-------------------------------------------|
| Visuel assisté          | Élevée                | ON                                        |
| Astrophoto              | Normale               | OFF                                       |


</div>
<div class="col-md-6">

## Langue {#language}

Définit la langue de l'interface utilisateur d'ALS

🖱️ 3 choix sont offert :

- **Système** : ALS suit la langue du système
- **Français**
- **Anglais**

Si votre système est configuré dans une autre langue que le français ou l'anglais, ALS sera affiché en anglais.

</div>
</div>

{{< center >}}
{{< figure src="proflang.png"
caption="Préférences de profil et de langue"
width="609px"
height="153px"
alt="Interface logicielle affichant les paramètres du dossier de travail avec le chemin défini sur /home/astrogeek/sorties_als, et un bouton Modifier pour configurer ce chemin." >}}
{{< /center >}}




- 🖱️ Le profil `Visuel assisté` met l'accent sur la réactivité. 

   Recommandé pour des brutes de taille moyenne arrivant à cadence élevée : quelques secondes entre chaque brute

- 🖱️ Le profil `Suivi session astrophoto` met l'accent sur la fiabilité.

   Recommandé pour des brutes de grande taille arrivant à cadence lente : plusieurs minutes entre chaque brute 

⚙️ Vous trouverez les détails de l'impact du profil sur le **Scanner** dans la [documentation dédiée](../../../modules/scanner#wait)

{{% alert title="🐛 Bug connu" color="danger" %}}
Utiliser le profil **visuel assisté** avec des brutes au format carré 1:1 provoque des erreurs d'alignement

Les brutes s'empilent en formant des carrées imbriqués de tailles décroitantes
{{% /alert %}}


## Données {#data}

### Journaux détaillés {#logs}

Gestion du niveau de détail des messages écrits dans le fichier journal

Le fichier journal est nommé **als.log**. Il est situé dans votre dossier personnel :

{{< tabpane text=true >}}
  {{% tab header="**Système**" disabled=true /%}}
  {{% tab header="Linux" %}}
  <span style="font-family: monospace;">/home/astrogeek/als.log</span>
  {{% /tab %}}
  {{< tab header="Windows" >}}
  <span style="font-family: monospace;">C:\Users\astrogeek\als.log</span>
  {{< /tab >}}
  {{% tab header="macOS"  %}}
  <span style="font-family: monospace;">/Users/astrogeek/als.log</span>
  {{% /tab %}}
{{< /tabpane >}}


🖱️ Cochez `Journaux détaillés` pour activer l'écriture de messages détaillés

Les journaux détaillés peuvent ralentir l'application. Utilisez cette option quand vous avez besoin d'analyser
un problème de fonctionnement ou que vous comptez [signaler un problème](https://github.com/deufrai/als/issues) et 
nous fournir le plus d'informations possible 

Les journaux détaillés contiennent :
<div class="row">
<div class="col-md-6">

- la configuration de démarrage de l'application

- les caractéristiques de votre système

- des métriques spécifiques à l'application

</div>
<div class="col-md-6">

- les communications entre les différents modules

- les détails des étapes de traitement
</div>
</div>


{{< center >}}
{{< figure src="data.png"
caption="Préférences de données"
width="622px"
height="198px"
alt="" >}}
{{< /center >}}

### Statistiques d'utilisation

🖱️ Cochez `Statistiques d'utilisation` pour activer la collecte de données d'utilisation d'ALS

Les données collectées sont anonymes et servent à améliorer l'application

Vous trouverez les détails de la collecte de données dans le [guide de démarrage rapide](../../../quickstart#usage-stats)

