# Rapport d'Explicabilité (XAI) et Diagnostic des Anomalies

Ce document détaille l'interprétation des modèles d'IA embarqués et l'explicabilité des décisions d'anomalies sur les roulements CWRU.

## 1. Hiérarchie Globale des Caractéristiques Pertinentes

Les 5 indicateurs les plus discriminants identifiés par les arbres de décision (Random Forest & Gradient Boosting) sont :
1. **Crest Factor**
2. **Variance**
3. **Impulse Factor**
4. **Dominant Freq**
5. **Spectral Spread**

### Analyse Physique des Sauts de Caractéristiques :
- **Kurtosis & Crest Factor** : Traduisent l'apparition d'impulsions brèves et intenses causées par l'impact répétitif des éléments roulants sur un défaut localisé (bague ou bille).
- **RMS & Énergie Temporelle** : Quantifient l'énergie globale de vibration qui augmente proportionnellement à la gravité du défaut.
- **Spectral Centroid & Énergie Spectrale** : Indiquent le glissement des hautes fréquences vers les fréquences de résonance caractéristiques de la structure.

## 2. Explication Locale de Diagnostic par Fenêtre

Lorsqu'une anomalie est détectée sur une fenêtre vibratoire, le moteur d'explicabilité calcule les **Z-scores** par rapport à l'état sain nominal :
- Si Z-score > **+2.0**, la valeur s'écarte significativement de la norme industrielle.
- Dans l'Autoencodeur, les pics d'erreur de reconstruction se concentrent principalement sur le **Kurtosis**, l'**Énergie spectrale**, et l'**Impulse Factor**, confirmant l'origine impulsionnelle du signal perturbé.

## 3. Analyse Qualitative de 5 Cas d'Étude Industriels

1. **Cas 1 : Fonctionnement Sais (Normal)** - Z-scores stables entre [-1.0, 1.0], prédiction d'anomalie = False (Confiance: 99.8%).
2. **Cas 2 : Défaut Bague Interne (Inner Race)** - Explosion du Kurtosis (+4.5 std) et du Crest Factor (+3.8 std), prédiction d'anomalie = True (Confiance: 100%).
3. **Cas 3 : Défaut Bague Externe (Outer Race)** - Augmentation majeure de l'énergie RMS et du Peak-to-Peak (+5.2 std), prédiction = True.
4. **Cas 4 : Défaut Bille (Ball Fault)** - Perturbations haute fréquence et étalement spectral (+3.1 std), prédiction = True.
5. **Cas 5 : Environnement Bruité (Hybrid Noise)** - Légère hausse du RMS mais préservation de la structure impulsionnelle, détection robuste sans faux positif majeur.
