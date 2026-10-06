# 🍓 Projet de Simulation Matérielle Wokwi : Edge AI & Maintenance Prédictive

Ce dossier contient l'ensemble des fichiers nécessaires pour simuler le banc IoT complet (Microcontrôleur ESP32 / Raspberry Pi Pico, Capteur Accéléromètre MPU6050, Écran OLED 128x64, LEDs, Relais E-Stop et Buzzer) sur le simulateur en ligne gratuit **Wokwi** (https://wokwi.com).

---

## 📁 Contenu du Dossier

| Fichier | Description |
| :--- | :--- |
| [`diagram.json`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/diagram.json) | Schéma de câblage complet et placement des composants virtuels sur Wokwi |
| [`sketch.ino`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/sketch.ino) | Code embarqué Arduino C++ complet (Traitement du signal, Kurtosis, RMS, Écran OLED, GPIOs, Relais, JSON série) |
| [`libraries.txt`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/libraries.txt) | Liste des dépendances de bibliothèques Arduino pour Wokwi |
| [`main.py`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/main.py) | Variante alternative en **MicroPython** pour ESP32 / Raspberry Pi Pico |

---

## 🚀 Comment Lancer la Simulation sur Wokwi (en 30 secondes)

1. Ouvrez votre navigateur et allez sur **[https://wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32)**.
2. Dans l'éditeur Wokwi :
   - Cliquez sur l'onglet **`diagram.json`** et remplacez tout son contenu par celui du fichier [`wokwi/diagram.json`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/diagram.json).
   - Cliquez sur l'onglet de code **`sketch.ino`** et collez le contenu du fichier [`wokwi/sketch.ino`](file:///c:/Users/marie/Desktop/Projets/Stage%20antigravity/wokwi/sketch.ino).
   - Créez ou ouvrez l'onglet **`libraries.txt`** et collez-y :
     ```text
     Adafruit MPU6050
     Adafruit SSD1306
     Adafruit GFX Library
     Adafruit Unified Sensor
     ```
3. Cliquez sur le bouton vert **Play ▶️ (Start the simulation)** en haut à droite !

---

## 🎬 Scénario de Démonstration pour le Jury

Dès le démarrage de la simulation sur Wokwi :

1. **Fonctionnement Nominal (Machine Saine)** :
   - L'écran OLED s'allume et affiche :
     - `EDGE AI : FONCTIONNEMENT NOMINAL`
     - `Kurtosis : ~2.95 (Normale = 3.0)`
     - `RMS : ~0.075 g`
     - `Santé (HI) : 98% | Zone A`
     - Jauge de santé pleine à 98%
   - La **LED Verte (GPIO 18)** est allumée.
   - Le **Relais E-Stop (GPIO 5)** est au repos (circuit fermé, moteur autorisé à tourner).
   - Le **Buzzer (GPIO 4)** est silencieux.
   - Le moniteur série affiche la télémétrie JSON en continu.

2. **Simulation d'une Panne Industrielle (Action Démo)** :
   - Cliquez sur le bouton rouge **`SIMULER CHOC`** dans Wokwi.
   - **Résultat immédiat (< 2 millisecondes)** :
     - Le Kurtosis explose au-dessus de **6.5** (détection d'impacts métalliques BPFO).
     - La LED Verte s'éteint et la **LED Rouge (GPIO 23)** se met à clignoter.
     - Le **Buzzer émet un son d'alarme**.
     - Le **Relais E-Stop bascule instantanément** (coupure de sécurité de l'alimentation moteur LOTO).
     - L'écran OLED affiche en rouge/blanc : `PANNE BPFO DETECTEE ! RELAIS : COUPURE ACTIF !`
     - L'Indice de Santé chute sous **25% (Zone D - Danger)**.

---

## 💡 Pourquoi Wokwi est un Argument Majeur pour la Soutenance ?
- **Validation matérielle prouvée** : Démontre que votre algorithme ne fonctionne pas seulement en théorie sur un PC, mais qu'il est déjà **compilé, dimensionné et validé sur microcontrôleur embarqué**.
- **Zéro matériel physique à transporter** : Vous pouvez projeter la simulation Wokwi directement dans votre navigateur devant le jury pendant la soutenance !
