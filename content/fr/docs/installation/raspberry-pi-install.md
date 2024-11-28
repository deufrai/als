---
hidden: true
title: "Install sur Raspberry Pi"
description: "Instructions détaillées pour extraire et exécuter Astro Live Stacker (ALS) sur un Raspberry Pi sous Linux."
author: "ALS Team"
date: 2024-11-27
lastmod: 2024-11-27
keywords: ["installation", "raspberry pi", "linux", "astro live stacker", "guide"]
draft: false
type: "instructions"
---


<div class="content-wrapper">
  <!-- markdown content start -->

### Instructions pour extraire et exécuter une archive ALS `.tgz` sous Linux

1. **Ouvrir le dossier de téléchargements**:
   - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre gestionnaire de fichiers (par exemple, Nautilus, Dolphin, ou Thunar) et en sélectionnant "Téléchargements" dans le menu de navigation à gauche.
   - Alternativement, vous pouvez ouvrir un terminal et entrer la commande suivante pour accéder directement au dossier de téléchargements :
     ```bash
     cd ~/Téléchargements
     ```

2. **Identifier l'archive ALS**:
   - Recherchez l'archive dont le nom commence par `als` et se termine par `.tgz`. Par exemple, cela pourrait être `als-v0.7-beta6.tgz`.

3. **Extraire l'archive**:
   - Pour extraire l'archive, vous pouvez utiliser un gestionnaire de fichiers ou le terminal.
   
   **Via le gestionnaire de fichiers** :
     - Faites un clic droit sur l'archive `als-v0.7-beta6.tgz`.
     - Sélectionnez "Extraire ici" ou une option similaire.
   
   **Via le terminal** :
     - Ouvrez un terminal et assurez-vous d'être dans le dossier de téléchargements :
       ```bash
       cd ~/Téléchargements
       ```
     - Exécutez la commande suivante pour extraire l'archive :
       ```bash
       tar -xzvf als-v0.7-beta6.tgz
       ```

4. **Naviguer vers le dossier extrait**:
   - L'archive extrait un dossier nommé `als-v0.7-beta6`, qui contient l'exécutable `als-v0.7-beta6`.
   - **Via le terminal** :
     - Accédez à ce dossier via le terminal :
       ```bash
       cd als-v0.7-beta6
       ```
   - **Via le gestionnaire de fichiers** :
     - Ouvrez le dossier `als-v0.7-beta6` en double-cliquant dessus dans votre gestionnaire de fichiers.

5. **Lancer l'exécutable**:
   - **Via le terminal** :
     - Toujours dans le terminal, exécutez la commande suivante pour lancer l'application :
       ```bash
       ./als-v0.7-beta6
       ```
   - **Via le gestionnaire de fichiers** :
     - Faites un double clic sur le fichier `als-v0.7-beta6`.
     - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution du fichier, choisissez l'option pour exécuter ou ouvrir le fichier.

Bonne utilisation d'ALS ! 🚀✨

  <!-- markdown content end -->
</div>
