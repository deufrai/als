---
title: "Premier démarrage"
description: "Tout savoir pour bien débuter avec ALS."
author: "ALS Team"
date: 2024-11-28
lastmod: 2024-12-03T19:59:08Z
keywords: ["Premier démarrage d'ALS"]
draft: false
type: "docs"
tags: ['preferences']
weight: 31
---

Ce chapitre a pour but de vous permettre d'utiliser ALS le plus rapidement possible. 

{{% alert title="TODO" color="info" %}}
ADD reminder about launch
{{% /alert %}}

{{< tabpane text=true >}}
  {{% tab header="**Système**:" disabled=true /%}}
  {{% tab header="PC/Linux" %}}
  Welcome!
  {{% /tab %}}
  {{% tab header="Raspberry Pi" %}}
  Welcome!
  {{% /tab %}}
  {{% tab header="Windows" %}}
  Ta mère !
  {{% /tab %}}
  {{% tab header="Mac" %}}
  Welcome!
  {{% /tab %}}
{{< /tabpane >}}

# Bienvenue

À votre tout premier démarrage, ALS vous souhaite la bienvenue et vous demande de définir les 2 réglages 
indispensables à son fonctionnement :

- **Scan folder** : Le dossier de votre système dans lequel ALS surveille l'arrivée des nouvelles brutes
- **Work folder** : Le dossier de votre système dans lequel ALS enregistre les images produites

{{< center >}}
{{< figure src="welcome.png" >}}
{{< /center >}}

Un click sur `OK` et ALS vous présente la fenêtre des préférences

---

# Configurer les dossiers critiques

{{< center >}}
{{< figure src="prefs_01.png" >}}
{{< /center >}}

Les deux dossiers critiques d'ALS sont définis dans la partie supérieure de la fenêtre des préférences.

Vous pouvez désigner des dossiers existants, mais nous vous conseillons de créer des dossiers spécifiques pour ALS.

Commençons par le dosser **scan**. Cliquez sur le bouton `Modifier...` en regard de **Dossier scanné** (1)

---

{{< center >}}
{{< figure src="prefs_02.png" >}}
{{< /center >}}


Naviguer vers le dossier dans lequel vous voulez créer le dossier **scan** puis cliquez le petit bouton 
**Créer un nouveau dossier** 


---

{{< center >}}
{{< figure src="prefs_03.png" >}}
{{< /center >}}

Saisissez le nom désiré. _Exemple : "als_scan"_

---

{{< center >}}
{{< figure src="prefs_04.png" >}}
{{< /center >}}

Validez votre choix en cliquant `Choisir`

---

{{< center >}}
{{< figure src="prefs_05.png" >}}
{{< /center >}}

Répéter la même procédure pour le dossier **work** et ne validez pas encore les préférences.
Il reste un point important à aborder

---

# Statistique d'utilisation

{{< center >}}
{{< figure src="prefs_06.png" >}}
{{< /center >}}

Il est très utile pour nous de savoir quelles versions d'ALS sont utilisées, et surtout sur quelle plateforme et quel
système d'exploitation.

Pour nous aider, vous pouvez autoriser ALS à nous envoyer les informations suivantes à chaque démarrage :
- Version d'ALS
- Type de processeur machine : PC, Mac ou Raspberry Pi
- Type de système d'exploitation

Vous pouvez vérifier la nature des informations envoyées par ALS en consultant le 
[code source de cette fonctionnalité](https://github.com/deufrai/als/blob/release/0.7/src/als/main.py#L46)

<details>
  <summary>code source de la fonctionnalité "call home" d'ALS</summary>

  ``` python
  def call_home():
      home_host = "ping.als-app.org"
      home_port = 16810
  
      try:
          home_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          message = f"{VERSION}||{platform.machine()}||{platform.system()}"
          home_socket.sendto(message.encode(), (home_host, home_port))
          home_socket.close()
      except socket.error:
          pass
  ```
</details>

---

# voilivoilouch !!

{{< center >}}
{{< figure src="ready.png" >}}
{{< /center >}}

bliblobliblo lorem etc... Et pecat !