# Document D3 : Guide des Caractéristiques Temporelles et Fréquentielles Extraites

## 1. Caractéristiques Temporelles (8 Indicateurs Statistiques)
Pour un signal vibratoire temporel \(x(t)\) découpé en une fenêtre de \(N\) points :

1. **Valeur Moyenne (Mean)** : \(\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i\)
2. **Écart-type (Std Dev)** : \(\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2}\)
3. **Variance** : \(\sigma^2\)
4. **Valeur Efficace (RMS - Root Mean Square)** : \(X_{rms} = \sqrt{\frac{1}{N}\sum_{i=1}^N x_i^2}\) - Indicateur de l'énergie globale.
5. **Valeur Crête-à-Crête (Peak-to-Peak)** : \(X_{p2p} = \max(x) - \min(x)\)
6. **Énergie Temporelle** : \(E = \sum_{i=1}^N x_i^2\)
7. **Facteur d'Asymétrie (Skewness)** : Indicateur de la dissymétrie de la distribution du signal.
8. **Facteur d'Aplatissement (Kurtosis)** : \(K = \frac{\frac{1}{N}\sum (x_i - \bar{x})^4}{\sigma^4}\) - Sensible aux chocs impulsionnels brifs (Normal \(\approx 3.0\), Défaut \(> 4.5\)).

## 2. Indicateurs Formes & Facteurs d'Impulsion (2 Indicateurs)
9. **Facteur de Crête (Crest Factor)** : \(CF = \frac{\max(|x|)}{X_{rms}}\) - Évalue le niveau impulsionnel par rapport à l'énergie continue.
10. **Facteur d'Impulsion (Impulse Factor)** : \(IF = \frac{\max(|x|)}{\frac{1}{N}\sum |x_i|}\)

## 3. Caractéristiques Fréquentielles FFT (6 Indicateurs Spectraux)
Calculés sur le spectre d'amplitude \(S(f) = |\text{FFT}(x)|\) :

11. **Énergie Spectrale Totale** : Somme des puissances du spectre de Fourier.
12. **Fréquence Dominante** : Fréquence correspondant à la valeur d'amplitude maximale.
13. **Centroïde Spectral (Spectral Centroid)** : Centre de gravité du spectre vibratoire.
14. **Étalement Spectral (Spectral Spread)** : Écart-type du spectre autour de son centroïde.
