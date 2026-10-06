# Document D14 : Diagnostic Acoustique par Microphone et Émission Acoustique (AE)

## Principe Physique de la Diagnostic Acoustique
Lorsqu'un élément roulant passe sur une anomalie (micro-fissure ou cratère d'écaillage), le choc métal-sur-métal génère :
1. Une onde de contrainte élastique haute fréquence (vibration transmise par les structures mécaniques).
2. Une onde de pression aérienne audible (son généré par la résonance du palier et du carter).

Un microphone omnidirectionnel ou un stéthoscope électronique industriel capte cette onde de pression acoustique. Le signal temporel brut acquis $s(t)$ possède la **même structure d'onde** qu'un signal accélérométrique.

## Pipeline de Traitement Audio
Pour rendre un signal sonore compatible avec le modèle Edge AI entraîné sur des données accélérométriques CWRU (12 kHz) :
1. **Chargement et Conversion Mono** : Lecture via `librosa.load(sr=12000, mono=True)`.
2. **Rééchantillonnage Numérique (Resampling)** : Interpolation polyphasée vers la fréquence d'échantillonnage standard $F_s = 12\,000\,\text{Hz}$ (respect de la bande passante de Nyquist $f_{max} = 6\,000\,\text{Hz}$).
3. **Normalisation de l'Amplitude** : Mise à l'échelle dans l'intervalle $[-1.0, +1.0]$ pour s'affranchir du gain du microphone.
4. **Extraction des 16 Caractéristiques Temporelles et Fréquentielles** : Kurtosis, Crest Factor, RMS, Skewness, Énergie spectrale FFT, Fréquence dominante.
5. **Inférence Gradient Boosting** : Diagnostic instantané (< 0.25 ms).

## Avantages du Diagnostic Acoustique en Industrie
- **Capteur sans contact** : Possibilité d'inspecter des machines dangereuses, très chaudes ou difficilement accessibles sans fixer d'accéléromètre.
- **Audit rapide et mobile** : Un opérateur équipé d'une tablette ou d'un smartphone peut enregistrer le bruit d'un palier et obtenir un diagnostic immédiat.
- **Détection des chocs ultrasonores** : Les harmoniques de choc sont parfaitement captées même à distance modérée (< 1 mètre).
