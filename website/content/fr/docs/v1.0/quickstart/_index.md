---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"
lastmod: 2025-11-25T18:50:31Z
keywords: [ "Premier démarrage d'ALS" ]
draft: false
type: "docs"
categories: [ "bien débuter" ]
tags: [ "linux", "dossier scanné", "session", "dossier de travail"  ]
weight: 100280
---

# Introduction

À la fin de ce chapitre, vous aurez :

- Configuré les seuls paramètres requis pour un démarrage rapide avec les réglages par défaut d'ALS.
- Lancé votre première session d'empilement et obtenu vos premiers résultats.

# Dans la peau du personnage... {#character}

Tout au long de ce voyage, vous incarnerez un nouvel utilisateur d'ALS :

- **Nom d'utilisateur**&nbsp;: Votre nom d'utilisateur est **astrogeek**
- **Système utilisé**&nbsp;: Vous utilisez ALS sur un système Linux
- **Organisation des brutes**&nbsp;: votre système d'acquisition enregistre les brutes dans le dossier **astroshots** de
  votre dossier personnel, organisées par cible avec les brutes dans des sous-dossiers **Light**.

  Exemple : Session sur Messier 27, les brutes sont enregistrées dans le dossier **astroshots/M_27/Light**.

{{< center >}}
{{< figure
src="lights_placement.png"
width="888px" height="484px"
caption="Emplacement des brutes"
alt="Fenêtre du gestionnaire de fichiers affichant le sous-dossier Light dans le répertoire astroshots/M_27/Light, montrant huit fichiers FITS." >}}
{{< /center >}}

# Configuration initiale

Lors du premier démarrage, ALS vous accueille et vous demande de définir deux réglages essentiels :

- **Dossier scanné** : Le dossier où ALS surveille l'arrivée de nouvelles brutes.
- **Dossier de travail** : Le dossier où ALS enregistre les images produites.

{{< center >}}
{{< figure src="welcome.png"
caption="Message de bienvenue"
width="461px"
height="172px"
alt="Boîte de dialogue de bienvenue pour ALS avec un texte indiquant qu'il s'agit de la première utilisation de l'utilisateur et des instructions pour définir les chemins des dossiers scanné et de travail. Un bouton OK est en bas à droite." >}}
{{< /center >}}

🖱️ Cliquez sur `OK` pour accéder aux préférences.

---

## Configurer les dossiers critiques

Les dossiers critiques pour le fonctionnement d'ALS sont :

- Le **Dossier scanné** : ALS surveille l'arrivée de nouvelles brutes dans ce dossier.
- Le **Dossier de travail** : ALS enregistre les images produites dans ce dossier.

### Dossier scanné

{{% alert color="info" %}}
ℹ️ La détection fonctionne, quelle que soit la structure des sous-dossiers à l'intérieur du **dossier scanné**.
{{% /alert %}}

Configurez ALS pour surveiller le dossier **astroshots** :

{{< center >}}
{{< figure src="prefs_01.png"
caption="Bouton permettant de définir le **dossier scanné**"
width="623px"
height="240px"
alt="Capture d'écran des préférences ALS montrant l'onglet Général. Une flèche rouge pointe vers le bouton Dossier scanné..." >}}
{{< /center >}}

🖱️ Cliquez sur `Dossier scanné...`. Un sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_02.png"
caption="Le sélecteur de **dossier scanné**"
width="641px"
height="443px"
alt="Boîte de dialogue de sélection de fichier intitulée 'Sélectionner dossier scanné' avec le dossier astroshots surligné sous le répertoire de l'utilisateur astrogeek. Le bouton Choisir est surligné, indiquant que l'utilisateur est sur le point de confirmer la sélection." >}}
{{< /center >}}

1. 🖱️ Sélectionnez le dossier **astroshots**.
2. 🖱️ Cliquez sur `Choisir`.

---

### Dossier de travail

Créez un sous-dossier pour ALS nommé **sorties_als** dans votre dossier personnel :

{{< center >}}
{{< figure src="prefs_03.png"
caption="Les réglages de l'enregistrement d'images"
width="622px"
height="332px"
alt="Capture d'écran montrant l'onglet Sortie dans les préférences ALS. La section Dossiers de sortie comprend un bouton Dossier de travai... pour le configurer" >}}
{{< /center >}}

1. 🖱️ Basculez vers l'onglet **Sortie**
2. 🖱️ Cliquez `Dossier de travail...`. Un sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_04.png"
caption="Bouton permettant de créer un nouveau dossier"
width="789px"
height="454px"
alt="Boîte de dialogue de sélection de fichier intitulée 'Sélectionner le dossier de travail' affichant le contenu du répertoire /home/astrogeek, montrant divers dossiers et un fichier journal. Une flèche rouge pointe vers le bouton 'Créer un nouveau dossier', indiquant l'option de créer un nouveau dossier." >}}
{{< /center >}}

🖱️ Cliquez sur `Créer un nouveau dossier`.

---

{{< center >}}
{{< figure src="prefs_05.png"
caption="Nouveau dossier prêt à être renommé"
width="641px"
height="443px"
alt="Boîte de dialogue de sélection de fichier intitulée 'Sélectionner le dossier de travail' affichant le contenu du répertoire /home/astrogeek. Un nouveau dossier nommé 'Nouveau Dossier' est surligné en bleu, prêt à être renommé. La partie inférieure de la boîte de dialogue comporte des champs pour le répertoire et le type de fichiers, avec des boutons intitulés Choisir et Annuler." >}}
{{< /center >}}

Un nouveau dossier apparaît, prêt à être renommé.

---

{{< center >}}
{{< figure src="prefs_06.png"
caption="nouveau dossier renommé et validation"
width="641px"
height="443px"
alt="Boîte de dialogue de sélection de fichier intitulée 'Sélectionner le dossier de travail' affichant le contenu du répertoire /home/astrogeek, y compris plusieurs dossiers et un fichier journal. Le nouveau dossier nommé als_output est surligné, et le bouton Choisir est surligné, indiquant que l'utilisateur est sur le point de confirmer la sélection." >}}
{{< /center >}}

1. ⌨️ Nommez-le {{< als-code >}}sorties_als{{< /als-code >}}
2. 🖱️ Cliquez sur `Choisir`

🖱️ Revenez à l'onglet **Général**.



{{% alert color="warning" %}}
**⚠️ Ne validez pas encore les préférences**, il reste un point important à aborder :
{{% /alert %}}

## Statistiques d'utilisation {#usage-stats}

Il nous est très utile de savoir quelles versions d'ALS sont utilisées et sur quelle plateforme.

{{< center >}}
{{< figure src="prefs_07.png"
caption="Case indiquant le choix d'envoi des statistiques d'utilisation"
width="622px"
height="660px"
alt="Capture d'écran des préférences ALS montrant l'onglet Général. La section Données est mise en une flèche rouge pointe vers une case servant à activer les Statistiques d'utilisation." >}}
{{< /center >}}

Nous vous serions très reconnaissants d'autoriser ALS à nous envoyer des statistiques d'utilisation, mais nous
comprenons
également que vous puissiez être réticent à autoriser une telle fonctionnalité.

Sachez que :

- ALS nous enverra **uniquement** les informations suivantes à chaque démarrage :
    - Version d'ALS.
    - Type de processeur.
    - Type de système d'exploitation.
- Nous ne cherchons pas à identifier ni géo-localiser la source de ces informations

<details>
    <summary>Cliquez ici pour savoir comment vous pouvez vérifier ces affirmations par vous-même</summary>

ALS et nos outils de suivi sont des logiciels **opensource**, leur code source est disponible publiquement.

- <a href="https://github.com/deufrai/als/blob/release/1.0/src/als/main.py#L46" target="_blank">code de l'envoi
  des statistiques par ALS</a> <i class="fa-brands fa-square-github"></i>
- <a href="https://github.com/deufrai/als-stats-receiver/blob/master/listen.py#L35" target="_blank">code de
  l'enregistrement des statistiques reçues par nos serveurs</a> <i class="fa-brands fa-square-github"></i>

</details>

---

🖱️ Votre choix fait, cliquez sur `OK` pour valider les préférences.

---

# Votre toute première session

{{< center >}}
{{< figure src="ready.png"
caption="ALS prêt à démarrer sa toute première session"
width="1388px"
height="761px"
alt="Fenêtre principale d'ALS montrant une interface logicielle pour empiler des images astronomiques en temps réel. L'interface comprend des sections pour les contrôles principaux (démarrer, pause, arrêter), les paramètres d'empilement (aligner, seuil), le serveur d'images (démarrer, arrêter), la sauvegarde d'images (sauvegarder l'image actuelle, sauvegarder chaque image), les modules (taille de la file d'attente, statut), le traitement (histogramme, étirement automatique, niveaux, balance RGB) et le journal de session." >}}
{{< /center >}}

## Démarrage de la session

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
alt="Journal de session affichant des messages d'information avec horodatages. Les entrées incluent 'Démarrage de nouvelle session...' 'Scanneur d'entrée démarré,' et 'Session démarrée en mode moyenne avec alignement True.' Des boutons étiquetés Acquitter, problèmes seuls, suivre. La barre de status indique 'Session démarrée'." >}}
{{< /center >}}

--- 

🎛️ Démarrez maintenant les acquisitions avec votre système habituel. ALS détecte et traîte chaque nouvelle brute détectée.

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

## Partez à la découverte{#explore}

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

## Arrêt de la session

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

{{< center >}}
{{< figure src="launcher_menu.png"
caption="Menu de création du lanceur"
width="537px"
height="194px"
alt="L'image montre une capture d'écran d'une interface logicielle avec un thème sombre. La barre de menu supérieure comprend des options telles que Fichier, Session, Édition, Image, Vue, Utilitaires et Aide. Le menu Utilitaires est développé, révélant deux options : QR Code et Créer lanceur, avec ce dernier surligné en bleu et un curseur pointant vers lui." >}}
{{< /center >}}

🖱️ Ouvrez le menu **Utilitaires** d'ALS et sélectionnez l'item **Créer lanceur**. Un sélecteur de fichier apparaît...

1. 🖱️ Naviguer vers le dossier où se trouve ALS
    - **PC**: Naviguer vers {{< als-code >}}/home/astrogeek/Applications/ALS{{< /als-code >}}
    - **Raspberry PI**: Naviguer vers {{< als-code >}}/home/astrogeek/Applications/ALS/als-v1.0{{< /als-code >}}
2. 🖱️ Sélectionner l'exécutable
    - **PC**: Sélectionner le fichier {{< als-code >}}als-v1.0.run{{< /als-code >}}
    - **Raspberry PI**: Sélectionner le fichier {{< als-code >}}als-v1.0{{< /als-code >}}
3. 🖱️ Cliquez sur `Ouvrir`

ALS vous confirme la bonne création du lanceur
{{< center >}}
{{< figure src="launcher_created.png"
caption="Fenêtre de confirmation de création du lanceur"
width="391px"
height="129px"
alt="Fenêtre de notification avec le titre 'Lanceur ALS créé / mis à jour avec succès.' La notification contient une icône d'ampoule et le texte 'Vous trouverez ALS avec les applications graphiques.' Il y a un bouton 'OK' en bas à droite de la fenêtre." >}}
{{< /center >}}

Vous pourrez maintenant facilement démarrer ALS en utilisant votre menu système
{{< center >}}
{{< figure src="launcher_ok.png"
caption="ALS dans la section **Graphisme** du menu système "
width="542px"
height="412px"
alt="L'image montre une section d'un écran d'ordinateur affichant le menu 'Applications', mettant en évidence la catégorie 'Graphisme'. Le menu répertorie diverses applications liées aux graphismes disponibles sur le système, y compris Astro Live Stacker - Live Stacking Made in France. Le curseur pointe vers la catégorie 'Graphismes', indiquant qu'elle est actuellement sélectionnée." >}}
{{< /center >}}

</details>
{{% /alert %}}

---

# Conclusion

ALS est maintenant correctement configuré et prêt à traiter vos brutes avec ses paramètres par défaut

Vous avez aussi terminé votre première session d'empilement et obtenu votre premier résultat.

Prochaine étape : plonger dans le guide utilisateur
