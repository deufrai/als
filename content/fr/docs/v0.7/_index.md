---
title: "Documentation"
lastmod: 2024-11-29T01:49:30Z
description: "Astro Live Stacker."
type: "docs"
weight: 1
---

# 🔭 Vue d'ensemble d'ALS

{{< center >}}
{{< figure src="/images/docs/fr/als_doc_screenshot.png" >}}
{{< /center >}}


ALS est une application de livestacking d'astrophotographie

---

# 🖥️ Configuration système requise

Bonne nouvelle : ALS n’est pas trop gourmand en ressources.

## Ordinateurs de bureau et portables
- Rien de spécial, vraiment. N'importe quel système moderne fera l'affaire.

## Raspberry Pi
- Raspberry Pi 4 minimum
- 4 Go de RAM minimum

Cependant, on n'a jamais trop de puissance CPU et de RAM. Plus il y en a mieux c'est ! Cela rendra ALS plus fluide. 😊

---

# 🆕 Notes de version

## Version 0.7

### Nouveautés
- Envoi de statistiques d'utilisation avec le consentement de l'utilisateur
- Lecture des fichiers .CR3 Canon Raw
- Introduction des profils (paramètres par défaut pour Visuel assisté & Photo)
- Ajout d'un affichage de QR code menant au serveur WEB intégré
- Ajout de la lecture des fichiers jpeg, png et tiff
- Traduction française
- Soustraction de darks
- Suppression des pixels chauds
- Mode nuit 

### Améliorations
- Meilleur autostretch
- Amélioration du zoom avec réinitialisation aux paramètres par défaut et raccourcis clavier
- Enregistrement de journaux dans le dossier personnel de l'utilisateur
- Capacité à n'afficher que les problèmes dans le journal de session
- Capacité à surcharger manuellement le modèle Bayer utilisé pour le dématriçage
- Le nombre minimum de similitudes pour l'alignement est définissable par l'utilisateur
- Écriture du contenu web dans un dossier spécifique
- Les informations critiques de la session sont déplacées dans la barre d'état pour qu'elles soient toujours visibles
- Mode nuit commutable

### Corrections
- Windows : échec de l'écriture des images vers des chemins contenant des caractères non-ascii
- Prise en charge des FITS avec extension .fts
- RPI : crash lors de l'enregistrement des images en noir et blanc

## Version 0.6.1 (2019-11-18)

### Corrections
- Dématriçage défectueux des images prises avec des appareils photo ayant un modèle CFA GBRG

## Version 0.6 (2019-11-14)

### Nouveautés
- Boîte de dialogue des paramètres utilisateur
- Pan et zoom dans l'image avec clics de souris et la molette
- 2 méthodes de réglage automatique de la luminosité au choix
- Affichage de l'histogramme
- Équilibre des couleurs RGB

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

## Version 0.5 (2019-07-10)

### Nouveautés
- L'image empilée peut être servie par le nouveau serveur web intégré

## Version 0.4 (2019-06-22)

### Nouveautés
- Nouveau processeur d'images empilées : Ondelettes

## Version 0.3 (2019-05-23)

### Nouveautés
- Prise en charge des fichiers Raw DSLR courants
- Le scanner de dossiers peut être mis en pause
- Bouton de réinitialisation des contrôles de traitement d'image
- Nouveau processeur d'images empilées : SCNR

## Version 0.2 (2019-05-21)

### Nouveautés
- Le contraste et la luminosité des images empilées peuvent être ajustés

## Version 0.1 (2019-05-18)

### Première release
- Alignement et empilement des fichiers Fits
