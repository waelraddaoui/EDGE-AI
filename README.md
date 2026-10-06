# Edge AI Explicable et Agent IA/RAG pour la Détection d'Anomalies Industrielles sur Raspberry Pi

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyTorch 2.5](https://img.shields.io/badge/PyTorch-2.5-orange.svg)](https://pytorch.org/)
[![Raspberry Pi Ready](https://img.shields.io/badge/Raspberry%20Pi-Compatible-green.svg)](https://www.raspberrypi.com/)

---

## 📌 Présentation du Projet

Ce dépôt contient le code complet, la documentation, les rapports et le cas d'étude pédagogique pour le projet de maintenance prédictive embarquée **Edge AI** sur roulements industriels (Dataset CWRU).

Le système associe :
1. **Un moteur de détection d'anomalies ultra-rapide (< 1 ms)** pour Raspberry Pi (Gradient Boosting, Random Forest, 1D-CNN, Isolation Forest, Autoencodeur).
2. **Un module d'explicabilité (XAI)** basé sur l'analyse d'importance de variables et les Z-scores par rapport à l'état sain.
3. **Un agent conversationnel RAG** indexant la base documentaire technique (D1 à D8) et générant automatiquement des rapports de diagnostic pour techniciens.
4. **Un dossier pédagogique ingénieur complet (16h TP)** avec énoncé et grille d'évaluation (barème 20 pts).

---

## 🗂️ Structure du Dépôt

```
├── data/
│   ├── raw/                      # Signal CWRU brut et métadonnées JSON
│   ├── processed/                # Dataset fenêtré et features (.parquet, .npz)
│   └── pedagogical_subset/       # Echantillon pédagogique réduit
├── figures/                      # Figures PNG HD (01 à 10)
├── models/                       # Modèles entraînés (.joblib, .pth, scaler)
├── notebooks/                    # Notebook exploratoire (01_exploration.ipynb)
├── rag_agent/
│   ├── documents/                # Base documentaire D1 à D8 (.md)
│   ├── build_index.py            # Construction de l'index TF-IDF
│   ├── ask_agent.py              # Assistant RAG interactif
│   └── generate_diagnostic.py    # Générateur automatique de rapports
├── raspberry/
│   ├── inference_edge.py         # Moteur d'inférence temps réel & IoT streaming
│   ├── benchmark_edge.py         # Profiler de latence, RAM, CPU et robustesse
│   └── logs/                     # Logs d'inférence streaming et benchmark JSON
├── reports/                      # Rapports Markdown (Rapport final, Article, Slides, Cas TP)
└── src/
    ├── data_preparation.py       # Génération et fenêtrage des signaux CWRU
    ├── feature_extraction.py     # Extraction des 16 features (Temporelles & FFT)
    ├── train_models.py           # Entraînement des 5 modèles IA légers
    ├── evaluate_models.py        # Évaluation des métriques & matrices de confusion
    ├── explainability.py         # Module XAI (Figure 06, 07, 08 & Z-scores)
    └── generate_edge_synthesis.py# Synthèse et grille de décision multicritères
```

---

## 🚀 Guide d'Exécution Pas-à-Pas

### 1. Préparation des Données & Exploration
```bash
python src/data_preparation.py
python src/run_exploration.py
```

### 2. Feature Engineering (16 Indicateurs Temporels & FFT)
```bash
python src/feature_extraction.py
```

### 3. Entraînement & Évaluation des Modèles IA
```bash
python src/train_models.py
python src/evaluate_models.py
```

### 4. Inférence Edge AI, Profilage & Robustesse sur Raspberry Pi
```bash
python raspberry/inference_edge.py
python raspberry/benchmark_edge.py
python src/explainability.py
python src/generate_edge_synthesis.py
```

### 5. Agent RAG & Génération de Diagnostic
```bash
python rag_agent/build_index.py
python rag_agent/ask_agent.py
python rag_agent/generate_diagnostic.py
```

---

## 📊 Inventaire des Livrables de Stage (L1 à L17)

| Code | Intitulé du Livrable | Emplacement dans le Dépôt |
| :---: | :--- | :--- |
| **L1** | Fichiers bruts & nettoyés CWRU | `data/raw/`, `data/processed/` |
| **L2** | Dataset synthétique hybride perturbé | `data/processed/features_hybrid.parquet` |
| **L3** | Dataset pédagogique réduit | `data/pedagogical_subset/` |
| **L4** | Notebook exploratoire des signaux | `notebooks/01_exploration.ipynb` |
| **L5** | Code Python prétraitement & fenêtrage | `src/data_preparation.py` |
| **L6** | Module d'extraction de caractéristiques FFT | `src/feature_extraction.py` |
| **L7** | Code d'entraînement des 5 modèles | `src/train_models.py` |
| **L8** | Code d'évaluation & matrices de confusion | `src/evaluate_models.py` |
| **L9** | Moteur d'inférence Edge AI IoT | `raspberry/inference_edge.py` |
| **L10**| Profiler de ressources & robustesse | `raspberry/benchmark_edge.py` |
| **L11**| Fichier de logs de benchmark JSON | `raspberry/logs/benchmark_results.json` |
| **L12**| Module d'explicabilité XAI | `src/explainability.py` |
| **L13**| Figures et fiches comparatives Edge AI | `figures/` (01 à 10), `reports/edge_decision_matrix.md` |
| **L14**| Base documentaire RAG D1-D8 | `rag_agent/documents/` |
| **L15**| Code agent RAG & générateur de diagnostic| `rag_agent/ask_agent.py`, `rag_agent/generate_diagnostic.py` |
| **L16**| Cas d'étude pédagogique & grille | `reports/cas_pedagogique.md`, `reports/grille_evaluation.md` |
| **L17**| Rapport final, Article & Slides | `reports/rapport_final.md`, `draft_article.md`, `presentation_slides.md` |
