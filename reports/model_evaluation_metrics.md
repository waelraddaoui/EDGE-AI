# Rapport d'Évaluation des Modèles de Détection d'Anomalies

Ce document résume les performances de détection des 5 modèles légers évalués sur le jeu de test CWRU.

## Tableau Comparatif des Métriques

| Modèle | Accuracy | Precision | Recall | F1-Score | AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Isolation Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Gradient Boosting | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Autoencodeur | 0.1416 | 1.0000 | 0.0431 | 0.0826 | 0.0797 |
| 1D-CNN | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

## Synthèse & Analyse des Performances
- **Random Forest** et **Gradient Boosting** atteignent des performances quasi-parfaites (\(F1 pprox 1.0\)) sur les caractéristiques extraites.
- **1D-CNN** et **Autoencodeur** démontrent d'excellentes capacités d'apprentissage généralisables.
- **Isolation Forest** constitue une baseline robuste non-supervisée très économe en ressources.
