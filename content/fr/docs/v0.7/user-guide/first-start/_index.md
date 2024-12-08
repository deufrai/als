---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"
lastmod: 2024-12-08T16:22:53Z
keywords: ["Premier démarrage d'ALS"]
draft: false
type: "docs"
tags: ['Config initiale', 'Premier Pas', 'Bases']
weight: 31
---

# Introduction

À la fin de ce chapitre, vous aurez :
- Configuré les seuls paramètres requis pour un démarrage rapide avec les réglages par défaut d'ALS.
- Lancé votre première session d'empilement et obtenu vos premiers résultats.

{{% alert title="ℹ️ INFO" color="info" %}}
N'oubliez pas de vous mettre <a href="/fr/docs/v0.7/user-guide/#dans-la-peau-du-personnage" target="_blank">dans la
peau du personnage</a> avant de suivre ce guide de démarrage 🌝
{{% /alert %}}

# Configuration minimale

Lors du premier démarrage, ALS vous accueille et vous demande de définir deux réglages essentiels :

- **Dossier scanné** : Le dossier où ALS surveille l'arrivée de nouvelles brutes.
- **Dossier de travail** : Le dossier où ALS enregistre les images produites.

{{< center >}}
{{< figure src="welcome.png" 
    caption="Message de bienvenue" 
    width="461px" 
    height="172px" 
    alt="Message de bienvenue" >}}
{{< /center >}}

🖱️ Cliquez sur `OK` pour accéder aux préférences.

---

## Configurer les dossiers critiques

Les dossiers critiques sont définis dans la section **Chemins** de l'onglet **Général**.

### Dossier scanné

Configurez ALS pour surveiller le dossier **astroshots** :

{{< center >}}
{{< figure src="prefs_01.png"
    caption="Bouton permettant de définir le **dossier scanné**"
    width="628px"
    height="254px"
    alt="Section chemins des préférences" >}}
{{< /center >}}


🖱️ Cliquez sur `Modifier...` à côté de **Dossier scanné**. Un sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_02.png" 
    caption="Le sélecteur de **dossier scanné**" 
    width="641px" 
    height="443px" 
    alt="Sélecteur du dossier scanné" >}}
{{< /center >}}

1. 🖱️ Sélectionnez le dossier **astroshots**.
2. 🖱️ Cliquez sur `Choisir`.

---

### Dossier de travail

Créez un sous-dossier pour ALS nommé **sorties_als** dans votre dossier personnel :

{{< center >}}
{{< figure src="prefs_03.png" 
    caption="Bouton permettant de définir le **dossier de travail**"
    width="628px" 
    height="263px" 
    alt="Section chemins des préférences" >}}
{{< /center >}}

🖱️ Cliquez sur `Modifier...` à côté de **Dossier de travail**. Un sélecteur de dossier apparaît...

---

{{< center >}}
{{< figure src="prefs_04.png" 
    caption="Bouton permettant de créer un nouveau dossier" 
    width="789px" 
    height="454px" 
    alt="Bouton créer un nouveau dossier" >}}
{{< /center >}}

🖱️ Cliquez sur `Créer un nouveau dossier`.

---

{{< center >}}
{{< figure src="prefs_05.png" 
    caption="Nouveau dossier prêt à être renommé" 
    width="641px" 
    height="443px" 
    alt="Renommage du nouveau dossier - étape 1" >}}
{{< /center >}}

Un nouveau dossier apparaît, prêt à être renommé.

---

{{< center >}}
{{< figure src="prefs_06.png"
    caption="nouveau dossier renommé et validation" 
    width="641px" 
    height="443px" 
    alt="Renommage du nouveau dossier - étape 2" >}}
{{< /center >}}

- ⌨️ Nommez-le **sorties_als**.
- 🖱️ Cliquez sur `Choisir`.

---

**ℹ️ Ne validez pas encore les préférences**, il reste un point important à aborder

---

## Statistiques d'utilisation

Il nous est très utile de savoir quelles versions d'ALS sont utilisées et sur quelle plateforme.

{{< center >}}
{{< figure src="prefs_07.png"
    caption="Case indiquant le choix d'envoi des statistiques d'utilisation" 
    width="628px" 
    height="607px" 
    alt="Ecran des préférences - Onglet général" >}}
{{< /center >}}

Nous vous serions très reconnaissants d'autoriser ALS à nous envoyer des statistiques d'utilisation, mais nous comprenons
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

- <a href="https://github.com/deufrai/als/blob/release/0.7/src/als/main.py#L46" target="_blank">code de l'envoi 
des statistiques par ALS</a> <i class="fa-brands fa-square-github"></i>
- <a href="https://github.com/deufrai/als-stats-receiver/blob/master/listen.py#L35" target="_blank">code de 
l'enregistrement des statistiques reçues par nos serveurs</a> <i class="fa-brands fa-square-github"></i>
</details>

---

🖱️ Cliquez ensuite sur `OK` pour valider les préférences.

---

# Votre toute première session

ALS est maintenant prêt à vous servir.

{{< center >}}
{{< figure src="ready.png"
    caption="ALS prêt à démarrer sa toute première session" 
    width="1920px" 
    height="1053px" 
    alt="Fenêtre principale d'ALS" >}}
{{< /center >}}

## Démarrage de la session

{{< center >}}
{{< figure src="start.png"
    caption="Le bouton de démarrage de session" 
    width="296px" 
    height="164px" 
    alt="Panneau de contrôle de session avant démarrage" >}}
{{< /center >}}

🖱️ Cliquez sur `START` dans la section **session** en haut à gauche

--- 

ALS confirme le bon démarrage de la session :

{{< center >}}
{{< figure src="started.png"
    caption="Le statut et les boutons de contrôle de la session sont mis à jour" 
    width="296px" 
    height="164px" 
    alt="Panneau de contrôle de session après démarrage" >}}
{{< /center >}}


{{< center >}}
{{< figure src="status.png"
    caption="Le **journal de session** affiche les derniers événements et la **barre de statut** est mise à jour" 
    width="864px" 
    height="178px" 
    alt="Journal de session" >}}
{{< /center >}}

--- 

🎛️ Démarrez maintenant les acquisitions avec votre système habituel. ALS détecte et traîte chaque nouvelle image capturée. 

{{< center >}}
{{< figure src="stacked_01.png"
    caption="ALS après traitement de la 1<sup>ère</sup> image" 
    width="1920px" 
    height="1053px" 
    alt="Fenêtre principale d'ALS - Stack 1" >}}
{{< /center >}}

La première image détectée par ALS sert de **référence pour l'alignement** des images suivantes.

---

Toutes les nouvelles images capturées sont d'abord alignées sur cette référence puis empilées par moyenne avec toutes 
les images déjà traitées.

{{< center >}}
{{< figure src="stacked_15.png"
    caption="ALS après traitement de la 15<sup>ème</sup> image. Le contraste et le bruit s'améliorent" 
    width="1920px" 
    height="1053px" 
    alt="Fenêtre principale d'ALS - Stack 15" >}}
{{< /center >}}

Après chaque alignement et empilement d'une nouvelle image, ALS ajuste automatiquement la luminosité et la balance 
des couleurs avant d'afficher le résultat dans la **zone centrale**. 

À mesure que vous empilez les images, vous verrez le résultat gagner en contraste et en détails. Et l'aspect
granuleux du fond de ciel s'estompera petit à petit.

---

## Partez à la découverte

Laissez ALS travailler sur les images qui continuent d'arriver et perdez-vous un peu dans la **zone centrale** :

- 🖱️ Zoomez en utilisant la molette de votre souris
- 🖱️ Naviguez dans l'image en la faisant glisser, comme avec tout autre logiciel de visualisation
- 🖱️ Réinitialisez le zoom en cliquant avec le bouton droit de la souris

L'image dans la zone centrale sera mise à jour instantanément après le traitement de chaque nouvelle brute, sans 
interrompre votre navigation.

---

{{< center >}}
{{< figure src="stacked_200.png"
    caption="ALS après traitement de la 200<sup>ème</sup> image. Une belle image, détaillée et lissée" 
    width="1920px" 
    height="1053px" 
    alt="Fenêtre principale d'ALS - Stack 200" >}}
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
    width="320px" 
    height="164px" 
    alt="Panneau de contrôle de session avant arrêt" >}}
{{< /center >}}

🖱️ Cliquez sur `STOP` dans la section **session** en haut à gauche. Une fenêtre de confirmation apparaît...

---

{{< center >}}
{{< figure src="stop.png"
    caption="Fenêtre de confirmation d'arrêt de session" 
    width="608px" 
    height="151px" 
    alt="Confirmation d'arrêt de session" >}}
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
    alt="Entrée de menu pour création du lanceur" >}}
{{< /center >}}

🖱️ Ouvrez le menu **Utilitaires** d'ALS et sélectionnez l'item **Créer lanceur**. Un sélecteur de fichier apparaît...

{{< center >}}
<div style="display: flex; justify-content: center; gap: 1rem;">
{{< figure src="exe_picker.png" 
    caption="Sélecteur de fichier pour **PC**" 
    width="661px" 
    height="463px" 
    alt="Sélecteur de fichier PC" >}}
{{< figure src="exe_picker_rpi.png" 
    caption="Sélecteur de fichier pour **Raspberry PI**" 
    width="661px" 
    height="463px" 
    alt="Sélecteur de fichier Raspberry Pi" >}}
</div>
{{< /center >}}

1. 🖱️ Naviguer vers le dossier où se trouve ALS
    - **PC**: Naviguer vers `/home/astrogeek/Applications/ALS`
    - **Raspberry PI**: Naviguer vers `/home/astrogeek/Applications/ALS/als-v0.7-beta7`
2. 🖱️ Sélectionner l'exécutable
    - **PC**: Sélectionner le fichier `als-v0.7-beta7.run`
    - **Raspberry PI**: Sélectionner le fichier `als-v0.7-beta7`
3. 🖱️ Clicker `Ouvrir`

ALS vous confirme la bonne création du lanceur
{{< center >}}
{{< figure src="launcher_created.png" 
    caption="Fenêtre de confirmation de création du lanceur" 
    width="391px" 
    height="129px" 
    alt="Fenêtre de confirmation de création du lanceur" >}}
{{< /center >}}

Vous pourrez maintenant facilement démarrer ALS en utilisant votre menu système
{{< center >}}
{{< figure src="launcher_ok.png" 
    caption="ALS dans la section **Graphisme** du menu système " 
    width="542px" 
    height="412px" 
    alt="Menu système" >}}
{{< /center >}}

</details>
{{% /alert %}}

---

# Conclusion

Nous espérons que ce chapitre vous a permis de démarrer ALS rapidement et de prendre en main les concepts de base 
d'une session de livestacking.

Prochaine étape : prise en main approfondie de l'interface graphique d'ALS


