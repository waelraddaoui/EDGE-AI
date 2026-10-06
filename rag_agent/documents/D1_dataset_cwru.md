# Document D1 : Description Détaillée du Jeu de Données CWRU (Case Western Reserve University)

## 1. Origine et Contexte Expérimental
Le jeu de données de la Case Western Reserve University (CWRU) est la référence internationale pour le diagnostic de défaillances des roulements à billes par analyse vibratoire. 

Les données ont été collectées sur un banc d'essai comprenant :
- Un moteur électrique de **2 chevaux** (1.5 kW),
- Un dynamomètre de mesure de couple,
- Un roulement de test supportant l'arbre moteur (**SKF 6205-2RS JEM**).

## 2. Types de Defauts et Sévérités
Des défauts synthétiques ont été introduits par électro-érosion (EDM) avec des diamètres d'endommagement calibrés :
1. **Défaut de Bague Interne (Inner Race Fault - BPFI)** : 0.007, 0.014 et 0.021 pouces.
2. **Défaut de Bague Externe (Outer Race Fault - BPFO)** : 0.007, 0.014 et 0.021 pouces (placé à 6h, 3h et 12h).
3. **Défaut d'Élément Roulant / Bille (Ball Fault - BSF)** : 0.007, 0.014 et 0.021 pouces.

## 3. Conditions de Charge et Fréquences d'Échantillonnage
- **Charges moteur** : 0, 1, 2, 3 HP (correspondant à des vitesses de rotation de 1797 à 1730 RPM).
- **Fréquences d'échantillonnage** : 12 000 Hz (12 kHz) pour les données standard, et 48 000 Hz (48 kHz) pour le point d'appui côté moteur.
- **Accéléromètres** : Placés sur le logement côté moteur (Drive End - DE) et côté ventilateur (Fan End - FE).
