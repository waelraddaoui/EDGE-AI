# Document D12 : Dataset NASA IMS, Indice de Santé (Health Index) et Pronostic RUL

## Contexte et Protocole Expérimental NASA IMS
Le jeu de données **NASA IMS (Intelligent Maintenance Systems)** de l'Université de Cincinnati est la référence internationale pour l'étude de la dégradation continue de roulements industriels en mode *Run-to-Failure* (fonctionnement jusqu'à rupture totale).

- **Banc d'essai** : 4 roulements Rexnord ZA-2115 montés sur un même arbre rotatif entraîné par moteur AC à **2000 RPM**.
- **Charge radiale appliquée** : 6000 lbs (~2700 kg) appliquée en continu par ressorts hélicoïdaux.
- **Acquisition** : Accéléromètres PCB 353B33 (sensibilité 10 mV/g), fréquence d'échantillonnage **20 kHz**, enregistrement d'instantanés de 20 480 points toutes les 10 minutes pendant 35 jours consécutifs (> 100 millions de points collectés).

## Les Trois Stades de Dégradation du Roulement
L'analyse temporelle et spectrale des données NASA IMS permet d'identifier 3 phases distinctes du cycle de vie du roulement :

1. **Stade 1 : Fonctionnement Sain / Nominal (Jours 1 à 25)**
   - Indice de Santé (HI) : **90% à 100%**
   - Kurtosis : $Kurt \approx 3.0$ (distribution gaussienne normale)
   - Valeur RMS : $< 0.08\,g$ (très faible niveau d'énergie)
   - Durée de vie restante estimée (RUL) : **> 12 mois**

2. **Stade 2 : Dégradation Précoce / Incipient Fault (Jours 26 à 31)**
   - Indice de Santé (HI) : **50% à 85%**
   - Phénomène : Micro-fissures sous-cutanées et début d'écaillage (spalling) sur la bague externe.
   - Kurtosis : Montée nette de $Kurt = 4.5$ à $8.0$ due aux micro-chocs impulsionnels.
   - Durée de vie restante estimée (RUL) : **1 à 3 mois** (planification de la maintenance recommandée).

3. **Stade 3 : Endommagement Sévère / Failure (Jours 32 à 35)**
   - Indice de Santé (HI) : **< 30%**
   - Phénomène : Écaillage massif généralisé, destruction de la piste de roulement, échauffement et vibrations violentes.
   - RMS : Explosion de la valeur RMS de $0.15\,g$ à plus de $1.2\,g$.
   - Durée de vie restante estimée (RUL) : **< 48 heures** (Arrêt d'urgence immédiat obligatoire).

## Formule Mathématique de l'Indice de Santé (Health Index)
L'Indice de Santé $HI \in [0, 100]\%$ est calculé par déviation multivariée par rapport à l'état de référence sain :
$$HI = 100 \times \exp\left( -0.22 \times D_{score} \right)$$
Où la distance de déviation $D_{score}$ est pondérée par les Z-scores du Kurtosis et du RMS :
$$D_{score} = 0.55 \times Z_{Kurtosis} + 0.45 \times Z_{RMS}$$
$$Z_{Kurtosis} = \max\left(0, \frac{Kurt - 3.0}{\sigma_{kurt}}\right), \quad Z_{RMS} = \max\left(0, \frac{RMS - RMS_{sain}}{\sigma_{rms}}\right)$$
