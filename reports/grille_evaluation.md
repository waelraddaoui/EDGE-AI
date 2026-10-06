# Grille d'Évaluation Détaillée et Guide Enseignant (Barème 20 Points)

## 🎯 Bareme Synthétique d'Évaluation

| Module | Compétence Évaluée | Points | Critères d'Exigence |
| :---: | :--- | :---: | :--- |
| **Module 1** | Pretraitement & Fenêtrage | **4 pts** | Fenêtrage temporel 1024 pts sans chevauchement parasite. Génération correcte du jeu hybride perturbé. |
| **Module 2** | Extraction de Caractéristiques | **4 pts** | Justesse mathématique des 16 caractéristiques (Kurtosis, RMS, Centroïde FFT). Normalisation StandardScaler sans data leakage. |
| **Module 3** | Entraînement & Évaluation IA | **4 pts** | 5 modèles entraînés. Calcul rigoureux d'Accuracy, F1, ROC-AUC et génération des matrices de confusion. |
| **Module 4** | Benchmark Edge AI & Robustesse | **4 pts** | Mesure précise de latence (ms), RAM (MB), débit (fps). Construction de la matrice de décision multicritère. |
| **Module 5** | Explicabilité XAI & Agent RAG | **4 pts** | Analyse d'importance Gini/Z-scores. Indexation et réponse documentée de l'agent RAG avec rapport automatique. |

---

## 🔍 Éléments de Correction et Réponses Attendues (Guide Enseignant)

### 1. Fréquences Karactéristiques SKF 6205-2RS (N = 1772 RPM, fr = 29.53 Hz)
- **BPFI (Bague Interne)** : ~162.2 Hz (5.43 x fr)
- **BPFO (Bague Externe)** : ~103.6 Hz (3.57 x fr)
- **BSF (Bille)** : ~67.4 Hz (2.32 x fr)

### 2. Choix d'Architecture Embarquée Recommandée
- **Gradient Boosting** (Recommandation N°1) : Latence 0.218 ms, Débit 4560 fps, F1=0.9781 perturbé, Taille 30.6 KB.
- **Random Forest** (Recommandation N°2) : Latence 1.217 ms, F1=0.9945 perturbé, Taille 20.1 KB.
- **1D-CNN** (Option Deep Learning) : Latence 0.536 ms, F1=0.9666 perturbé, Taille 11.3 KB.
