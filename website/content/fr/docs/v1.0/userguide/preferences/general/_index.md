---
title: "Onglet général"
description: "Documentation de l'onglet Général des préférences d'ALS"
author: "ALS Team"
lastmod: 2026-06-06T18:11:21Z
keywords: [ "ALS general settings", "préférences générales ALS" ]
draft: false
type: "docs"
categories: ["configuration", "dépannage"]
tags: [ "dossier scanné", "memoire", "profil", "langue" ]
weight: 100331
---

Les réglages les plus critiques d'ALS sont présentés dans l'onglet `Général`

# Vue d'ensemble

<div class="row">
<div class="col-md-4">

Cet onglet est divisé en 3 sections :

- [Scanner](#scanner)
- [Mémoire](#memory)
- [Moteur](#core)

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

Si votre système d'acquisition enregistre les brutes dans des sous-dossiers organisés par cible ou date, surveillez
le dossier parent de ces sous-dossiers.
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

ℹ️ Par défaut : ∅

# Utilisation Mémoire {#memory}

Définit le comportement d'ALS concernant la quantité de mémoire à laisser à la disposition des autres applications

{{< center >}}
{{< figure src="memory.png"
caption="Préférences de gestion de la mémoire"
width="600px"
height="209px"
alt="" >}}
{{< /center >}}

Les noms associés aux valeurs de ce curseur sont aussi flous que la gestion de la mémoire peut l'être.

Nous vous conseillons d'expérimenter avec un esprit ouvert et joyeux...

⚙️ Ou allez consulter la [documentation détaillée](../../../reference/modules/scanner#ram) du module **Scanner**

ℹ️ Par défaut : **Injuste**

---

# Moteur {#core}

{{% alert color="info" %}}
ℹ️ Les modifications faites aux paramètres moteur nécessitent un redémarrage d'ALS pour être prises en compte
{{% /alert %}}


## Profil {#profile}

ALS propose deux modes de fonctionnement différents, appelés **profils**

Les profils optimisent le comportement d'ALS pour des usages particuliers :

| Profil                       | Réactivité Scanner | Priorité donnée à       | Rejet sigma |
|------------------------------|--------------------|-------------------------|-------------|
| Visuel assisté               | Élevée             | Calibration et stacking | OFF         |
| Suivi session astrophoto     | Normale            | Traitements d'image     | ON          |

`Visuel assisté` garde la détection, la calibration et le stacking réactifs afin que les nouvelles brutes soient
intégrées rapidement pendant une session live.

`Suivi session astrophoto` donne plus de priorité aux traitements d'image, couramment utilisés entre les
brutes arrivant à cadence lente. Il active aussi le rejet sigma en stacking en mode **moyenne** afin d'éliminer les
artefacts lumineux transitoires comme les traînées de satellites.

- 🖱️ Sélectionnez le profil correspondant à l'activité que vous voulez confier à ALS.

⚙️ Vous trouverez les détails de l'impact du profil sur le **Scanner** dans la [documentation dédiée](../../../reference/modules/scanner#wait)

ℹ️ Par défaut : **Visuel assisté**

{{< center >}}
{{< figure src="proflang.png"
caption="Préférences de profil et de langue"
width="609px"
height="153px"
alt="Interface logicielle affichant les paramètres du dossier de travail avec le chemin défini sur /home/astrogeek/sorties_als, et un bouton Modifier pour configurer ce chemin." >}}
{{< /center >}}

## Langue {#language}

Définit la langue de l'interface utilisateur d'ALS

- 🖱️ Les choix suivants sont disponibles :

  - **Système** : ALS suit la langue du système
  - **Français**
  - **Anglais**
  - **Russe**

ℹ️ Par défaut : **Système**

{{% alert color="info" %}}
Si vous choisissez **système** et que votre système utilise une langue non prise en charge par ALS, l'interface sera affichée en anglais.
{{% /alert %}}

---

## Données {#data}

### Journaux détaillés {#logs}

Gestion du niveau de détail des messages écrits dans le fichier journal

Le fichier journal est nommé **als.log**. Il est situé dans votre dossier personnel :

{{< tabpane text=true >}}
  {{% tab header="Linux" %}}
  <span style="font-family: monospace;">/home/astrogeek/als.log</span>
  {{% /tab %}}
  {{% tab header="Windows" %}}
  <span style="font-family: monospace;">C:\Users\astrogeek\als.log</span>
  {{% /tab %}}
  {{% tab header="macOS"  %}}
  <span style="font-family: monospace;">/Users/astrogeek/als.log</span>
  {{% /tab %}}
{{< /tabpane >}}


- 🖱️ Cochez `Journaux détaillés` pour activer l'écriture de messages détaillés

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

ℹ️ Par défaut : **OFF**

{{< center >}}
{{< figure src="data.png"
caption="Préférences de données"
width="622px"
height="198px"
alt="" >}}
{{< /center >}}

### Statistiques d'utilisation

Il nous est très utile de savoir quelles versions d'ALS sont utilisées et sur quelle plateforme.

Nous vous serions très reconnaissants d'autoriser ALS à nous envoyer des statistiques d'utilisation, mais nous comprenons
également que vous puissiez être réticent à autoriser une telle fonctionnalité.

Sachez que :

- ALS nous enverra **uniquement** les informations suivantes à chaque démarrage :
  - Version d'ALS.
  - Architecture de la machine.
  - Type de système d'exploitation.
- Nous ne cherchons pas à identifier ni géolocaliser la source de ces informations.

<details>
    <summary>Cliquez ici pour savoir comment vous pouvez vérifier ces affirmations par vous-même</summary>

ALS et nos outils de suivi sont des logiciels **opensource**, leur code source est disponible publiquement.

- <a href="https://github.com/deufrai/als/blob/v1.0/src/als/main.py#L51" target="_blank">code de l'envoi
  des statistiques par ALS</a> <i class="fa-brands fa-square-github"></i>
- <a href="https://github.com/deufrai/als-stats-receiver/blob/master/listen.py#L42" target="_blank">code de
  l'enregistrement des statistiques reçues par nos serveurs</a> <i class="fa-brands fa-square-github"></i>

</details>

- 🖱️ Cochez `Statistiques d'utilisation` pour activer la collecte de données d'utilisation d'ALS

ℹ️ Par défaut : **OFF**
