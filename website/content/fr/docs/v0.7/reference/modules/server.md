---
title: "Serveur"
description: "Documentation détaillée du module Serveur d'images d'ALS"
author: "ALS Team"
lastmod: 2025-10-22T18:33:34Z
keywords: ["serveur d'images ALS", "module web ALS", "partage distant ALS"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "serveur", "utilitaire", "web", "diffusion"]
weight: 362
---

# Présentation

Le module utilitaire **Server** expose les résultats d'ALS via un service HTTP et WebSocket léger.

Il est chargé de :

- Publier la **dernière image empilée** et les métriques de session dans le **dossier web** configuré
- Servir l'**application web de visualisation** (`index.html`, JavaScript et icônes)
- Diffuser en direct les **notifications de nouvelle image** aux navigateurs connectés par WebSocket
- Fournir une URL compatible **QR code** pour que tablettes et téléphones rejoignent la session rapidement

Le module fonctionne dans sa propre boucle d'événements asyncio et accepte plusieurs clients simultanés. Il n'altère jamais le pipeline de traitement : il se contente de servir les sorties produites par le module **Save**.

{{% alert color="info" %}}
ℹ️ Le serveur livre le contenu stocké dans le **dossier web**. Par défaut, ce dossier est un alias du **dossier de travail** ; vous pouvez dédier un dossier séparé depuis les [Préférences de sortie](../../userguide/preferences/output/#web-dedicated).
{{% /alert %}}

# Configuration

| Paramètre             | Source                                                                            | Type de donnée         | Requis  | Valeur par défaut               |
|-----------------------|-----------------------------------------------------------------------------------|------------------------|---------|---------------------------------|
| **Dossier web**       | Préférences : [Onglet Sorties](../../userguide/preferences/output/#web-folder)    | Chemin vers un dossier | Oui     | Alias du **dossier de travail** |
| **Dossier web dédié** | Préférences : [Onglet Sorties](../../userguide/preferences/output/#web-dedicated) | Booléen                | Non     | Désactivé                       |
| **Port**              | Préférences : [Onglet Sorties](../../userguide/preferences/output/#server-port)   | Entier (1024–65535)    | Oui     | 8000                            |

# Contrôle

| Source                                                                      | Type               | Réponse                                                                                                               |
|-----------------------------------------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|
| Panneau [Contrôles principaux](../../userguide/ui/controls/#server-section) | Commande : `START` | Prépare les ressources web et lance le thread serveur                                                                 |
| Panneau [Contrôles principaux](../../userguide/ui/controls/#server-section) | Commande : `STOP`  | Prévient les clients et arrête proprement le serveur. Les ressources web restent disponibles ; l'UI masque le QR code |

# Sorties

Une fois démarré, le module maintient les artefacts suivants dans le dossier web :

| Artefact                      | Description                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|
| `index.html`                  | Interface embarquée affichant l'image empilée en direct                          |
| `favicon.ico` & `icons/*.png` | Ressources du visualiseur copiées depuis le bundle d'ALS                         |
| `data.json`                   | Métriques de session (`STACK_SIZE`, `EXPO`) mises à jour après chaque empilement |
| `web_image.jpg`               | Dernière image traitée sauvegardée en JPEG pour le navigateur                    |
| `openseadragon.min.js`        | Bibliothèque de visualisation à zoom profond utilisée par l'interface            |

# Comportement

## Séquence de démarrage

1. **Valider la disponibilité** — le module résout l'adresse IP de l'hôte et vérifie que le port configuré est libre. Un `PortInUseError` est levé si un autre processus écoute déjà.
2. **Publier les ressources statiques** — `index.html`, les icônes et l'image d'attente sont écrits (ou rafraîchis) dans le dossier web pour un chargement immédiat des clients.
3. **Exposer les métriques de session** — `data.json` est généré avec la taille de stack courante et le temps d'exposition cumulé.
4. **Lancer la boucle serveur** — une boucle asyncio démarre dans un thread dédié servant `http://<hôte>:<port>` et acceptant les connexions WebSocket sur `/ws`.
5. **Annoncer la disponibilité** — l'interface met à jour son statut et le QR code, et journalise l'URL finale.

Si ALS ne peut se lier qu'à `127.0.0.1`, le module reste actif mais signale **Accès limité au serveur web** afin que vous puissiez corriger la connectivité réseau.

## Mises à jour en direct

- Après chaque image traitée, le JPEG courant et `data.json` sont réécrits dans le dossier web.
- `notify_browsers_about_new_image()` envoie `{ "type": "new_image" }` à tous les clients WebSocket pour qu'ils rechargent la texture sans scrutation.
- La même infrastructure diffuse `{ "type": "disconnect" }` juste avant l'arrêt, permettant aux clients d'afficher un message approprié.

## Arrêt

Lorsque la commande `STOP` est déclenchée :

1. Tous les clients reçoivent un message `disconnect`.
2. Le module attend brièvement (2 secondes) que les navigateurs ferment la connexion.
3. Le runner asyncio est nettoyé et le thread dédié s'arrête.
4. L'interface réinitialise le statut et le QR code ; les fichiers statiques restent présents pour la prochaine session.

# Référence WebSocket

| Message | Charge utile | Déclencheur |
|---------|--------------|-------------|
| `new_image` | `{ "type": "new_image" }` | Une nouvelle image traitée est disponible |
| `disconnect` | `{ "type": "disconnect" }` | Le serveur est en cours d'arrêt |

{{% alert title="Dépannage" color="warning" %}}
- Changez le port dans les préférences si ALS signale que le port est déjà utilisé.
- Si les appareils externes n'atteignent pas l'URL, vérifiez qu'ALS n'est pas retombé sur `127.0.0.1` et que votre pare-feu autorise les connexions entrantes sur le port configuré.
{{% /alert %}}
