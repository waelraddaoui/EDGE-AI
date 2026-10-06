# Document D9 : Théorie Avancée du Traitement du Signal pour la Maintenance Prédictive

## 1. Introduction à l'Analyse Vibratoire
L'analyse vibratoire est la méthode la plus fiable et la plus couramment utilisée pour surveiller l'état de santé (Condition Monitoring) des machines tournantes, en particulier les roulements à billes. Toute machine génère un spectre de vibrations naturel. Lorsqu'un défaut apparaît (écaillage, fissure, usure), il modifie ce spectre de manière caractéristique.

## 2. La Transformée de Fourier Rapide (FFT)
La Fast Fourier Transform (FFT) est un algorithme fondamental qui convertit un signal temporel (amplitude en fonction du temps) en un spectre fréquentiel (amplitude en fonction de la fréquence). 
Cela permet d'isoler des fréquences spécifiques. Par exemple, si une machine tourne à 30 Hz (1800 tr/min), on s'attend à voir un pic à 30 Hz. Si le roulement est endommagé, de nouveaux pics apparaîtront à des fréquences très spécifiques appelées fréquences de défaut.

## 3. Fréquences de Défaut des Roulements
Les roulements possèdent quatre fréquences de défaut critiques (calculables à partir de la géométrie du roulement et de la vitesse de rotation) :
- **BPFI (Ball Pass Frequency Inner)** : Fréquence de passage des billes sur la bague interne. C'est souvent la fréquence la plus élevée.
- **BPFO (Ball Pass Frequency Outer)** : Fréquence de passage sur la bague externe. C'est généralement une anomalie très commune car la bague externe supporte la charge statique de la machine.
- **BSF (Ball Spin Frequency)** : Fréquence de rotation des billes sur elles-mêmes.
- **FTF (Fundamental Train Frequency)** : Fréquence de rotation de la cage.

## 4. Les Indicateurs Statistiques Temporels
Avant même d'utiliser la FFT, des indicateurs statistiques temporels permettent d'alerter sur l'apparition de défauts :
- **RMS (Root Mean Square)** : Mesure l'énergie globale de la vibration. Une augmentation du RMS indique une dégradation globale, mais ne précise pas l'origine.
- **Kurtosis (Facteur d'aplatissement)** : Mesure l'impulsivité du signal. Un signal normal suit une distribution gaussienne (Kurtosis = 3). Lorsqu'un roulement commence à s'écailler, des chocs impulsifs se créent, ce qui fait bondir le Kurtosis (> 4). C'est le meilleur indicateur pour la détection précoce.
- **Skewness (Asymétrie)** : Mesure si les pics de vibrations penchent davantage vers des valeurs positives ou négatives. Utile pour certains défauts de frottement.
- **Crest Factor (Facteur de Crête)** : Ratio entre le pic maximum et la valeur RMS.

## 5. Pourquoi utiliser l'Intelligence Artificielle plutôt que les seuils classiques ?
Historiquement, la maintenance se faisait par la méthode des "Seuils" (si le RMS dépasse 5mm/s, on déclenche une alarme). Cette approche produit énormément de faux positifs car la charge de la machine et le bruit environnant font varier les vibrations.
L'IA (Machine Learning / Deep Learning) permet d'apprendre la "signature" complexe de la machine saine (en combinant le Kurtosis, l'énergie des bandes FFT, la Skewness) et d'isoler avec précision les anomalies naissantes, de manière multidimensionnelle et non-linéaire.
