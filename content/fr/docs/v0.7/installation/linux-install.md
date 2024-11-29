---
title: "PC/Linux"
description: "Installer ALS sur un PC sous Linux."
author: "ALS Team"
date: 2024-11-27
lastmod: 2024-11-29T18:28:25Z
keywords: ["installation", "linux", "astro live stacker", "guide"]
draft: false
type: "docs"
weight: 21
---

1. **Ouvrir le dossier de téléchargements**
   - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre gestionnaire de fichiers (par exemple, Nautilus, Dolphin, ou Thunar) et en sélectionnant "Téléchargements" dans le menu de navigation à gauche.
   - Alternativement, vous pouvez ouvrir un terminal et entrer la commande suivante pour accéder directement au dossier de téléchargements
     ```bash
     cd ~/Téléchargements
     ```

2. **Identifier le fichier ALS**
   - Recherchez le fichier dont le nom commence par `als` et se termine par `.run`. Par exemple, cela pourrait être `als-v0.7-beta6.run`.

3. **Rendre le fichier exécutable**
   - Pour rendre le fichier exécutable, vous devez modifier ses permissions. Cela peut être fait directement depuis le gestionnaire de fichiers ou via le terminal.
   
   **Via le gestionnaire de fichiers**
     - Faites un clic droit sur le fichier `als-v0.7-beta6.run`.
     - Sélectionnez "Propriétés".
     - Accédez à l'onglet "Permissions".
     - Cochez l'option "Autoriser l'exécution du fichier comme un programme".

   **Via le terminal**
     - Ouvrez un terminal et assurez-vous d'être dans le dossier de téléchargements
       ```bash
       cd ~/Téléchargements
       ```
     - Exécutez la commande suivante pour rendre le fichier exécutable
       ```bash
       chmod +x als-v0.7-beta6.run
       ```

4. **Déplacer ALS vers un emplacement permanent**

   **Via le gestionnaire de fichiers**
     - Ouvrez votre gestionnaire de fichiers (par exemple, Nautilus).
     - Accédez à votre répertoire personnel (`/home/nom_utilisateur`).
     - Faites un clic droit dans le répertoire et sélectionnez "Créer un nouveau dossier".
     - Nommez le dossier `Applications` et appuyez sur "Entrée".
     - Double-cliquez sur le dossier `Applications` pour l'ouvrir.
     - Créez un autre dossier à l'intérieur appelé `ALS` et appuyez sur "Entrée".
     - Accédez au dossier de téléchargements (`Téléchargements`), faites un clic droit sur le fichier `als-v0.7-beta6.run` et sélectionnez "Couper".
     - Retournez dans le dossier `ALS` (`/home/nom_utilisateur/Applications/ALS`), faites un clic droit et sélectionnez "Coller".

   **Via le terminal**
     - Ouvrez un terminal.
     - Exécutez les commandes suivantes pour créer les répertoires et déplacer le fichier
       ```bash
       mkdir -p ~/Applications/ALS
       mv ~/Téléchargements/als-v0.7-beta6.run ~/Applications/ALS/
       ```

5. **Lancer le fichier exécutable**

   **Via le terminal**
     - Toujours dans le terminal, accédez au répertoire et lancez ALS
       ```bash
       cd ~/Applications/ALS
       ./als-v0.7-beta6.run
       ```

   **Via le gestionnaire de fichiers**
     - Faites un double clic sur le fichier `als-v0.7-beta6.run`.
     - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution du fichier, choisissez l'option pour exécuter ou ouvrir le fichier.

### Section optionnelle : Créer et utiliser un fichier Desktop

**Pourquoi créer un fichier Desktop ?**

Créer un fichier Desktop permet de lancer rapidement l'application ALS directement depuis votre bureau, sans avoir à naviguer dans les répertoires ou à utiliser le terminal. Cela facilite l'accès et améliore l'expérience utilisateur.

**Étapes pour créer un fichier Desktop :**

1. **Ouvrir un éditeur de texte**
   - Ouvrez un éditeur de texte comme Gedit ou Nano.

2. **Créer le fichier Desktop**
   - Dans l'éditeur de texte, ajoutez les lignes suivantes
     ```ini
     [Desktop Entry]
     Version=1.0
     Type=Application
     Name=ALS
     Comment=Astro Live Stacker
     Exec=/home/nom_utilisateur/Applications/ALS/als-v0.7-beta6.run
     Terminal=false
     Categories=Graphics;
     ```
   - Enregistrez ce fichier sous le nom `ALS.desktop` dans le répertoire `~/Bureau`.

3. **Rendre le fichier exécutable**
   - Faites un clic droit sur le fichier `ALS.desktop` sur votre bureau.
   - Sélectionnez "Propriétés".
   - Accédez à l'onglet "Permissions".
   - Cochez l'option "Autoriser l'exécution du fichier comme un programme".

4. **Lancer ALS depuis le bureau**
   - Faites un double clic sur l'icône `ALS.desktop` sur votre bureau pour lancer l'application.

Bonne utilisation d'ALS ! 🚀
