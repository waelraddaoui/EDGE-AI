# Dossier d'Activité Pédagogique : Détection d'Anomalies Industrielles par IA Embarquée (Edge AI)

**Niveau** : École d'Ingénieurs / Master (Génie Industriel, Informatique, IA & Systèmes Embarqués)  
**Volume Horaire** : 16 heures de Travaux Pratiques (4 séances de 4h)  
**Auteurs** : Équipe Pédagogique Edge AI & Maintenance 4.0  

---

## 🎯 Objectifs Apprentissage & Compétences Visées

À l'issue de ce cas pratique, l'étudiant ingénieur sera capable de :
1. **Traiter des signaux vibratoires réels (CWRU)** : Comprendre le fenêtrage temporel glissant et l'extraction de caractéristiques temporelles et fréquentielles (FFT).
2. **Concevoir une chaîne de Machine Learning & Deep Learning** : Entraîner et évaluer 5 architectures complémentaires (Isolation Forest, Random Forest, Gradient Boosting, Autoencodeur PyTorch, 1D-CNN).
3. **Déployer et Profiler sur Nano-Ordinateur (Raspberry Pi)** : Mesurer la latence en temps réel, l'empreinte RAM, la taille binaire et évaluer la robustesse aux perturbations de capteurs.
4. **Intégrer des Outils d'Explicabilité (XAI)** : Analyser les facteurs d'aplatissement (Kurtosis), RMS et Z-scores pour expliquer le diagnostic aux techniciens de maintenance.
5. **Développer un Assistant Intelligent RAG** : Créer un moteur de recherche documentaire et un générateur automatique de rapports de diagnostic de maintenance.

---

## 🛠️ Contexte Industriel et Mise en Situation

Vous êtes recruté(e) comme ingénieur(e) IA & Maintenance Prédictive chez **IndusTech Solutions**. Le client exploite un parc de moteurs électriques industriels entraînant des pompes critiques. Pour éviter les arrêts de production inopinés coûteux, le client souhaite installer un nano-calculateur **Raspberry Pi** directement connecté aux accéléromètres pour réaliser un diagnostic continu en temps réel.

### Défi Technique :
- **Contrainte de temps réel** : Moins de 10 ms par fenêtre d'inférence.
- **Contrainte mémoire** : Moins de 50 MB de RAM.
- **Explicabilité obligatoire** : Le système ne doit pas être une "boîte noire", le technicien doit comprendre pourquoi une alerte est émise.

---

## 📋 Travail à Réaliser (4 Séances Pratiques)

### TP 1 : Exploration des Signaux & Extraction de Caractéristiques (4h)
- Charger les fichiers vibratoires CWRU (Sain, Bague Interne, Bague Externe, Bille).
- Découper les signaux en fenêtres glissantes de 1024 points.
- Extraire 16 caractéristiques (8 temporelles, 2 indicateurs de forme, 6 caractéristiques spectraux FFT).
- Générer un jeu de données synthétique hybride perturbé (bruit gaussien + pertes de trames).

### TP 2 : Modélisation IA & Évaluation Comparative (4h)
- Entraîner les 5 modèles de détection d'anomalies.
- Tracer les matrices de confusion et les courbes ROC-AUC.
- Calculer l'Accuracy, Precision, Recall, et F1-score.

### TP 3 : Profilage Edge AI & Robustesse sur Raspberry Pi (4h)
- Simuler un flux de données capteur streaming avec journalisation JSON.
- Profiler la latence moyenne, P95, la consommation RAM et CPU de chaque modèle.
- Construire la grille de décision multicritères pour sélectionner la meilleure architecture embarquée.

### TP 4 : Module XAI & Assistant Virtuel RAG (4h)
- Calculer les importances de variables (Gini / SHAP) et les Z-scores par fenêtre.
- Indexer la base documentaire technique (D1 à D8) via un moteur RAG TF-IDF.
- Développer un générateur automatique de rapports de diagnostic de maintenance.

---

## 📦 Livrables Attendus par l'Étudiant
1. Code source Python structuré (`src/`, `raspberry/`, `rag_agent/`).
2. Rapport de synthèses avec graphiques et matrices de confusion.
3. Rapport de diagnostic généré automatiquement par l'agent RAG.
