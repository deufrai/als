---
title: "Journal de session"
description: "Documentation du panneau Journal de session de ALS"
author: "Équipe ALS"
lastmod: 2025-04-20T17:32:13Z
keywords: [ "journal de session", "suivi", "erreurs", "log", "panneaux" ]
type: "docs"
tags: [ "journal", "problèmes", "erreurs", "panneaux" ]
categories: [ "utilisation" ]
weight: 323
---

# Introduction

Dans cette section, vous allez apprendre comment rester informé des événements survenant pendant votre session.

# Aperçu

Le `Journal de session` se compose de deux parties principales :

- [**Vue du journal :**](#log-view) Une liste des messages enregistrés, affichés en temps réel.
- [**Boutons de contrôle :**](#control-buttons) Des options interactives pour filtrer, suivre et gérer les entrées de journal.

Il vous permet non seulement de surveiller les traitements, mais aussi de faciliter la résolution des
problèmes et l’analyse des performances.

{{< center >}}
{{< figure src="log.png"
caption="Le panneau Journal de session"
width="1307px"
height="210px"
alt="Le panneau Journal de session de ALS affichant des messages de traitement." >}}
{{< /center >}}

---

# Vue du journal {#log-view}

La **Vue du journal** affiche les messages chronologiquement, avec les plus récents en bas. 

Chaque entrée inclut :
- **Horodatage :** L’heure à laquelle le message a été enregistré.
- **Type :** Le niveau d’importance du message : INFO, WARNING ou ERROR.
- **Détail :** Une description de l'événement.

Lorsqu’un événement imprévu survient pendant une session (par exemple : erreur dans le traitement des fichiers, échec de
processus), celui-ci est consigné dans le journal sous forme de **WARNING** ou **ERROR**, selon sa gravité :

- **WARNING :** Problème pouvant sans doute être ignoré, sans impact significatif sur la session en cours.
- **ERROR :** Problème susceptible d’avoir un impact sur les résultats de la session.

Exemples de messages :

- INFO Image sauvegardée : web_image.jpg
- WARNING Impossible de stacker l'image \[...\] L'image est ABANDONNEE
- ERROR Echec de sauvegarde image \[...\]

### Copie des messages

Un clic sur une ligne du journal copie automatiquement son contenu dans le presse-papier, facilitant son partage ou son
analyse.

---

# Boutons de contrôle {#control-buttons}

Le panneau `Journal de session` inclut plusieurs boutons pour gérer l’affichage et les alertes. 

<div class="row">
<div class="col-md-8">

## Acquitter

Le bouton `Acquitter` est accompagné d'un indicateur de nouveaux problèmes.
L'indicateur s’affiche sur le bouton lorsqu’un nouveau problème est détecté. Ce système
visuel vous aidera à remarquer rapidement les événements notables. 

🖱️ Cliquez sur `Acquitter` pour signaler que vous avez pris connaissance des nouveaux messages. L'indicateur disparaît.

## Problèmes seuls

Le bouton `Problèmes seuls` permet de filter l’affichage du journal pour ne montrer que les messages critiques.

🖱️ Cliquez sur `Problèmes seuls` pour basculer l'état du filtre

ℹ️ Par défaut : OFF

## Suivre

Le bouton `Suivre` garantit que le dernier message du journal reste toujours visible.

🖱️ Cliquez sur `Suivre` pour activer ou désactiver le défilement automatique vers le dernier message.

ℹ️ Par défaut : ON

</div>


<div class="col-md-4 d-flex align-items-center justify-content-center">
{{< center >}}
{{< figure src="controls.png"
caption="Les boutons du Journal de session"
width="164px"
height="210px"
alt="Les boutons Suivre, Problèmes seuls et Acquitter du panneau Journal de session." >}}
{{< /center >}}
</div>
</div>

---

# Conclusion

Vous savez maintenant comment rester informé tout au long de vos sessions.

Prochaine étape : Les précieux raccourcis clavier.
