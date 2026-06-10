---
title: Installation sur un Mac Intel
description: Installation d'ALS sur Mac Intel
author: ALZ Team

lastmod: 2026-06-10T23:53:27Z
keywords: ["installation", "mac", "intel", "astro live stacker", "guide"]
weight: 100240
categories: ['procédures']
tags: ['installation', 'Mac', 'Intel Mac']
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
   - Recherchez l'image disque dont le nom commence par {{< als-code >}}als{{< /als-code >}} et se termine par {{< als-code >}}-amd64.dmg{{< /als-code >}}. Par exemple, cela pourrait être {{< als-code >}}als-v1.0-amd64.dmg{{< /als-code >}}.

3. **Monter l'image disque**
   - Double-cliquez sur l'image disque {{< als-code >}}als-v1.0-amd64.dmg{{< /als-code >}}. Cela montera l'image disque.
   - Une nouvelle fenêtre Finder affichera le contenu de l'image disque. Vous verrez l'icône de l'application {{< als-code >}}ALS{{< /als-code >}} à gauche et un raccourci vers le dossier {{< als-code >}}Applications{{< /als-code >}} du système à droite.

4. **Copier l'application dans le dossier Applications**
   - Faites glisser l'icône de l'application {{< als-code >}}ALS{{< /als-code >}} de la fenêtre du Finder vers le raccourci {{< als-code >}}Applications{{< /als-code >}} dans la même fenêtre.
   - Si vous y êtes invité, entrez votre mot de passe administrateur pour autoriser cette opération.

5. **Gérer les permissions de l'app**
   - macOS versions antérieures à Catalina (10.15)
     - Une boîte de dialogue s'affichera, indiquant que l'application provient d'un développeur inconnu. Cliquez sur "Ouvrir" pour confirmer.
     - Une fois que l'application est autorisée, double-cliquez à nouveau sur l'application {{< als-code >}}ALS{{< /als-code >}} dans le dossier {{< als-code >}}Applications{{< /als-code >}} pour la lancer.
   - macOS Catalina (10.15) jusqu'à Sonoma (14.x.x)
     - Une boîte de dialogue s'affichera, indiquant que l'application ne peut pas être ouverte car elle provient d'un développeur inconnu. Cliquez sur "Annuler".
     - Allez dans "Préférences Système" > "Sécurité et confidentialité" > "Général", puis cliquez sur "Ouvrir quand même" à côté du message concernant {{< als-code >}}ALS{{< /als-code >}}.
     - Confirmez en cliquant à nouveau sur "Ouvrir" dans la nouvelle boîte de dialogue qui s'affiche.
     - Une fois que l'application est autorisée, double-cliquez à nouveau sur l'application {{< als-code >}}ALS{{< /als-code >}} dans le dossier {{< als-code >}}Applications{{< /als-code >}} pour la lancer.
   - macOS Sequoia (15.x.x)
     - Ouvrez le Finder et allez dans le dossier {{< als-code >}}Applications{{< /als-code >}}
     - Ensuite, allez dans le sous-dossier {{< als-code >}}Utilitaires{{< /als-code >}}.
     - Dans ce sous-dossier, double-cliquez sur l'application {{< als-code >}}Terminal{{< /als-code >}} pour l'ouvrir.
     - Dans la fenêtre du Terminal, tapez la commande suivante
     
       {{< als-code >}}sudo xattr -r -d com.apple.quarantine /Applications/als.app{{< /als-code >}}
     - Appuyez sur {{< als-ks >}}Entrée{{< /als-ks >}}. Entrez votre mot de passe si vous y êtes invité et appuyez à nouveau sur {{< als-ks >}}Entrée{{< /als-ks >}}.

6. **Lancement d'ALS**
     - Accédez au dossier {{< als-code >}}Applications{{< /als-code >}}, puis double-cliquez sur l'application {{< als-code >}}ALS{{< /als-code >}} pour l'exécuter.

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 
