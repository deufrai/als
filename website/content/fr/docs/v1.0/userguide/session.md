---
title: "Une session réussie"
description: "Guide étape par étape pour réaliser une session avec ALS"
author: "ALS Team"

lastmod: 2026-06-11T00:20:10Z
keywords: [ "session ALS", "flux de travail ALS" ]
draft: false
type: "docs"
categories: [ "utilisation", "configuration" ]
tags: [ "session", "serveur d’images", "profil" ]
weight: 100317
---

# 📘 Introduction

Ce chapitre est votre guide pour organiser une session ALS réussie et en suivre le déroulement. 

Il clôture la présentation des concepts principaux d'ALS avant de passer au guide de l'interface utilisateur.

---

# ⚡ Démarrage
ALS peut être lancé soit depuis son interface graphique, soit directement depuis la ligne de commande, selon votre flux de travail ou vos besoins d'automatisation.

- **Lancement graphique** :  
  Démarrez simplement ALS comme toute autre application. Vous arriverez dans la fenêtre principale, prêt à configurer votre session.

- **Lancement en ligne de commande** :  
  ALS prend en charge deux paramètres de démarrage optionnels qui peuvent automatiser l'initialisation de la session ou le partage en direct. 
  
  | Paramètre                            | Description                                                                                                                                                      |
  |--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | {{< als-code >}}-s{{< /als-code >}}  | Démarrer une session de stacking immédiatement après le lancement d'ALS. La session commence avec **l'alignement activé** et le **mode de stacking en moyenne**. |
  | {{< als-code >}}-w{{< /als-code >}}  | Démarrer automatiquement le serveur web intégré, permettant une visualisation à distance et en direct juste après le démarrage.                                  |

  Ces paramètres peuvent être combinés si vous souhaitez qu'ALS commence à traiter et diffuser l'image empilée immédiatement.

---

# ⚙️ Configuration

Que vous réalisiez des prises de vue en direct, prépariez des données pour un traitement avancé ou exploriez des approches plus artistiques, ces étapes vous garantiront une expérience optimale avec ALS.

## ✔️ Choisir votre profil

<div class="row">
<div class="col-md-6">

- **Visuel assisté** : Prises de vue en direct.  

  ALS traite les brutes rapidement et produit des images colorées, visualisables en temps réel.

</div>

<div class="col-md-6">

- **Astrophoto** : Superviser une session d'astrophoto

  ALS agit comme un outil de diagnostic permettant de vous assurer du bon déroulement de vos acquisitions et de la
  qualité de vos brutes

</div>
</div>

## ✔️ Préparer votre calibration

- Disposez-vous d’un master dark adapté à votre capteur et à sa température ?  

  Si oui, utilisez la **soustraction de dark** pour éliminer le bruit thermique.

- Disposez-vous d’un master flat adapté à votre configuration optique ?

  Si oui, utilisez la **calibration par flat** pour corriger le vignettage et les poussières.

## ✔️ Ajuster le stacking

- Activez **Aligner** pour l'imagerie des objets du ciel profond ou désactivez-le pour des projets artistiques comme 
  les filés d'étoiles ou les time-lapses.
- Définissez le mode de stacking :  
  - **Moyenne** pour des images homogènes et sans bruit.  
  - **Somme** pour une luminosité amplifiée et une approche créative.

---

# 🚀 Déroulement

Lancez la session et laissez ALS prendre les commandes.  

Voici comment tout garder sous contrôle et apprécier les résultats :

## 📊 Suivi

Surveillez votre session en consultant les retours d'ALS sur les performances et les éventuels problèmes liés au traitement des brutes.

## 🌦️ Adaptez-vous

Ajustez le nombre minimal de correspondances pour gérer les changements de conditions météorologiques et les
spécificités de votre setup.

## 🎨 Ajustez votre image

Affinez les paramètres de traitement d'image d'ALS pour ajuster l'image à mesure que de nouvelles brutes sont ajoutées.

## 🔍 Explorez votre image

Zoomez et parcourez l'image pour identifier les zones qui méritent votre attention ou simplement pour en profiter.

## 🌐 Partagez vos progrès

Idéal pour des événements publics ou des discussions collaboratives :  

Permettez à d'autres de suivre votre session en direct en activant le serveur d'images et en partageant le QR code généré.  

Les spectateurs peuvent explorer votre image en cours d'évolution avec les mêmes fonctionnalités de navigation que l'application principale ALS, optimisées pour les appareils de bureau et mobiles.

---

# 📦 Clôture

Stoppez votre session et récupérez l'image finale dans le **dossier de travail**.

{{< alert color="info" >}}
Pour terminer une session démarrée **depuis la ligne de commande**, utilisez {{< als-ks >}}Ctrl+C{{< /als-ks >}} dans le terminal où ALS s'exécute.
Cela quittera également **l'application entière**.
{{< /alert >}}


---

# 🎯 Conclusion

Il est temps pour **vous** de prendre en main ALS grâce au prochain chapitre : l'interface utilisateur.
