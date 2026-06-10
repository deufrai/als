---
title: Installation sur Windows
description: Installation d'ALS sur PC Windows
author: ALZ Team
lastmod: 2026-06-10T23:57:05Z
keywords: [ "installation ALS", "windows", "astro live stacker", "guide" ]
weight: 70230
Categories: ['procédures']
tags: [ 'installation', 'Windows', 'PC' ]
---

# 🖥️ Configuration minimale requise

## Version système

Windows 10 ou supérieur

## Exigences Matérielles

|                    | Minimum |
|--------------------|---------|
| **RAM**            | 4 Go    |
| **Stockage libre** | 400 Mo  | 

# 📦 Installation

1. **Ouvrir le dossier de téléchargements**
    - Lorsque le téléchargement est terminé, ouvrez l'Explorateur de fichiers en cliquant sur son icône dans la barre
      des
      tâches (une icône en forme de dossier).
    - Accédez à votre dossier de téléchargements en sélectionnant "Téléchargements" dans le menu de navigation à gauche.
    - Vous devriez y voir l'installeur d'ALS dont le nom commence par `als` et se termine par `_Setup.exe`.
      Par exemple, cela pourrait être `als-v0.7_Setup.exe`.

2. **Exécuter l'installeur**
    - Double-cliquez sur le fichier `als-v0.7_Setup.exe` dans le dossier où vous l'avez téléchargé pour lancer 
      l'installation. Si ALS a déjà été installé sur votre système, cet installeur procèdera à une mise à jour.
    - Une fenêtre d'alerte de sécurité de Windows s'ouvrira probablement, indiquant que l'éditeur de l'application est
      inconnu.

3. **Gérer l'alerte de sécurité**
    - Windows 10
        - Cliquez sur "Informations complémentaires" dans la fenêtre d'alerte.
        - Ensuite, cliquez sur "Exécuter quand même".
    - Windows 11
        - Cliquez sur "Afficher plus" dans la fenêtre d'alerte.
        - Ensuite, cliquez sur "Exécuter quand même".

4. **Autoriser les modifications**
    - Une fenêtre de contrôle de compte d'utilisateur (UAC) s'ouvrira peut-être, vous demandant si vous souhaitez
      permettre à cette application d'apporter des modifications à votre système.
    - Cliquez sur "Oui" pour autoriser l'application à s'exécuter.

5. **Autoriser l'application dans le pare-feu Windows**
    - La première fois que vous lancez le serveur d'images d'ALS, une fenêtre de pare-feu Windows peut s'ouvrir, 
      vous demandant si vous souhaitez autoriser l'application à communiquer sur les réseaux publics et/ou privés.
    - Cochez les cases appropriées en fonction de vos préférences, puis cliquez sur "Autoriser l'accès".

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 
