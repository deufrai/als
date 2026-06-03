---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"
lastmod: 2026-06-03T19:59:26Z
keywords: [ "Premier démarrage d'ALS" ]
draft: false
type: "docs"
categories: [ "bien débuter" ]
tags: [ "linux", "dossier scanné", "session", "dossier de travail"  ]
weight: 100280
---

# Introduction {#introduction}

À la fin de ce chapitre, vous aurez :

- Configuré les seuls paramètres requis pour un démarrage rapide.
- Lancé votre première session d'empilement et obtenu vos premiers résultats.

# Configuration initiale {#initial-configuration}

Lors du premier démarrage, ALS vous présente les étapes de configuration requises avant de débuter :

ALS a besoin de connaître le chemin de deux **dossiers critiques** :

- Le **dossier scanné** : Le dossier où ALS surveille l'arrivée de nouvelles brutes.
- Le **dossier de travail** : Le dossier où ALS enregistre les images produites.

{{< center >}}
{{< figure src="welcome.png"
caption="Écran d'accueil ALS avec les options de configuration"
width="787px"
height="461px"
alt="Écran d'accueil ALS avec les options de configuration" >}}
{{< /center >}}

Vous avez deux options :

## Configuration par défaut {#default-configuration}

- 🖱️ Cliquez sur le bouton de gauche pour laisser ALS créer les 2 dossiers sur **votre bureau** puis démarrer l'application

## Configuration personnalisée {#custom-configuration}

- 🖱️ Cliquez sur le bouton de droite pour choisir des dossiers personnalisés

{{< center >}}
{{< figure src="custom_config.png"
caption="Écran de configuration personnalisée des dossiers"
width="787px"
height="461px"
alt="Écran de configuration personnalisée des dossiers" >}}
{{< /center >}}

- 🖱️ Cliquez sur les deux boutons pour sélectionner le **dossier scanné** et le **dossier de travail** qu'ALS utilisera

Vous pouvez sélectionner ou créer n'importe quel dossier sur votre système, mais nous recommandons d'utiliser des
dossiers situés sur un disque rapide

- 🖱️ Une fois les deux dossiers définis, cliquez sur `GO !` pour démarrer l'application

# Votre toute première session {#your-very-first-session}

{{< center >}}
{{< figure src="ready.png"
caption="ALS prêt à démarrer sa toute première session"
width="1388px"
height="761px"
alt="Fenêtre principale d'ALS montrant une interface logicielle pour empiler des images astronomiques en temps réel. L'interface comprend des sections pour les contrôles principaux (démarrer, pause, arrêter), les paramètres d'empilement (aligner, seuil), le serveur d'images (démarrer, arrêter), la sauvegarde d'images (sauvegarder l'image actuelle, sauvegarder chaque image), les modules (taille de la file d'attente, statut), le traitement (histogramme, étirement automatique, niveaux, balance RGB) et le journal de session." >}}
{{< /center >}}

## Démarrage de la session {#starting-the-session}

{{< center >}}
{{< figure src="start.png"
caption="Le bouton de démarrage de session"
width="300px"
height="129px"
alt="Section des contrôles principaux d'ALS avec la sous-section Session, montrant les boutons START, PAUSE et STOP. Le bouton START est surligné avec une flèche rouge pointant vers lui. En dessous, des indicateurs pour la taille de la stack (0) et l'exposition de la pile (n/a) sont affichés. Le statut indique 'stoppée'." >}}
{{< /center >}}

🖱️ Cliquez sur `START` dans la section **session** en haut à gauche

--- 

ALS confirme le bon démarrage de la session :

{{< center >}}
{{< figure src="started.png"
caption="Le statut et les boutons de contrôle de la session sont mis à jour"
width="301px"
height="128px"
alt="Section des contrôles principaux d'ALS avec la sous-section Session, montrant les boutons START, PAUSE et STOP. En dessous de ces boutons, des indicateurs pour la taille de la stack (0) et l'exposition de la stack (n/a) sont affichés. Le statut indique 'démarrée' avec une flèche rouge pointant vers lui." >}}
{{< /center >}}

{{< center >}}
{{< figure src="status.png"
caption="Le **journal de session** affiche les derniers événements et la **barre de statut** est mise à jour"
width="978px"
height="166px"
alt="Journal de session affichant des messages d'information avec horodatages. Les entrées incluent 'Démarrage de nouvelle session...' 'Scanneur d'entrée démarré,' et 'Session démarrée en mode moyenne avec alignement True.' Des boutons étiquetés Acquitter, problèmes seuls, suivre. La barre de statut indique 'Session démarrée'." >}}
{{< /center >}}

--- 

🎛️ Démarrez maintenant les acquisitions avec votre système habituel. ALS détecte et traite chaque nouvelle brute détectée.

À titre d'exemple, nous allons illustrer les sections suivantes avec une session sur Messier 27 : caméra ZWO ASI224MC,
200 poses de 4 sec.

{{< center >}}
{{< figure src="stacked_01.png"
caption="ALS après traitement de la 1<sup>ère</sup> image"
width="1388px"
height="761px"
alt="Fenêtre principale d'ALS après le traitement de la première brute, affichant une image initiale et légèrement bruitée de la nébuleuse Messier 27 avec des étoiles éparpillées. Le journal de session montre des messages de traitement réussi. Le panneau de traitement sur la droite offre des ajustements de l'histogramme et des niveaux, l'équilibre RGB et les réglages d'étirement automatique." >}}
{{< /center >}}

{{% alert color="info" %}}
ℹ️ La première brute détectée sert de **référence d'alignement** pour toute la session
{{% /alert %}}

---

Toutes les nouvelles brutes sont d'abord alignées sur cette référence puis empilées par moyenne avec toutes
les brutes déjà traitées.

{{< center >}}
{{< figure src="stacked_15.png"
caption="ALS après traitement de la 15<sup>ème</sup> image. Le contraste et le bruit s'améliorent"
width="1388px"
height="761px"
alt="Fenêtre principale d'ALS après le traitement de la 15e brute, affichant une image moins bruitée et plus détaillée de la nébuleuse Messier 27 avec des étoiles éparpillées. Le journal de session montre des messages de traitement réussi. Le panneau de traitement sur la droite offre des ajustements de l'histogramme et des niveaux, l'équilibre RGB et les réglages d'étirement automatique." >}}
{{< /center >}}

Après chaque alignement et empilement d'une nouvelle brute, ALS ajuste automatiquement la luminosité et la balance
des couleurs avant d'afficher le résultat dans la **zone centrale**.

À mesure que vous empilez les brutes, vous verrez le résultat gagner en contraste et en détails. Et l'aspect
granuleux du fond de ciel s'estompera petit à petit.

---

## Partez à la découverte {#explore}

Laissez ALS travailler sur les brutes qui continuent d'arriver et perdez-vous un peu dans la **zone centrale** :

- 🖱️ Zoomez en utilisant la molette de votre souris
- 🖱️ Naviguez dans l'image en la faisant glisser, comme avec tout autre logiciel de visualisation
- 🖱️ Réinitialisez le zoom en cliquant avec le bouton droit de la souris dans l'image

L'image dans la **zone centrale** est mise à jour instantanément après le traitement de chaque nouvelle brute, sans
interrompre la navigation.

---

{{< center >}}
{{< figure src="stacked_200.png"
caption="ALS après traitement de la 200<sup>ème</sup> image. Une belle image, détaillée et lissée"
width="1388px"
height="761px"
alt="Fenêtre principale d'Astro Live Stacker (ALS) après le traitement de la 200e brute, affichant une image lisse, détaillée et à fort contraste de la nébuleuse Messier 27 avec de nombreuses étoiles. Le journal de session en bas montre des messages de traitement réussi et le panneau de sauvegarde d'images à gauche indique que les images ont été sauvegardées avec succès. Le panneau de droite comprend des options de traitement telles que les ajustements d'histogramme, l'étirement automatique, les niveaux et l'équilibre RGB." >}}
{{< /center >}}

Ce guide de démarrage rapide ne couvre pas les autres fonctionnalités et réglages d'ALS. Toutefois, ALS a été conçu pour
être très intuitif. N'hésitez pas à explorer et expérimenter les différents contrôles situés à droite de l'écran dans
la section **Traitements**.

---

## Arrêt de la session {#stopping-the-session}

Notre visite guidée express touche à sa fin, arrêtez la session en cours.

{{< center >}}
{{< figure src="stopping.png"
caption="Le bouton d'arrêt de session"
width="301px"
height="128px"
alt="Section des contrôles principaux dans l'interface du logiciel ALS, plus précisément la zone Session affichant les boutons START, PAUSE et STOP. Le bouton STOP est surligné avec une flèche rouge pointant vers lui. En dessous des boutons se trouvent la taille de la stack (200) et l'exposition de la stack (0:13:20). Le statut indique 'démarrée'." >}}
{{< /center >}}

🖱️ Cliquez sur `STOP` dans la section **session** en haut à gauche. Une fenêtre de confirmation apparaît...

---

{{< center >}}
{{< figure src="stop.png"
caption="Fenêtre de confirmation d'arrêt de session"
width="608px"
height="151px"
alt="Boîte de dialogue intitulée 'Arrêt de session,' demandant une confirmation pour arrêter la session en cours avec un message : 'Stopper la session courante remettra la stack et les traitements à zéro. Êtes-vous sûr de vouloir stopper la session courante ?' En dessous du message se trouvent une case à cocher intitulée 'Sauver image avant arrêt' et deux boutons intitulés 'Non' et 'Oui.' Le bouton 'Non' est surligné en rouge et le bouton 'Oui' est surligné en vert." >}}
{{< /center >}}

🖱️ Cliquez sur `Oui`

Vous retrouverez le résultat final de cette session dans le fichier nommé **stack_image.jpg** enregistré dans le
**dossier de travail**

---

{{% alert title="ℹ️ Systèmes Linux" color="info" %}}
Cette section s'adresse exclusivement aux utilisateurs d'ALS sous Linux, que ce soit sur PC ou Raspberry Pi
<details>
<summary>Création d'un lanceur système pour ALS</summary>

Cette étape optionnelle crée un lanceur dans le menu des applications de votre système, afin de démarrer ALS sans
parcourir le dossier d'installation à chaque fois.

🖱️ Ouvrez le menu **Utilitaires** d'ALS et sélectionnez **Créer lanceur**. Un sélecteur de fichier apparaît.

1. 🖱️ Naviguez vers le dossier où se trouve ALS
    - **PC**: Naviguez vers {{< als-code >}}/home/astrogeek/Applications/ALS{{< /als-code >}}
    - **Raspberry Pi**: Naviguez vers {{< als-code >}}/home/astrogeek/Applications/ALS/als-v1.0{{< /als-code >}}
2. 🖱️ Sélectionnez l'exécutable
    - **PC**: Sélectionnez le fichier {{< als-code >}}als-v1.0.run{{< /als-code >}}
    - **Raspberry Pi**: Sélectionnez le fichier {{< als-code >}}als-v1.0{{< /als-code >}}
3. 🖱️ Cliquez sur `Ouvrir`

ALS vous confirme la bonne création du lanceur

ALS est maintenant accessible depuis votre menu système, dans la section Graphisme

</details>
{{% /alert %}}

---

# Conclusion {#conclusion}

ALS est maintenant correctement configuré et prêt à traiter vos brutes avec ses paramètres par défaut

Vous avez aussi terminé votre première session d'empilement et obtenu votre premier résultat.

Prochaine étape : plonger dans le [guide utilisateur](../userguide/)
