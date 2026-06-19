---
title: Notes de versions
description: Notes de version d'ALS
author: ALS Team
lastmod: 2026-06-19T03:10:11Z
keywords: [ 'Notes de version ALS' ]
weight: 100550
---

## Version 1.0 {#1.0}

**Date:** bientôt :)

### Nouveautés

- Interface sombre unifiée
- Ajustement de la saturation des couleurs
- Calibration par flat
- Rejet des valeurs aberrantes par écrêtage sigma lors de l'empilement en mode moyenne, uniquement avec le profil Photo
- Vérification optionnelle au démarrage d'une nouvelle version d'ALS disponible

### Améliorations

- Les données d'image FITS stockées dans des extensions Image ou d'image compressée sont maintenant prises en charge

### Corrections

- L'arrêt d'une session vide pouvait enregistrer une image finale horodatée
- Certaines transitions de session étaient loggées de manière incorrect
- La détection de la langue du système ne fonctionnait pas sur les systèmes macOS
- Les sélecteurs de fichiers sur macOS pouvaient afficher certains dossiers comme étant vides
- Le démarrage du serveur d'images pouvait bloquer l'interface
- Le serveur d'images n'affichait pas son image d'attente lorsqu'il était démarré avant une session
- L'alignement progressif pouvait produire des artefacts rectangulaires imbriqués après d'importantes rotations du champ
- Le profil Visuel assisté pouvait tenter de lire les brutes avant la fin de leur écriture sur le stockage
- Les brutes de taille nulle pouvaient bloquer indéfiniment le prétraitement
- L'image et les données d'exposition du webview pouvaient rester périmées à cause de la mise en cache navigateur entre 
  deux brutes.

---

## Version 0.7.1 {#0.7.1}

**Date :** 31 mai 2026

### Améliorations

- Le serveur d'images est maintenant accessible lorsque le système exécutant ALS fait aussi office de hotspot ou dispose de plusieurs connexions réseau.

---

## Version 0.7 {#0.7}

**Date:** 27 octobre 2025

### Nouveautés

- Linux : Utilitaire pour la création d'un lanceur système
- Envoi de statistiques d'utilisation avec le consentement de l'utilisateur
- Lecture des fichiers .CR3 Canon
- Introduction des profils (paramètres par défaut pour visuel assisté ou photo)
- Ajout d'un affichage de code QR menant au serveur web intégré
- Ajout de la lecture des fichiers jpeg, png et tiff
- Traductions française et russe
- Soustraction de darks
- Suppression des pixels chauds
- Mode nuit

### Améliorations

- Amélioration du serveur web : mode plein écran, pan & zoom, actualisation uniquement lors de changements
- Windows : ALS est maintenant livré sous la forme d'un installeur
- Amélioration de l'autostretch
- Amélioration du zoom avec réinitialisation aux paramètres par défaut et raccourcis clavier
- Enregistrement des journaux dans le dossier personnel de l'utilisateur
- Possibilité d'afficher uniquement les problèmes dans le journal de session
- Capacité à surcharger manuellement le modèle Bayer utilisé pour le dématriçage
- Le nombre minimum de similitudes pour l'alignement est définissable par l'utilisateur
- Écriture du contenu web dans un dossier spécifique
- Les informations critiques de la session sont déplacées dans la barre d'état pour qu'elles soient toujours visibles
- Mode nuit commutable

### Corrections

- Windows : échec de l'écriture des images vers des chemins contenant des caractères non-ascii
- Prise en charge des FITS avec extension .fts
- RPI : crash lors de l'enregistrement des images en noir et blanc

---

## Version 0.6.1

**Date:** 18 novembre 2019

### Corrections

- Dématriçage défectueux des images prises avec des appareils photo ayant un modèle CFA GBRG

---

## Version 0.6

**Date:** 14 novembre 2019

### Nouveautés

- Boîte de dialogue des paramètres utilisateur
- Pan et zoom dans l'image avec clics de souris et la molette
- Deux méthodes de réglage automatique de la luminosité au choix
- Affichage de l'histogramme
- Équilibre des couleurs RVB

### Améliorations

- Le port du serveur d'images est configurable
- La page du serveur d'images est actualisée automatiquement avec une période de temps configurable
- Mémorisation de la taille et de la position de la fenêtre
- Type de fichier d'enregistrement d'image configurable
- La fenêtre de journal, les contrôles de session et les contrôles de traitement peuvent être masqués
- Mode plein écran
- Interface graphique beaucoup plus réactive

### Corrections

- Crash si de nouvelles images sont écrites sur un périphérique de stockage lent
- Image servie par le serveur web trop lumineuse
- Crash si la nouvelle image ne peut pas être alignée avec la pile actuelle
- Crash si une nouvelle session est démarrée alors que le dossier scan est manquant

---

## Version 0.5

**Date:** 10 juillet 2019

### Nouveautés

- L'image empilée peut être servie par le nouveau serveur web intégré

---

## Version 0.4

**Date:** 22 juin 2019

### Nouveautés

- Nouveau processeur d'images empilées : Ondelettes

---

## Version 0.3

**Date:** 23 mai 2019

### Nouveautés

- Prise en charge des fichiers Raw DSLR courants
- Le scanner de dossiers peut être mis en pause
- Bouton de réinitialisation des contrôles de traitement d'image
- Nouveau processeur d'images empilées : SCNR

---

## Version 0.2

**Date:** 21 mai 2019

### Nouveautés

- Le contraste et la luminosité des images empilées peuvent être ajustés

---

## Version 0.1

**Date:** 18 mai 2019

### Première release

- Alignement et empilement des fichiers Fits
