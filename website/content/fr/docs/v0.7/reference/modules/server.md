---
title: "Server"
description: "Documentation détaillée du module Server d'ALS"
author: "ALS Team"
lastmod: 2025-06-16T13:45:25Z
keywords: ["serveur ALS", "web"]
draft: false
type: "docs"
categories: ["documentations détaillées"]
tags: ["module", "web", "serveur"]
weight: 351
---

# Présentation

Le module **Server** prend en charge le partage sur le réseau de la **sortie web** du module **Save**.

Il sert une page web minimaliste affichant le dernier résultat de traitement et la met à jour automatiquement à chaque nouvelle image enregistrée.

# Configuration

|                    | Source                                                        | Type de donnée | Requis | Valeur par défaut |
|--------------------|---------------------------------------------------------------|----------------|--------|-------------------|
| Port d'écoute      | [Préférences : onglet Sortie](../../userguide/preferences/output/#server-port) | entier | Oui | 8000 |

# Contrôle

| Source | Type | Réponse |
|--------|------|---------|
| Interface : [Serveur d'images](../../userguide/ui/controls/#server-section) | Commande : START | Démarrer le serveur |
| Interface : [Serveur d'images](../../userguide/ui/controls/#server-section) | Commande : STOP | Arrêter le serveur |

# Entrée

| Donnée | Type |
|--------|------|
| Notification du module **Save** | Événement |

# Comportement

- Sert le contenu du **dossier web** sur le port configuré.
- Envoie une notification WebSocket aux navigateurs connectés à chaque enregistrement d'image.

# Sortie

Page web mise à jour avec le dernier résultat de traitement.
