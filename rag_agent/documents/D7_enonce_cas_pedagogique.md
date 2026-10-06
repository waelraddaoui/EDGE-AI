# Document D7 : Énoncé du Cas d'Étude Ingénieur - Détection d'Anomalies Roulements

## 1. Contexte du Projet Ingénieur
Vous êtes ingénieur en IA embarquée et maintenance prédictive au sein d'une usine 4.0. Le responsable maintenance souhaite installer un système autonome de détection d'anomalies sur Raspberry Pi pour surveiller un parc de moteurs électriques entraînant des pompes critiques.

## 2. Objectifs Globaux
1. Analyser les signaux vibratoires du dataset CWRU et comprendre les signatures physiques de défaillance.
2. Concevoir une chaîne d'extraction de caractéristiques temporelles et FFT.
3. Entraîner et évaluer 5 modèles IA (Isolation Forest, Random Forest, Gradient Boosting, Autoencodeur, 1D-CNN).
4. Profiler la latence et l'empreinte mémoire sur Raspberry Pi pour sélectionner le modèle optimal.
5. Intégrer un module d'explicabilité XAI pour fournir un rapport de diagnostic intelligible pour les techniciens de maintenance.
