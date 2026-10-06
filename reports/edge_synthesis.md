# Rapport de Synthèse Edge AI et Recommandation de Déploiement

## 1. Recommandation Principale pour Raspberry Pi
L'architecture **Gradient Boosting** est officiellement recommandée pour le déploiement opérationnel sur Raspberry Pi.

### Points Forts Clés :
- **Vitesse exceptionnelle** : Latence moyenne de **0.218 ms** et un débit de **4560.9 fenêtres/s**.
- **Haute Précision & Robustesse** : F1-score de **1.0000** (données propres) et **0.9781** sous perturbations de bruit et pertes de trames.
- **Ultra-Compact** : Empreinte de seulement **30.6 KB** sur le stockage local.

## 2. Recommandation Secondaire (Alternative ML)
En seconde position, **1D-CNN** offre un excellent compromis avec une précision de **1.0000** et une excellente interprétabilité des arbres de décision.

## 3. Synthèse des Livrables de la Phase 2
- [x] Moteur d'inférence temps réel (`raspberry/inference_edge.py`)
- [x] Profiler de ressources système et robustesse (`raspberry/benchmark_edge.py`)
- [x] Module d'explicabilité XAI (`src/explainability.py`)
- [x] Figures comparatives (06 à 10) dans `figures/`
- [x] Rapports de validation dans `reports/`
