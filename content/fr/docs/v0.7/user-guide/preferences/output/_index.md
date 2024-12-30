---
title: "Onglet Sortie"
description: "Documentation de l'onglet Sortie des préférences d'ALS"
author: "ALS Team"
lastmod: 2024-12-30T02:08:09Z
keywords: [ "ALS outout settings", "préférences Sortie  d'ALS" ]
draft: false
type: "docs"
categories: [ "guide utilisateur" ]
tags: [ "preferences", "output", "formats", "serveur" ]
weight: 333
---

Les régissant les résultats produits sont présentés dans l'onglet `Sortie` des préférences.

<div class="row">
<div class="col-md-4">

# Vue d'ensemble

Cet onglet est divisé en 2 sections :

- [Enregistreur de fichiers](#save)
- [Serveur web](#server)

</div>
<div class="col-md-8 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="whole_tab.png"
caption="L'onglet Sortie des préférences"
width="622px"
height="604px"
alt="L'onglet Sortie des préférences" >}}
{{< /center >}}

</div>
</div>

# Enregistreur de fichiers {#save}

Ici sont configurés le format des images sauvegardées et la fonction de sauvegarde auto à l'arrêt de la session.

<div class="row">
<div class="col-md-8">

## Format

- Format des images sauvegardées

  |           |                                      |
  |-----------|--------------------------------------|
  |Type de donnée       | choix :<br>- TIFF<br>- PNG<br>- JPEG |
  | Requis | Oui                                  |
  | Valeur par défaut | JPEG                                 |

Les boutons `Format` définissent le format des fichiers enregistrés

## Enregistrement auto fin de session

- Activation

  |           |          |
  |-----------|----------|
  |Type de donnée       | ON / OFF |
  | Requis | ∅        |
  | Valeur par défaut | OFF      |

La case à cocher `Enregistrement auto fin de session` active la sauvegarde automatique du **dernier** résultat
du module **Process** dans un nouveau fichier horodaté quand la session est arrêtée :

- **emplacemnt du fichier** : **dossier de travail**
- **nom du fichier** : composé de **stack_image** et d'un suffixe d'horodatage
- **Format et extension du fichier** : en fonction du format choisi

</div>
<div class="col-md-4 d-flex align-items-center justify-content-center">

{{< center >}}
{{< figure src="saver.png"
caption="Préférences de l'enregistreur de fichiers"
width="307px"
height="103px"
alt="Préférences de l'enregistreur de fichiers" >}}
{{< /center >}}

</div>
</div>


# serveur {#server}

