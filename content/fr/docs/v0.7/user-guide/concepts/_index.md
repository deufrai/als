---
title: "Concepts de base"
description: "Les concepts de base d'ALS"
author: "ALS Team"

lastmod: 2024-12-28T07:20:57Z
keywords: ["concepts ALS"]
draft: false
type: "docs"
tags: ["Bases"]
weight: 315
---

# Introduction

À la fin de ce chapitre, l'architecture et les concepts de base d'ALS n'auront plus de secret pour vous. 

# Modules

ALS adopte une architecture modulaire. Les modules partages les resources de votre ordinateur pour garantir la 
fluidité de l'application

Les modules d'ALS sont divisés en deux catégories :

## Modules principaux

ALS utilise 4 modules de traitements principaux organisés dans cet ordre :

- [Pre-process](#pre-process-module)
- [Stack](#stack-module)
- [Process](#process-module)
- [Sauvegarde](#save-module)

Chacun de ces modules possède sa propre file d'attente et exécute les actions suivantes, en boucle :
1. Attend qu'une nouvelle image soit ajoutée à la file d'attente
2. Traite l'image
3. Ajoute l'image traitée à la file d'attente du module suivant

Entrons maintenant dans les détails de chacun des modules principaux :

### Pre-process {#pre-process-module}

Dès qu'une nouvelle image est détectée dans le **dossier scanné**, elle est ajoutée à la file d'attente de ce module.

Le module de **pre-process** applique sur chaque image les pré-traitements habituels en astrophoto :

1. **Suppression des pixels chauds**

   Remplace la valeur des pixels chauds par la valeur moyenne des pixels voisins.

2. **Soustraction de master dark**

   Utilise un master dark fourni par l'utilisateur pour soustraire le bruit thermique de l'image. 

   Si le format de données du master dark est différent de celui de l'image à traiter, le master dark est
   converti à la volée avant son utilisation. (_ex. : master dark en nombres flottants et brutes en entiers_)

3. **Dématriçage**

   Les images couleur au format FITS ou Raw sont converties en couleur RVB en utilisant la matrice de Bayer décrite 
   dans les entêtes du fichier.

   <details>
     <summary>Cliquer ici pour des détails sur les entêtes utilisés</summary>

     - Fichier FITS : Entête FITS **BAYERPAT**
     - Fichier Raw : Entête EXIF standard

   </details>

### Stack {#stack-module}

Prend en charge l'alignement et l'empilement des images et maintient la stack courante.

1. **Alignement**
    - Calcule les transformations à appliquer à l'image pour l'aligner sur la référence de la session
    - Applique ces transformations à l'image
2. **Empilement**
    - Ajoute l'image à la stack courante
    - Calcule l'image résultante en fonction du mode d'empilement choisi

### Process {#process-module}

Module de traitement d'image proprement dit. Il applique les traitements suivants :

1. **Auto stretch**

   Ajuste automatiquement les niveaux de l'image pour une visualisation optimale

2. **Niveaux**

   Permet de régler l'écrêtage des noirs et des blancs, et le niveau des tons moyens de l'image

3. **Balance RVB**

   Permet de régler la balance des couleurs de l'image

### Sauvegarde {#save-module}

Module en charge de l'enregistrement sur disque des images traitées.

Après le traitement de chaque nouvelle image, ALS enregistre l'image de la zone centrale dans un fichier du
**dossier de travail** :

- **nom du fichier** : **stack_image**

  Le fichier est écrasé à chaque nouvelle image traitée.

- **Type et extension du fichier** : en fonction du format d'enregistrement choisi dans
  les [Préférences](../../preferences/).

  Par défaut : format **JPEG** et extension **.jpg**.

## Modules utilitaires

ALS utilise d'autres modules qui ne sont pas impliqués dans les traitements d'image. Ils sont cependant essentiels au
bon fonctionnement de l'application :

### Détecteur d'images

Ce module est en charge de détecter les nouvelles images dans le **dossier scanné** et de les placer dans la file 
d'attente du module de **pre-process**.

### Serveur web

Ce module prend en charge le partage de l'image affichée dans la zone centrale d'ALS sur le réseau auquel la machine 
qui exécute ALS est connectée.

L'image affichée dans la page web servie est rafraîchie périodiquement par le navigateur.

---

# La session {#session}

Au sain d'ALS, la session occupe une place prépondérante.

**La session** peut être définie comme l'association de la stack courante et du détecteur d'images.

1. **Démarrage** :
    - Le démarrage de la session active le module de détection d'images et vide la stack courante.
    - **Première Détection** : La première image détectée sera la référence d'alignement pour toute la session.

2. **Traitement des Images** :
    - Pendant que la session est en cours, chaque nouvelle image détectée est alignée sur l'image de référence, puis
      ajoutée à la stack courante, par moyenne ou somme. 

      Les résultats successifs de cet empilement sont traités et affichés par l'application.

    - La session peut être mise en pause : ALS stoppe le détecteur d'images et la stack courante **est conservée**. 

      Relancer la session redémarre simplement le détecteur d'images

3. **Arrêt** :
    - À l'arrêt de la session, le détecteur d'images est stoppé et la stack courante est marquée pour être remise à
      zéro au prochain démarrage de session.

{{% alert title="ℹ️ INFO" color="info" %}}
ALS ne traite pas les images déjà présentes dans le **dossier scanné** quand une session démarre
{{% /alert %}}

# Conclusion

Vous avez maintenant une vision claire de l'architecture et des concepts de base d'ALS. 

Prochaine étape : l'interface graphique d'ALS.
