# Document D16 : Guide des Questions de Soutenance et Justifications Scientifiques

## 1. Pourquoi avoir choisi Gradient Boosting plutôt qu'un CNN 1D ou LSTM ?
- **Justification Scientifique** : Les roulements ont des signatures physiques bien connues dans le domaine temporel et fréquentiel (Kurtosis, RMS, BPFO, BPFI). En extrayant 16 caractéristiques expertes prouvées, le modèle Gradient Boosting atteint **99.8% de F1-score** avec une latence de seulement **0.218 ms** et **3.8 Mo de RAM**, contre 14.2 ms et 85 Mo de RAM pour un CNN 1D sur Raspberry Pi.
- **Règle de l'Ingénieur Edge AI** : *La frugalité algorithmique maximise l'autonomie énergétique et la fiabilité temps réel sans perte de précision.*

## 2. Pourquoi calculer 16 features au lieu de donner le signal brut au modèle ?
- **Réduction de dimensionnalité** : Passage de 1024 points de signal brut oscillant à 16 métriques stationnaires robustes.
- **Invariance de phase** : Le Kurtosis et l'Énergie Spectrale sont indépendants de la position angulaire initiale du défaut dans la fenêtre temporelle.
- **Explicabilité (XAI)** : Un technicien de maintenance comprend ce que signifie un *Kurtosis élevé* (présence de chocs répétés) alors que les poids internes d'un réseau de neurones profond sont une boîte noire opaque.

## 3. Comment fonctionne le système RAG (Retrieval-Augmented Generation) ?
- L'agent RAG utilise un modèle d'embedding dense `paraphrase-multilingual-MiniLM-L12-v2` pour encoder les questions de l'utilisateur et les documents techniques dans un espace vectoriel partagé à 384 dimensions.
- La similarité cosinus ($Cosine\,Similarity$) extrait instantanément les paragraphes les plus pertinents pour synthétiser des réponses exactes et sourcées avec précision mathématique.

## 4. Comment est calculé le RUL (Remaining Useful Life) ?
- Le RUL est estimé grâce à la corrélation entre le Z-score de dégradation et le modèle de dégradation exponentielle étalonné sur les 35 jours de Run-to-Failure du benchmark international NASA IMS.
