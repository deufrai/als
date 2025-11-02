---
title: Installation sur Raspberry Pi
description: Installation d'ALS sur Raspberry Pi
author: ALZ Team

lastmod: 2025-11-02T19:02:52Z
keywords: [ "installation", "raspberry pi", "linux", "astro live stacker", "guide" ]
weight: 220
Categories: ['procédures']
tags: ['install', 'Linux', 'Raspberry Pi']
---

# 🖥️ Configuration minimale requise

## Distribution GNU/Linux 64bits*
- Raspberry Pi OS - Bullseye (Version 11)
- Raspberry Pi OS - Bookworm
- toute autre distribution proposant GLIBC 2.31 ou supérieur

## Exigences Matérielles
|                    | Minimum      |
|--------------------|--------------|
| **Modèle**         | Pi 4 Model B | 
| **RAM**            | 4 Go         |
| **Stockage libre** | 650 Mo       | 

*_Les versions d'ALS proposées au téléchargement pour Raspberry Pi sont destinés aux systèmes en 64bits.
Mais vous pouvez facilement adapter ce [script de build](https://github.com/deufrai/als/blob/release/0.7/ci/builds/build_dist_arm64_linux.sh)
pour packager une version d'ALS en 32bits depuis les sources. L'unique contrainte forte est d'utiliser Python en verion
3.6.x. N'hésitez pas à [nous contacter](mailto://support@als-app.org) 
si vous avez besoin d'aide._

# 📦 Installation

1. **Ouvrir le dossier de téléchargements**
    - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre
      gestionnaire de fichiers (par exemple, PCManFM) et en sélectionnant "Téléchargements" dans le menu de navigation à
      gauche.

2. **Identifier l'archive ALS**
    - Recherchez l'archive dont le nom commence par `als` et se termine par `.tgz`. Par exemple, cela pourrait être
      `als-v0.7.tgz`.

3. **Extraire l'archive**
    - Pour extraire l'archive, vous pouvez utiliser un gestionnaire de fichiers :
        - Faites un clic droit sur l'archive `als-v0.7.tgz`.
        - Sélectionnez "Extraire ici" ou une option similaire.

4. **Déplacer ALS vers un emplacement permanent**

   **Pourquoi déplacer ALS en dehors du dossier de téléchargements ?**

   Déplacer ALS dans un répertoire dédié permet de mieux organiser vos fichiers et d'assurer que l'application est
   installée dans un emplacement stable et permanent. Le dossier de téléchargements est souvent utilisé pour des
   fichiers temporaires et peut être nettoyé régulièrement, entraînant la suppression accidentelle de fichiers
   importants. En créant un dossier spécifique pour ALS, vous vous assurez que l'application reste accessible et en
   sécurité.

    - Ouvrez votre gestionnaire de fichiers (par exemple, PCManFM).
    - Accédez à votre répertoire personnel (`/home/nom_utilisateur`).
    - Faites un clic droit dans le répertoire et sélectionnez "Créer un nouveau dossier".
    - Nommez le dossier `Applications` et appuyez sur "Entrée".
    - Double-cliquez sur le dossier `Applications` pour l'ouvrir.
    - Créez un autre dossier à l'intérieur appelé `ALS` et appuyez sur "Entrée".
    - Accédez au dossier de téléchargements (`Téléchargements`) dans une autre fenêtre de votre gestionnaire de
      fichiers. Il est important d'avoir deux fenêtres distinctes et visibles pour pouvoir glisser facilement les
      fichiers.
    - Trouvez le dossier `als-v0.7` dans le dossier de téléchargements, puis faites glisser ce dossier dans le
      dossier `ALS` (`/home/nom_utilisateur/Applications/ALS`).

5. **Lancer l'exécutable**
    - Accédez au dossier `als-v0.7` dans le gestionnaire de fichiers.
    - Faites un double clic sur le fichier `als-v0.7`.
    - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution, choisissez l'option pour exécuter ou
      ouvrir le fichier.

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 

