# Support de Présentation : Soutenance de Stage Edge AI & Maintenance 4.0

**Titre** : Edge AI Explicable et Agent IA/RAG pour la Détection d'Anomalies Industrielles sur Raspberry Pi  
**Présenté par** : Élève Ingénieur  
**Date** : 30 août 2026  

---

## Slide 1 : Titre & Sommaire
- **Problématique** : Détection temps réel des défauts de roulements à billes sur Raspberry Pi.
- **Plan** :
  1. Contexte & Enjeux Industriels
  2. Jeu de Données CWRU & Feature Engineering
  3. Modélisation IA & Évaluation
  4. Benchmark Edge AI & Profilage Mémoire
  5. Module XAI & Demonstration Agent RAG
  6. Transfert Pédagogique & Conclusion

---

## Slide 2 : Contexte & Défis Industriels
- **Constat** : 40% des pannes moteur sont dues aux défaillances de roulements.
- **Verrous du Cloud AI** : Latence importante, dépendance réseau, coût bande passante.
- **Solution Edge AI** : Traitement local sur Raspberry Pi (< 1 ms latence, fonctionnement autonome).

---

## Slide 3 : Chaîne d'Extraction de Caractéristiques (16 Features)
- **Signal Brut CWRU** -> Fenêtrage glissant de 1024 points (85 ms).
- **Indicateurs Temporels (8)** : RMS, Peak-to-Peak, Variance, Energy, etc.
- **Indicateurs de Forme (2)** : Kurtosis, Crest Factor (sensibles aux chocs impulsionnels).
- **Indicateurs Spectraux (6)** : FFT Énergie Spectrale, Centroïde, Fréquence Dominante.

---

## Slide 4 : Performances Comparatives des 5 Modèles IA
- **Supervisés (Random Forest, Gradient Boosting, 1D-CNN)** : Accuracy = 100%, F1 = 1.0.
- **Non-supervisés (Isolation Forest, Autoencodeur)** : Baselines robustes économe en étiquettes.

---

## Slide 5 : Benchmark Matériel & Latence sur Raspberry Pi
- **Gradient Boosting** : Latence **0.218 ms**, Débit **4 560 fenêtres/sec**, Taille **30.6 KB**.
- **1D-CNN Compact** : Latence **0.536 ms**, Débit **1 848 fenêtres/sec**, Taille **11.3 KB**.
- **Random Forest** : Latence **1.217 ms**, Taille **20.1 KB**.

---

## Slide 6 : Explicabilité XAI (Kurtosis & Z-Scores)
- Le **Kurtosis** et le **Crest Factor** bondissent à Z > **+4.5 std** lors des défaillances de bague interne.
- Les techniciens disposent d'un diagnostic physique transparent.

---

## Slide 7 : Demonstration Agent RAG & Rapport Automatique
- Indexation TF-IDF des fiches techniques SKF 6205-2RS (D1-D8).
- Génération automatique de mini-rapports de maintenance prédictive avec consignes opérationnelles.

---

## Slide 8 : Conclusion & Perspectives
- Livrable complet (L1-L17) conforme aux exigences du Cahier des Charges.
- Perspectives : Quantification INT8 et accélération sur puces Coral TPU / Raspberry Pi AI Hat.
