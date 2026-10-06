# Document D5 : Explicabilité (XAI) et Analyse d'Erreurs de Détection

## 1. Top 5 des Caractéristiques les Plus Discriminantes
L'analyse par arbres de décision et importance de Gini/MDI montre que la détection d'anomalies repose principalement sur :
1. **Kurtosis (Facteur d'aplatissement)** : Réagit instantanément aux chocs impulsionnels brifs provoqués par les défauts de roulement.
2. **RMS (Root Mean Square)** : Mesure l'accroissement de l'énergie vibratoire globale du moteur.
3. **Crest Factor (Facteur de Crête)** : Identifie le rapport entre l'amplitude maximale de crête et l'énergie moyenne.
4. **Spectral Energy (Énergie Spectrale)** : Capture le déplacement d'énergie vers les hautes fréquences.
5. **Impulse Factor (Facteur d'Impulsion)** : Renforce la sensibilité aux anomalies de surface.

## 2. Analyse par Z-Score et Explication Locale
- Un Z-score individuel mesuré au-delà de **+2.0 écarts-types** signale un dysfonctionnement matériel critique.
- Lors de défauts de bague interne (Inner Race), le Kurtosis peut atteindre des Z-scores supérieurs à **+4.5**, confirmant l'impact impulsionnel à chaque passage de bille.
