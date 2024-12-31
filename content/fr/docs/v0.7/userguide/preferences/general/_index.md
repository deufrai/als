---
title: "Onglet général"
description: "Documentation de l'onglet Général des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-31T03:07:07Z
keywords: [ "ALS general settings", "préférences générales ALS" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "preferences", "general", "dossier scanné", "dossier de travail" ]
weight: 331
---

Les réglages les plus critiques d'ALS sont présentés dans l'onglet `Général`

<div class="row">
<div class="col-md-4">

# Vue d'ensemble

Cet onglet est divisé en 4 sections :

- [Chemins](#paths)
- [Profil](#profile)
- [Gestion de la mémoire](#memory)
- [Général](#general)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Général des préférences"
width="622px"
height="604px"
alt="Fenêtre de préférences ALS avec l'onglet Général sélectionné, affichant les sections Chemins, Profil, Gestion de la mémoire et Paramètres de base, y compris les chemins des dossiers de numérisation et de travail, les options de profil, le curseur de mémoire, le paramètre de langue, les journaux de débogage et les statistiques d'utilisation." >}}
{{< /center >}}

</div>
</div>

# Chemins {#paths}

{{% alert color="info" %}}
ℹ️ Ces paramètres ne sont accessibles que quand la session est stoppée
{{% /alert %}}

## Dossier scanné {#scan-folder}

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
height="198px"
alt="Interface logicielle affichant les paramètres du dossier scanné avec le chemin défini sur /home/astrogeek/astroshots, et un bouton Modifier pour configurer ce chemin." >}}
{{< /center >}}

1. `Modifier...` permet de configurer le **dossier scanné**.
2. Le chemin configuré est affiché à droite du bouton

## Dossier de travail {#work-folder}

Définit le chemin du **dossier de travail**

{{< center >}}
{{< figure src="work_folder.png"
caption="Préférences du dossier de travail"
width="609px"
height="153px"
alt="Interface logicielle affichant les paramètres du dossier de travail avec le chemin défini sur /home/astrogeek/sorties_als, et un bouton Modifier pour configurer ce chemin." >}}
{{< /center >}}

1. `Modifier...` permet de configurer le **dossier de travail**.
2. Le chemin configuré est affiché à droite du bouton

# Profil {#profile}

# Gestion de la mémoire {#memory}

# Général {#general}

Oops, twice general. 🫡