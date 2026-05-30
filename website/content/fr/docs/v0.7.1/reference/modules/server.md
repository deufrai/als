---
title: "Serveur"
description: "Documentation détaillée du module Serveur d'images d'ALS"
author: "ALS Team"
lastmod: 2026-05-30T03:04:03Z
keywords: ["serveur d'images ALS", "module web ALS", "partage distant ALS"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "serveur", "utilitaire", "web", "diffusion"]
weight: 71362
---

# Présentation {#overview}

Le module utilitaire **Server** expose les résultats d'ALS via un service HTTP et WebSocket léger.

Il est chargé de :

- Publier la **dernière image empilée** et les métriques de session dans le **dossier web** configuré
- Servir l'**application web de visualisation** (`index.html`, JavaScript et icônes)
- Diffuser en direct les **notifications de nouvelle image** aux navigateurs connectés par WebSocket

Le module fonctionne dans sa propre boucle d'événements asyncio et accepte plusieurs clients simultanés. Il n'altère jamais le pipeline de traitement : il se contente de servir les sorties produites par le module **Save**.

{{% alert color="info" %}}
ℹ️ Le serveur livre le contenu stocké dans le **dossier web**. Par défaut, ce dossier est un alias du **dossier de travail** ; vous pouvez dédier un dossier séparé depuis les [Préférences de sortie](../../userguide/preferences/output/#web-dedicated).
{{% /alert %}}

# Configuration {#configuration}

| Paramètre              | Source                                                                             | Type de donnée         | Requis  | Valeur par défaut               |
|------------------------|------------------------------------------------------------------------------------|------------------------|---------|---------------------------------|
| **Dossier web**        | Préférences : [Onglet Sorties](../../userguide/preferences/output/#web-folder)     | Chemin vers un dossier | Oui     | Alias du **dossier de travail** |
| **Dossier web dédié**  | Préférences : [Onglet Sorties](../../userguide/preferences/output/#web-dedicated)  | Booléen                | Non     | Désactivé                       |
| **Adresse affichée**   | Préférences : [Onglet Sorties](../../userguide/preferences/output/#server-address) | Chaîne (`auto` ou `ip:<adresse>`) | Oui     | Auto - recommandé               |
| **Port**               | Préférences : [Onglet Sorties](../../userguide/preferences/output/#server-port)    | Entier (1024–65535)    | Oui     | 8000                            |

# Contrôle {#control}

| Source                                                                      | Type               | Réponse                                                                                                               |
|-----------------------------------------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|
| Panneau [Contrôles principaux](../../userguide/ui/controls/#server-section) | Commande : `START` | Prépare les ressources web et lance le thread serveur                                                                 |
| Panneau [Contrôles principaux](../../userguide/ui/controls/#server-section) | Commande : `STOP`  | Prévient les clients et arrête le serveur. Les ressources web restent disponibles sur le disque                       |

# Sorties {#outputs}

Une fois démarré, le module maintient les artefacts suivants dans le dossier web :

| Artefact                      | Description                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|
| `index.html`                  | Interface embarquée affichant l'image empilée en direct                          |
| `favicon.ico` & `icons/*.png` | Ressources du visualiseur copiées depuis le bundle d'ALS                         |
| `data.json`                   | Métriques de session (`STACK_SIZE`, `EXPO`) mises à jour après chaque empilement |
| `web_image.jpg`               | Dernière image traitée sauvegardée en JPEG pour le navigateur                    |
| `openseadragon.min.js`        | Bibliothèque de visualisation à zoom profond utilisée par l'interface            |

# Comportement {#behavior}

## Séquence de démarrage {#startup-sequence}

1. **Publier les ressources statiques** — `index.html`, les icônes et l'image d'attente sont écrits (ou rafraîchis) dans le dossier web pour un chargement immédiat des clients.
2. **Exposer les métriques de session** — `data.json` est généré avec la taille de stack courante et le temps d'exposition cumulé.
3. **Valider la disponibilité** — le module tente la liaison réelle du serveur sur `0.0.0.0:<port>`. Un `PortInUseError` est levé si le port configuré ne peut pas être utilisé.
4. **Lancer la boucle serveur** — une boucle asyncio démarre dans un thread dédié, sert HTTP sur toutes les interfaces IPv4 locales et accepte les connexions WebSocket sur `/ws`.
5. **Annoncer la disponibilité** — ALS résout la préférence **Adresse affichée** configurée et met à jour son interface avec l'adresse sélectionnée.

## Liaison et adresse affichée {#binding-and-displayed-address}

L'adresse de liaison et l'adresse affichée sont volontairement séparées :

- Le serveur se lie à `0.0.0.0` pour accepter les connexions depuis toute interface IPv4 locale disponible.
- L'URL affichée utilise une adresse locale concrète qu'un autre appareil peut ouvrir dans un navigateur.

Si l'adresse affichée sélectionnée est `127.0.0.1`, le module reste actif mais signale **Accès limité au serveur web** afin que vous puissiez corriger la connectivité réseau.

## Mises à jour en direct {#live-updates}

- Après chaque image traitée, le JPEG courant et `data.json` sont réécrits dans le dossier web.
- `notify_browsers_about_new_image()` envoie `{ "type": "new_image" }` à tous les clients WebSocket pour qu'ils rechargent la texture sans scrutation.
- La même infrastructure diffuse `{ "type": "disconnect" }` juste avant l'arrêt, permettant aux clients d'afficher un message approprié.

## Arrêt {#shutdown}

Lorsque la commande `STOP` est déclenchée :

1. Tous les clients reçoivent un message `disconnect`.
2. Le module attend brièvement (2 secondes) que les navigateurs ferment la connexion.
3. Le runner asyncio est nettoyé et le thread dédié s'arrête.
4. L'interface réinitialise le statut et le QR code ; les fichiers statiques restent présents pour la prochaine session.

# Référence WebSocket {#websocket-reference}

| Message | Charge utile | Déclencheur |
|---------|--------------|-------------|
| `new_image` | `{ "type": "new_image" }` | Une nouvelle image traitée est disponible |
| `disconnect` | `{ "type": "disconnect" }` | Le serveur est en cours d'arrêt |

{{% alert title="Dépannage" color="warning" %}}
- Changez le port dans les préférences si ALS signale que le port est déjà utilisé.
- Si un autre appareil n'atteint pas l'URL affichée, sélectionnez une adresse affichée appartenant au même réseau que l'appareil qui utilise le navigateur, puis réessayez l'URL ou le QR code.
- Vérifiez que votre pare-feu autorise les connexions entrantes sur le port configuré.
{{% /alert %}}
