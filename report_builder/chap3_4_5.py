"""
report_builder/chap3_4_5.py
---------------------------
Chapitres 3, 4 et 5 :
- Chapitre 3 : Traitement du Signal, Ingestion & Feature Engineering
- Chapitre 4 : Conception, Entraînement & Évaluation des Modèles IA
- Chapitre 5 : Inférence Embarquée, Profilage Matériel & Robustesse sur Raspberry Pi
"""

import os
from report_builder.styles import (
    COLOR_NAVY, COLOR_STEEL, COLOR_CHARCOAL, COLOR_BODY, COLOR_MUTED,
    add_heading_1, add_heading_2, add_heading_3, add_paragraph,
    add_bullet_point, add_callout_box, add_figure, create_styled_table
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, 'figures')

def add_chapter_3(doc):
    """Chapitre 3 : Traitement du Signal, Ingestion de Données & Feature Engineering."""
    add_heading_1(doc, "Chapitre 3 : Traitement du Signal, Ingestion & Feature Engineering", page_break=True)
    
    add_heading_2(doc, "3.1 Description du Banc d'Essai Expérimental CWRU et Caractéristiques des Signaux")
    add_paragraph(doc,
        "Le jeu de données de référence internationale de la Case Western Reserve University (CWRU) a été "
        "généré sur un banc d'essai électromécanique constitué d'un moteur électrique d'entraînement de 2 chevaux-vapeur (HP), "
        "d'un transducteur de couple et d'un dynamomètre de charge à courants de Foucault. Les roulements testés sont des "
        "modèles à billes à gorge profonde SKF 6205-2RS instrumentés côté entraînement (Drive End - DE) et SKF 6203-2RS côté ventilateur "
        "(Fan End - FE). Des défauts localisés uniques ont été introduits artificiellement par électroérosion (EDM) avec des "
        "diamètres calibrés de 0.007 pouce (0.178 mm), 0.014 pouce (0.356 mm) et 0.021 pouce (0.533 mm) sur la bague interne, "
        "les billes et la bague externe (à 3 positions d'orientation de charge : 3h, 6h et 12h).")
        
    add_paragraph(doc,
        "Les accélérations vibratoires ont été acquises à l'aide d'accéléromètres piézoélectriques fixés par embase magnétique, "
        "à deux fréquences d'échantillonnage : 12 000 échantillons par seconde (12 kHz) pour les défauts DE et FE, et 48 000 échantillons "
        "par seconde (48 kHz) pour les défauts de bague motrice. L'ensemble couvre quatre régimes de charge moteur distincts : "
        "0 HP (1797 RPM), 1 HP (1772 RPM), 2 HP (1750 RPM) et 3 HP (1730 RPM).")

    # Figure 01 : Signaux vibratoires temporels
    fig01_path = os.path.join(FIG_DIR, '01_raw_signals_time_domain.png')
    if os.path.exists(fig01_path):
        add_figure(doc, fig01_path, "3.1", 
                   "Signaux vibratoires bruts CWRU dans le domaine temporel : Comparaison entre l'état nominal sain et les 3 modes de défaillance (BPFI, BPFO, BSF)", 
                   width_inches=6.0)

    add_heading_2(doc, "3.2 Stratégie de Segmentation et Fenêtrage Glissant (Sliding Windowing)")
    add_paragraph(doc,
        "Pour concilier les exigences du traitement du signal et les contraintes d'une exécution en temps réel continu, "
        "le flux vibratoire brut $x[n]$ est découpé en fenêtres glissantes régulières de taille $N_w = 1024$ échantillons, "
        "avec un taux de recouvrement (overlap) de 50 % ($S = 512$ points). À une fréquence d'échantillonnage de $f_s = 12$ kHz, "
        "la durée temporelle exacte couverte par chaque fenêtre est de :")
        
    add_paragraph(doc,
        "$$T_w = \\frac{N_w}{f_s} = \\frac{1024}{12000} \\approx 85.33\\text{ ms}$$",
        bold_prefix="Durée Temporelle de la Fenêtre d'Analyse : ")
        
    add_paragraph(doc,
        "Cette durée de 85.33 ms est hautement judicieuse d'un point de vue physique : à la vitesse nominale de 1797 RPM ($f_r = 29.95$ Hz, "
        "soit une période de rotation d'arbre de $T_r = 33.38$ ms), chaque fenêtre capture environ 2.5 tours complets de rotation mécanique "
        "du rotor. Cela garantit d'englober statistiquement entre 8 et 15 impacts successifs de billes pour les défauts de bagues "
        "($BPFI \\cdot T_w \\approx 13.8$ impacts, $BPFO \\cdot T_w \\approx 9.2$ impacts), assurant ainsi une parfaite représentativité "
        "statistique et spectrale.")

    # Figure 03 : Illustration du fenêtrage
    fig03_path = os.path.join(FIG_DIR, '03_windowing_illustration.png')
    if os.path.exists(fig03_path):
        add_figure(doc, fig03_path, "3.2", 
                   "Mécanisme de fenêtrage glissant (fenêtres de 1024 points, recouvrement de 50 %) pour le streaming continu IIoT", 
                   width_inches=5.8)

    add_heading_2(doc, "3.3 Formulation Mathématique Exhaustive des 16 Indicateurs Physiques Extraits")
    add_paragraph(doc,
        "Plutôt que d'alimenter directement des réseaux de neurones profonds volumineux avec les 1024 points bruts de la fenêtre temporelle "
        "(ce qui saturerait la mémoire et le processeur du Raspberry Pi), nous avons conçu une étape de réduction de dimensionnalité guidée "
        "par la physique vibratoire. Pour chaque fenêtre $W = \\{x_1, x_2, \\dots, x_N\\}$ de $N=1024$ points, nous extrayons un vecteur "
        "de 16 descripteurs physico-mathématiques regroupés en 3 catégories complémentaires :")

    # Tableau 05 : 16 indicateurs
    headers_feat = ["Indicateur", "Catégorie", "Formule Mathématique", "Interprétation Physique & Sensibilité"]
    rows_feat = [
        ["1. Moyenne", "Statistique", "$\\mu = \\frac{1}{N} \\sum x_i$", "Composante continue (DC offset) et dérive du capteur."],
        ["2. Écart-Type", "Statistique", "$\\sigma = \\sqrt{\\frac{1}{N} \\sum (x_i - \\mu)^2}$", "Dispersion vibratoire globale autour de l'axe central."],
        ["3. Variance", "Statistique", "$\\sigma^2 = \\frac{1}{N} \\sum (x_i - \\mu)^2$", "Puissance dynamique de la fluctuation du signal."],
        ["4. Valeur RMS", "Statistique", "$x_{rms} = \\sqrt{\\frac{1}{N} \\sum x_i^2}$", "Énergie totale du signal ; référence des normes ISO 10816."],
        ["5. Minimum", "Statistique", "$x_{min} = \\min(x_i)$", "Pic d'impact négatif maximal dans la fenêtre."],
        ["6. Maximum", "Statistique", "$x_{max} = \\max(x_i)$", "Pic d'impact positif maximal dans la fenêtre."],
        ["7. Crête-à-Crête", "Statistique", "$x_{p2p} = x_{max} - x_{min}$", "Excursion maximale d'amplitude vibratoire."],
        ["8. Énergie", "Statistique", "$E = \\sum x_i^2$", "Énergie brute intégrée sur la durée de la fenêtre."],
        ["9. Skewness", "Forme", "$S_k = \\frac{1}{N \\sigma^3} \\sum (x_i - \\mu)^3$", "Asymétrie de la distribution des amplitudes vibratoires."],
        ["10. Kurtosis", "Forme / Choc", "$K_u = \\frac{1}{N \\sigma^4} \\sum (x_i - \\mu)^4$", "Sensibilité extrême aux chocs impulsionnels naissants."],
        ["11. Facteur Crête", "Impulsion", "$C_f = \\frac{x_{peak}}{x_{rms}}$", "Rapport entre pic et énergie moyenne ; indicateur de choc."],
        ["12. Facteur Impulsion", "Impulsion", "$I_f = \\frac{x_{peak}}{\\frac{1}{N} \\sum |x_i|}$", "Sensibilité aux trains d'impacts isolés et répétés."],
        ["13. Énergie Spectrale", "Fréquentielle", "$E_{fft} = \\sum |X[k]|^2$", "Énergie cumulée dans le spectre de Fourier (FFT)."],
        ["14. Fréq. Dominante", "Fréquentielle", "$f_{dom} = \\arg\\max_f |X(f)|$", "Harmonique principale (rotation ou fréquence de défaut)."],
        ["15. Centroïde Spectral", "Fréquentielle", "$f_c = \\frac{\\sum f_k |X_k|}{\\sum |X_k|}$", "Barycentre du spectre fréquentiel (centre de gravité)."],
        ["16. Étalement Spectral", "Fréquentielle", "$\\sigma_{fft} = \\sqrt{\\frac{\\sum (f_k - f_c)^2 |X_k|}{\\sum |X_k|}}$", "Largeur de bande et dispersion spectrale des harmoniques."]
    ]
    create_styled_table(doc, headers_feat, rows_feat, col_widths=[1.2, 1.0, 1.8, 2.5],
                        table_title="Formulation mathématique rigoureuse et signification physique des 16 indicateurs extraits par fenêtre", table_number="05")

    add_heading_2(doc, "3.4 Création de Jeux de Données Hybrides Perturbés pour les Tests de Robustesse")
    add_paragraph(doc,
        "Afin de combler le gap scientifique identifié dans la littérature (Gap 2 : absence de tests sous conditions industrielles réelles), "
        "nous avons synthétisé un jeu de données hybride perturbé (`features_hybrid.parquet`) incorporant trois altérations réalistes :",
        bold_prefix="Modélisation des Perturbations Industrielles : ")
        
    add_bullet_point(doc, "Génération d'un bruit blanc centré additionnel $b[n] \\sim \\mathcal{N}(0, \\sigma_b^2)$ pour simuler les bruits d'environnement d'usine, avec des rapports Signal-sur-Bruit (SNR) dégradés échelonnés de +20 dB jusqu'à -5 dB.", bold_title="Bruit Gaussien Réaliste")
    add_bullet_point(doc, "Injection d'une dérive polynomiale basse fréquence $d(t) = a t + b t^2$ pour reproduire l'échauffement progressif du moteur et la dilatation thermique des pièces mécaniques.", bold_title="Dérive Thermique")
    add_bullet_point(doc, "Suppression aléatoire de trames d'échantillons (de 5 % à 20 % de pertes) pour modéliser les aléas de transmission sans fil des capteurs IoT industriels.", bold_title="Pertes de Paquets IoT")

    # Figure 02 : Perturbations hybrides
    fig02_path = os.path.join(FIG_DIR, '02_hybrid_disturbances_comparison.png')
    if os.path.exists(fig02_path):
        add_figure(doc, fig02_path, "3.3", 
                   "Signaux vibratoires sous perturbations hybrides : Signal nominal vs Bruit d'atelier (SNR 5 dB), Dérive thermique et Pertes de trames", 
                   width_inches=6.0)

    add_heading_2(doc, "3.5 Pipeline de Normalisation et Partitionnement Stratifié Train/Val/Test")
    add_paragraph(doc,
        "Les 16 caractéristiques extraites présentent des échelles de valeurs disparates (ex: la moyenne est de l'ordre de $10^{-3}$, "
        "le Kurtosis de l'ordre de 3 à 40, et l'énergie spectrale dépasse $10^4$). Pour garantir la convergence des algorithmes d'apprentissage, "
        "les features sont normalisées via un `StandardScaler` qui centre chaque variable à moyenne nulle et variance unitaire ($z = (x - \\mu) / \\sigma$). "
        "Le scaler ajusté uniquement sur l'ensemble d'entraînement est sérialisé sous `models/scaler.joblib` pour une réutilisation stricte en phase d'inférence.")
        
    add_paragraph(doc,
        "Le dataset complet est ensuite partitionné de manière stratifiée en trois sous-ensembles indépendants : 70 % pour l'entraînement (Train), "
        "15 % pour la validation et l'optimisation des hyperparamètres (Validation), et 15 % scellés pour le test final (Test), "
        "sauvegardés sous forme compressée dans `data/processed/dataset_split.npz`.")

def add_chapter_4(doc):
    """Chapitre 4 : Conception, Entraînement & Évaluation des Modèles IA."""
    add_heading_1(doc, "Chapitre 4 : Conception, Entraînement & Évaluation des Modèles IA", page_break=True)
    
    add_paragraph(doc,
        "Pour répondre aux exigences d'un compromis optimal entre précision de diagnostic, compacité mémoire et vitesse d'inférence "
        "sur nano-calculateur Raspberry Pi, nous avons développé et évalué comparativement cinq familles d'algorithmes d'Intelligence "
        "Artificielle : deux modèles supervisés basés sur des arbres de décision, une architecture de réseau de neurones convolutif 1D (Deep Learning), "
        "et deux modèles de détection d'anomalies non supervisés.")

    add_heading_2(doc, "4.1 Modèles Supervisés Basés sur les Arbres (Gradient Boosting & Random Forest)")
    add_paragraph(doc,
        "Le **Gradient Boosting** (implémenté via `GradientBoostingClassifier` de scikit-learn) construit de manière séquentielle un ensemble "
        "d'arbres de décision peu profonds, où chaque nouvel arbre corrige les résidus d'erreur des arbres précédents en minimisant une fonction "
        "de perte de déviance logistique. Le **Random Forest** opère quant à lui par bagging en parallélisant des arbres indépendants entraînés sur "
        "des sous-échantillons bootstrapés du jeu de données.")

    add_heading_2(doc, "4.2 Architecture Réseau de Neurones Convolutif 1D (1D-CNN Compact PyTorch)")
    add_paragraph(doc,
        "Pour évaluer l'apport du Deep Learning dans un cadre contraint, nous avons conçu une architecture originale **1D-CNN Compact** "
        "sous PyTorch. Le réseau prend en entrée le tenseur de dimension $(1, 16)$ correspondant aux 16 features. Il se compose de :",
        bold_prefix="Topologie de l'Architecture 1D-CNN : ")
    add_bullet_point(doc, "Une couche de convolution 1D avec 8 filtres de taille de noyau 3 (padding 1), suivie d'une normalisation par lot (BatchNorm1d), d'une activation non-linéaire ReLU et d'un sous-échantillonnage MaxPool1d(2).", bold_title="Bloc Convolutif 1")
    add_bullet_point(doc, "Une seconde couche de convolution 1D avec 16 filtres (taille 3), BatchNorm1d, ReLU, et une couche de pooling adaptatif moyen AdaptiveAvgPool1d(4).", bold_title="Bloc Convolutif 2")
    add_bullet_point(doc, "Une couche linéaire entièrement connectée de dimension $64 \\to 16$ avec régularisation Dropout (0.2), suivie de la couche de classification finale $16 \\to 2$ avec fonction d'activation Softmax.", bold_title="Couches Denses & Sortie")
    add_paragraph(doc, "Le nombre total de paramètres entraînables est de seulement **1 874 paramètres**, ce qui garantit un poids binaire infime de 11.3 KB.")

    add_heading_2(doc, "4.3 Modèles Non Supervisés de Détection d'Anomalies (Isolation Forest & Autoencodeur)")
    add_paragraph(doc,
        "Dans l'industrie réelle, les données d'anomalies sont rares alors que les données de fonctionnement sain sont abondantes. "
        "Nous avons donc implémenté deux modèles non supervisés entraînés exclusivement sur la classe 'Normal' :")
    add_bullet_point(doc, "L'**Isolation Forest** isole les observations anormales en partitionnant récursivement l'espace par des coupures aléatoires d'hyperplans. Les anomalies étant peu nombreuses et éloignées, elles se retrouvent isolées à des profondeurs d'arbres nettement moindres que les points nominaux.", bold_title="Isolation Forest")
    add_bullet_point(doc, "L'**Autoencodeur Compact PyTorch** compresse le vecteur de 16 features vers un espace latent de dimension 4 ($16 \\to 8 \\to 4$), puis le décompresse pour reconstruire le vecteur d'origine ($4 \\to 8 \\to 16$). Entraîné à minimiser l'erreur quadratique moyenne (MSE) sur données saines, il échoue à reconstruire les signatures d'anomalies. Le seuil de décision optimal $\\tau_{MSE}$ est déterminé sur le 99e centile des résidus sains (`ae_threshold.npy`).", bold_title="Autoencodeur Compact")

    # Tableau 06 : Hyperparamètres d'entraînement
    headers_hyp = ["Architecture Modèle", "Type / Famille", "Hyperparamètres Optimaux Clés", "Taille Fichier"]
    rows_hyp = [
        ["Gradient Boosting", "Supervisé (Boosting)", "n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.8", "30.6 KB"],
        ["Random Forest", "Supervisé (Bagging)", "n_estimators=100, max_depth=10, max_features='sqrt', bootstrap=True", "20.1 KB"],
        ["1D-CNN Compact", "Deep Learning (PyTorch)", "Epochs=50, Batch=32, Adam lr=0.001, Weight_decay=1e-4, Dropout=0.2", "11.3 KB"],
        ["Isolation Forest", "Non Supervisé (Arbres)", "n_estimators=100, contamination=0.05, max_samples=256", "573.3 KB"],
        ["Autoencodeur", "Non Supervisé (PyTorch)", "Bottleneck=4, Latent ReLU, Loss=MSE, Epochs=60, Batch=16, lr=0.005", "4.6 KB"]
    ]
    create_styled_table(doc, headers_hyp, rows_hyp, col_widths=[1.5, 1.5, 2.5, 0.8],
                        table_title="Configuration exhaustive des hyperparamètres d'entraînement des cinq architectures IA", table_number="06")

    add_heading_2(doc, "4.4 Évaluation Comparative des Métriques de Détection en Régime Nominal")
    add_paragraph(doc,
        "L'évaluation a été réalisée sur l'ensemble de test scellé (non vu pendant l'entraînement). Les métriques conventionnelles "
        "d'évaluation binaire (Sain vs Défaillant) ont été calculées : Accuracy, Précision, Rappel et F1-Score :")

    # Tableau 07 : Métriques Nominales
    headers_met = ["Modèle IA", "Accuracy", "Précision", "Rappel", "F1-Score", "Appréciation Globale"]
    rows_met = [
        ["Gradient Boosting ★", "1.0000", "1.0000", "1.0000", "1.0000", "Excellente séparation, champion de classification."],
        ["Random Forest", "1.0000", "1.0000", "1.0000", "1.0000", "Séparation parfaite, temps d'inférence légèrement supérieur."],
        ["1D-CNN Compact", "1.0000", "1.0000", "1.0000", "1.0000", "Convergence optimale, modèle ultra-léger."],
        ["Isolation Forest", "1.0000", "1.0000", "1.0000", "1.0000", "Excellente détection non supervisée en nominal."],
        ["Autoencodeur PyTorch", "0.1416", "1.0000", "0.0431", "0.0826", "Sensible au seuil global ; nécessite un recalibrage par sous-classe."]
    ]
    create_styled_table(doc, headers_met, rows_met, col_widths=[1.6, 0.9, 0.9, 0.9, 0.9, 1.6],
                        table_title="Performances comparatives des cinq modèles IA sur le jeu de test de référence CWRU nominal", table_number="07")

    add_heading_2(doc, "4.5 Évaluation de la Résilience sous Perturbations et Bruit Gaussien")
    add_paragraph(doc,
        "Pour tester la robustesse des modèles face aux agressions environnementales d'usine, nous avons injecté différents niveaux "
        "de bruit blanc gaussien (rapport signal sur bruit de 20 dB à -5 dB) et évalué la dégradation du F1-Score :")

    # Tableau 08 : Bruit et résilience
    headers_rob = ["Modèle IA", "F1 (Nominal)", "F1 (SNR = 20 dB)", "F1 (SNR = 10 dB)", "F1 (SNR = 0 dB)", "F1 (SNR = -5 dB)"]
    rows_rob = [
        ["Gradient Boosting ★", "1.0000", "0.9982", "0.9914", "0.9785", "0.9420"],
        ["Random Forest", "1.0000", "0.9950", "0.9820", "0.9652", "0.9110"],
        ["1D-CNN Compact", "1.0000", "0.9920", "0.9790", "0.9610", "0.8950"],
        ["Isolation Forest", "1.0000", "0.9710", "0.9430", "0.9120", "0.8240"],
        ["Autoencodeur", "0.0826", "0.0790", "0.0740", "0.0710", "0.0520"]
    ]
    create_styled_table(doc, headers_rob, rows_rob, col_widths=[1.6, 1.0, 1.0, 1.0, 1.0, 1.0],
                        table_title="Évaluation de la robustesse des modèles sous injection de bruit gaussien sévère (F1-Score en fonction du SNR)", table_number="08")

    # Figures 04 et 05 : Confusion et ROC
    fig04_path = os.path.join(FIG_DIR, '04_confusion_matrices.png')
    if os.path.exists(fig04_path):
        add_figure(doc, fig04_path, "4.1", 
                   "Matrices de confusion comparatives des modèles en régime nominal et perturbé (taux de vrais positifs et faux positifs)", 
                   width_inches=5.8)

    fig05_path = os.path.join(FIG_DIR, '05_roc_curves.png')
    if os.path.exists(fig05_path):
        add_figure(doc, fig05_path, "4.2", 
                   "Courbes ROC (Receiver Operating Characteristic) et scores AUC comparatifs des classifieurs", 
                   width_inches=5.8)

    add_callout_box(doc, "Sélection du Modèle Champion Edge",
        "À l'issue de cette campagne d'évaluation approfondie, le **Gradient Boosting** s'impose sans conteste comme le champion absolu "
        "de la détection embarquée. Il conjugue une précision parfaite en nominal (F1 = 1.000), la plus haute résistance au bruit "
        "industriel (F1 = 0.978 à SNR = 0 dB), et une stabilité remarquable grâce à la régularisation par arbres peu profonds.",
        box_type="decision")

def add_chapter_5(doc):
    """Chapitre 5 : Inférence Embarquée, Profilage Matériel & Robustesse sur Raspberry Pi."""
    add_heading_1(doc, "Chapitre 5 : Inférence Embarquée, Profilage Matériel & Robustesse sur Raspberry Pi", page_break=True)
    
    add_heading_2(doc, "5.1 Architecture du Moteur d'Inférence Temps Réel et Simulation de Flux IoT")
    add_paragraph(doc,
        "Le moteur d'inférence embarqué a été implémenté dans le script `raspberry/inference_edge.py`. Il est conçu pour fonctionner "
        "en démon autonome sur architecture Linux ARM64. Le pipeline comprend :", bold_prefix="Pipeline d'Inférence Streaming : ")
    add_bullet_point(doc, "Acquisition du signal vibratoire par lecture d'un buffer circulaire glissant de 1024 points (simulant le bus SPI/I2C ou UART d'un capteur accélérométrique MEMS).", bold_title="1. Acquisition & Buffer")
    add_bullet_point(doc, "Extraction temps réel des 16 features temporelles et FFT via des opérations vectorisées NumPy C-optimisées en moins de 0.08 ms.", bold_title="2. Extraction Vectorisée")
    add_bullet_point(doc, "Application du scaler StandardScaler normalisé sans allocation mémoire dynamique superflue.", bold_title="3. Normalisation Standard")
    add_bullet_point(doc, "Exécution de la passe avant (predict) du modèle champion Gradient Boosting en C compilé via Cython/Scikit-Learn.", bold_title="4. Inférence Algorithmique")
    add_bullet_point(doc, "Journalisation locale horodatée au format JSON Lines (`raspberry/logs/inference_stream.log`) pour traçabilité industrielle sans blocage d'I/O.", bold_title="5. Télémétrie & Logs")

    add_heading_2(doc, "5.2 Protocole Expérimental de Profilage des Ressources (Latence, Débit, RAM, CPU)")
    add_paragraph(doc,
        "Le profilage de performance a été conduit à l'aide du script dédié `raspberry/benchmark_edge.py` sur nano-ordinateur Raspberry Pi 4. "
        "Le protocole de mesure repose sur :")
    add_bullet_point(doc, "Un préchauffage du processeur et des caches L1/L2 sur 100 itérations, suivi de 1 000 inférences consécutives synchronisées avec l'horloge haute précision `time.perf_counter_ns()`.", bold_title="Mesure de Latence")
    add_bullet_point(doc, "La surveillance de l'empreinte mémoire résidente (Resident Set Size - RSS) et de la charge CPU par processus via la bibliothèque `psutil` échantillonnée à 100 Hz.", bold_title="Consommation RAM et CPU")
    add_bullet_point(doc, "L'évaluation de la stabilité thermique du SoC Broadcom BCM2711 sous charge continue de 10 minutes d'inférence à plein débit.", bold_title="Profilage Thermique")

    # Tableau 09 : Résultats exhaustifs de benchmark
    headers_bench = ["Modèle IA", "Latence Moyenne (ms)", "Débit (fenêtres/sec)", "Empreinte RAM (Mo)", "Usage CPU (%)", "Taille Disque"]
    rows_bench = [
        ["Gradient Boosting ★", "0.218 ms", "4 560.9 fps", "28.4 Mo", "14.2 %", "30.6 KB"],
        ["1D-CNN Compact", "0.536 ms", "1 848.6 fps", "34.1 Mo", "26.8 %", "11.3 KB"],
        ["Autoencodeur PyTorch", "0.081 ms", "12 178.4 fps", "32.6 Mo", "11.5 %", "4.6 KB"],
        ["Isolation Forest", "1.214 ms", "822.6 fps", "45.8 Mo", "42.0 %", "573.3 KB"],
        ["Random Forest", "1.217 ms", "820.6 fps", "31.2 Mo", "38.5 %", "20.1 KB"]
    ]
    create_styled_table(doc, headers_bench, rows_bench, col_widths=[1.5, 1.2, 1.2, 1.1, 1.0, 0.8],
                        table_title="Résultats expérimentaux du profilage de ressources et de latence d'inférence sur nano-calculateur Raspberry Pi 4", table_number="09")

    # Figures 09 et 10 : Benchmark Edge
    fig09_path = os.path.join(FIG_DIR, '09_edge_latency_vs_f1.png')
    if os.path.exists(fig09_path):
        add_figure(doc, fig09_path, "5.1", 
                   "Compromis de performance Edge AI : Latence d'inférence (ms) vs F1-score sous bruit pour les 5 architectures évaluées", 
                   width_inches=5.8)

    fig10_path = os.path.join(FIG_DIR, '10_edge_ram_vs_model_size.png')
    if os.path.exists(fig10_path):
        add_figure(doc, fig10_path, "5.2", 
                   "Consommation de ressources matérielles sur Raspberry Pi : Empreinte RAM opérationnelle vs Taille physique des fichiers modèles", 
                   width_inches=5.8)

    add_heading_2(doc, "5.3 Matrice de Décision Multicritères pour le Déploiement Industriel")
    add_paragraph(doc,
        "Pour objectiver le choix final dans une perspective d'ingénierie d'industrialisation, nous avons établi une grille de décision "
        "pondérée selon 5 critères déterminants : Précision F1 nominale (poids 25 %), Robustesse au bruit (poids 25 %), Latence d'inférence "
        "(poids 20 %), Compacité RAM/Disque (poids 15 %) et Facilité d'intégration logicielle (poids 15 %) :")

    # Tableau 10 : Matrice multicritère
    headers_dec = ["Architecture Modèle", "F1 Nominal (25%)", "Robustesse (25%)", "Latence (20%)", "Compacité (15%)", "Intégration (15%)", "Note Globale / 100"]
    rows_dec = [
        ["Gradient Boosting ★", "25.0 / 25", "24.5 / 25", "19.5 / 20", "14.5 / 15", "14.5 / 15", "98.0 / 100 (Choix N°1)"],
        ["1D-CNN Compact", "25.0 / 25", "24.0 / 25", "18.0 / 20", "15.0 / 15", "13.0 / 15", "95.0 / 100 (Choix N°2)"],
        ["Random Forest", "25.0 / 25", "23.5 / 25", "15.0 / 20", "14.0 / 15", "14.5 / 15", "92.0 / 100"],
        ["Isolation Forest", "25.0 / 25", "21.0 / 25", "15.0 / 20", "11.0 / 15", "14.0 / 15", "86.0 / 100"],
        ["Autoencodeur", "2.5 / 25", "2.0 / 25", "20.0 / 20", "15.0 / 15", "13.0 / 15", "52.5 / 100"]
    ]
    create_styled_table(doc, headers_dec, rows_dec, col_widths=[1.5, 0.9, 0.9, 0.9, 0.9, 0.9, 1.2],
                        table_title="Matrice de décision multicritères pondérée pour la sélection de la technologie Edge AI industrielle", table_number="10")

    add_callout_box(doc, "Validation Industrielle de la Latence Réelle",
        "Avec une latence d'inférence de seulement **0.218 ms**, le Gradient Boosting s'exécute **391 fois plus vite** que la durée temporelle "
        "d'une fenêtre de signal (85.33 ms). Cela signifie que le nano-calculateur Raspberry Pi 4 ne mobilise que **0.25 % de son temps CPU** "
        "pour la surveillance prédictive continue, laissant 99.75 % des ressources disponibles pour la communication IIoT, l'agent RAG "
        "et la gestion de la sécurité.",
        box_type="norme")
