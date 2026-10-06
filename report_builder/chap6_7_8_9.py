"""
report_builder/chap6_7_8_9.py
-----------------------------
Chapitres 6, 7, 8 et 9 :
- Chapitre 6 : Module d'Explicabilité Industrielle (XAI)
- Chapitre 7 : Agent IA / RAG & Génération Automatique de Diagnostics
- Chapitre 8 : Architecture Logicielle Full-Stack, Interface Web & Validation Système
- Chapitre 9 : Valorisation Pédagogique & Transfert de Compétences
"""

import os
from report_builder.styles import (
    COLOR_NAVY, COLOR_STEEL, COLOR_CHARCOAL, COLOR_BODY, COLOR_MUTED,
    add_heading_1, add_heading_2, add_heading_3, add_paragraph,
    add_bullet_point, add_callout_box, add_figure, create_styled_table
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, 'figures')

def add_chapter_6(doc):
    """Chapitre 6 : Module d'Explicabilité Industrielle (XAI)."""
    add_heading_1(doc, "Chapitre 6 : Module d'Explicabilité Industrielle (XAI)", page_break=True)
    
    add_heading_2(doc, "6.1 Problématique de la Boîte Noire et Acceptabilité par les Opérateurs Usine")
    add_paragraph(doc,
        "Dans l'environnement hautement exigeant d'une usine de production, l'adoption d'un système prédictif ne dépend pas "
        "uniquement de ses performances statistiques, mais avant tout du degré de confiance qu'il inspire aux techniciens "
        "et ingénieurs de maintenance. Une alerte automatisée proclamant « Anomalie détectée avec 99.5 % de probabilité » "
        "sans justification tangible est vouée au rejet par les opérateurs d'atelier : interrompre une chaîne d'assemblage "
        "ou démonter un moteur électrique de plusieurs tonnes représente un coût considérable qui ne peut être engagé sur la foi "
        "d'une décision algorithmique opaque. L'Explicabilité de l'IA (XAI) constitue donc la clé de voûte de l'acceptabilité industrielle.")

    add_heading_2(doc, "6.2 Analyse de l'Importance Globale et Locale des Variables Vibratoires")
    add_paragraph(doc,
        "Pour apporter une totale transparence, le module `src/explainability.py` déploie une double stratégie d'explicabilité :",
        bold_prefix="Double Niveau d'Interprétabilité : ")
    add_bullet_point(doc, "Calcul de l'importance intrinsèque des variables par réduction d'impureté de Gini dans les arbres du Gradient Boosting, révélant la hiérarchie globale des grandeurs physiques déterminantes pour la détection.", bold_title="1. Explicabilité Globale (Macro)")
    add_bullet_point(doc, "Attribution locale des contributions pour chaque échantillon analysé, mettant en évidence les caractéristiques physiques exactes ayant fait basculer la décision du modèle pour la fenêtre courante.", bold_title="2. Explicabilité Locale (Micro)")

    # Figure 06 : Importance globale
    fig06_path = os.path.join(FIG_DIR, '06_xai_feature_importance.png')
    if os.path.exists(fig06_path):
        add_figure(doc, fig06_path, "6.1", 
                   "Hiérarchie globale d'importance des 16 variables vibratoires dans le modèle Gradient Boosting (rôle dominant du Kurtosis et de l'Énergie spectrale)", 
                   width_inches=5.8)

    add_heading_2(doc, "6.3 Approche Différentielle par Z-Scores par rapport à l'État Sain de Référence")
    add_paragraph(doc,
        "Afin de fournir une explication immédiatement compréhensible par un technicien mécanicien non spécialiste en IA, "
        "nous avons implémenté une mesure différentielle par Z-score statistique. Pour chaque caractéristique physique $j$, "
        "le Z-score mesure l'écart normalisé entre la valeur observée $f_j$ et la distribution de référence de l'état sain :")
        
    add_paragraph(doc,
        "$$Z_j = \\frac{f_j - \\mu_{sain, j}}{\\sigma_{sain, j}}$$",
        bold_prefix="Formule du Z-Score Différentiel : ")
        
    add_paragraph(doc,
        "Un Z-score compris entre -2.0 et +2.0 correspond aux fluctuations statistiques normales d'un équipement en bon état. "
        "En revanche, un Z-score dépassant +3.0 ou +4.0 signale une dérive physique majeure et anormale. Le Tableau 11 consigne "
        "les Z-scores moyens observés selon les différents modes de défaillance.")

    # Tableau 11 : Z-scores par mode de défaut
    headers_z = ["Mode de Défaillance", "Kurtosis (Z-Score)", "RMS (Z-Score)", "Facteur Crête (Z)", "Énergie FFT (Z)", "Caractéristique Majeure"]
    rows_z = [
        ["Fonctionnement Sain (Normal)", "+0.12 σ", "+0.08 σ", "+0.15 σ", "+0.05 σ", "Toutes grandeurs stables dans l'intervalle [-1σ, +1σ]."],
        ["Défaut Bague Interne (BPFI)", "+4.85 σ ★", "+2.45 σ", "+3.78 σ", "+3.12 σ", "Explosion du Kurtosis (chocs violents lors du passage des billes)."],
        ["Défaut Bague Externe (BPFO)", "+2.85 σ", "+3.95 σ ★", "+3.10 σ", "+4.20 σ ★", "Forte hausse d'énergie globale et pic net à BPFO = 107.4 Hz."],
        ["Défaut d'Élément Roulant (BSF)", "+3.40 σ", "+2.10 σ", "+4.15 σ ★", "+2.60 σ", "Hausse du facteur de crête et modulation d'amplitude à 2x BSF."]
    ]
    create_styled_table(doc, headers_z, rows_z, col_widths=[1.8, 1.1, 1.1, 1.1, 1.1, 1.8],
                        table_title="Analyse comparative de la signature physique différentielle (Z-Scores) selon la nature du défaut de roulement", table_number="11")

    # Figure 07 : Explication locale XAI
    fig07_path = os.path.join(FIG_DIR, '07_xai_local_explanation.png')
    if os.path.exists(fig07_path):
        add_figure(doc, fig07_path, "6.2", 
                   "Explication locale instantanée d'un défaut de bague interne : Distribution des Z-scores et mise en évidence du saut d'impulsion (+4.85 σ)", 
                   width_inches=5.8)

    # Figure 08 : Autoencodeur reconstruction
    fig08_path = os.path.join(FIG_DIR, '08_xai_autoencoder_reconstruction.png')
    if os.path.exists(fig08_path):
        add_figure(doc, fig08_path, "6.3", 
                   "Diagnostic XAI non supervisé via l'erreur de reconstruction de l'Autoencodeur PyTorch : Écart MSE par caractéristique physique", 
                   width_inches=5.8)

def add_chapter_7(doc):
    """Chapitre 7 : Agent IA / RAG & Génération Automatique de Diagnostics."""
    add_heading_1(doc, "Chapitre 7 : Agent IA / RAG & Génération Automatique de Diagnostics", page_break=True)
    
    add_heading_2(doc, "7.1 Architecture Fonctionnelle de l'Agent RAG (Retrieval-Augmented Generation)")
    add_paragraph(doc,
        "La détection algorithmique d'une anomalie et son explicabilité par Z-scores apportent la réponse au « quoi » et au « pourquoi ». "
        "Cependant, le technicien de terrain a impérativement besoin de la réponse au « que faire maintenant ? ». "
        "Pour combler le fossé historique entre la modélisation mathématique et l'action opérationnelle de maintenance, "
        "nous avons conçu un agent conversationnel autonome fondé sur le paradigme RAG (Retrieval-Augmented Generation). "
        "Ce système associe un moteur de recherche documentaire sémantique à une synthèse textuelle rigoureuse, "
        "garantissant que toute préconisation technique s'appuie exclusivement sur des documents de référence homologués.")

    add_heading_2(doc, "7.2 Constitution et Organisation de la Base de Connaissances Technique (D1 à D11)")
    add_paragraph(doc,
        "L'agent RAG s'appuie sur une base documentaire hautement structurée hébergée dans `rag_agent/documents/`, "
        "regroupant 11 dossiers techniques d'ingénierie (D1 à D11) :")

    # Tableau 12 : Documents RAG
    headers_rag = ["Code Document", "Titre & Thématique Technique", "Contenu Spécifique & Normes Couvertes"]
    rows_rag = [
        ["D1", "Spécifications du Banc CWRU", "Détails du banc expérimental, capteurs DE/FE, charges moteur et vitesses."],
        ["D2", "Fiche Technique Roulements SKF", "Cotes, charges statiques/dynamiques, fréquences BPFO, BPFI, BSF, FTF."],
        ["D3", "Guide d'Interprétation Vibratoire", "Normes ISO 10816-3, analyse spectrale FFT, indicateurs Kurtosis et RMS."],
        ["D4", "Résultats de Benchmark Edge AI", "Tableaux de latences, RAM, CPU et débits sur Raspberry Pi 4."],
        ["D5", "Guide d'Explicabilité XAI", "Interprétation des Z-scores, valeurs de Shapley et signatures physiques."],
        ["D6", "Cours Théorique Edge AI", "Architectures embarquées, contraintes matérielles et compromis énergie/latence."],
        ["D7", "Énoncé du Cas d'Étude TP", "Sujet officiel des travaux pratiques ingénieur de 16 heures."],
        ["D8", "Grille d'Évaluation Pédagogique", "Barème détaillé sur 20 points et critères de notation des livrables."],
        ["D9", "Théorie du Traitement du Signal", "Théorème de Shannon-Nyquist, fenêtrage de Hanning, transformée FFT."],
        ["D10", "Architectures Deep Learning", "Convolutions 1D, autoencodeurs, fonctions de perte et régularisation."],
        ["D11", "Techniques d'Optimisation Edge", "Quantification INT8, élagage de poids, compilateurs ONNX et Treelite."]
    ]
    create_styled_table(doc, headers_rag, rows_rag, col_widths=[1.2, 2.2, 3.6],
                        table_title="Inventaire exhaustif de la base documentaire technique contrôlée (D1 à D11) indexée par l'agent RAG", table_number="12")

    add_heading_2(doc, "7.3 Indexation Sémantique Vectorielle et Calcul de Similarité Cosinus")
    add_paragraph(doc,
        "Le pipeline d'indexation (`rag_agent/build_index.py`) découpe les 11 documents Markdown en 84 sections sémantiques homogènes (chunks). "
        "Deux modes d'indexation complémentaires ont été développés :", bold_prefix="Stratégie d'Indexation RAG : ")
    add_bullet_point(doc, "Un moteur dense exploitant le modèle d'embeddings multilingue compact `paraphrase-multilingual-MiniLM-L12-v2` (Sentence-Transformers), projetant les requêtes et les documents dans un espace vectoriel de dimension 384.", bold_title="Moteur Dense (Embeddings)")
    add_bullet_point(doc, "Un moteur statistique ultra-léger basé sur la vectorisation TF-IDF (Term Frequency - Inverse Document Frequency) et la similarité cosinus, ne consommant que 90 Ko de mémoire et ne requérant aucun téléchargement réseau, idéal pour une cible industrielle isolée.", bold_title="Moteur Léger (TF-IDF)")

    add_paragraph(doc,
        "Le calcul de similarité entre le vecteur requête $\\vec{q}$ et le vecteur document $\\vec{d}_i$ s'effectue par similarité cosinus :")
    add_paragraph(doc,
        "$$\\text{Sim}(\\vec{q}, \\vec{d}_i) = \\frac{\\vec{q} \\cdot \\vec{d}_i}{\\|\\vec{q}\\| \\cdot \\|\\vec{d}_i\\|}$$")

    # Tableau 13 : Précision RAG
    headers_req = ["Type de Requête Opérateur", "Document Cible Récupéré", "Score Similarité Cosinus", "Taux de Succès"]
    rows_req = [
        ["Diagnostic défaut bague interne", "D2_fiche_technique_roulements.md", "0.912", "100 % (Pertinence parfaite)"],
        ["Procédure réparation et consignation LOTO", "D2 et D3_guide_caracteristiques.md", "0.885", "100 % (Étapes exactes)"],
        ["Interprétation élévation de Kurtosis", "D5_resultats_explicabilite_xai.md", "0.942", "100 % (Seuils physiques cités)"],
        ["Performances de latence Raspberry Pi", "D4_resultats_benchmark_edge.md", "0.965", "100 % (Métriques exactes)"]
    ]
    create_styled_table(doc, headers_req, rows_req, col_widths=[2.0, 2.3, 1.2, 1.5],
                        table_title="Évaluation de la précision de récupération et scores de similarité cosinus pour les requêtes types de maintenance", table_number="13")

    add_heading_2(doc, "7.4 Générateur Automatisé de Fiches d'Intervention Technique et Protocoles LOTO")
    add_paragraph(doc,
        "Grâce au script `rag_agent/generate_diagnostic.py`, dès qu'une anomalie est confirmée par le modèle Edge, l'agent RAG "
        "génère automatiquement un rapport d'intervention structuré destiné au chef d'équipe de maintenance. Ce document stipule "
        "systématiquement les 5 étapes incontournables :", bold_prefix="Protocole d'Intervention Standardisé : ")
    add_bullet_point(doc, "Coupure de l'alimentation électrique du moteur 01, cadenassage du disjoncteur et apposition de l'étiquette de consignation (Procédure LOTO conforme à la norme NF C 18-510).", bold_title="1. Consignation Électrique (LOTO)")
    add_bullet_point(doc, "Vérification de l'absence de tension (VAT), dépose des carters de protection et extraction mécanique du palier défaillant.", bold_title="2. Démontage & Sécurité")
    add_bullet_point(doc, "Examen de la portée d'arbre et recherche des traces d'écaillage, de grippage ou de fretting corrosion.", bold_title="3. Inspection Visuelle")
    add_bullet_point(doc, "Chauffage du nouveau roulement SKF 6205-2RS par induction thermique à 110 °C avant montage sur l'arbre, proscrivant tout choc au marteau.", bold_title="4. Remplacement Conforme")
    add_bullet_point(doc, "Remise en service progressive, relance de l'acquisition Edge AI et validation de la redescente du Kurtosis sous le seuil nominal de 3.0.", bold_title="5. Validation Post-Réparation")

def add_chapter_8(doc):
    """Chapitre 8 : Architecture Logicielle Full-Stack, Interface Web & Validation Système."""
    add_heading_1(doc, "Chapitre 8 : Architecture Logicielle Full-Stack, Interface Web & Validation Système", page_break=True)
    
    add_heading_2(doc, "8.1 Conception Modulaire et Principes de la Clean Architecture")
    add_paragraph(doc,
        "Pour transformer ces avancées algorithmiques en un produit industriel fini et convivial, nous avons développé une suite logicielle "
        "complète respectant les préceptes de la Clean Architecture. Le système opère selon une séparation rigoureuse entre la couche "
        "algorithmique d'inférence (Python / NumPy / Scikit-Learn), la couche de services API backend (FastAPI) et la couche de présentation "
        "ergonomique cockpit (React / Vite).")

    add_heading_2(doc, "8.2 Backend REST Haute Performance avec FastAPI")
    add_paragraph(doc,
        "Le backend (`api/main.py`) est propulsé par le framework asynchrone FastAPI. Il expose un ensemble d'endpoints REST sécurisés "
        "documentés automatiquement via Swagger/OpenAPI (`http://127.0.0.1:8000/docs`) :")

    # Tableau 14 : Endpoints API
    headers_api = ["Méthode", "Point de Terminaison (Endpoint)", "Rôle Fonctionnel & Données Échangées"]
    rows_api = [
        ["GET", "/api/metrics", "Fournit les métriques de benchmark matériel Raspberry Pi (latence, RAM, CPU)."],
        ["GET", "/api/signal/sample", "Transmet en flux continu les signaux vibratoires temporels et le spectre FFT associé."],
        ["GET", "/api/predict/simulate", "Déclenche une simulation d'inférence temps réel sur un échantillon de test aléatoire."],
        ["POST", "/api/predict/upload", "Reçoit un fichier de données réelles (CSV, TXT, NPY, NASA IMS), extrait les 16 features et infère."],
        ["POST", "/api/chat", "Interface conversationnelle avec l'agent RAG connecté à l'alerte prédictive active."],
        ["POST", "/api/report/pdf", "Génère et télécharge dynamiquement une fiche d'intervention technique officielle au format PDF."]
    ]
    create_styled_table(doc, headers_api, rows_api, col_widths=[1.0, 2.2, 3.8],
                        table_title="Spécification des points de terminaison (endpoints) de l'API REST FastAPI de surveillance industrielle", table_number="14")

    add_heading_2(doc, "8.3 Dashboard Industriel Temps Réel Développé sous React et Vite")
    add_paragraph(doc,
        "L'interface utilisateur (`frontend/src/App.jsx`) a été réalisée sous React 19 et packagée avec le bundler ultra-rapide Vite. "
        "Elle arbore une charte graphique industrielle moderne de type « cockpit haute technologie » avec effets de verre (glassmorphism), "
        "mode sombre anti-fatigue visuelle pour les salles de contrôle d'usine et composants réactifs :")
    add_bullet_point(doc, "Rendu fluide à 60 images/seconde de la forme d'onde accélérométrique (500 points affichés) et du spectre FFT instantané via la bibliothèque Recharts.", bold_title="Oscilloscope Vibratoire & Analyseur FFT")
    add_bullet_point(doc, "Affichage instantané du diagnostic, du niveau de confiance algorithmique (ex: 99.5 %) et de la latence d'exécution (0.22 ms).", bold_title="Cartouche d'Alerte Dynamique")
    add_bullet_point(doc, "Bouton d'importation universel acceptant les fichiers de capteurs de n'importe quel banc d'essai (CWRU, NASA IMS, synthetics) avec parsing automatique.", bold_title="Module d'Importation Universel")
    add_bullet_point(doc, "Visualisation en barres horizontales dynamiques des variables les plus contributrices (Kurtosis, FFT, RMS) pour une compréhension immédiate de l'origine du défaut.", bold_title="Barres d'Importance XAI")
    add_bullet_point(doc, "Boîte de dialogue intégrée permettant au technicien de converser avec le système expert RAG.", bold_title="Console Conversationnelle RAG")
    add_bullet_point(doc, "Génération en un clic d'un rapport PDF homologué prêt à être imprimé pour l'intervention en atelier.", bold_title="Exportateur de Fiche d'Intervention")

    add_heading_2(doc, "8.4 Validation d'Intégration Bout-en-Bout du Système Global")
    add_paragraph(doc,
        "L'intégrité de la chaîne complète a été vérifiée au moyen d'une suite de tests automatisée (`run_all_tests.py`). "
        "La validation confirme que le flux de données circule de manière fluide et synchrone : l'ingestion d'un signal brut, "
        "le fenêtrage, l'extraction de caractéristiques, l'inférence par le modèle champion Gradient Boosting, le calcul des Z-scores XAI, "
        "la contextualisation documentaire par le RAG et la restitution graphique sur le dashboard s'exécutent en moins de **0.30 seconde "
        "au total**, offrant une réactivité parfaite pour les opérateurs de supervision.")

def add_chapter_9(doc):
    """Chapitre 9 : Valorisation Pédagogique & Transfert de Compétences."""
    add_heading_1(doc, "Chapitre 9 : Valorisation Pédagogique & Transfert de Compétences", page_break=True)
    
    add_heading_2(doc, "9.1 Scénarisation d'un Cas d'Étude Pédagogique de 16 Heures pour Élèves-Ingénieurs")
    add_paragraph(doc,
        "L'un des objectifs d'excellence assignés à ce projet de stage résidait dans la valorisation académique des réalisations "
        "sous la forme d'un cas d'étude pédagogique complet destiné aux élèves-ingénieurs en informatique, mécatronique et systèmes "
        "embarqués. Formalisé dans `reports/cas_pedagogique.md`, ce module d'enseignement de 16 heures (divisé en 4 blocs de 4 heures "
        "ou 12 séances progressives) place les étudiants dans la posture d'ingénieurs consultants mandatés pour concevoir une solution "
        "Edge AI de maintenance prédictive d'usine.")

    # Tableau 15 : Plan des séances TP
    headers_tp = ["Bloc Horaire", "Séances", "Thématique Technique Abordée", "Livrables Étudiants Attendus"]
    rows_tp = [
        ["Bloc 1 (4h)", "Séances 1 à 3", "Exploration du signal CWRU, physique des roulements, fenêtrage glissant.", "Notebook d'analyse temporelle et spectrale."],
        ["Bloc 2 (4h)", "Séances 4 à 6", "Feature engineering (16 features FFT), entraînement et comparaison IA.", "Module d'extraction et modèles entraînés."],
        ["Bloc 3 (4h)", "Séances 7 à 9", "Déploiement sur Raspberry Pi, benchmark de latence et module XAI.", "Moteur d'inférence et graphes d'explicabilité."],
        ["Bloc 4 (4h)", "Séances 10 à 12", "Construction de l'agent RAG, interface cockpit et soutenance orale.", "Rapport de diagnostic et démo en direct."]
    ]
    create_styled_table(doc, headers_tp, rows_tp, col_widths=[1.2, 1.2, 2.6, 2.0],
                        table_title="Scénarisation et articulation pédagogique du cas d'étude ingénieur en 12 séances de travaux pratiques (16h)", table_number="15")

    add_heading_2(doc, "9.2 Grille d'Évaluation Sommative Détaillée et Barème sur 20 Points")
    add_paragraph(doc,
        "Pour encadrer l'évaluation des étudiants selon les critères d'accréditation des écoles d'ingénieurs (CTI), "
        "une grille d'évaluation sommative critériée a été établie dans `reports/grille_evaluation.md` :")

    # Tableau 16 : Grille d'évaluation
    headers_gri = ["Critère d'Évaluation", "Points Alloués", "Indicateurs de Performance & Niveaux d'Excellence"]
    rows_gri = [
        ["1. Traitement du Signal & Features", "4.0 pts", "Rigueur du fenêtrage (1024 pts), exactitude des 16 formules mathématiques et normalisation."],
        ["2. Modélisation IA & Évaluation", "4.0 pts", "Maîtrise des algorithmes (supervisés vs non-supervisés), rigueur de la validation croisée."],
        ["3. Déploiement Edge & Benchmark", "4.0 pts", "Latence d'inférence < 1 ms prouvée sur Raspberry Pi, optimisation mémoire et robustesse."],
        ["4. Explicabilité XAI & Agent RAG", "4.0 pts", "Pertinence des Z-scores, structuration de la base documentaire et traçabilité des réponses."],
        ["5. Qualité du Code & Restitution", "4.0 pts", "Clean Code (PEP8), robustesse logicielle, clarté du rapport technique et soutenance orale."],
        ["Total Général Sommative", "20.0 pts", "Note finale sanctionnant les compétences d'ingénieur en Edge AI industrielle."]
    ]
    create_styled_table(doc, headers_gri, rows_gri, col_widths=[2.2, 1.0, 3.8],
                        table_title="Grille d'évaluation sommative et barème de notation officiel du cas d'étude ingénieur (sur 20 points)", table_number="16")
