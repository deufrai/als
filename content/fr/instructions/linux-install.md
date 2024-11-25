---
title: "Installation sur PC/Linux"
---

<div class="content-wrapper">
  <!-- markdown content start -->

### Instructions pour exécuter un fichier ALS `.run` sous Linux

1. **Ouvrir le dossier de téléchargements**:
   - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre gestionnaire de fichiers (par exemple, Nautilus, Dolphin, ou Thunar) et en sélectionnant "Téléchargements" dans le menu de navigation à gauche.
   - Alternativement, vous pouvez ouvrir un terminal et entrer la commande suivante pour accéder directement au dossier de téléchargements :
     ```bash
     cd ~/Téléchargements
     ```

2. **Identifier le fichier ALS**:
   - Recherchez le fichier dont le nom commence par `als` et se termine par `.run`. Par exemple, cela pourrait être `als-v0.7-beta6.run`.

3. **Rendre le fichier exécutable**:
   - Pour rendre le fichier exécutable, vous devez modifier ses permissions. Cela peut être fait directement depuis le gestionnaire de fichiers ou via le terminal.
   
   **Via le gestionnaire de fichiers** :
     - Faites un clic droit sur le fichier `als-v0.7-beta6.run`.
     - Sélectionnez "Propriétés".
     - Accédez à l'onglet "Permissions".
     - Cochez l'option "Autoriser l'exécution du fichier comme un programme".

   **Via le terminal** :
     - Ouvrez un terminal et assurez-vous d'être dans le dossier de téléchargements :
       ```bash
       cd ~/Téléchargements
       ```
     - Exécutez la commande suivante pour rendre le fichier exécutable :
       ```bash
       chmod +x als-v0.7-beta6.run
       ```

4. **Lancer le fichier exécutable**:
   - **Via le terminal** :
     - Toujours dans le terminal, exécutez la commande suivante :
       ```bash
       ./als-v0.7-beta6.run
       ```
   - **Via le gestionnaire de fichiers** :
     - Faites un double clic sur le fichier `als-v0.7-beta6.run`.
     - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution du fichier, choisissez l'option pour exécuter ou ouvrir le fichier.

Bonne utilisation d'ALS ! 🚀✨

  <!-- markdown content end -->
</div>