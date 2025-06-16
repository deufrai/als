---
title: Installation sur PC/Linux
description: Installation d'ALS sur PC Linux
author: ALZ Team
lastmod: 2025-01-07T16:31:56Z
keywords: [ "installation", "linux", "astro live stacker", "guide" ]
weight: 210
Categories: ['procédures']
tags: ['install', 'Linux', 'PC']
---

# 🖥️ Configuration minimale requise

## Distribution GNU/Linux 64bits
- Ubuntu 22.04 ou supérieur
- Fedora 34 ou supérieur
- Debian 11 (Bullseye) ou supérieur
- openSUSE Leap 15.3 ou supérieur
- Linux Mint 21 ou supérieur
- toute autre distribution proposant GLIBC 2.35 ou supérieur

## Exigences Matérielles
|                    | Minimum |
|--------------------|---------|
| **RAM**            | 4 Go    |
| **Stockage libre** | 950 Mo  | 

# 📦 Installation

1. **Ouvrir le dossier de téléchargements**
    - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre
      gestionnaire de fichiers (par exemple, Nautilus, Dolphin, ou Thunar) et en sélectionnant "Téléchargements" dans le
      menu de navigation à gauche.

2. **Identifier le fichier ALS**
    - Recherchez le fichier dont le nom commence par `als` et se termine par `.run`. Par exemple, cela pourrait être
      `als-v0.7-beta10.run`.

3. **Rendre le fichier exécutable**
    - Pour rendre le fichier exécutable, vous devez modifier ses permissions. Cela peut être fait directement depuis le
      gestionnaire de fichiers :
        - Faites un clic droit sur le fichier `als-v0.7-beta10.run`.
        - Sélectionnez "Propriétés".
        - Accédez à l'onglet "Permissions".
        - Cochez l'option "Autoriser l'exécution du fichier comme un programme".

4. **Déplacer ALS vers un emplacement permanent**

   **Pourquoi déplacer ALS en dehors du dossier de téléchargements ?**

   Déplacer ALS dans un répertoire dédié permet de mieux organiser vos fichiers et d'assurer que l'application est
   installée dans un emplacement stable et permanent. Le dossier de téléchargements est souvent utilisé pour des
   fichiers temporaires et peut être nettoyé régulièrement, entraînant la suppression accidentelle de fichiers
   importants. En créant un dossier spécifique pour ALS, vous vous assurez que l'application reste accessible et en
   sécurité.

    - Ouvrez votre gestionnaire de fichiers (par exemple, Nautilus).
    - Accédez à votre répertoire personnel (`/home/nom_utilisateur`).
    - Faites un clic droit dans le répertoire et sélectionnez "Créer un nouveau dossier".
    - Nommez le dossier `Applications` et appuyez sur "Entrée".
    - Double-cliquez sur le dossier `Applications` pour l'ouvrir.
    - Créez un autre dossier à l'intérieur appelé `ALS` et appuyez sur "Entrée".
    - Accédez au dossier de téléchargements (`Téléchargements`) dans une autre fenêtre de votre gestionnaire de
      fichiers. Il est important d'avoir deux fenêtres distinctes et visibles pour pouvoir glisser facilement les
      fichiers.
    - Trouvez le fichier `als-v0.7-beta10.run` dans le dossier de téléchargements, puis faites glisser ce fichier dans le
      dossier `ALS` (`/home/nom_utilisateur/Applications/ALS`).

5. **Lancer le fichier exécutable**
    - Faites un double clic sur le fichier `als-v0.7-beta10.run`.
    - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution du fichier, choisissez l'option pour
      exécuter ou ouvrir le fichier.

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 
