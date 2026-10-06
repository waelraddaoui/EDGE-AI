"""
report_builder/intro_chap1_2.py
-------------------------------
Introduction Générale, Chapitre 1 (Contexte & Cahier des charges) et
Chapitre 2 (État de l'Art Scientifique de niveau Revue Q1).
"""

import os
from report_builder.styles import (
    COLOR_NAVY, COLOR_STEEL, COLOR_CHARCOAL, COLOR_BODY, COLOR_MUTED,
    add_heading_1, add_heading_2, add_heading_3, add_paragraph,
    add_bullet_point, add_callout_box, add_figure, create_styled_table
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, 'figures')

def add_introduction(doc):
    """Introduction Générale du mémoire."""
    add_heading_1(doc, "Introduction Générale", page_break=True)
    
    add_paragraph(doc,
        "La quatrième révolution industrielle, communément qualifiée d'Industrie 4.0, se caractérise par "
        "la convergence des technologies de l'information et des processus opérationnels de production. "
        "Au cœur de cette mutation, l'Internet Industriel des Objets (IIoT) et l'Intelligence Artificielle "
        "redéfinissent en profondeur les paradigmes de la maintenance d'usine. Autrefois réactive (intervention "
        "après rupture) puis préventive systématique (remplacement programmé calendaire souvent prématuré et coûteux), "
        "la maintenance s'oriente désormais résolument vers la maintenance prédictive (Predictive Maintenance ou PdM). "
        "Cette stratégie novatrice repose sur l'auscultation continue de l'état de santé effectif des équipements critiques "
        "afin de détecter les micro-signes précurseurs de défaillance bien avant que ne survienne un arrêt catastrophique "
        "de la ligne de fabrication.")

    add_paragraph(doc,
        "Parmi les composants mécaniques les plus sollicités au sein du tissu manufacturier, les machines tournantes "
        "(moteurs électriques, compresseurs, turbines, ventilateurs et pompes industrielles) constituent la force motrice "
        "de l'outil productif. Au sein de ces machines, les roulements à billes représentent l'organe d'usure par excellence. "
        "Les études industrielles convergent pour estimer qu'entre 45 % et 55 % des défaillances imprévues des moteurs "
        "électriques sont directement imputables à la dégradation de leurs roulements (écaillage, fatigue de contact, "
        "grippage ou défaut de lubrification). Dans des secteurs à haute exigence de continuité de service tels que la sidérurgie, "
        "l'agroalimentaire, l'énergie ou les transports ferroviaires, une rupture inopinée de palier se traduit par des coûts "
        "d'arrêt pouvant s'élever à plusieurs dizaines de milliers d'euros par heure, sans omettre les risques considérables pour "
        "la sécurité physique des opérateurs et l'intégrité de l'environnement de travail.")

    add_paragraph(doc,
        "Durant la dernière décennie, la majorité des solutions de maintenance prédictive s'est construite sur une "
        "architecture centralisée dans le Cloud Computing. Les capteurs vibratoires collectent les séries temporelles haute "
        "fréquence et les transmettent via passerelle réseau vers des serveurs distants où sont hébergés de volumineux "
        "modèles d'apprentissage profond (Deep Learning). Cependant, ce schéma purement Cloud se heurte aujourd'hui à des "
        "verrous technologiques et opérationnels majeurs :", bold_prefix="Les verrous de l'approche Cloud traditionnelle : ")

    add_bullet_point(doc, 
        "Les signaux vibratoires échantillonnés entre 12 kHz et 48 kHz génèrent des volumes de données gigaoctets par heure et par machine. "
        "Leur transfert continu sature la bande passante locale et entraîne des coûts récurrents prohibitifs de télécommunication.",
        bold_title="Saturation de la bande passante IIoT")
        
    add_bullet_point(doc, 
        "Le temps d'aller-retour réseau (RTT) et la file d'attente d'inférence Cloud introduisent une latence oscillant entre plusieurs "
        "centaines de millisecondes et plusieurs secondes. Ce délai est totalement incompatible avec les mécanismes de coupure "
        "d'urgence ou d'alerte critique en temps réel nécessitant un temps de réponse déterministe inférieur à la dizaine de millisecondes.",
        bold_title="Latence incompatible avec le temps réel strict")
        
    add_bullet_point(doc, 
        "Les industriels manifestent une réticence légitime à exporter hors de leurs usines des signatures vibratoires pouvant refléter "
        "les cadences réelles de production ou des secrets de fabrication. De surcroît, une interruption de la connectivité Internet "
        "prive instantanément l'usine de toute protection prédictive.",
        bold_title="Confidentialité des données et dépendance réseau")

    add_paragraph(doc,
        "Pour surmonter ces obstacles, le paradigme de l'Intelligence Artificielle Embarquée à la Périphérie (Edge AI) "
        "s'impose comme l'alternative incontournable. En déportant les algorithmes d'inférence directement au plus près des machines, "
        "sur des nano-ordinateurs à faible coût et basse consommation énergétique tels que le Raspberry Pi, l'Edge AI garantit "
        "un traitement ultra-rapide, autonome, confidentiel et résilient aux coupures de réseau. Toutefois, le déploiement "
        "d'algorithmes d'IA sur des cibles matérielles aux ressources de calcul et de mémoire limitées soulève un défi d'ingénierie "
        "complexe : comment concevoir des modèles d'une extrême légèreté sans sacrifier la précision de détection ?")

    add_paragraph(doc,
        "À ce défi matériel s'ajoute un second verrou fondamental : la défiance des équipes de maintenance face à l'effet "
        "« boîte noire » des modèles d'IA complexes. Un technicien d'atelier ne peut interrompre une ligne de production "
        "sur la base d'une simple probabilité mathématique abstraite sans comprendre la justification physique de l'alerte. "
        "L'explicabilité (XAI - Explainable AI) devient ainsi un prérequis indispensable pour corréler les décisions algorithmiques "
        "avec des grandeurs physiques tangibles (Kurtosis, chocs impulsionnels, fréquences de passage des billes). De plus, "
        "face à une anomalie avérée, l'opérateur a besoin de consignes techniques précises et conformes aux protocoles de sécurité "
        "(Lockout/Tagout - LOTO). C'est ici qu'interviennent les agents intelligents autonomes augmentés par récupération "
        "documentaire (RAG - Retrieval-Augmented Generation), capables d'indexer les manuels constructeurs et les fiches "
        "mécaniques pour fournir une assistance conversationnelle contextualisée en langage naturel.")

    add_callout_box(doc, "Problématique Centrale du Stage",
        "Dans quelle mesure est-il possible de concevoir, d'optimiser et de déployer sur nano-ordinateur Raspberry Pi un système "
        "de détection d'anomalies de roulements mécaniques ultra-léger (< 1 ms de latence), explicable (XAI) et résilient aux bruits "
        "industriels, tout en couplant ce moteur à un agent conversationnel RAG capable de contextualiser les alertes et de guider "
        "les techniciens d'atelier au moyen de recommandations de maintenance rigoureuses et traçables ?",
        box_type="norme")

    add_paragraph(doc,
        "Le présent mémoire retrace l'intégralité de la démarche scientifique et technique menée pour répondre à cette problématique. "
        "Le document est articulé autour de 9 chapitres complémentaires :", bold_prefix="Organisation du Mémoire : ")

    add_bullet_point(doc, "Exposition des besoins, analyse fonctionnelle FAST et spécifications matérielles.", bold_title="Chapitre 1")
    add_bullet_point(doc, "Revue bibliographique exhaustive, cinématique des défauts et gaps scientifiques pour revue Q1.", bold_title="Chapitre 2")
    add_bullet_point(doc, "Ingestion des signaux CWRU/NASA, fenêtrage glissant et extraction des 16 caractéristiques temporelles/FFT.", bold_title="Chapitre 3")
    add_bullet_point(doc, "Conception, entraînement et comparaison des 5 architectures IA (arbres, 1D-CNN, autoencodeur).", bold_title="Chapitre 4")
    add_bullet_point(doc, "Moteur d'inférence en streaming IoT et benchmark approfondi sur Raspberry Pi (latence, RAM, CPU).", bold_title="Chapitre 5")
    add_bullet_point(doc, "Module d'explicabilité industrielle (XAI), attribution locale et dynamique des Z-scores.", bold_title="Chapitre 6")
    add_bullet_point(doc, "Agent IA / RAG, structuration de la base D1-D11 et génération automatique de rapports de diagnostic.", bold_title="Chapitre 7")
    add_bullet_point(doc, "Architecture logicielle full-stack, API FastAPI et dashboard React/Vite temps réel.", bold_title="Chapitre 8")
    add_bullet_point(doc, "Dossier pédagogique de travaux pratiques (16h) et grille d'évaluation sommative.", bold_title="Chapitre 9")

def add_chapter_1(doc):
    """Chapitre 1 : Contexte Industriel, Cahier des Charges & Analyse du Besoin."""
    add_heading_1(doc, "Chapitre 1 : Contexte Industriel, Cahier des Charges & Analyse du Besoin", page_break=True)
    
    add_heading_2(doc, "1.1 Contexte Général : La Révolution de la Maintenance Prédictive 4.0")
    add_paragraph(doc,
        "L'automatisation industrielle contemporaine exige une disponibilité opérationnelle quasi-continue des équipements. "
        "Dans ce contexte, la maintenance n'est plus considérée comme un centre de coût inévitable mais comme un levier stratégique "
        "de création de valeur. Le passage de la maintenance corrective (réaction post-avarie) à la maintenance préventive conditionnelle, "
        "puis prédictive, s'appuie sur la surveillance continue de paramètres physiques tels que la vibration, la température, le courant "
        "absorbé et l'émission acoustique. Parmi ces grandeurs, la vibration mécanique constitue l'indicateur le plus précoce et le plus "
        "riche d'enseignements : plus de 80 % des défauts mécaniques naissants se manifestent d'abord par des perturbations vibratoires "
        "bien avant toute élévation mesurable de température ou émission d'odeur de surchauffe.")

    add_heading_2(doc, "1.2 Problématique de Défaillance des Organes Rotatifs et Roulements")
    add_paragraph(doc,
        "Les roulements à billes ou à rouleaux ont pour fonction mécanique essentielle de guider la rotation d'un arbre tout en reprenant "
        "les charges radiales et axiales appliquées, en minimisant les frottements. Un roulement standard se compose de quatre éléments : "
        "la bague intérieure (solidaire de l'arbre tournant), la bague extérieure (solidaire du logement fixe ou palier), les éléments "
        "roulants (billes ou rouleaux) et la cage de guidage. Soumis à des contraintes de contact hertziennes cycliques très élevées "
        "(souvent supérieures à 1.5 GPa), ces éléments subissent au cours de leur cycle de vie des phénomènes de fatigue de sous-couche, "
        "conduisant à l'apparition de micro-fissures puis à l'écaillage superficiel (spalling).")
        
    add_paragraph(doc,
        "Chaque passage d'un élément roulant sur une discontinuité géométrique (défaut) génère un choc mécanique extrêmement bref "
        "(de l'ordre de quelques dizaines de microsecondes). Ces chocs répétés excitent les fréquences propres du roulement et de la structure, "
        "se traduisant dans le signal vibratoire par des trains d'ondes impulsionnelles amorties. Selon l'élément endommagé, la fréquence "
        "de répétition de ces chocs est rigoureusement régie par les rapports géométriques du composant et la vitesse de rotation.")

    add_heading_2(doc, "1.3 Analyse Fonctionnelle du Besoin (Méthode FAST et Exigences Opérationnelles)")
    add_paragraph(doc,
        "Afin de structurer avec rigueur le périmètre du projet, une analyse fonctionnelle descendante a été menée selon la méthode FAST "
        "(Function Analysis System Technique). La fonction globale (FP) attribuée au système s'énonce ainsi : « Surveiller en temps réel "
        "l'intégrité vibratoire d'un roulement industriel sur processeur embarqué, détecter et classifier toute anomalie naissante en moins "
        "d'une milliseconde, et guider l'opérateur humain dans son intervention de maintenance ».")

    add_paragraph(doc, "Cette fonction globale se décline en cinq fonctions de service principales :", bold_prefix="Décomposition Fonctionnelle : ")
    add_bullet_point(doc, "Acquérir le signal accélérométrique et découper le flux temporel en fenêtres glissantes normalisées.", bold_title="FS1 - Ingestion & Prétraitement")
    add_bullet_point(doc, "Extraire un vecteur compact d'indicateurs statistiques temporels et spectraux FFT à forte séparabilité physique.", bold_title="FS2 - Caractérisation")
    add_bullet_point(doc, "Exécuter l'inférence via un algorithme IA optimisé pour architecture ARM avec une latence inférieure à 1 ms.", bold_title="FS3 - Inférence Edge")
    add_bullet_point(doc, "Calculer l'attribution des variables (Z-scores, SHAP) pour rendre la décision intelligible par un technicien.", bold_title="FS4 - Explicabilité XAI")
    add_bullet_point(doc, "Assister l'opérateur via un agent RAG indexant la documentation technique et générer les fiches d'intervention.", bold_title="FS5 - Assistance RAG")

    add_heading_2(doc, "1.4 Spécifications Matérielles et Exigences Temps Réel sur Raspberry Pi")
    add_paragraph(doc,
        "Le cahier des charges impose le déploiement du prototype sur une cible matérielle représentative des passerelles IIoT d'atelier : "
        "le nano-ordinateur Raspberry Pi 4 Modèle B (processeur Broadcom BCM2711, Quad-core Cortex-A72 ARM v8 64-bit à 1.5 GHz, 4 Go de RAM LPDDR4). "
        "Cette cible matérielle impose des contraintes sévères :", bold_prefix="Contraintes Matérielles Strictes : ")
        
    add_bullet_point(doc, "Le temps de traitement total (extraction de features + inférence) doit être strictement inférieur à la durée de la fenêtre temporelle analysée (85.3 ms) et idéalement inférieur à 1.0 ms pour préserver 98 % des cycles CPU pour les tâches système et de communication.", bold_title="Budget de Latence Temps Réel")
    add_bullet_point(doc, "L'empreinte mémoire vive allouée au modèle d'IA ne doit pas excéder 50 Mo afin de cohabiter avec le système d'exploitation Linux et les services réseau.", bold_title="Empreinte Mémoire RAM")
    add_bullet_point(doc, "Le modèle sauvegardé doit présenter une taille de fichier minimale (< 1 Mo) pour faciliter les mises à jour logicielles OTA (Over-The-Air) sur des réseaux industriels à bas débit.", bold_title="Compacité du Modèle")
    add_bullet_point(doc, "Le système doit maintenir un taux de fausse alarme inférieur à 2 % même en présence d'un environnement électromagnétique bruité et de pertes ponctuelles d'échantillons.", bold_title="Robustesse Environnementale")

    add_heading_2(doc, "1.5 Découpage en Livrables (L1 à L17) et Planning Stratégique")
    add_paragraph(doc,
        "Conformément au cahier des charges officiel du stage, les travaux ont été scrupuleusement jalonnés selon un plan d'assurance "
        "qualité en 17 livrables majeurs (L1 à L17), couvrant les volets données, algorithmes, déploiement embarqué, documentation et pédagogie.")

    # Tableau 01 : Matrice de conformité des 17 livrables
    headers_l = ["Code", "Intitulé Officiel du Livrable", "Emplacement dans le Dépôt", "Statut de Validation"]
    rows_l = [
        ["L1", "Fichiers bruts & nettoyés CWRU", "data/raw/, data/processed/", "Validé (100 %)"],
        ["L2", "Dataset synthétique hybride perturbé", "data/processed/features_hybrid.parquet", "Validé (100 %)"],
        ["L3", "Dataset pédagogique réduit", "data/pedagogical_subset/cwru_pedagogical_subset.csv", "Validé (100 %)"],
        ["L4", "Notebook exploratoire des signaux", "notebooks/01_exploration.ipynb", "Validé (100 %)"],
        ["L5", "Code Python prétraitement & fenêtrage", "src/data_preparation.py", "Validé (100 %)"],
        ["L6", "Module extraction de caractéristiques FFT", "src/feature_extraction.py", "Validé (100 %)"],
        ["L7", "Code d'entraînement des 5 modèles IA", "src/train_models.py", "Validé (100 %)"],
        ["L8", "Code d'évaluation & matrices de confusion", "src/evaluate_models.py", "Validé (100 %)"],
        ["L9", "Moteur d'inférence Edge AI IoT streaming", "raspberry/inference_edge.py", "Validé (100 %)"],
        ["L10", "Profiler de ressources & robustesse", "raspberry/benchmark_edge.py", "Validé (100 %)"],
        ["L11", "Logs de benchmark JSON & streaming", "raspberry/logs/benchmark_results.json", "Validé (100 %)"],
        ["L12", "Module d'explicabilité XAI (Z-scores)", "src/explainability.py", "Validé (100 %)"],
        ["L13", "Figures HD et fiches de décision Edge", "figures/ (01 à 10), reports/edge_decision_matrix.md", "Validé (100 %)"],
        ["L14", "Base documentaire technique RAG (D1-D11)", "rag_agent/documents/", "Validé (100 %)"],
        ["L15", "Agent conversationnel RAG & diagnostic", "rag_agent/ask_agent.py, generate_diagnostic.py", "Validé (100 %)"],
        ["L16", "Dossier pédagogique TP (16h) & grille", "reports/cas_pedagogique.md, grille_evaluation.md", "Validé (100 %)"],
        ["L17", "Rapport final, Article Q1 & Présentation", "reports/rapport_final.md, draft_article.md, pptx", "Validé (100 %)"]
    ]
    create_styled_table(doc, headers_l, rows_l, col_widths=[0.6, 2.5, 2.3, 1.1], 
                        table_title="Matrice de conformité et de validation des 17 livrables du cahier des charges", table_number="01")

    # Insertion de la Figure 11
    fig11_path = os.path.join(FIG_DIR, '11_system_architecture_pipeline.png')
    if os.path.exists(fig11_path):
        add_figure(doc, fig11_path, "1.1", 
                   "Architecture globale et flux fonctionnel du système unifié : De l'acquisition IIoT à l'assistance RAG et au cockpit React", 
                   width_inches=6.2)

def add_chapter_2(doc):
    """Chapitre 2 : État de l'Art Scientifique Approfondi (Revue Q1)."""
    add_heading_1(doc, "Chapitre 2 : État de l'Art Scientifique Approfondi (Revue de Rang Q1)", page_break=True)
    
    add_paragraph(doc,
        "La rédaction de ce chapitre s'inscrit dans les exigences de rigueur méthodologique formulées par l'encadrante académique "
        "Mme Amina Rouis pour la préparation d'un article scientifique destiné à une revue internationale de premier rang (Q1, telle que "
        "IEEE Transactions on Industrial Informatics ou Mechanical Systems and Signal Processing). L'objectif est de dresser un état de l'art "
        "critique, comparatif et fondé sur des références bibliographiques vérifiées au format IEEE, en mettant en exergue les méthodes, "
        "les protocoles, les limites méthodologiques, les informations non rapportées dans la littérature et les gaps scientifiques que "
        "ce projet ambitionne de combler.")

    add_heading_2(doc, "2.1 Panorama des Datasets Vibratoires de Référence dans la Littérature")
    add_paragraph(doc,
        "La communauté de recherche en maintenance prédictive s'appuie sur plusieurs corpus de données publiques pour benchmarker les "
        "algorithmes de détection de défauts. L'analyse critique de ces jeux de données permet de justifier le choix du banc CWRU complété "
        "par les essais run-to-failure de la NASA IMS pour notre étude expérimentale.")

    # Tableau 02 : Analyse comparative des datasets
    headers_d = ["Dataset", "Type de Signal", "Conditions d'Essai", "Modes de Défaillance", "Atouts & Limites"]
    rows_d = [
        ["CWRU Bearing Data", "Vibrations 12/48 kHz (accéléromètres)", "4 charges moteur (0 à 3 HP), vitesse 1720-1797 RPM", "Bague interne (BPFI), Bague externe (BPFO), Billes (BSF)", "Standard mondial, reproductibilité parfaite. Limite : défauts créés artificiellement par électroérosion."],
        ["NASA IMS Bearing", "Vibrations 20 kHz (essais d'endurance)", "Vitesse fixe 2000 RPM, charge radiale 6000 lbs", "Dégradation naturelle continue jusqu'à rupture (Run-to-Failure)", "Phénomène physique d'usure réelle. Limite : absence d'états intermédiaires étiquetés avec précision."],
        ["PRONOSTIA (FEMTO-ST)", "Vibrations 25.6 kHz + Température", "Vitesse et charges dynamiques variables", "Dégradation accélérée sous forte charge", "Excellente richesse dynamique pour le RUL. Limite : durées d'essais très courtes (< quelques heures)."],
        ["MIMII Dataset", "Acoustique / Audio (microphones)", "4 types d'équipements (pompes, vannes, rails)", "Usure globale et anomalies sonores", "Non invasif. Limite : très forte sensibilité au bruit ambiant d'atelier d'usinage."],
        ["SWaT / WADI", "Séries multivariées (51 capteurs IIoT)", "Banc pilote de traitement des eaux en continu", "Cyberattaques physiques et anomalies process", "Très réaliste pour la cybersécurité IIoT. Limite : accès restreint sur convention académique."]
    ]
    create_styled_table(doc, headers_d, rows_d, col_widths=[1.2, 1.2, 1.3, 1.3, 1.5],
                        table_title="Analyse comparative multi-critères des jeux de données de référence pour la maintenance prédictive", table_number="02")

    add_heading_2(doc, "2.2 Fondements Physiques Vibratoires et Équations Cinématiques des Défauts")
    add_paragraph(doc,
        "Lorsqu'un défaut localisé apparaît sur une surface de roulement, chaque impact produit une impulsion mécanique périodique. "
        "La théorie cinématique du contact élastodynamique permet de calculer avec exactitude les fréquences fondamentales de défaut "
        "en fonction de la géométrie du roulement et de la vitesse de rotation de l'arbre $f_r$ (en Hz) :")

    add_paragraph(doc,
        "1. Fréquence de passage sur la bague externe (Ball Pass Frequency Outer Race - BPFO) :\n"
        "   $$BPFO = \\frac{N_b}{2} \\cdot f_r \\cdot \\left( 1 - \\frac{d}{D} \\cos \\alpha \\right)$$\n\n"
        "2. Fréquence de passage sur la bague interne (Ball Pass Frequency Inner Race - BPFI) :\n"
        "   $$BPFI = \\frac{N_b}{2} \\cdot f_r \\cdot \\left( 1 + \\frac{d}{D} \\cos \\alpha \\right)$$\n\n"
        "3. Fréquence de rotation propre de la bille (Ball Spin Frequency - BSF) :\n"
        "   $$BSF = \\frac{D}{2d} \\cdot f_r \\cdot \\left( 1 - \\left( \\frac{d}{D} \\cos \\alpha \\right)^2 \\right)$$\n\n"
        "4. Fréquence de rotation de la cage (Fundamental Train Frequency - FTF) :\n"
        "   $$FTF = \\frac{1}{2} \\cdot f_r \\cdot \\left( 1 - \\frac{d}{D} \\cos \\alpha \\right)$$",
        bold_prefix="Formules Cinématiques Fondamentales : ")

    add_paragraph(doc,
        "Où $N_b$ représente le nombre de billes, $d$ le diamètre de la bille, $D$ le diamètre primitif du roulement (Pitch Diameter), "
        "$\\alpha$ l'angle de contact mécanique, et $f_r$ la fréquence de rotation de l'arbre ($f_r = \\text{RPM} / 60$). "
        "Pour le roulement de référence SKF 6205-2RS instrumenté sur le banc CWRU à une vitesse nominale de 1797 RPM ($f_r = 29.95$ Hz), "
        "les grandeurs cinématiques exactes sont récapitulées dans le Tableau 03.")

    # Tableau 03 : Caractéristiques SKF 6205-2RS
    headers_skf = ["Paramètre Mécanique", "Symbole", "Valeur Numérique", "Unité / Définition"]
    rows_skf = [
        ["Diamètre d'alésage intérieur", "d_in", "25.0", "mm"],
        ["Diamètre extérieur du palier", "d_out", "52.0", "mm"],
        ["Diamètre primitif moyen", "D", "39.04", "mm (Pitch Diameter)"],
        ["Diamètre des éléments roulants (billes)", "d", "7.94", "mm (0.3125 pouce)"],
        ["Nombre d'éléments roulants", "N_b", "9", "billes"],
        ["Angle de contact opérationnel", "alpha", "0.0", "degrés (charge purement radiale)"],
        ["Fréquence de passage bague externe", "BPFO", "107.4", "Hz (3.58 x f_r)"],
        ["Fréquence de passage bague interne", "BPFI", "162.2", "Hz (5.41 x f_r)"],
        ["Fréquence de rotation propre de bille", "BSF", "47.1", "Hz (2.35 x f_r)"],
        ["Fréquence fondamentale de cage", "FTF", "11.9", "Hz (0.398 x f_r)"]
    ]
    create_styled_table(doc, headers_skf, rows_skf, col_widths=[2.2, 0.9, 1.2, 2.2],
                        table_title="Paramètres géométriques et fréquences caractéristiques de défaut du roulement SKF 6205-2RS à 1797 RPM", table_number="03")

    # Tableau 04 : Norme ISO 10816-3
    headers_iso = ["Zone de Sévérité", "Vitesse Efficace RMS (mm/s)", "État de la Machine", "Action Technique Préconisée"]
    rows_iso = [
        ["Zone A (Vert)", "< 1.4 mm/s", "Machine neuve ou venant d'être révisée", "Fonctionnement optimal sans restriction."],
        ["Zone B (Jaune)", "1.4 à 2.8 mm/s", "Fonctionnement normal admissible", "Exploitation continue autorisée à long terme."],
        ["Zone C (Orange)", "2.8 à 4.5 mm/s", "Fonctionnement dégradé non admissible", "Planifier une intervention de maintenance sous 48h."],
        ["Zone D (Rouge)", "> 4.5 mm/s", "Vibrations dangereuses, risque de rupture", "Arrêt d'urgence immédiat et consignation LOTO."]
    ]
    create_styled_table(doc, headers_iso, rows_iso, col_widths=[1.4, 1.6, 1.8, 1.7],
                        table_title="Seuils vibratoires globaux selon la norme internationale ISO 10816-3 (Machines de Classe I et II)", table_number="04")

    add_heading_2(doc, "2.3 Algorithmes d'Apprentissage Automatique pour la Détection d'Anomalies")
    add_paragraph(doc,
        "La littérature académique recense trois grandes familles d'approches algorithmiques pour la détection et la classification d'anomalies :")
    add_bullet_point(doc, "Les forêts aléatoires (Random Forest) et les arbres stimulés par gradient (Gradient Boosting / XGBoost) combinés à une extraction de caractéristiques expertes. Ils dominent historiquement par leur compacité mémoire, leur faible coût computationnel et leur grande interprétabilité.", bold_title="Machine Learning Classique Supervisé")
    add_bullet_point(doc, "Réseaux convolutifs 1D (1D-CNN), réseaux récurrents (LSTM) et architectures Transformer temporelles (PatchTST). Capables d'apprendre des représentations hiérarchiques directement depuis les signaux bruts, ils exigent toutefois des ressources de calcul prohibitives pour l'embarqué sans accélération matérielle.", bold_title="Deep Learning End-to-End")
    add_bullet_point(doc, "Isolation Forest, One-Class SVM et Autoencodeurs neuronaux. Entraînés exclusivement sur des données saines, ils détectent les dérives par rapport à la normale via une métrique de distance ou une erreur de reconstruction (MSE).", bold_title="Apprentissage Non Supervisé / Semi-Supervisé")

    add_heading_2(doc, "2.4 Technologies d'Optimisation et de Déploiement Embarqué Edge AI")
    add_paragraph(doc,
        "Le déploiement sur nano-calculateur requiert des techniques d'optimisation spécifiques : la quantification post-entraînement "
        "(passage des poids de FP32 à INT8), l'élagage structurel (pruning) et l'exploitation de moteurs d'inférence légers tels que "
        "ONNX Runtime, TensorFlow Lite ou des frameworks compilés C/C++ (Treelite). Les revues récentes indiquent que la quantification INT8 "
        "permet de diviser par quatre la consommation mémoire tout en accélérant l'inférence d'un facteur 2 à 3 sur architecture ARM Cortex-A72, "
        "avec une dégradation de précision généralement inférieure à 0.5 %.")

    add_heading_2(doc, "2.5 L'Explicabilité (XAI) dans les Processus Industriels Critiques")
    add_paragraph(doc,
        "L'adoption de l'IA par les équipes d'exploitation industrielle exige une totale transparence des prédictions. "
        "Deux méthodes dominent la littérature : SHAP (Shapley Additive exPlanations), fondée sur la théorie des jeux coopératifs pour attribuer "
        "à chaque variable une contribution additive équitable, et LIME (Local Interpretable Model-agnostic Explanations), qui approxime "
        "localement la frontière de décision par un modèle linéaire. Toutefois, le calcul exact des valeurs SHAP s'avère extrêmement coûteux "
        "en temps de calcul sur processeur embarqué. Une approche prometteuse consiste à combiner l'importance intrinsèque des arbres de décision "
        "avec une analyse différentielle par Z-scores par rapport au profil sain de référence.")

    add_heading_2(doc, "2.6 L'Avènement des Agents Intelligents et du RAG pour le Diagnostic IIoT")
    add_paragraph(doc,
        "L'émergence des modèles de langage de grande taille (LLM) et des architectures RAG (Retrieval-Augmented Generation) en 2024-2026 "
        "ouvre une perspective inédite pour l'assistance technique. Des frameworks industriels pionniers tels que MindRAG structurent "
        "les manuels constructeurs, les historiques de pannes et les schémas cinématiques dans une base vectorielle dense. Lorsqu'une alerte "
        "vibratoire est déclenchée, l'agent RAG récupère les chunks documentaires les plus similaires pour synthétiser un rapport d'intervention "
        "complet et factuel, éliminant tout risque d'hallucination en contraignant la réponse aux documents sources vérifiés.")

    add_heading_2(doc, "2.7 Synthèse Critique, Limites des Approches Existantes et Identification des Gaps")
    add_paragraph(doc,
        "L'analyse approfondie de plus de 35 publications récentes permet de dégager trois gaps scientifiques et technologiques majeurs "
        "qui justifient la contribution singulière de ce projet de stage :", bold_prefix="Identification des Gaps de Recherche : ")
        
    add_bullet_point(doc, "La très grande majorité des études publie des métriques algorithmiques théoriques (Accuracy, AUC) calculées sur des serveurs PC puissants (GPU Nvidia), sans jamais profiler la latence réelle, l'usage CPU, l'empreinte RAM dynamique et la dérive thermique sur une cible matérielle représentative telle qu'un Raspberry Pi en conditions de streaming continu.", bold_title="Gap 1 — Absence de benchmark matériel resource-aware complet")
    add_bullet_point(doc, "Les publications évaluent presque exclusivement les modèles sur des signaux CWRU propres et idéaux. Les performances sous bruits sévères d'atelier (dérives thermiques, pertes de paquets IoT, bruits électromagnétiques) ne sont quasiment jamais rapportées de manière comparative.", bold_title="Gap 2 — Manque d'évaluation de la robustesse face aux perturbations d'atelier")
    add_bullet_point(doc, "Il n'existe dans la littérature aucun système unifié intégrant la chaîne complète : de l'acquisition vibratoire brute jusqu'à l'assistance conversationnelle RAG et à la génération automatique d'ordres de travail pour techniciens, le tout orchestré de manière sobre et fonctionnelle.", bold_title="Gap 3 — Rupture entre la détection algorithmique et l'action humaine de maintenance")
