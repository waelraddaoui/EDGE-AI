"""
report_builder/front_matter.py
------------------------------
Sections liminaires du rapport : Page de Garde, Remerciements,
Résumés (FR/EN), Table des Matières, Listes des Figures/Tableaux et Glossaire.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from report_builder.styles import (
    COLOR_NAVY, COLOR_STEEL, COLOR_CHARCOAL, COLOR_BODY, COLOR_MUTED,
    HEX_NAVY, HEX_LIGHT_BLUE, add_heading_1, add_heading_2, add_paragraph,
    create_styled_table
)

def add_title_page(doc):
    """Génère une page de garde solennelle et institutionnelle."""
    # En-tête institutionnel
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(2)
    
    r_school = p_inst.add_run("ÉCOLE SUPÉRIEURE PRIVÉE D'INGÉNIERIE ET DE TECHNOLOGIES (ESPRIM)\n")
    r_school.font.name = 'Calibri'
    r_school.font.size = Pt(13)
    r_school.font.bold = True
    r_school.font.color.rgb = COLOR_NAVY
    
    r_dept = p_inst.add_run("Département Génie Informatique & Systèmes Embarqués\n")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = COLOR_STEEL
    
    r_sub = p_inst.add_run("Cycle de Formation d'Ingénieurs — Spécialité Intelligence Artificielle & IIoT")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    # Ligne décorative horizontale
    p_sep = doc.add_paragraph()
    p_sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sep.paragraph_format.space_before = Pt(14)
    p_sep.paragraph_format.space_after = Pt(20)
    r_line = p_sep.add_run("_________________________________________________________________________________")
    r_line.font.color.rgb = COLOR_STEEL
    r_line.font.size = Pt(8)

    # Nature du document
    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_before = Pt(10)
    p_type.paragraph_format.space_after = Pt(10)
    r_mem = p_type.add_run("MÉMOIRE DE STAGE DE FIN D'ÉTUDES D'INGÉNIEUR")
    r_mem.font.name = 'Calibri'
    r_mem.font.size = Pt(14)
    r_mem.font.bold = True
    r_mem.font.color.rgb = COLOR_STEEL

    # Titre du Sujet dans un cadre soigné
    table_title = doc.add_table(rows=1, cols=1)
    table_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_title.autofit = False
    cell_t = table_title.cell(0, 0)
    cell_t.width = Inches(6.5)
    
    tcPr = cell_t._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), HEX_LIGHT_BLUE)))
    borders = parse_xml(r'''
        <w:tcBorders %s>
            <w:top w:val="single" w:sz="16" w:space="0" w:color="%s"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="%s"/>
            <w:bottom w:val="single" w:sz="16" w:space="0" w:color="%s"/>
            <w:right w:val="single" w:sz="16" w:space="0" w:color="%s"/>
        </w:tcBorders>
    ''' % (nsdecls('w'), HEX_NAVY, HEX_NAVY, HEX_NAVY, HEX_NAVY))
    tcPr.append(borders)
    
    p_tit = cell_t.paragraphs[0]
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(14)
    p_tit.paragraph_format.space_after = Pt(12)
    
    r_tit = p_tit.add_run("EDGE AI EXPLICABLE ET AGENT IA / RAG POUR LA DÉTECTION D'ANOMALIES INDUSTRIELLES SUR RASPBERRY PI\n")
    r_tit.font.name = 'Calibri'
    r_tit.font.size = Pt(17)
    r_tit.font.bold = True
    r_tit.font.color.rgb = COLOR_NAVY
    
    r_stit = p_tit.add_run("Conception, Déploiement Embarqué (< 0.25 ms), Explicabilité XAI,\nSupervision Interactive et Valorisation Pédagogique")
    r_stit.font.name = 'Calibri'
    r_stit.font.size = Pt(11.5)
    r_stit.font.italic = True
    r_stit.font.color.rgb = COLOR_CHARCOAL

    # Informations Auteur et Encadrement
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(36)
    p_meta.paragraph_format.space_after = Pt(20)
    
    table_meta = doc.add_table(rows=4, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False
    
    meta_data = [
        ("Auteur :", "Élève-Ingénieur en Génie Informatique & IA"),
        ("Encadrante Académique :", "Mme Amina Rouis (ESPRIM)"),
        ("Cadre de Réalisation :", "Projet de Recherche Appliquée & Usine 4.0"),
        ("Année Universitaire :", "2025 – 2026")
    ]
    
    for idx, (label, val) in enumerate(meta_data):
        row = table_meta.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.3)
        c1.width = Inches(4.2)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(4)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY
        r0.font.size = Pt(11)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(4)
        r1 = p1.add_run(val)
        r1.font.color.rgb = COLOR_BODY
        r1.font.size = Pt(11)

    # Mention Jury
    p_jury = doc.add_paragraph()
    p_jury.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_jury.paragraph_format.space_before = Pt(40)
    p_jury.paragraph_format.space_after = Pt(0)
    r_j = p_jury.add_run("Présenté et soutenu publiquement devant le jury composé de :\n"
                         "Président du Jury  |  Rapporteur  |  Encadrante : Mme Amina Rouis\n"
                         "Session : Août / Septembre 2026")
    r_j.font.size = Pt(9.5)
    r_j.font.italic = True
    r_j.font.color.rgb = COLOR_MUTED

def add_acknowledgements(doc):
    """Page de remerciements."""
    add_heading_1(doc, "Remerciements", page_break=True)
    
    add_paragraph(doc, 
        "Au terme de ce travail marquant l'aboutissement de mon cycle de formation d'ingénieur, "
        "je tiens à exprimer ma profonde gratitude à l'ensemble des personnes dont le soutien intellectuel, "
        "technique et humain a rendu possible la concrétisation de ce projet de recherche et développement.")
    
    add_paragraph(doc, 
        "J'adresse mes remerciements les plus sincères et les plus respectueux à mon encadrante académique, "
        "Mme Amina Rouis, pour sa confiance continue, sa disponibilité remarquable et ses orientations méthodologiques "
        "d'une rigueur exemplaire. Ses retours exigeants, sa vision scientifique pointue et ses conseils bienveillants ont "
        "constitué un guide précieux pour hisser ce travail au niveau des standards internationaux des revues de rang Q1.",
        bold_prefix="À mon encadrante, Mme Amina Rouis : ")
        
    add_paragraph(doc,
        "Je remercie chaleureusement le corps professoral et l'équipe pédagogique de l'ESPRIM pour la qualité "
        "exceptionnelle des enseignements dispensés tout au long de mon cursus en informatique et systèmes embarqués. "
        "Leur dévouement a constitué le socle solide sur lequel ce projet pluridisciplinaire (traitement du signal, "
        "optimisation matérielle, machine learning et architectures logicielles) a pu s'épanouir.",
        bold_prefix="À l'équipe pédagogique de l'ESPRIM : ")
        
    add_paragraph(doc,
        "J'exprime également ma reconnaissance aux membres éminents du jury qui m'ont fait l'honneur d'évaluer "
        "ce mémoire de stage et d'assister à ma soutenance. Leurs observations critiques et leurs questions constructives "
        "représentent une opportunité inestimable d'enrichir ma démarche d'ingénieur-chercheur.",
        bold_prefix="Aux membres du jury : ")

    add_paragraph(doc,
        "Enfin, j'adresse une pensée toute particulière à ma famille et à mes proches, pour leur soutien indéfectible, "
        "leur patience et leurs encouragements constants au cours de ces intenses mois d'efforts.",
        bold_prefix="À mes proches : ")

def add_abstract(doc):
    """Page bilingue : Résumé en français et Abstract en anglais."""
    add_heading_1(doc, "Résumé & Abstract", page_break=True)
    
    # Version Française
    add_heading_2(doc, "Résumé")
    add_paragraph(doc,
        "Dans l'écosystème de l'Industrie 4.0 et de l'Internet Industriel des Objets (IIoT), la maintenance prédictive "
        "des organes rotatifs — en particulier des roulements mécaniques — représente un enjeu critique de productivité "
        "et de sûreté opérationnelle. Face aux limitations intrinsèques du Cloud Computing (latence excessive, dépendance "
        "au réseau, coûts de bande passante et risques de confidentialité), ce projet de stage conçoit, déploie et évalue "
        "une architecture complète d'Intelligence Artificielle Embarquée (Edge AI), explicable (XAI) et couplée à un agent "
        "conversationnel autonome de génération augmentée par récupération (RAG), hébergée sur nano-ordinateur Raspberry Pi.")
    
    add_paragraph(doc,
        "En s'appuyant sur les signaux accélérométriques du banc d'essai CWRU (Case Western Reserve University) complétés "
        "par les données run-to-failure de la NASA IMS et des signaux synthétiques perturbés, une chaîne de prétraitement "
        "par fenêtrage glissant (1024 points, 85.3 ms) extrait 16 indicateurs physiques temporels, statistiques et spectraux (FFT). "
        "Cinq architectures IA (Gradient Boosting, Random Forest, 1D-CNN compact, Isolation Forest et Autoencodeur PyTorch) ont été "
        "entraînées et benchmarkées en conditions matérielles réelles. Le modèle Gradient Boosting s'impose comme le champion Edge, "
        "délivrant une latence d'inférence exceptionnelle de 0.218 ms (< 1 ms imposé), un débit supérieur à 4 500 fenêtres/seconde, "
        "une empreinte mémoire minime de 30.6 KB et un F1-score de 0.978 sous perturbations sévères (bruit gaussien à SNR négatif).")
        
    add_paragraph(doc,
        "Un module d'explicabilité (XAI) basé sur les Z-scores met en lumière l'élévation spectaculaire du Kurtosis (+4.5 écarts-types) "
        "et l'émergence des fréquences caractéristiques cinématiques (BPFI, BPFO). En parallèle, un agent RAG indexe la base "
        "documentaire technique (D1 à D11) pour transformer instantanément les alertes prédictives en fiches d'intervention détaillées "
        "avec protocoles LOTO. L'ensemble est interconnecté via une API REST FastAPI et un tableau de bord React/Vite professionnel, "
        "puis formalisé en un dossier pédagogique de 16 heures de TP pour élèves-ingénieurs.")

    add_paragraph(doc,
        "Edge AI, Maintenance Prédictive, Roulements Industriels, CWRU, Raspberry Pi, Inférence Temps Réel, "
        "Explicabilité (XAI), Kurtosis, Agent IA, RAG (Retrieval-Augmented Generation), FastAPI, React.",
        bold_prefix="Mots-clés : ")

    # Ligne de séparation
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Version Anglaise
    add_heading_2(doc, "Abstract")
    add_paragraph(doc,
        "In the context of Industry 4.0 and the Industrial Internet of Things (IIoT), predictive maintenance of rotating "
        "machinery—especially rolling element bearings—constitutes a vital challenge for operational safety and cost efficiency. "
        "To overcome traditional Cloud bottlenecks (latency, bandwidth consumption, cyber-risks, and network outages), this engineering "
        "thesis develops, deploys, and benchmarks a full-stack, resource-aware Edge AI system paired with Explainable AI (XAI) and "
        "an autonomous Retrieval-Augmented Generation (RAG) diagnostic agent running directly on a Raspberry Pi single-board computer.")
        
    add_paragraph(doc,
        "Leveraging high-frequency vibration datasets from Case Western Reserve University (CWRU), NASA IMS run-to-failure endurance tests, "
        "and noise-perturbed synthetic streams, a sliding-window pipeline (1024 points, 85.3 ms) extracts 16 physical time-domain and FFT "
        "features. Five lightweight machine learning and deep learning models were trained and profiled. Gradient Boosting emerged as the "
        "Edge champion, achieving an ultra-fast inference latency of 0.218 ms, an inference throughput of over 4,500 frames/s, a compact "
        "memory size of 30.6 KB, and a resilient F1-score of 0.978 under harsh signal degradations.")
        
    add_paragraph(doc,
        "The XAI module reveals a marked Kurtosis leap (+4.5σ) and kinematic peak shifts (BPFO, BPFI). Concurrently, the RAG agent retrieves "
        "relevant technical guidelines (D1-D11) to synthesize actionable maintenance work orders including LOTO safety procedures. "
        "The end-to-end framework is fully operational via a FastAPI backend and a real-time React/Vite dashboard, and is formalized as a "
        "16-hour engineering laboratory case study.")

    add_paragraph(doc,
        "Edge AI, Predictive Maintenance, Vibration Analysis, CWRU Bearings, Raspberry Pi, Low Latency, "
        "Explainable AI (XAI), RAG, Fault Diagnosis, Full-Stack Dashboard, IIoT.",
        bold_prefix="Keywords: ")

def add_table_of_contents(doc):
    """Sommaire académique exhaustif et pré-rempli."""
    add_heading_1(doc, "Table des Matières", page_break=True)
    
    toc_entries = [
        ("Introduction Générale", "1"),
        ("Chapitre 1 : Contexte Industriel, Cahier des Charges & Analyse du Besoin", "5"),
        ("   1.1 Contexte Général : La Révolution de la Maintenance Prédictive 4.0", "5"),
        ("   1.2 Problématique de Défaillance des Organes Rotatifs et Roulements", "6"),
        ("   1.3 Analyse Fonctionnelle du Besoin (FAST et Contraintes Opérationnelles)", "7"),
        ("   1.4 Spécifications Matérielles et Exigences Temps Réel sur Raspberry Pi", "8"),
        ("   1.5 Découpage en Livrables (L1 à L17) et Planning Stratégique", "9"),
        ("Chapitre 2 : État de l'Art Scientifique Approfondi (Revue de Rang Q1)", "11"),
        ("   2.1 Panorama des Datasets de Référence (CWRU, NASA IMS, PRONOSTIA, MIMII)", "11"),
        ("   2.2 Fondements Physiques Vibratoires et Équations Cinématiques des Défauts", "13"),
        ("   2.3 Algorithmes d'Apprentissage Automatique pour Séries Temporelles Industrielles", "15"),
        ("   2.4 Technologies d'Optimisation et de Déploiement Embarqué Edge AI", "17"),
        ("   2.5 L'Explicabilité (XAI) dans les Processus Industriels Critiques", "18"),
        ("   2.6 L'Avènement des Agents Intelligents et du RAG pour le Diagnostic IIoT", "20"),
        ("   2.7 Synthèse Critique, Limites des Approches Existantes et Identification des Gaps", "21"),
        ("Chapitre 3 : Traitement du Signal, Ingestion & Feature Engineering", "24"),
        ("   3.1 Banc d'Essai Expérimental CWRU et Caractéristiques des Signaux", "24"),
        ("   3.2 Pipeline de Prétraitement et Stratégie de Fenêtrage Glissant", "25"),
        ("   3.3 Formulation Mathématique Exhaustive des 16 Indicateurs Physiques Extraits", "26"),
        ("   3.4 Création de Jeux de Données Hybrides Perturbés pour les Tests de Robustesse", "28"),
        ("   3.5 Pipeline de Normalisation et Partitionnement Stratifié Train/Val/Test", "29"),
        ("Chapitre 4 : Conception, Entraînement & Évaluation des Modèles IA", "31"),
        ("   4.1 Modèles Supervisés Basés sur les Arbres (Gradient Boosting, Random Forest)", "31"),
        ("   4.2 Architecture Réseau de Neurones Convolutif 1D (1D-CNN Compact PyTorch)", "33"),
        ("   4.3 Modèles Non Supervisés de Détection d'Anomalies (Isolation Forest, Autoencodeur)", "34"),
        ("   4.4 Évaluation Comparative des Métriques (Accuracy, Précision, Rappel, F1-Score)", "36"),
        ("   4.5 Analyse des Matrices de Confusion et des Courbes ROC-AUC", "37"),
        ("   4.6 Sélection Motivée du Modèle Champion pour Déploiement Embarqué", "38"),
        ("Chapitre 5 : Inférence Embarquée, Profilage Matériel & Robustesse sur Raspberry Pi", "40"),
        ("   5.1 Architecture du Moteur d'Inférence Temps Réel et Simulation de Flux IoT", "40"),
        ("   5.2 Protocole Expérimental de Profilage des Ressources (Latence, Débit, RAM, CPU)", "41"),
        ("   5.3 Analyse Chiffrée des Résultats de Benchmark sur Processeur ARM / Raspberry Pi", "42"),
        ("   5.4 Évaluation de la Robustesse face aux Bruits Extrêmes et Pertes de Trames", "44"),
        ("   5.5 Grille Multicritères d'Aide à la Décision pour le Déploiement Industriel", "45"),
        ("Chapitre 6 : Module d'Explicabilité Industrielle (XAI)", "47"),
        ("   6.1 Problématique de la Boîte Noire et Acceptabilité par les Opérateurs Usine", "47"),
        ("   6.2 Analyse de l'Importance Globale et Locale des Variables Vibratoires", "48"),
        ("   6.3 Approche Différentielle par Z-Scores par rapport à l'État Sain de Référence", "49"),
        ("   6.4 Corrélation Physique des Signatures de Chocs (Kurtosis et Facteur de Crête)", "50"),
        ("   6.5 Détection des Profils d'Anomalie par l'Erreur de Reconstruction de l'Autoencodeur", "51"),
        ("Chapitre 7 : Agent IA / RAG & Génération Automatique de Diagnostics", "53"),
        ("   7.1 Architecture Fonctionnelle de l'Agent RAG (Retrieval-Augmented Generation)", "53"),
        ("   7.2 Constitution et Organisation de la Base de Connaissances Technique (D1 à D11)", "54"),
        ("   7.3 Indexation Sémantique Vectorielle et Calcul de Similarité Cosinus", "55"),
        ("   7.4 Moteur Conversationnel Expert et Contextualisation des Prédictions Edge", "56"),
        ("   7.5 Générateur Automatisé de Fiches d'Intervention Technique et Protocoles LOTO", "57"),
        ("Chapitre 8 : Architecture Logicielle Full-Stack, Interface Web & Validation Système", "59"),
        ("   8.1 Conception Modulaire et Principes de la Clean Architecture", "59"),
        ("   8.2 Backend REST Haute Performance avec FastAPI", "60"),
        ("   8.3 Dashboard Industriel Temps Réel Développé sous React et Vite", "61"),
        ("   8.4 Visualisation Dynamique des Signaux Bruts, Spectre FFT et Inférence Multi-Formats", "62"),
        ("   8.5 Module d'Exportation Instantanée de Rapports PDF Homologués", "63"),
        ("   8.6 Validation d'Intégration Bout-en-Bout du Système Global", "64"),
        ("Chapitre 9 : Valorisation Pédagogique & Transfert de Compétences", "66"),
        ("   9.1 Scénarisation d'un Cas d'Étude Pédagogique de 16 Heures pour Élèves-Ingénieurs", "66"),
        ("   9.2 Déroulement Structuré des 12 Séances de Travaux Pratiques", "67"),
        ("   9.3 Grille d'Évaluation Sommative Détaillée et Barème sur 20 Points", "68"),
        ("Conclusion Générale & Perspectives d'Avenir", "70"),
        ("Références Bibliographiques (Norme IEEE)", "73"),
        ("Annexes", "77"),
        ("   Annexe A : Fiche Technique du Roulement SKF 6205-2RS", "77"),
        ("   Annexe B : Échantillon de Logs de Streaming Inférence IoT", "78"),
        ("   Annexe C : Extraits du Code Source des Modules Clés", "79")
    ]
    
    table_toc = doc.add_table(rows=len(toc_entries), cols=2)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_toc.autofit = False
    
    for idx, (title, page_str) in enumerate(toc_entries):
        row = table_toc.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.8)
        c1.width = Inches(0.7)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(title)
        r0.font.size = Pt(10)
        if title.startswith("Chapitre") or title.startswith("Introduction") or title.startswith("Conclusion") or title.startswith("Références") or title.startswith("Annexes"):
            r0.font.bold = True
            r0.font.color.rgb = COLOR_NAVY
        else:
            r0.font.color.rgb = COLOR_BODY
            
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_str)
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_STEEL

def add_lists_and_acronyms(doc):
    """Listes des figures, des tableaux et glossaire des acronymes."""
    add_heading_1(doc, "Listes des Figures & des Tableaux", page_break=True)
    
    add_heading_2(doc, "Liste des Figures")
    figures_list = [
        ("Figure 01", "Signaux vibratoires bruts CWRU dans le domaine temporel (Normal, BPFI, BPFO, BSF)"),
        ("Figure 02", "Comparaison des signaux sous perturbations hybrides (bruit gaussien SNR, dérive, pertes)"),
        ("Figure 03", "Illustration méthodologique du fenêtrage glissant (fenêtre 1024 points, chevauchement 50 %)"),
        ("Figure 04", "Matrices de confusion comparatives des 5 modèles IA (Nominal vs Perturbé)"),
        ("Figure 05", "Courbes ROC et scores AUC comparatifs des classifieurs"),
        ("Figure 06", "Analyse globale d'importance des variables vibratoires (Feature Importance)"),
        ("Figure 07", "Explication locale XAI et distribution des Z-scores par rapport à l'état sain"),
        ("Figure 08", "Reconstruction du signal et seuil d'erreur MSE par l'Autoencodeur PyTorch"),
        ("Figure 09", "Compromis de performance Edge AI : Latence d'inférence (ms) vs F1-score"),
        ("Figure 10", "Empreinte mémoire RAM opérationnelle vs Taille physique des fichiers modèles"),
        ("Figure 11", "Architecture générale de la chaîne bout-en-bout Edge AI, RAG et Dashboard Full-Stack")
    ]
    for fig_id, fig_title in figures_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r_id = p.add_run(f"{fig_id} : ")
        r_id.font.bold = True
        r_id.font.color.rgb = COLOR_NAVY
        r_title = p.add_run(fig_title)
        r_title.font.color.rgb = COLOR_BODY

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_heading_2(doc, "Liste des Tableaux")
    tables_list = [
        ("Tableau 01", "Matrice de conformité des 17 livrables de stage (L1 à L17)"),
        ("Tableau 02", "Analyse comparative des datasets vibratoires publics de référence"),
        ("Tableau 03", "Caractéristiques physiques et fréquences cinématiques du roulement SKF 6205-2RS"),
        ("Tableau 04", "Seuils vibratoires globaux selon la norme internationale ISO 10816-3"),
        ("Tableau 05", "Formulation mathématique et interprétation des 16 indicateurs physiques extraits"),
        ("Tableau 06", "Hyperparamètres optimaux d'entraînement des 5 architectures IA"),
        ("Tableau 07", "Évaluation comparative des métriques de détection en régime nominal"),
        ("Tableau 08", "Évaluation de la résilience et du F1-Score sous différents régimes de bruit gaussien"),
        ("Tableau 09", "Résultats exhaustifs du profilage matériel sur nano-calculateur Raspberry Pi 4"),
        ("Tableau 10", "Matrice de décision multicritères pour le choix du modèle Edge champion"),
        ("Tableau 11", "Analyse comparative des Z-scores des indicateurs physiques selon le mode de défaut"),
        ("Tableau 12", "Inventaire structuré de la base de connaissances documentaire RAG (D1 à D11)"),
        ("Tableau 13", "Matrice de confusion des requêtes et score de similarité cosinus de l'agent RAG"),
        ("Tableau 14", "Spécification des endpoints de l'API REST FastAPI"),
        ("Tableau 15", "Plan de déroulement pédagogique des 12 séances de travaux pratiques (16h)"),
        ("Tableau 16", "Grille d'évaluation sommative du TP ingénieur et barème sur 20 points")
    ]
    for tab_id, tab_title in tables_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r_id = p.add_run(f"{tab_id} : ")
        r_id.font.bold = True
        r_id.font.color.rgb = COLOR_STEEL
        r_title = p.add_run(tab_title)
        r_title.font.color.rgb = COLOR_BODY

    # Glossaire et Acronymes
    add_heading_1(doc, "Glossaire & Liste des Acronymes", page_break=True)
    acronyms = [
        ("AI / IA", "Artificial Intelligence / Intelligence Artificielle"),
        ("AUC", "Area Under the Curve (Aire sous la courbe ROC)"),
        ("BPFI", "Ball Pass Frequency Inner Ring (Fréquence de passage des billes sur bague interne)"),
        ("BPFO", "Ball Pass Frequency Outer Ring (Fréquence de passage des billes sur bague externe)"),
        ("BSF", "Ball Spin Frequency (Fréquence de rotation propre de la bille sur elle-même)"),
        ("CNN", "Convolutional Neural Network (Réseau de neurones convolutif)"),
        ("CWRU", "Case Western Reserve University (Jeu de données vibratoires de référence mondiale)"),
        ("DE", "Drive End (Accéléromètre positionné côté entraînement moteur)"),
        ("Edge AI", "Intelligence Artificielle Embarquée directement sur dispositif périphérique"),
        ("FE", "Fan End (Accéléromètre positionné côté ventilateur moteur)"),
        ("FFT", "Fast Fourier Transform (Transformée de Fourier Rapide)"),
        ("FTF", "Fundamental Train Frequency (Fréquence de rotation de la cage de maintien)"),
        ("FPS", "Frames Per Second (Nombre de fenêtres de signal traitées par seconde)"),
        ("IIoT", "Industrial Internet of Things (Internet Industriel des Objets)"),
        ("ISO", "International Organization for Standardization"),
        ("LIME", "Local Interpretable Model-agnostic Explanations"),
        ("LOTO", "Lockout / Tagout (Procédure industrielle de consignation électrique et mécanique)"),
        ("MSE", "Mean Squared Error (Erreur quadratique moyenne de reconstruction)"),
        ("NPU", "Neural Processing Unit (Puce matérielle d'accélération neuronale dédiée)"),
        ("ONNX", "Open Neural Network Exchange (Format standard d'interopérabilité des modèles IA)"),
        ("PdM", "Predictive Maintenance (Maintenance Prédictive)"),
        ("RAG", "Retrieval-Augmented Generation (Génération de texte augmentée par recherche documentaire)"),
        ("RMS", "Root Mean Square (Valeur efficace du signal vibratoire liée à l'énergie totale)"),
        ("ROC", "Receiver Operating Characteristic (Courbe de performance de classification binaire)"),
        ("RPM", "Revolutions Per Minute (Tours par minute, vitesse de rotation de l'arbre moteur)"),
        ("SHAP", "SHapley Additive exPlanations (Attribution d'importance théorique par valeurs de Shapley)"),
        ("SLM", "Small Language Model (Modèle de langage compact adapté aux architectures embarquées)"),
        ("SNR", "Signal-to-Noise Ratio (Rapport Signal sur Bruit exprimé en décibels dB)"),
        ("TF-IDF", "Term Frequency - Inverse Document Frequency (Pondération fréquentielle statistique)"),
        ("XAI", "Explainable Artificial Intelligence (Intelligence Artificielle Explicable)")
    ]
    
    headers_acr = ["Acronyme", "Définition Complète & Rôle dans le Projet"]
    rows_acr = [[a, d] for a, d in acronyms]
    create_styled_table(doc, headers_acr, rows_acr, col_widths=[1.5, 4.8])
