# Document D4 : Résultats du Benchmark D'Inférence Embarquée (Edge AI)

## 1. Synthèse des Mesures Matérielles
Les tests d'inférence ont été réalisés par simulation temporelle et profilage direct de processeur ARM / CPU local :

- **Gradient Boosting** :
  - Latence moyenne : **0.218 ms** / fenêtre
  - Débit d'inférence : **4 560.9 fenêtres/sec**
  - Taille sur disque : **30.6 KB**
  - F1-score propre : **1.0000** | F1-score perturbé : **0.9781**
  - Score Global : **75.18 / 100** (Recommandation N°1)

- **1D-CNN Compact PyTorch** :
  - Latence moyenne : **0.536 ms** / fenêtre
  - Débit d'inférence : **1 848.6 fenêtres/sec**
  - Taille sur disque : **11.3 KB**
  - F1-score propre : **1.0000** | F1-score perturbé : **0.9666**
  - Score Global : **71.86 / 100** (Recommandation Deep Learning N°1)

- **Random Forest Légers** :
  - Latence moyenne : **1.217 ms** / fenêtre
  - Débit d'inférence : **820.6 fenêtres/sec**
  - Taille sur disque : **20.1 KB**
  - F1-score propre : **1.0000** | F1-score perturbé : **0.9945**
  - Score Global : **68.80 / 100** (Recommandation N°2)

- **Isolation Forest** :
  - Latence moyenne : **1.214 ms** / fenêtre
  - Taille sur disque : **573.3 KB**
  - F1-score propre : **1.0000** | F1-score perturbé : **0.9474**
  - Score Global : **65.18 / 100**
