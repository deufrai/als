---
title: Installation
description: installation d'ALS
author: ALZ Team
lastmod: 2024-12-08T16:40:59Z
weight: 20
tags: ['installation']
---

# 🖥️ Configuration système requise

Bonne nouvelle, ALS n’est pas trop gourmand en ressources.

Cependant, on n'a jamais trop de puissance CPU et de RAM. Plus il y en a mieux c'est ! Cela rendra ALS plus fluide. 😊

---

## Tous ordinateurs de bureau et portables
- Rien de spécial, vraiment. N'importe quel système moderne fera l'affaire.

## Raspberry Pi
- Raspberry Pi 4 minimum
- 4 Go de RAM minimum
 
Les versions d'ALS proposées au téléchargement pour Raspberry Pi sont destinés aux systèmes en 64bits.

Mais vous pouvez facilement adapter ce [script de build](https://github.com/deufrai/als/blob/release/0.7/ci/builds/build_dist_arm64_linux.sh)
pour packager une version d'ALS en 32bits depuis les sources. L'unique contrainte forte est d'utiliser Python en verion
3.6.x. N'hésitez pas à [nous contacter](mailto://support@als-app.org) 
si vous avez besoin d'aide.

---

{{% alert title="INFO" color="info" %}}
Les procédures d'installation de ce chapitre sont rédigées pour un système en langue française. Si votre système
utilise une autre langue, faites les ajustements nécessaires. Bonne installation !
{{% /alert %}}
