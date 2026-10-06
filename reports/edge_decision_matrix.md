# Grille de Décision Multicritères pour la Sélection du Modèle Edge AI

Cette grille pondère l'efficacité des modèles selon 5 critères industriels pré-définis :
- **Précision Propre (30%)** : F1-score sur données nominales
- **Robustesse (25%)** : F1-score sur données perturbées
- **Débit d'Inférence (20%)** : Fenêtres traitées / seconde
- **Vitesse de Latence (15%)** : Temps de traitement d'une fenêtre (ms)
- **Taille Mémoire (10%)** : Empreinte binaire sur le stockage local

## Tableau Récapitulatif et Classement Final

| Rang | Modèle | Score Global / 100 | Latence Moy. (ms) | Débit (fps) | F1 Propre | F1 Perturbé | Taille (KB) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Gradient Boosting** | **75.18** | 0.218 | 4560.9 | 1.0000 | 0.9781 | 30.6 |
| 2 | **1D-CNN** | **71.86** | 0.536 | 1848.6 | 1.0000 | 0.9666 | 11.3 |
| 3 | **Random Forest** | **68.80** | 1.217 | 820.6 | 1.0000 | 0.9945 | 20.1 |
| 4 | **Isolation Forest** | **65.18** | 1.214 | 822.6 | 1.0000 | 0.9474 | 573.3 |
| 5 | **Autoencodeur** | **6.57** | 0.081 | 12178.4 | 0.0826 | 0.9267 | 4.6 |
