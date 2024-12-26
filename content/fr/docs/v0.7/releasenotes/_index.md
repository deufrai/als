---
title: Notes de versions
description: Notes de version d'ALS
author: ALS Team
lastmod: 2024-12-26T19:27:46Z
keywords: [ 'Notes de version ALS' ]
tags: [ 'release' ]
weight: 550
---

## Version 0.7

**Date:** À déterminer

### Nouveautés

- Linux : Utilitaire pour la création d'un lanceur système
- Envoi de statistiques d'utilisation avec le consentement de l'utilisateur
- Lecture des fichiers .CR3 Canon Raw
- Introduction des profils (paramètres par défaut pour visuel assisté ou photo)
- Ajout d'un affichage de code QR menant au serveur web intégré
- Ajout de la lecture des fichiers jpeg, png et tiff
- Traduction française
- Soustraction de darks
- Suppression des pixels chauds
- Mode nuit

### Améliorations

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
