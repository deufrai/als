---
title: Installation sur un Mac Apple Silicon
description: Installation d'ALS sur Mac Apple Silicon
author: ALZ Team

lastmod: 2024-12-30T03:58:46Z
keywords: ["installation", "mac", "m1", "m2", "astro live stacker", "guide"]
weight: 240
Categories: ['installation']
tags: ['Mac', 'Apple Silicon']
---

# 🖥️ Configuration minimale requise

## Version système

macOS 10.13 (High Sierra) ou version ultérieure

## Exigences Matérielles
|                    | Minimum |
|--------------------|---------|
| **RAM**            | 4 Go    |
| **Stockage libre** | 400 Mo  | 

# 📦 Installation

1. **Ouvrir le dossier de téléchargements**
   - Lorsque le téléchargement est terminé, ouvrez le Finder en cliquant sur son icône dans le Dock.
   - Accédez à votre dossier de téléchargements en sélectionnant "Téléchargements" dans le menu de navigation à gauche.

2. **Identifier l'image disque als**
   - Recherchez l'image disque dont le nom commence par `als` et se termine par `-arm64.dmg`. Par exemple, cela pourrait être `als-v0.7-beta8-arm64.dmg`.

3. **Monter l'image disque**
   - Double-cliquez sur l'image disque `als-v0.7-beta8-arm64.dmg`. Cela montera l'image disque.
   - Une nouvelle fenêtre Finder affichera le contenu de l'image disque. Vous verrez l'icône de l'application `ALS` à gauche et un raccourci vers le dossier `Applications` du système à droite.

4. **Copier l'application dans le dossier Applications**
   - Faites glisser l'icône de l'application `ALS` de la fenêtre du Finder vers le raccourci `Applications` dans la même fenêtre.
   - Si vous y êtes invité, entrez votre mot de passe administrateur pour autoriser cette opération.

5. **Gérer les permissions de l'app**
   - macOS versions antérieures à Catalina (10.15)
     - Une boîte de dialogue s'affichera, indiquant que l'application provient d'un développeur inconnu. Cliquez sur "Ouvrir" pour confirmer.
     - Une fois que l'application est autorisée, double-cliquez à nouveau sur l'application `ALS` dans le dossier `Applications` pour la lancer.
   - macOS Catalina (10.15) jusqu'à Sonoma (14.x.x)
     - Une boîte de dialogue s'affichera, indiquant que l'application ne peut pas être ouverte car elle provient d'un développeur inconnu. Cliquez sur "Annuler".
     - Allez dans "Préférences Système" > "Sécurité et confidentialité" > "Général", puis cliquez sur "Ouvrir quand même" à côté du message concernant `ALS`.
     - Confirmez en cliquant à nouveau sur "Ouvrir" dans la nouvelle boîte de dialogue qui s'affiche.
     - Une fois que l'application est autorisée, double-cliquez à nouveau sur l'application `ALS` dans le dossier `Applications` pour la lancer.
   - macOS Sequoia (15.x.x)
     - Ouvrez le Finder et allez dans le dossier `Applications`
     - Ensuite, allez dans le sous-dossier `Utilitaires`.
     - Dans ce sous-dossier, double-cliquez sur l'application `Terminal` pour l'ouvrir.
     - Dans la fenêtre du Terminal, tapez la commande suivante
       ```bash
       sudo xattr -r -d com.apple.quarantine /Applications/als.app
       ```
     - Appuyez sur `Entrée`. Entrez votre mot de passe administrateur si vous y êtes invité et appuyez à nouveau sur `Entrée`.

6. **Lancement d'ALS**
     - Accédez au dossier `Applications`, puis double-cliquez sur l'application `ALS` pour l'exécuter.

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 
