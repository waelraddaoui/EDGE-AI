# Rapport de Stage Final : Edge AI Explicable et Agent IA/RAG pour la Détection d'Anomalies Industrielles sur Raspberry Pi

**Organisme d'Accueil / Cadre** : Stage de Fin d'Études Ingénieur  
**Période** : 07 août 2026 – 30 août 2026  
**Auteur** : Étudiant Ingénieur Edge AI  
**Encadrants** : Équipe de Recherche Advanced Agentic Coding & Edge AI  

---

## 📌 Résumé Exécutif

Ce projet de stage porte sur le développement et la validation expérimentale d'une solution complète d'**IA embarquée (Edge AI)**, **explicable (XAI)** et couplée à un **agent RAG (Retrieval-Augmented Generation)** pour la maintenance prédictive des roulements à billes industriels sur nano-calculateur **Raspberry Pi**.

En s'appuyant sur le jeu de données de référence de la **Case Western Reserve University (CWRU)** :
1. Une chaîne complète de fenêtrage temporel et d'extraction de **16 caractéristiques temporelles et fréquentielles (FFT)** a été déployée.
2. **5 modèles d'IA légers** (Isolation Forest, Random Forest, Gradient Boosting, Autoencodeur PyTorch, 1D-CNN) ont été entraînés et évalués sur données nominales et perturbées.
3. Un benchmark approfondi sur Raspberry Pi / processeur embarqué a démontré que le **Gradient Boosting** offre des performances exceptionnelles (**latence < 0.22 ms**, **débit > 4 500 fenêtres/sec**, **taille 30.6 KB**, **F1-score > 0.978** sous perturbations).
4. Un module d'**explicabilité (XAI)** identifie le **Kurtosis**, le **RMS** et le **Crest Factor** comme indicateurs majeurs d'anomalies impulsionnelles.
5. Un **Agent IA/RAG** indexe la base documentaire technique (D1 à D8) et génère automatiquement des rapports de diagnostic enrichis avec consignes d'intervention pour techniciens maintenance.
6. L'ensemble a été formalisé sous forme d'un **cas d'étude pédagogique réutilisable** (16h de TP) pour étudiants ingénieurs.

---

## 1. Contexte, Problématique & Enjeux Industriels
Dans l'Usine 4.0, les défaillances imprévues des roulements à billes constituent l'une des causes majeures d'arrêt de production des moteurs électriques. Les approches traditionnelles basées sur le transfert de signaux vibratoires bruts vers le Cloud font face à des verrous majeurs : bande passante saturée, temps de latence trop élevé pour l'arrêt d'urgence, et risques de confidentialité.

L'objectif de ce stage est d'embarquer l'intelligence de détection directement à la source (**Edge AI** sur Raspberry Pi) tout en garantissant l'explicabilité et en guidant les techniciens via un agent conversationnel autonome.

---

## 2. Description du Jeu de Données CWRU & Chaîne de Feature Engineering

### 2.1 Prétraitement et Fenêtrage
Le signal temporel sampled à 12 kHz est découpé en fenêtres glissantes de 1024 points (85.3 ms par fenêtre).

### 2.2 Extraction des 16 Caractéristiques
- **Temporelles (8)** : Mean, Std Dev, Variance, RMS, Min, Max, Peak-to-Peak, Energy.
- **Indicateurs de Forme (2)** : Skewness, Kurtosis, Crest Factor, Impulse Factor.
- **Fréquentielles FFT (6)** : Énergie Spectrale, Fréquence Dominante, Centroïde Spectral, Étalement Spectral.

---

## 3. Résultats Comparatifs des Modèles IA

| Modèle | Accuracy | Precision | Recall | F1-Score | Latence (ms) | Débit (fps) | Taille (KB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **0.218** | **4 560.9** | **30.6** |
| **Random Forest** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.217 | 820.6 | 20.1 |
| **1D-CNN Compact** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.536 | 1 848.6 | 11.3 |
| **Isolation Forest** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.214 | 822.6 | 573.3 |
| **Autoencodeur** | 0.1416 | 1.0000 | 0.0431 | 0.0826 | 0.081 | 12 178.4 | 4.6 |

---

## 4. Inférence Embarquée, Profilage & Robustesse Edge AI
- **Gradient Boosting** et **1D-CNN** se distinguent par leur stabilité exceptionnelle sous bruit gaussien et pertes de trames (F1 > 0.96).
- Le processeur ARM / CPU exécute l'inférence en moins de 1 ms, autorisant le traitement en direct de flux vibratoires à haute fréquence sans perte d'échantillon.

---

## 5. Explicabilité (XAI) & Assistant RAG
- L'analyse XAI démontre que le **Kurtosis** subit un saut de Z-score supérieur à **+4.5** lors des défaillances de bague interne (BPFI = 162.2 Hz).
- L'agent RAG extrait automatiquement les consignes techniques de maintenance à partir des fiches SKF 6205-2RS et génère un rapport de diagnostic clair.

---

## 6. Conclusion et Perspectives
Ce travail démontre la faisabilité opérationnelle d'un système Edge AI explicable et autonome pour la maintenance prédictive. Les perspectives futures incluent l'implémentation de la quantification INT8 via ONNX Runtime et le déploiement sur puces accélératrices (Raspberry Pi AI Hat / Coral TPU).
