---
title: Installation sur Raspberry Pi
description: Installation d'ALS sur Raspberry Pi
author: ALZ Team

lastmod: 2026-06-11T00:08:22Z
keywords: [ "installation", "raspberry pi", "linux", "astro live stacker", "guide" ]
weight: 100220
categories: ['procédures d’installation']
tags: ['linux', 'Raspberry Pi']
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

*_Les versions d'ALS proposées au téléchargement pour Raspberry Pi sont destinées aux systèmes en 64 bits.
Mais vous pouvez facilement adapter ce [script de build](https://github.com/deufrai/als/blob/release/1.0/ci/builds/build_dist_arm64_linux.sh)
pour packager une version d'ALS en 32 bits depuis les sources. L'unique contrainte forte est d'utiliser Python en version
3.6.x. N'hésitez pas à [nous contacter](mailto:support@als-app.org) 
si vous avez besoin d'aide._

# 📦 Installation

1. **Ouvrir le dossier de téléchargements**
    - Accédez à votre dossier de téléchargements. Vous pouvez généralement le trouver en cliquant sur l'icône de votre
      gestionnaire de fichiers (par exemple, PCManFM) et en sélectionnant "Téléchargements" dans le menu de navigation à
      gauche.

2. **Identifier l'archive ALS**
    - Recherchez l'archive dont le nom commence par {{< als-code >}}als{{< /als-code >}} et se termine par {{< als-code >}}.tgz{{< /als-code >}}. Par exemple, cela pourrait être
      {{< als-code >}}als-v1.0.tgz{{< /als-code >}}.

3. **Extraire l'archive**
    - Pour extraire l'archive, vous pouvez utiliser un gestionnaire de fichiers :
        - Faites un clic droit sur l'archive {{< als-code >}}als-v1.0.tgz{{< /als-code >}}.
        - Sélectionnez "Extraire ici" ou une option similaire.

4. **Déplacer ALS vers un emplacement permanent**

   **Pourquoi déplacer ALS en dehors du dossier de téléchargements ?**

   Déplacer ALS dans un répertoire dédié permet de mieux organiser vos fichiers et d'assurer que l'application est
   installée dans un emplacement stable et permanent. Le dossier de téléchargements est souvent utilisé pour des
   fichiers temporaires et peut être nettoyé régulièrement, entraînant la suppression accidentelle de fichiers
   importants. En créant un dossier spécifique pour ALS, vous vous assurez que l'application reste accessible et en
   sécurité.

    - Ouvrez votre gestionnaire de fichiers (par exemple, PCManFM).
    - Accédez à votre répertoire personnel ({{< als-code >}}/home/nom_utilisateur{{< /als-code >}}).
    - Faites un clic droit dans le répertoire et sélectionnez "Créer un nouveau dossier".
    - Nommez le dossier {{< als-code >}}Applications{{< /als-code >}} et appuyez sur "Entrée".
    - Double-cliquez sur le dossier {{< als-code >}}Applications{{< /als-code >}} pour l'ouvrir.
    - Créez un autre dossier à l'intérieur appelé {{< als-code >}}ALS{{< /als-code >}} et appuyez sur "Entrée".
    - Accédez au dossier de téléchargements ({{< als-code >}}Téléchargements{{< /als-code >}}) dans une autre fenêtre de votre gestionnaire de
      fichiers. Il est important d'avoir deux fenêtres distinctes et visibles pour pouvoir glisser facilement les
      fichiers.
    - Trouvez le dossier {{< als-code >}}als-v1.0{{< /als-code >}} dans le dossier de téléchargements, puis faites glisser ce dossier dans le
      dossier {{< als-code >}}ALS{{< /als-code >}} ({{< als-code >}}/home/nom_utilisateur/Applications/ALS{{< /als-code >}}).

5. **Lancer l'exécutable**
    - Accédez au dossier {{< als-code >}}als-v1.0{{< /als-code >}} dans le gestionnaire de fichiers.
    - Faites un double clic sur le fichier {{< als-code >}}als-v1.0{{< /als-code >}}.
    - Si une boîte de dialogue apparaît vous demandant de confirmer l'exécution, choisissez l'option pour exécuter ou
      ouvrir le fichier.

Prochaine étape : Le guide de [premier démarrage](../quickstart/). 
