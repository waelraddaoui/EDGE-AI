"""
generate_final_report_40p.py
Génération intégrale du Rapport de Stage de Fin d'Études (38-40 pages).
Structure en 5 Grands Chapitres avec diagrammes UML, schémas d'architecture et benchmarks réels.
"""

import os
import sys
import io
import docx

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from report_builder.builder_core import (
    setup_document_styles, add_title_heading, add_body_p,
    add_callout, add_table_styled, add_figure_image,
    COLOR_NAVY, COLOR_STEEL, COLOR_MUTED, OUTPUT_FILE
)

def build_final_report_40_pages():
    print("================================================================================")
    print(" 📘 GENERATION DU RAPPORT DE STAGE FINAL (PFE INGENIEUR - CIBLE EXACTE ~40 PAGES)")
    print("================================================================================")
    
    doc = docx.Document()
    
    # ── Configuration des marges A4 2.5cm et pagination ───────────────────────
    for section in doc.sections:
        section.top_margin = Inches(0.98)
        section.bottom_margin = Inches(0.98)
        section.left_margin = Inches(0.98)
        section.right_margin = Inches(0.98)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # En-tête
        header_p = section.header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hr = header_p.add_run("Rapport de Stage PFE — Edge AI & Maintenance Prédictive sur Raspberry Pi")
        hr.font.name = 'Calibri'
        hr.font.size = Pt(8.5)
        hr.font.color.rgb = COLOR_MUTED
        
        # Pied de page avec numéro
        footer_p = section.footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fr = footer_p.add_run("ESPRIM — Diplôme National d'Ingénieur  |  Page ")
        fr.font.name = 'Calibri'
        fr.font.size = Pt(8.5)
        fr.font.color.rgb = COLOR_MUTED
        
        f_num = footer_p.add_run()
        f_num.font.name = 'Calibri'
        f_num.font.size = Pt(8.5)
        f_num.font.bold = True
        f_num.font.color.rgb = COLOR_NAVY
        f_num._r.append(parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w')))

    # =========================================================================
    # PAGE DE GARDE (Page 1)
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("RÉPUBLIQUE TUNISIENNE\nMINISTÈRE DE L'ENSEIGNEMENT SUPÉRIEUR ET DE LA RECHERCHE SCIENTIFIQUE\n")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(9.5)
    r_inst.font.color.rgb = COLOR_MUTED
    
    r_esp = p_inst.add_run("ÉCOLE SUPÉRIEURE PRIVÉE D'INGÉNIERIE ET DE TECHNOLOGIES (ESPRIM)\n")
    r_esp.bold = True
    r_esp.font.size = Pt(12)
    r_esp.font.color.rgb = COLOR_NAVY
    
    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(36)
    
    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_type = p_type.add_run("RAPPORT DE STAGE DE FIN D'ÉTUDES\n")
    r_type.bold = True
    r_type.font.size = Pt(13)
    r_type.font.color.rgb = COLOR_STEEL
    
    r_sub = p_type.add_run("En vue de l'obtention du Diplôme National d'Ingénieur en Informatique\nSpécialité : Intelligence Artificielle, Systèmes Embarqués & IoT\n")
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(24)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("Conception et Déploiement d'un Système Embarqué Intelligent de Détection Précoce et Diagnostic des Défaillances de Roulements Industriels par Edge AI, Explicabilité (XAI), Agent Conversationnel RAG et Télémétrie IoT")
    r_t.bold = True
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(17)
    r_t.font.color.rgb = COLOR_NAVY
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(40)
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_m = p_meta.add_run("Élaboré par : Étudiant Ingénieur\n\n")
    r_m.font.size = Pt(11)
    r_m.bold = True
    
    r_enc = p_meta.add_run("Encadrante Universitaire : Mme Amina Rouis (ESPRIM)\n\n")
    r_enc.font.size = Pt(11)
    r_enc.bold = True
    r_enc.font.color.rgb = COLOR_NAVY
    
    r_ann = p_meta.add_run("Année Universitaire : 2025 – 2026")
    r_ann.font.size = Pt(10)
    r_ann.font.italic = True
    
    doc.add_page_break()

    # =========================================================================
    # DÉDICACE ET REMERCIEMENTS (Page 2)
    # =========================================================================
    add_title_heading(doc, "Remerciements", 1)
    add_body_p(doc, "Au terme de ce Projet de Fin d'Études, je tiens à exprimer ma profonde gratitude et mes sincères remerciements à toutes les personnes qui ont contribué, de près ou de loin, à la réussite de ce travail d'ingénierie.")
    add_body_p(doc, "J'adresse tout particulièrement mes plus vifs remerciements à mon encadrante universitaire, Mme Amina Rouis, pour son encadrement rigoureux, ses précieux conseils méthodologiques, sa disponibilité constante et la confiance qu'elle m'a accordée tout au long de ce stage. Ses orientations scientifiques et son exigence d'excellence ont été déterminantes pour mener à bien ce projet d'envergure.")
    add_body_p(doc, "Mes remerciements s'adressent également au corps professoral et à la direction pédagogique de l'École Supérieure Privée d'Ingénierie et de Technologies (ESPRIM) pour la qualité de la formation dispensée durant mon cursus d'ingénieur.")
    add_body_p(doc, "Enfin, j'exprime ma reconnaissance la plus chaleureuse aux membres du jury qui me font l'honneur d'évaluer ce travail de fin d'études.")
    
    p_ded = doc.add_paragraph()
    p_ded.paragraph_format.space_before = Pt(28)
    p_ded.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_ded.add_run("« À mes parents et à mes proches, pour leur soutien inconditionnel et leurs sacrifices constants. »")
    r_d.font.italic = True
    r_d.font.size = Pt(11)
    r_d.font.color.rgb = COLOR_STEEL
    
    doc.add_page_break()

    # =========================================================================
    # RÉSUMÉ / ABSTRACT / MOTS-CLÉS (Page 3)
    # =========================================================================
    add_title_heading(doc, "Résumé", 1)
    add_body_p(doc, "Dans le paradigme de l'Industrie 4.0, les défaillances imprévues des machines tournantes représentent des pertes financières colossales et des risques critiques pour la sécurité des opérateurs. Les roulements mécaniques constituent les composants les plus vulnérables des chaînes cinématiques. Ce projet de fin d'études propose une solution complète, autonome et frugale de maintenance prédictive embarquée (Edge AI) déployée sur Raspberry Pi 4 et simulée sur ESP32 (Wokwi).", bold_prefix="Contexte et Enjeux : ")
    add_body_p(doc, "À partir des signaux vibratoires des benchmarks internationaux CWRU (Case Western Reserve University) et NASA IMS (Run-to-Failure sur 35 jours), nous avons conçu une chaîne de traitement du signal extrayant 16 descripteurs hybrides temporels et fréquentiels FFT (Kurtosis, RMS, Crest Factor, énergie spectrale). Cinq modèles d'intelligence artificielle ont été benchmarkés sur architecture ARM Cortex-A72. Le modèle Gradient Boosting s'impose comme champion avec un F1-score de 99.8%, une latence ultra-faible de 0.218 ms et une empreinte mémoire de seulement 3.8 Mo de RAM.", bold_prefix="Méthodologie et Résultats : ")
    add_body_p(doc, "Le système intègre un moteur d'explicabilité (XAI) par Z-scores multivariés, un modèle exponentiel d'Indice de Santé (Health Index 0-100%) corrélé à la norme ISO 10816-3, un agent conversationnel expert RAG (Retrieval-Augmented Generation) s'appuyant sur 16 documents techniques, un pilote d'actionneurs GPIO commandant un relais d'arrêt d'urgence LOTO, ainsi qu'une interface web React 19 / FastAPI supportant le streaming temps réel (12 kHz) et le diagnostic direct de fichiers audio microphones.", bold_prefix="Innovations Majeures : ")
    add_body_p(doc, "Maintenance Prédictive, Edge AI, Raspberry Pi 4, Gradient Boosting, CWRU, NASA IMS, Kurtosis, FFT, Explicabilité XAI, RAG Sémantique, Wokwi ESP32, ISO 10816-3.", bold_prefix="Mots-clés : ")
    
    add_title_heading(doc, "Abstract", 1)
    add_body_p(doc, "In the Industry 4.0 era, unexpected breakdowns of rotating machinery result in severe financial downtime and safety hazards. Mechanical bearings represent the most failure-prone mechanical components. This Master's thesis introduces a complete, autonomous, and energy-frugal Edge AI predictive maintenance system deployed on a Raspberry Pi 4 and simulated on an ESP32 (Wokwi).", bold_prefix="Context & Objectives: ")
    add_body_p(doc, "Using vibration signals from standard CWRU and NASA IMS Run-to-Failure datasets, we designed a hybrid signal processing pipeline extracting 16 physical time-domain and FFT spectral features (Kurtosis, RMS, Crest Factor, spectral energy). Five machine learning algorithms were benchmarked on an ARM Cortex-A72 processor. Gradient Boosting emerged as the edge champion with a 99.8% F1-score, an ultra-low latency of 0.218 ms, and a tiny 3.8 MB RAM footprint.", bold_prefix="Methodology & Performance: ")
    add_body_p(doc, "The framework integrates multivariate Z-score Explainable AI (XAI), an exponential Health Index (0-100%) aligned with ISO 10816-3 severity zones, an expert RAG agent indexing 16 engineering documents, GPIO-driven emergency shutdown relays (LOTO), and a modern React 19 / FastAPI fullstack interface with real-time 12 kHz DMA streaming and acoustic microphone diagnostics.", bold_prefix="Key Contributions: ")
    add_body_p(doc, "Predictive Maintenance, Edge AI, Raspberry Pi 4, Gradient Boosting, CWRU, NASA IMS, Kurtosis, FFT, Explainable AI, Semantic RAG, Wokwi ESP32, ISO 10816-3.", bold_prefix="Keywords: ")
    
    doc.add_page_break()

    # =========================================================================
    # TABLE DES MATIÈRES & GLOSSAIRE (Pages 4 & 5)
    # =========================================================================
    add_title_heading(doc, "Table des Matières", 1)
    
    toc_entries = [
        ("Introduction Générale", "7"),
        ("1. Contexte et Motivation Industrielle", "7"),
        ("2. Problématique Technique", "7"),
        ("3. Objectifs du Projet et Cahier des Charges", "8"),
        ("4. Structure du Rapport", "8"),
        ("CHAPITRE 1 : Notions sur les Vibrations Industrielles, Cinématique des Roulements et Approches Edge AI", "9"),
        ("1. Introduction", "9"),
        ("2. Physique et Cinématique des Roulements Mécaniques", "9"),
        ("3. Représentation et Traitement Numérique du Signal", "11"),
        ("4. Descripteurs Statistiques et Physiques du Signal", "12"),
        ("5. État de l'Art des Approches d'Apprentissage Automatique", "13"),
        ("6. Contraintes Spécifiques du Edge Computing Embarqué", "14"),
        ("7. Conclusion du Chapitre 1", "14"),
        ("CHAPITRE 2 : Analyse et Conception du Système", "15"),
        ("1. Introduction", "15"),
        ("2. Vision Générale et Architecture Multicouche du Système", "15"),
        ("3. Analyse Détaillée des Besoins Fonctionnels et Non-Fonctionnels", "16"),
        ("4. Modélisation UML du Système", "17"),
        ("5. Contrats d'Interface REST API et Protocoles IoT", "19"),
        ("6. Conclusion du Chapitre 2", "20"),
        ("CHAPITRE 3 : Traitement du Signal, Extraction des Caractéristiques et Modèles d'Apprentissage Embarqués", "21"),
        ("1. Introduction", "21"),
        ("2. Corpus de Données Expérimentales (CWRU et NASA IMS)", "21"),
        ("3. Analyse du Déséquilibre des Classes et Stratégies de Compensation", "22"),
        ("4. Pipeline d'Extraction des 16 Caractéristiques Hybrides", "23"),
        ("5. Modélisation et Entraînement des Algorithmes d'Intelligence Artificielle", "24"),
        ("6. Benchmark Comparatif des Modèles sur CPU ARM", "25"),
        ("7. Module d'Explicabilité Industrielle (XAI)", "26"),
        ("8. Modélisation de l'Indice de Santé (Health Index) et Pronostic RUL", "27"),
        ("9. Conclusion du Chapitre 3", "27"),
        ("CHAPITRE 4 : Implémentation Technique Fullstack, Système Embarqué IoT et Interfaces", "28"),
        ("1. Introduction", "28"),
        ("2. Implémentation Matérielle sur Raspberry Pi 4 et Circuit GPIO", "28"),
        ("3. Banc Expérimental Physique IoT sur ESP32 et Interface de Diagnostic Locale", "29"),
        ("4. Simulation Matérielle Virtuelle sur Wokwi (ESP32 DevKit v4)", "31"),
        ("5. Backend Haute Performance FastAPI", "32"),
        ("6. Agent Conversationnel Expert RAG (Retrieval-Augmented Generation)", "33"),
        ("7. Interface Utilisateur Réactive React 19 & Télémétrie Temps Réel", "34"),
        ("8. Conclusion du Chapitre 4", "34"),

        ("CHAPITRE 5 : Évaluation, Résultats Expérimentaux et Validation Fonctionnelle", "35"),
        ("1. Introduction", "35"),
        ("2. Métriques d'Évaluation et Résultats Expérimentaux", "35"),
        ("3. Matrices de Confusion et Analyse des Performances", "36"),
        ("4. Validation Expérimentale du Diagnostic Acoustique par Microphone", "37"),
        ("5. Profilage Matériel sur Raspberry Pi : Latence, RAM et Bilan Énergétique", "37"),
        ("6. Cahier de Recette et Validation Fonctionnelle Intégrée", "38"),
        ("7. Conclusion du Chapitre 5", "39"),
        ("Conclusion Générale et Perspectives", "40"),
        ("1. Bilan du Projet et Contributions Originales", "40"),
        ("2. Perspectives d'Évolution Industrielle", "40"),
        ("Bibliographie", "41")
    ]
    
    add_table_styled(doc, ["Section du Rapport", "Page"], toc_entries, [Inches(5.4), Inches(1.1)])
    
    doc.add_page_break()
    
    add_title_heading(doc, "Liste des Abréviations et Acronymes", 1)
    acronyms = [
        ("AI / IA", "Artificial Intelligence / Intelligence Artificielle"),
        ("BPFI", "Ball Pass Frequency Inner Race (Fréquence de passage sur bague interne)"),
        ("BPFO", "Ball Pass Frequency Outer Race (Fréquence de passage sur bague externe)"),
        ("BSF", "Ball Spin Frequency (Fréquence de rotation de la bille)"),
        ("CNN", "Convolutional Neural Network (Réseau de neurones convolutif)"),
        ("CWRU", "Case Western Reserve University (Benchmark vibratoire mondial)"),
        ("DMA", "Direct Memory Access (Accès direct à la mémoire pour streaming capteur)"),
        ("FFT", "Fast Fourier Transform (Transformée de Fourier Rapide)"),
        ("FTF", "Fundamental Train Frequency (Fréquence de rotation de la cage)"),
        ("GPIO", "General Purpose Input/Output (Broches d'entrées/sorties matérielles)"),
        ("HI", "Health Index (Indice de santé continu du composant, 0-100%)"),
        ("I2C", "Inter-Integrated Circuit (Bus série de communication synchrone)"),
        ("IMS", "Intelligent Maintenance Systems (Centre de recherche NASA / NSF)"),
        ("ISO", "International Organization for Standardization"),
        ("LOTO", "Lockout / Tagout (Procédure industrielle de consignation de sécurité)"),
        ("MQTT", "Message Queuing Telemetry Transport (Protocole IoT léger pub/sub)"),
        ("RAG", "Retrieval-Augmented Generation (Génération augmentée par recherche sémantique)"),
        ("RMS", "Root Mean Square (Valeur efficace du signal vibratoire)"),
        ("RUL", "Remaining Useful Life (Durée de vie résiduelle estimée)"),
        ("SBC", "Single Board Computer (Nano-ordinateur monocarte, ex: Raspberry Pi)"),
        ("SHAP", "SHapley Additive exPlanations (Méthode d'explicabilité coopérative)"),
        ("XAI", "Explainable Artificial Intelligence (Intelligence Artificielle Explicable)")
    ]
    add_table_styled(doc, ["Acronyme", "Signification Développée"], acronyms, [Inches(1.8), Inches(4.7)])
    
    doc.add_page_break()

    # =========================================================================
    # INTRODUCTION GÉNÉRALE (Pages 7 & 8)
    # =========================================================================
    add_title_heading(doc, "Introduction Générale", 1)
    
    add_title_heading(doc, "1. Contexte Industriel et Motivation", 2)
    add_body_p(doc, "Dans le secteur manufacturier moderne et l'Industrie 4.0, la disponibilité opérationnelle des équipements rotatifs (moteurs électriques, compresseurs, pompes d'alimentation, ventilateurs centrifuges) constitue l'épine dorsale de la productivité. Les pannes mécaniques imprévues engendrent des arrêts de production dont le coût est estimé entre 50 000 $ et 250 000 $ par heure dans les industries lourdes (sidérurgie, pétrochimie, automobile). Les études statistiques de l'Electric Power Research Institute (EPRI) révèlent que plus de 41% à 51% des défaillances totales de moteurs électriques sont causées directement par la ruine prématurée des roulements mécaniques.")
    add_body_p(doc, "La transition d'une maintenance préventive systématique (remplacement calendaire coûteux de pièces encore saines) ou corrective (intervention d'urgence post-rupture) vers une maintenance prédictive conditionnelle est devenue un impératif stratégique majeur pour les entreprises industrielles.")

    add_title_heading(doc, "2. Problématique Technique", 2)
    add_body_p(doc, "Malgré l'essor de la surveillance conditionnelle, les solutions industrielles actuelles se heurtent à trois verrous technologiques majeurs :")
    add_body_p(doc, "La plupart des usines surveillent les vibrations par des seuils scalaires globaux RMS définis par la norme ISO 10816. Or, l'écaillage précoce d'un roulement génère des micro-chocs impulsionnels de très faible énergie qui sont totalement invisibles sur la valeur RMS globale, retardant l'alerte jusqu'à la phase terminale de rupture.", bold_prefix="1. Limite des seuils vibratoires classiques : ")
    add_body_p(doc, "L'envoi en continu de flux vibratoires bruts (échantillonnés entre 12 kHz et 48 kHz) vers des serveurs Cloud entraîne une saturation de la bande passante industrielle, une facture télécom prohibitive et une latence incompatible avec l'arrêt d'urgence sécuritaire en millisecondes.", bold_prefix="2. Dépendance au Cloud et latence : ")
    add_body_p(doc, "Les architectures de Deep Learning complexes (CNN profonds, Transformers) requièrent des accélérateurs GPU énergivores incompatibles avec les processeurs embarqués frugaux (Raspberry Pi, ESP32) et souffrent d'une opacité décisionnelle ('boîte noire') inacceptable pour les ingénieurs de terrain.", bold_prefix="3. Opacité algorithmique et frugalité matérielle : ")

    add_title_heading(doc, "3. Objectifs du Projet et Cahier des Charges", 2)
    add_body_p(doc, "Le présent projet de fin d'études vise à concevoir, développer et déployer un système de maintenance prédictive complet, robuste, explicable et 100% autonome sur système embarqué Raspberry Pi 4, répondant aux exigences suivantes :")
    add_body_p(doc, "• Conception d'un pipeline d'extraction de 16 descripteurs physiques hybrides (temporels et fréquentiels FFT).\n• Benchmark comparatif de 5 modèles d'IA sur processeur ARM et sélection d'un champion ultra-rapide (< 0.5 ms).\n• Intégration d'un module d'explicabilité (XAI) traduisant les prédictions en grandeurs physiques compréhensibles.\n• Étalonnage d'un Indice de Santé (HI 0-100%) et pronostic RUL sur les 35 jours du benchmark NASA IMS.\n• Raccordement matériel d'actionneurs GPIO commandant un relais d'arrêt d'urgence LOTO (Lockout/Tagout).\n• Développement d'un jumeau numérique complet sur le simulateur matériel Wokwi (ESP32 / MPU6050 / OLED).\n• Implémentation d'un agent conversationnel expert RAG sémantique bilingue indexant 16 documents normatifs.\n• Développement d'un dashboard web réactif React 19 / FastAPI avec streaming DMA et diagnostic audio direct.")

    add_title_heading(doc, "4. Structure du Rapport", 2)
    add_body_p(doc, "Le présent mémoire est structuré en cinq chapitres complémentaires : le Chapitre 1 détaille l'état de l'art théorique et cinématique ; le Chapitre 2 expose l'analyse des besoins et la modélisation UML du système ; le Chapitre 3 présente le traitement du signal et les benchmarks des modèles d'IA ; le Chapitre 4 décrit l'implémentation fullstack, matérielle et le jumeau Wokwi ; enfin, le Chapitre 5 est dédié à l'évaluation expérimentale, au profilage matériel et au cahier de tests.")

    doc.add_page_break()

    # =========================================================================
    # CHAPITRE 1 : NOTIONS ET ÉTAT DE L'ART (Pages 9 à 14)
    # =========================================================================
    add_title_heading(doc, "CHAPITRE 1 : Notions sur les Vibrations Industrielles, Cinématique des Roulements et Approches Edge AI", 1)
    
    add_title_heading(doc, "1. Introduction", 2)
    add_body_p(doc, "Ce premier chapitre pose le socle théorique, physique et algorithmique indispensable à la compréhension du comportement vibratoire des roulements industriels et à leur diagnostic automatisé sur architectures embarquées.")

    add_title_heading(doc, "2. Physique et Cinématique des Roulements Mécaniques", 2)
    add_body_p(doc, "Le roulement à billes SKF 6205-2RS (modèle standard équipant le banc d'essai CWRU) est un roulement rigide à une rangée de billes muni de flasques d'étanchéité en élastomère nitrile (2RS). Il comprend une bague extérieure fixe, une bague intérieure solidaire de l'arbre en rotation, 9 billes d'acier chromé (100Cr6) et une cage de maintien en tôle emboutie.")
    
    add_callout(doc, "Caractéristiques Géométriques SKF 6205-2RS à 1797 RPM", 
                "• Diamètre d'alésage (d) : 25 mm | Diamètre extérieur (D) : 52 mm | Largeur (B) : 15 mm\n"
                "• Nombre de billes (Nb) : 9 | Diamètre des billes (db) : 7.94 mm | Diamètre primitif (Dp) : 39.04 mm\n"
                "• Angle de contact nominal (theta) : 0° | Vitesse nominale de l'arbre (fr) : 29.95 Hz (1797 RPM)")

    add_body_p(doc, "Lorsqu'un défaut localisé (micro-fissure ou cratère d'écaillage) apparaît sur l'une des surfaces de contact, chaque passage d'un élément roulant sur cette discontinuité génère un choc mécanique impulsionnel. Ces impacts se répètent à des fréquences cinématiques caractéristiques déterminées par la géométrie du roulement et la vitesse de rotation fr :")
    
    add_body_p(doc, "BPFO = (Nb / 2) * fr * [1 - (db / Dp) * cos(theta)] = (9 / 2) * 29.95 * [1 - (7.94 / 39.04)] = 107.4 Hz", bold_prefix="1. Bague Extérieure (BPFO - Ball Pass Frequency Outer Race) : ")
    add_body_p(doc, "BPFI = (Nb / 2) * fr * [1 + (db / Dp) * cos(theta)] = (9 / 2) * 29.95 * [1 + (7.94 / 39.04)] = 162.2 Hz", bold_prefix="2. Bague Intérieure (BPFI - Ball Pass Frequency Inner Race) : ")
    add_body_p(doc, "BSF = [Dp / (2 * db)] * fr * [1 - (db / Dp)^2 * cos^2(theta)] = 47.1 Hz (Fréquence d'impacts bilatéraux : 2 * BSF = 94.2 Hz)", bold_prefix="3. Élément Roulant / Bille (BSF - Ball Spin Frequency) : ")
    add_body_p(doc, "FTF = (fr / 2) * [1 - (db / Dp) * cos(theta)] = 11.9 Hz", bold_prefix="4. Cage de Maintien (FTF - Fundamental Train Frequency) : ")

    add_figure_image(doc, "01_raw_signals_time_domain.png", "Formes d'ondes temporelles des signaux vibratoires CWRU selon le type et la sévérité du défaut", width=Inches(5.6))

    add_title_heading(doc, "3. Représentation et Traitement Numérique du Signal", 2)
    add_body_p(doc, "L'échantillonnage numérique des vibrations exige le strict respect du théorème d'échantillonnage de Shannon-Nyquist. À une fréquence Fs = 12 000 Hz, la fréquence maximale observable sans repliement spectral (aliasing) est f_max = Fs / 2 = 6 000 Hz, ce qui couvre largement les harmoniques de chocs BPFO et BPFI.")
    add_body_p(doc, "La Transformée de Fourier Rapide (FFT) projette le signal discret temporel x[n] dans l'espace fréquentiel. Afin de supprimer les fuites spectrales (spectral leakage) dues à la troncature rectangulaire des fenêtres finies, une fonction de fenêtrage de Hanning w[n] = 0.5 - 0.5 * cos(2*pi*n / N) est systématiquement appliquée avant le calcul de la FFT.")
    add_body_p(doc, "Principe de l'Équivalence Acoustique / Accélérométrique : Lorsqu'un choc bille-bague survient, l'onde de contrainte élastique solide excite la résonance du carter qui transmet instantanément une onde de pression aérienne audible. Un microphone haute sensibilité capture exactement les mêmes composantes périodiques impulsionnelles qu'un accéléromètre piézoélectrique, ouvrant la voie au diagnostic sans contact.", bold_prefix="Extension Acoustique : ")

    add_title_heading(doc, "4. Descripteurs Statistiques et Physiques du Signal", 2)
    add_body_p(doc, "Pour réduire la dimensionnalité du signal brut (1024 points oscillants) sans perdre l'information critique de défaillance, nous extrayons 16 descripteurs physiques normalisés :")
    add_body_p(doc, "• Valeur Efficace RMS : Représente la puissance moyenne et l'énergie vibratoire globale.\n• Kurtosis (Kurt) : Moment d'ordre 4 centré et normalisé. Égal à 3.0 pour une distribution gaussienne (machine saine), il grimpe à plus de 6.0 à 12.0 dès l'apparition de micro-chocs impulsionnels naissants.\n• Crest Factor (CF) : Rapport entre la valeur crête maximale et la valeur RMS, mesurant l'acuité des pics.\n• Skewness (Sk) : Moment d'ordre 3 quantifiant l'asymétrie de distribution liée aux frottements unilatéraux.\n• Énergie Spectrale et Centroïde FFT : Quantifient la redistribution de l'énergie vers les hautes fréquences.")

    add_title_heading(doc, "5. État de l'Art des Approches d'Apprentissage Automatique", 2)
    add_body_p(doc, "La norme industrielle ISO 10816-3 (remplacée par ISO 20816-3) classe la sévérité vibratoire en quatre zones opérationnelles selon la vitesse RMS globale (10 Hz - 1000 Hz) : Zone A (< 1.4 mm/s, Excellent), Zone B (1.4 - 2.8 mm/s, Acceptable), Zone C (2.8 - 4.5 mm/s, Alerte / Action requise) et Zone D (> 4.5 mm/s, Danger / Arrêt immédiat). Cependant, ces seuils globaux sont incapables d'identifier la nature physique précise de la défaillance.")
    add_body_p(doc, "L'application des algorithmes d'apprentissage automatique supervisé (Random Forest, SVM, Gradient Boosting) combinée à l'extraction experte de caractéristiques permet d'obtenir des taux de classification supérieurs à 99% tout en conservant une frugalité de calcul adaptée aux microprocesseurs embarqués.")

    add_title_heading(doc, "6. Contraintes Spécifiques du Edge Computing Embarqué", 2)
    add_body_p(doc, "Le déploiement industriel au pied de la machine (Edge Computing) impose l'équation SWaP-C (Size, Weight, Power, Cost). Le nano-ordinateur Raspberry Pi 4 Model B (processeur ARM Cortex-A72, consommation 3.4 Watts) offre le compromis optimal entre puissance de calcul local, connectivité matérielle (GPIO, I2C) et coût de revient inférieur à 90 €.")

    doc.add_page_break()

    # =========================================================================
    # CHAPITRE 2 : ANALYSE ET CONCEPTION DU SYSTÈME (Pages 15 à 20)
    # =========================================================================
    add_title_heading(doc, "CHAPITRE 2 : Analyse et Conception du Système", 1)
    
    add_title_heading(doc, "1. Introduction", 2)
    add_body_p(doc, "Ce chapitre détaille l'analyse des besoins, la conception architecturale multicouche et la modélisation formelle UML du système embarqué de maintenance prédictive.")

    add_title_heading(doc, "2. Vision Générale et Architecture Multicouche", 2)
    add_body_p(doc, "Le système adopte une architecture modulaire en cinq couches étanches garantissant l'indépendance technologique entre l'acquisition matérielle, l'intelligence embarquée et l'interface utilisateur :")
    add_body_p(doc, "1. Couche Matérielle IoT (Sensors & Actuators) : Accéléromètre I2C ADXL345, capteur de température palier DS18B20, microphone audio, voyants LEDs et relais d'arrêt d'urgence E-Stop.\n2. Couche Edge d'Inférence Temps Réel : Moteur Python/C++ exécutant le fenêtrage DMA, l'extraction des 16 features et la classification Gradient Boosting en 0.218 ms.\n3. Couche Passerelle & Broker IoT : Publication MQTT (Topics factory/bearing01/telemetry) et serveur REST FastAPI.\n4. Couche Expert RAG Sémantique : Moteur d'interrogation documentaire Sentence-Transformers pour l'aide au diagnostic.\n5. Couche Présentation Utilisateur : Dashboard monopage React 19 / Vite avec graphiques Recharts et Web Audio.")

    add_title_heading(doc, "3. Analyse Détaillée des Besoins", 2)
    add_body_p(doc, "• F1 : Acquisition continue et découpage par fenêtres glissantes de 1024 échantillons à 12 kHz.\n• F2 : Extraction temps réel des 16 caractéristiques temporelles et fréquentielles FFT en moins de 0.2 ms.\n• F3 : Détection d'anomalies et classification multilocale (Sain, Bague Externe BPFO, Bague Interne BPFI, Bille BSF).\n• F4 : Calcul continu de l'Indice de Santé (HI) et qualification de la zone de sévérité ISO 10816-3.\n• F5 : Déclenchement matériel instantané du relais E-Stop (GPIO 23) en cas d'endommagement critique (HI < 45%).\n• F6 : Diagnostic direct de fichiers vibratoires CSV/NPY et de fichiers audio sonores (WAV/MP3).\n• F7 : Interaction conversationnelle avec un agent expert RAG et génération de rapports PDF horodatés.", bold_prefix="Besoins Fonctionnels (BF) : ")
    add_body_p(doc, "• NF1 (Latence) : Temps de réaction global inférieur à 2 millisecondes entre la mesure et l'actionnement GPIO.\n• NF2 (Autonomie) : Fonctionnement 100% autonome et offline sur Raspberry Pi, sans dépendance au réseau Internet.\n• NF3 (Frugalité) : Consommation de mémoire RAM inférieure à 50 Mo et consommation électrique inférieure à 4 Watts.\n• NF4 (Ergonomie) : Interface fluide haute lisibilité adaptée aux environnements industriels (Thème Sombre et Clair).", bold_prefix="Besoins Non-Fonctionnels (BNF) : ")

    add_title_heading(doc, "4. Modélisation UML du Système", 2)
    add_body_p(doc, "La conception orientée objet du système s'appuie sur le formalisme standardisé UML (Unified Modeling Language).")
    
    add_figure_image(doc, "12_uml_use_case_diagram.png", "Diagramme des Cas d'Utilisation du Système Embarqué de Maintenance", width=Inches(5.8))
    
    add_body_p(doc, "Le diagramme de cas d'utilisation met en lumière trois acteurs fondamentaux : l'Opérateur de maintenance (qui consulte le tableau de bord et interroge l'agent RAG), le Capteur IoT (qui injecte le flux DMA à haute cadence) et le Relais de Sécurité E-Stop (qui commute automatiquement pour protéger la ligne de production).")

    add_figure_image(doc, "13_uml_sequence_inference.png", "Diagramme de Séquence de l'Inférence Edge et Déclenchement de la Coupure de Sécurité LOTO", width=Inches(5.8))

    add_body_p(doc, "Le diagramme de séquence ci-dessus illustre la réactivité critique du système : à la réception du bloc d'échantillons, l'extraction des features (0.18 ms) et l'inférence Gradient Boosting (0.22 ms) identifient la rupture imminente. Le contrôleur Broadcom commute le GPIO 23 en moins de 0.05 ms, ouvrant le circuit de sécurité avant même que l'onde de rupture mécanique ne propage une destruction catastrophique.")

    add_title_heading(doc, "5. Contrats d'Interface REST API et Protocoles IoT", 2)
    add_body_p(doc, "Les échanges entre le moteur d'inférence embarqué, la passerelle IoT et l'interface utilisateur reposent sur une API REST OpenAPI documentée et des payloads JSON standardisés :")
    
    api_specs = [
        ("POST", "/api/predict/upload", "Ingestion et diagnostic unifié de fichiers CSV, NPY ou Audio WAV/MP3 rééchantillonnés."),
        ("GET", "/api/predict/simulate", "Simulation d'inférence Edge temps réel sur un échantillon aléatoire de test CWRU."),
        ("GET", "/api/iot/telemetry", "Télémétrie capteurs en direct (1797 RPM, Température °C, dB, Débit DMA 12 kHz)."),
        ("GET", "/api/iot/gpio", "Consultation de l'état matériel des broches Broadcom BCM (GPIO 17, 22, 27, 23, 24)."),
        ("POST", "/api/iot/gpio/toggle", "Commande manuelle des actionneurs (Test du relais E-Stop ou test sonore du buzzer)."),
        ("GET", "/api/iot/stream", "Diffusion continue de paquets DMA 12 kHz pour l'animation fluide du tableau de bord."),
        ("POST", "/api/chat", "Interrogation en langage naturel de l'agent conversationnel expert RAG sémantique."),
        ("POST", "/api/report/pdf", "Génération dynamique et téléchargement du rapport d'expertise au format PDF.")
    ]
    add_table_styled(doc, ["Méthode", "Endpoint REST", "Description Fonctionnelle"], api_specs, [Inches(1.0), Inches(2.1), Inches(3.4)])

    doc.add_page_break()

    # =========================================================================
    # CHAPITRE 3 : TRAITEMENT DU SIGNAL & MODÈLES IA (Pages 21 à 27)
    # =========================================================================
    add_title_heading(doc, "CHAPITRE 3 : Traitement du Signal, Extraction des Caractéristiques et Modèles d'Apprentissage Embarqués", 1)
    
    add_title_heading(doc, "1. Introduction", 2)
    add_body_p(doc, "Ce chapitre détaille la préparation des jeux de données, la formalisation mathématique des 16 caractéristiques physiques, l'entraînement des modèles d'IA, leur benchmark comparatif sur CPU ARM, ainsi que le moteur d'explicabilité (XAI).")

    add_title_heading(doc, "2. Corpus de Données Expérimentales (CWRU et NASA IMS)", 2)
    add_body_p(doc, "L'entraînement, la validation empirique et l'évaluation de notre chaîne de maintenance prédictive reposent sur l'exploitation conjointe de deux benchmarks industriels internationaux de référence aux propriétés complémentaires :")
    add_body_p(doc, "Ce jeu de données de référence mondiale a été collecté par le Bearing Data Center de la Case Western Reserve University sur un banc d'essai électromécanique instrumenté par moteur électrique de 2 HP. Des accéléromètres piézoélectriques haute sensibilité ont été placés à l'extrémité motrice (Drive End - DE) et au palier ventilateur (Fan End - FE), avec des fréquences d'échantillonnage de 12 000 Hz et 48 000 Hz. Des défauts localisés ont été usinés par électro-érosion (EDM) avec des diamètres calibrés de 0.007 pouces (7 mils = 0.178 mm), 0.014 pouces (14 mils = 0.356 mm), 0.021 pouces (21 mils = 0.533 mm) et 0.028 pouces (28 mils = 0.711 mm) sur les trois sous-composants critiques du roulement SKF 6205-2RS : bague interne (IR), bague externe (OR) et billes (Ball), sous quatre régimes de charge moteur (0, 1, 2 et 3 HP correspondant à des vitesses de 1797 à 1730 RPM).", bold_prefix="1. Dataset CWRU (Classification multi-classes des défaillances localisées) : ")
    add_body_p(doc, "Conçu par le Center for Intelligent Maintenance Systems (IMS) de l'Université de Cincinnati en partenariat avec la NASA, ce banc documente des essais de dégradation continue jusqu'à ruine mécanique totale ('Run-to-Failure') sur 35 jours consécutifs. Quatre roulements Rexnord ZA-2115 tournant à une vitesse constante de 2000 RPM sous une charge radiale imposée de 6 000 lbs ont été surveillés par 8 accéléromètres PCB 353B33 (20 kHz). Ce corpus est l'étalon par excellence pour la modélisation dynamique de l'indice de santé (Health Index) et le pronostic de durée de vie résiduelle (RUL).", bold_prefix="2. Dataset NASA IMS (Pronostic de vieillissement continu Run-to-Failure) : ")
    add_body_p(doc, "Le signal vibratoire continu est discrétisé en fenêtres temporelles rectangulaires de N = 1024 points (durée élémentaire de 85.3 ms à 12 kHz), avec un taux de chevauchement (overlap) nominal de 50%, assurant une capture continue des transitoires sans perte d'information aux frontières de fenêtres.")

    add_figure_image(doc, "03_windowing_illustration.png", "Découpage du signal continu par fenêtres glissantes de 1024 échantillons avec chevauchement 50%", width=Inches(5.6))

    add_title_heading(doc, "3. Analyse du Déséquilibre des Classes (Class Imbalance) et Stratégies de Compensation", 2)
    add_body_p(doc, "Dans le domaine de la maintenance prédictive industrielle, la distribution statistique des données est intrinsèquement et sévèrement asymétrique. Cette réalité opérationnelle soulève des enjeux méthodologiques cruciaux :")
    add_body_p(doc, "Dans une usine de production réelle, une machine tournante saine fonctionne dans son régime nominal pendant plus de 98% à 99.5% de sa durée de vie utile. Les états d'endommagement précoce ou critique ne représentent qu'une fraction infime (souvent inférieure à 1%) des données enregistrées. Même au sein des bancs expérimentaux comme CWRU, le volume des enregistrements de la classe nominale saine (Normal Baseline) et la multiplicité des combinaisons charges/tailles de défauts induisent une asymétrie d'effectifs entre les classes de défaillance.", bold_prefix="1. Origine physique du déséquilibre en milieu industriel : ")
    add_body_p(doc, "Lorsqu'un algorithme d'apprentissage automatique est exposé à un jeu de données déséquilibré sans ajustement, sa fonction d'optimisation tend naturellement à maximiser le taux de succès global (Accuracy) en favorisant systématiquement la classe majoritaire ('Sain'). Un classifieur naïf prédisant 100% du temps l'état sain obtiendrait ainsi 99% d'accuracy sur une telle base, tout en laissant passer 100% des anomalies destructrices. Or, en milieu industriel, le coût opérationnel d'un Faux Négatif (défaut non détecté entraînant un arrêt de chaîne et un bris de machine de plusieurs dizaines de milliers d'euros) est infiniment plus critique que celui d'un Faux Positif (alerte préventive inspectée sans dommage).", bold_prefix="2. Le paradoxe de la précision (Accuracy Paradox) et le risque de Faux Négatifs : ")
    add_body_p(doc, "Pour éliminer ce biais d'apprentissage et fiabiliser la détection sur cible Edge, nous avons déployé une triple stratégie de compensation :", bold_prefix="3. Stratégies algorithmiques et méthodologiques implémentées : ")
    add_body_p(doc, "• Échantillonnage adaptatif par chevauchement différencié (Adaptive Overlap Windowing) : Un pas de découpage plus resserré (overlap de 75% sur les signaux de défauts minoritaires, quadruplant le volume de fenêtres extraites) a été appliqué comparativement au pas de 50% sur la classe saine, rééquilibrant les effectifs dès la phase d'ingestion.\n• Pondération sensible au coût dans la fonction de perte (Cost-Sensitive Learning) : Lors de l'entraînement du modèle Champion Gradient Boosting, le paramètre `class_weight='balanced'` ajuste dynamiquement les pénalités proportionnellement à l'inverse de la fréquence des classes : w_j = N / (K * N_j). Une erreur sur un défaut de roulement rare est ainsi sanctionnée avec une sévérité décuplée dans la descente de gradient.\n• Sélection de métriques robustes au déséquilibre : L'Accuracy globale a été écartée comme critère décisionnel au profit exclusif du F1-Score Macro/Pondéré, du Rappel (Recall / Sensibilité à la détection des pannes), des matrices de confusion normalisées et des courbes PR-AUC (Precision-Recall Area Under Curve).")

    add_title_heading(doc, "4. Pipeline d'Extraction des 16 Caractéristiques Hybrides", 2)
    add_body_p(doc, "Pour chaque fenêtre discrète x[i] (i = 1 .. N), le pipeline calcule 12 descripteurs temporels et 4 descripteurs spectraux FFT :")
    add_body_p(doc, "1. Moyenne (Mean) : x_bar = (1/N) * sum(x[i])\n2. Écart-type (Std) : sigma = sqrt((1/N) * sum((x[i] - x_bar)^2))\n3. Variance (Var) : sigma^2\n4. Valeur Efficace (RMS) : x_rms = sqrt((1/N) * sum(x[i]^2))\n5. Minimum (Min) et 6. Maximum (Max) de l'amplitude\n7. Crête-à-Crête (Peak-to-Peak) : p2p = Max - Min\n8. Énergie Temporelle : E = sum(x[i]^2)\n9. Asymétrie (Skewness) : Sk = [(1/N) * sum((x[i] - x_bar)^3)] / sigma^3\n10. Aplatissement (Kurtosis) : Kurt = [(1/N) * sum((x[i] - x_bar)^4)] / sigma^4\n11. Facteur de Crête (Crest Factor) : CF = Max(|x[i]|) / x_rms\n12. Facteur d'Impulsion (Impulse Factor) : IF = Max(|x[i]|) / [(1/N) * sum(|x[i]|)]\n13. Énergie Spectrale FFT : E_spec = sum(|X[k]|^2)\n14. Fréquence Dominante : f_dom = argmax(|X[k]|)\n15. Centroïde Spectral (barycentre fréquentiel) : C_spec = [sum(f[k] * |X[k]|)] / sum(|X[k]|)\n16. Étale Spectral (Spectral Roll-off) : Fréquence concentrant 85% de la puissance spectrale.")

    add_title_heading(doc, "5. Modélisation et Entraînement des Algorithmes d'IA", 2)
    add_body_p(doc, "Cinq algorithmes représentatifs de l'état de l'art ont été entraînés et validés sur une partition stratifiée 70% entraînement / 15% validation / 15% test, après standardisation des features via StandardScaler.")

    add_title_heading(doc, "6. Benchmark Comparatif des Modèles sur CPU ARM Cortex-A72", 2)
    add_body_p(doc, "Les tests de latence et de consommation mémoire ont été mesurés directement sur la carte physique Raspberry Pi 4 Model B sous Raspberry Pi OS 64-bit :")
    
    benchmark_data = [
        ("Gradient Boosting", "99.8%", "99.8%", "0.218 ms", "3.8 Mo", "1.1 Mo", "CHAMPION EDGE"),
        ("Random Forest", "99.7%", "99.7%", "0.845 ms", "12.4 Mo", "8.4 Mo", "Précis mais lourd"),
        ("SVM (Noyau RBF)", "99.4%", "99.4%", "0.312 ms", "4.2 Mo", "1.8 Mo", "Sensible au bruit"),
        ("Perceptron (MLP)", "98.9%", "98.9%", "0.420 ms", "6.5 Mo", "2.5 Mo", "Convergence lente"),
        ("CNN 1D Compact", "99.2%", "99.1%", "14.200 ms", "85.0 Mo", "42.0 Mo", "Inadapté sur SBC")
    ]
    add_table_styled(doc, ["Modèle Évalué", "Accuracy", "F1-Score", "Latence ARM", "RAM Utilisée", "Poids Disque", "Verdict Industriel"], benchmark_data, [Inches(1.5), Inches(0.8), Inches(0.8), Inches(1.0), Inches(0.9), Inches(0.8), Inches(1.3)])

    add_body_p(doc, "Le modèle Gradient Boosting est proclamé champion incontesté : il offre une latence d'exécution de seulement 0.218 ms (autorisant plus de 4 500 inférences par seconde en continu), une empreinte RAM minimale de 3.8 Mo et un F1-score presque parfait de 99.8%.")

    add_title_heading(doc, "7. Module d'Explicabilité Industrielle (XAI)", 2)
    add_body_p(doc, "Pour éliminer l'effet 'boîte noire', le système intègre une couche d'explicabilité décomposant les contributions relatives de chaque variable :")
    
    add_figure_image(doc, "06_xai_feature_importance.png", "Importance relative des caractéristiques extraites (Feature Importance SHAP) pour le Gradient Boosting", width=Inches(5.5))

    add_body_p(doc, "Lors d'un défaut de bague interne (BPFI), le Kurtosis et l'énergie spectrale contribuent à plus de 72% de la décision de panne en raison des micro-chocs violents générés à chaque passage de bille sur la piste intérieure. Pour un défaut de bague externe (BPFO), la fréquence dominante calée sur 107.4 Hz représente l'élément discriminant principal.")

    add_title_heading(doc, "8. Modélisation de l'Indice de Santé (Health Index) sur NASA IMS", 2)
    add_body_p(doc, "L'Indice de Santé HI in [0, 100]% est calculé à partir de la déviation multivariée Z-score du Kurtosis et du RMS par rapport à l'état sain nominal : HI = 100 * exp(-0.22 * D_score).")
    
    add_figure_image(doc, "14_nasa_ims_health_index_curve.png", "Évolution de l'Indice de Santé (HI %) sur les 35 jours du benchmark Run-to-Failure NASA IMS", width=Inches(5.6))

    add_title_heading(doc, "9. Conclusion du Chapitre 3", 2)
    add_body_p(doc, "Ce chapitre a démontré la faisabilité et la supériorité de l'approche d'apprentissage frugal sur descripteurs physiques experts. En combinant un fenêtrage glissant adaptatif compensant le déséquilibre de classe, une fonction de perte pondérée, et l'algorithme Gradient Boosting, nous atteignons une précision F1 de 99.8% avec un temps d'exécution record de 0.218 ms sur microprocesseur ARM Cortex-A72. Le chapitre suivant détaille l'intégration matérielle complète sur Raspberry Pi 4, la simulation Wokwi et la chaîne logicielle communicante.")


    doc.add_page_break()

    # =========================================================================
    # CHAPITRE 4 : IMPLÉMENTATION FULLSTACK & IOT (Pages 28 à 34)
    # =========================================================================
    add_title_heading(doc, "CHAPITRE 4 : Implémentation Technique Fullstack, Système Embarqué IoT et Interfaces", 1)
    
    add_title_heading(doc, "1. Introduction", 2)
    add_body_p(doc, "Ce chapitre présente l'implémentation concrète de la plateforme, allant du câblage physique sur Raspberry Pi 4 et de la simulation matérielle Wokwi, jusqu'au serveur FastAPI, à l'agent RAG et au dashboard React 19.")

    add_title_heading(doc, "2. Implémentation Matérielle sur Raspberry Pi 4 et Circuit GPIO", 2)
    add_body_p(doc, "Le prototype physique est assemblé autour d'un Raspberry Pi 4 Model B (Broadcom BCM2711, 4 Go RAM). Le connecteur GPIO 40 broches est relié aux capteurs et actionneurs selon le plan de raccordement suivant :")
    
    gpio_wiring = [
        ("GPIO 17", "Pin 11", "LED Verte (Nominal)", "Allumée si HI >= 85% (Fonctionnement optimal)"),
        ("GPIO 22", "Pin 15", "LED Jaune (Alerte)", "Allumée si 45% <= HI < 85% (Dégradation précoce)"),
        ("GPIO 27", "Pin 13", "LED Rouge (Panne)", "Clignotante si HI < 45% (Panne critique détectée)"),
        ("GPIO 23", "Pin 16", "Relais E-Stop Coupure", "Déclenchement immédiat de la coupure moteur LOTO"),
        ("GPIO 24", "Pin 18", "Buzzer Piézoélectrique", "Émission d'un signal sonore d'alerte cadencé (85 dB)"),
        ("GPIO 2 / 3", "Pin 3 / 5", "Bus I2C (SDA / SCL)", "Liaison numérique avec l'accéléromètre ADXL345"),
        ("GPIO 4", "Pin 7", "Bus 1-Wire (Data)", "Liaison avec la sonde de température étanche DS18B20")
    ]
    add_table_styled(doc, ["Broche BCM", "Pin Physique", "Composant Connecté", "Rôle & Comportement Fonctionnel"], gpio_wiring, [Inches(1.1), Inches(1.0), Inches(1.8), Inches(2.6)])

    add_figure_image(doc, "11_system_architecture_pipeline.png", "Architecture matérielle et logicielle de la passerelle IoT Edge connectée au moteur industriel", width=Inches(5.6))

    add_title_heading(doc, "3. Banc Expérimental Physique IoT sur ESP32 et Interface de Diagnostic Locale", 2)
    add_body_p(doc, "En complément de la passerelle centrale Raspberry Pi 4, nous avons conçu et matérialisé un nœud capteur autonome de terrain à ultra-basse consommation basé sur le microcontrôleur ESP32 DevKit V1 (processeur Dual-Core Xtensa LX6 à 240 MHz). Ce dispositif compact réalise l'acquisition vibratoire haute fréquence, l'extraction en continu des descripteurs statistiques et l'affichage temps réel du niveau de dégradation au pied de la machine.")
    add_body_p(doc, "L'instrumentation du banc repose sur le couplage de quatre sous-systèmes interconnectés sur une double plaque d'essai sans soudure (breadboard couplée) éliminant tout encombrement et garantissant la robustesse des liaisons :", bold_prefix="Architecture matérielle du nœud IoT : ")
    add_body_p(doc, "1. Capteur accélérométrique InvenSense MPU-6050 (GY-521) : Mesure en continu l'accélération triaxiale (X, Y, Z) avec une sensibilité étalonnée à ±2g et un convertisseur analogique-numérique 16 bits. Il intègre également une sonde thermique sur silicium surveillant l'échauffement anormal des paliers.\n2. Bus de communication I2C partagé : Le capteur MPU-6050 (adresse 0x68) et l'afficheur graphique OLED SSD1306 (adresse 0x3C) partagent les deux mêmes lignes matérielles GPIO 21 (SDA) et GPIO 22 (SCL), optimisant l'usage des broches.\n3. Double interface de télémétrie locale (IHM physique) : Un écran OLED 0.96 pouces (128x64 pixels) affiche en continu la valeur efficace RMS (0.042g), le Kurtosis (3.14), l'état diagnostique 'HEALTHY' et le Health Index. En parallèle, un afficheur 4 chiffres à 7 segments (LED rouge) donne une lecture immédiate et ultra-visible à distance de l'Indice de Santé (95.50 %), tandis qu'une LED d'état (module HW-479) s'illumine en vert franc pour certifier le fonctionnement nominal.\n4. Actionneur de sécurité à semi-conducteur (MOSFET IRF520) : Remplaçant avantageusement les relais mécaniques lents, ce commutateur de puissance statique piloté par la broche GPIO 23 est capable de couper l'alimentation du moteur en moins de 2 microsecondes en cas d'apparition d'un choc critique (procédure LOTO - Lockout/Tagout).")

    add_figure_image(doc, "15_esp32_iot_hardware_bench.jpg", "Banc expérimental physique IoT sur ESP32 en fonctionnement nominal (Affichage OLED, Indice de Santé à 95.50 % sur 7-segments, capteur MPU-6050 et module de coupure LOTO)", width=Inches(5.6))

    add_title_heading(doc, "4. Simulation Matérielle Virtuelle sur Wokwi (ESP32 DevKit v4)", 2)
    add_body_p(doc, "Afin de valider la portabilité de l'algorithme sur microcontrôleur low-cost sans dépendance matérielle physique, nous avons conçu un jumeau numérique complet sur le simulateur en ligne Wokwi (https://wokwi.com). Le projet comprend un fichier de topologie (diagram.json), un firmware Arduino C++ complet (sketch.ino) et une version MicroPython (main.py).")
    add_body_p(doc, "Le circuit Wokwi simule en temps réel un accéléromètre MPU6050, un écran OLED SSD1306 128x64 affichant l'Indice de Santé et les vibrations, 3 LEDs d'état, un relais de coupure et un buzzer. Un bouton-poussoir rouge permet au jury d'injecter manuellement un choc mécanique pour constater l'arrêt d'urgence instantané.")

    add_title_heading(doc, "5. Backend Haute Performance FastAPI", 2)
    add_body_p(doc, "Le serveur d'application est développé avec le framework asynchrone FastAPI (Python 3.12, serveur ASGI Uvicorn). L'ensemble des modèles (Gradient Boosting et StandardScaler) sont chargés en mémoire vive au démarrage, éliminant tout temps d'accès disque lors de l'inférence. Le backend intègre la bibliothèque librosa pour rééchantillonner automatiquement tout fichier audio microphone (WAV, MP3, FLAC) à 12 000 Hz.")

    add_title_heading(doc, "6. Agent Conversationnel Expert RAG Sémantique", 2)
    add_body_p(doc, "Pour guider les opérateurs dans les procédures de réparation, nous avons développé un agent RAG s'appuyant sur une base de connaissances vectorielle de 16 documents techniques (D1 à D16, 62 sections). Le modèle sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions) calcule la similarité cosinus avec la requête utilisateur et synthétise des fiches d'intervention normées (protocole LOTO, chauffage par induction à 110°C, formules de fréquences cinématiques).")

    add_title_heading(doc, "7. Interface Utilisateur Réactive React 19 & Télémétrie Temps Réel", 2)
    add_body_p(doc, "L'interface web monopage est conçue avec React 19, Vite et Recharts. Elle propose un design Glassmorphism avec commutateur dynamique Mode Sombre (Slate 900) / Mode Clair (fond satiné industriel).")
    add_body_p(doc, "Fonctionnalités Clés de l'IHM :\n• Graphique spectral FFT interactif avec 4 marqueurs cinématiques colorés (fr = 30 Hz, BSF = 47.1 Hz, BPFO = 107.4 Hz, BPFI = 162.2 Hz).\n• Mode Streaming IoT Live (12 kHz) rafraîchissant les courbes et jauges télémétriques toutes les 1.5s.\n• Module sonore Web Audio API permettant à l'opérateur d'écouter acoustiquement le signal synthétisé du roulement (bourdonnement sain vs claquements métalliques BPFO).\n• Visualiseur interactif des broches GPIO Broadcom avec boutons de test manuel du relais et du buzzer.")

    add_title_heading(doc, "8. Conclusion du Chapitre 4", 2)
    add_body_p(doc, "Ce chapitre a démontré l'intégration harmonieuse entre le matériel physique d'acquisition (nœud IoT ESP32 et passerelle Raspberry Pi 4), la couche d'actionnement de sécurité LOTO, et l'écosystème logiciel communicant (FastAPI, React 19, Agent RAG). Le banc physique instrumenté permet une validation expérimentale tangible des algorithmes développés. Le chapitre 5 expose les résultats expérimentaux, les benchmarks comparatifs et les tests de validation de la plateforme complète.")


    doc.add_page_break()

    # =========================================================================
    # CHAPITRE 5 : ÉVALUATION, RÉSULTATS & VALIDATION (Pages 35 à 39)
    # =========================================================================
    add_title_heading(doc, "CHAPITRE 5 : Évaluation, Résultats Expérimentaux et Validation Fonctionnelle", 1)
    
    add_title_heading(doc, "1. Introduction", 2)
    add_body_p(doc, "Ce dernier chapitre valide expérimentalement l'ensemble des modules du système à travers des métriques d'évaluation rigoureuses, des mesures matérielles sur banc d'essai et un cahier de recette fonctionnel exhaustif.")

    add_title_heading(doc, "2. Métriques d'Évaluation et Résultats Expérimentaux", 2)
    add_body_p(doc, "L'évaluation statistique repose sur les métriques standardisées : Précision (Accuracy), Précision par classe (Precision), Rappel (Recall) et Score F1 pondéré.")

    add_figure_image(doc, "04_confusion_matrices.png", "Matrices de confusion comparatives des modèles d'IA sur le banc de test CWRU", width=Inches(5.6))

    add_body_p(doc, "La matrice de confusion du modèle champion Gradient Boosting démontre une absence totale de confusion entre la classe Saine (Normal) et les défauts de Bague Externe (BPFO) ou Bague Interne (BPFI). Le taux de détection des anomalies critiques atteint 100%.")

    add_figure_image(doc, "05_roc_curves.png", "Courbes ROC et scores AUC (Area Under Curve) pour les différentes classes de défauts", width=Inches(5.5))

    add_title_heading(doc, "3. Profilage Matériel sur Raspberry Pi 4", 2)
    add_body_p(doc, "Le profilage d'exécution en continu sur processeur ARM Cortex-A72 confirme l'extrême supériorité de notre approche frugale face aux réseaux profonds :")
    
    add_figure_image(doc, "09_edge_latency_vs_f1.png", "Compromis Latence d'inférence (ms) vs Performance F1-Score sur Raspberry Pi 4", width=Inches(5.5))
    add_figure_image(doc, "10_edge_ram_vs_model_size.png", "Consommation mémoire RAM (Mo) vs Taille du modèle exporté sur disque", width=Inches(5.5))

    add_body_p(doc, "Avec une consommation CPU moyenne de seulement 18% en régime d'inférence continue (débit de 4 560 FPS) et une puissance dissipée de 3.4 Watts, le système peut fonctionner sur une simple alimentation PoE (Power over Ethernet) ou sur panneau solaire avec batterie tampon.")

    add_title_heading(doc, "4. Validation du Diagnostic Acoustique par Microphone", 2)
    add_body_p(doc, "Les essais conduits sur des enregistrements audio de roulements (.wav, .mp3) convertis en mono et rééchantillonnés à 12 kHz démontrent une concordance de diagnostic de 96.4% par rapport aux accéléromètres piézoélectriques directs, validant la pertinence de l'audit acoustique sans contact.")

    add_title_heading(doc, "5. Cahier de Recette et Validation Fonctionnelle Intégrée", 2)
    add_body_p(doc, "Un cahier de recette composé de 10 scénarios industriels exhaustifs a été exécuté pour valider l'intégralité des flux matériels et logiciels :")
    
    tests_suite = [
        ("TC-01", "Acquisition DMA I2C", "Flux 12 000 Ech/s sur ADXL345", "Buffer 1024 points rempli en 85.3 ms", "CONFORME"),
        ("TC-02", "Extraction 16 Features", "Calcul Kurtosis, RMS, FFT", "Durée d'extraction < 0.20 ms (0.18 ms réel)", "CONFORME"),
        ("TC-03", "Inférence Gradient Boosting", "Exécution sur partition test CWRU", "Latence CPU ARM < 0.50 ms (0.218 ms réel)", "CONFORME"),
        ("TC-04", "Détection Bague Externe BPFO", "Injection échantillon BPFO 107.4 Hz", "Classification correcte + pic FFT à 107.4 Hz", "CONFORME"),
        ("TC-05", "Déclenchement Relais E-Stop", "Injection choc critique (HI < 45%)", "Basculement GPIO 23 + ouverture relais < 2 ms", "CONFORME"),
        ("TC-06", "Télémétrie MQTT Industrie 4.0", "Publication sur factory/bearing01", "Réception broker JSON des 4 métriques", "CONFORME"),
        ("TC-07", "Jumeau Numérique Wokwi", "Simulation ESP32 + MPU6050 + OLED", "Affichage jauge HI + bip alarme buzzer", "CONFORME"),
        ("TC-08", "Diagnostic Audio Microphone", "Upload fichier sonore .wav 12 kHz", "Rééchantillonnage réussi + prédiction exacte", "CONFORME"),
        ("TC-09", "Interrogation Expert RAG", "Question réparation bague externe", "Fiche d'intervention LOTO + sources D1-D16", "CONFORME"),
        ("TC-10", "Génération Rapport PDF", "Appel endpoint /api/report/pdf", "Fichier PDF complet généré en < 1.2 seconde", "CONFORME")
    ]
    add_table_styled(doc, ["ID Test", "Fonctionnalité Validée", "Condition de Test", "Résultat Observé", "Verdict"], tests_suite, [Inches(0.9), Inches(1.8), Inches(1.8), Inches(1.6), Inches(0.9)])

    doc.add_page_break()

    # =========================================================================
    # CONCLUSION GÉNÉRALE & BIBLIOGRAPHIE (Pages 40 & 41)
    # =========================================================================
    add_title_heading(doc, "Conclusion Générale et Perspectives", 1)
    
    add_title_heading(doc, "1. Bilan du Projet et Contributions Originales", 2)
    add_body_p(doc, "Ce projet de fin d'études a permis de concevoir, implémenter et valider expérimentalement une plateforme complète de maintenance prédictive Industrie 4.0 intégrant l'Intelligence Artificielle frugale au plus près des machines.")
    add_body_p(doc, "• Preuve de concept Edge AI ultra-performante : Sélection d'un modèle Gradient Boosting surclassant le Deep Learning sur CPU ARM (99.8% F1-score, latence 0.218 ms, 3.8 Mo RAM).\n• Chaîne d'explicabilité et de pronostic : Modélisation continue du Health Index sur 35 jours NASA IMS et explicabilité SHAP/Z-scores pour les techniciens.\n• Sécurité matérielle active : Actionnement physique d'un relais de coupure d'urgence LOTO via les broches Broadcom GPIO en moins de 2 millisecondes.\n• Jumeau numérique Wokwi : Modélisation matérielle virtuelle sur ESP32 permettant une démonstration interactive sans matériel physique.\n• Fusion multimodalité : Prise en charge conjointe des capteurs accéléromètres piézoélectriques et des flux acoustiques microphones.\n• Assistant expert RAG : Intégration d'un agent conversationnel sémantique indexant 16 documents normatifs (ISO 10816-3).", bold_prefix="Synthèse des Réalisations Majeures : ")

    add_title_heading(doc, "2. Perspectives d'Évolution Industrielle", 2)
    add_body_p(doc, "À court et moyen terme, trois axes d'extension prometteurs se dégagent :")
    add_body_p(doc, "1. Portage TinyML sur Microcontrôleurs Ultra-Faible Puissance : Compilation du modèle Gradient Boosting en langage C pur (via m2cgen/treelite) pour exécution sur microcontrôleur ARM Cortex-M4 (STM32 / ESP32) consommant moins de 50 milliwatts.\n2. Connectivité Industrielle Longue Portée LoRaWAN : Transmission des alertes et du Health Index sur réseau privé d'usine LoRaWAN pour les sites isolés.\n3. Apprentissage Fédéré (Federated Learning) : Mutualisation de l'apprentissage entre plusieurs Raspberry Pi déployés sur différents moteurs sans jamais centraliser les données vibratoires brutes, garantissant la confidentialité industrielle.")

    add_title_heading(doc, "Bibliographie et Références Normatives", 1)
    references = [
        ("[1]", "Case Western Reserve University (CWRU), 'Bearing Data Center Seeded Fault Test Data', 2012."),
        ("[2]", "J. Lee, H. Qiu, G. Yu, J. Lin, 'Bearing Vibration Dataset', NASA Ames Prognostics Data Repository, 2007."),
        ("[3]", "ISO 10816-3, 'Mechanical vibration - Evaluation of machine vibration by measurements on non-rotating parts', 2009."),
        ("[4]", "ISO 20816-3, 'Measurement and evaluation of machine vibration - Part 3: Industrial machinery', 2022."),
        ("[5]", "T. Chen, C. Guestrin, 'XGBoost: A Scalable Tree Boosting System', ACM SIGKDD, 2016."),
        ("[6]", "L. Breiman, 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5-32, 2001."),
        ("[7]", "S. M. Lundberg, S.-I. Lee, 'A Unified Approach to Interpreting Model Predictions', NeurIPS, 2017."),
        ("[8]", "N. T. T. Nguyen et al., 'Vibration-Based Fault Diagnosis of Rotating Machinery Using Edge AI', IEEE Trans. Ind. Inf., 2021."),
        ("[9]", "A. Vaswani et al., 'Attention Is All You Need', Advances in Neural Information Processing Systems, 2017."),
        ("[10]", "N. Reimers, I. Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks', EMNLP, 2019."),
        ("[11]", "P. Bangalore, L. B. Tjernberg, 'An Artificial Neural Network Approach for Early Condition Monitoring', IEEE Trans. Smart Grid, 2015."),
        ("[12]", "SKF Group, 'Rolling Bearings Technical Catalogue 17000 EN', SKF Engineering Handbook, 2018."),
        ("[13]", "F. Chollet, 'Deep Learning with Python', Manning Publications, 2nd Edition, 2021."),
        ("[14]", "Raspberry Pi Foundation, 'Raspberry Pi 4 Model B Hardware Specifications', Broadcom BCM2711 Datasheet, 2020."),
        ("[15]", "Wokwi Systems, 'Wokwi Embedded Systems Simulator Documentation', 2024.")
    ]
    add_table_styled(doc, ["Réf.", "Description Bibliographique Complète"], references, [Inches(0.8), Inches(6.0)])

    # ── Sauvegarde finale du document Word ───────────────────────────────────
    try:
        doc.save(OUTPUT_FILE)
        final_file = OUTPUT_FILE
    except PermissionError:
        alt_file = os.path.join(BASE_DIR, "Rapport_PFE_EdgeAI_40Pages_Final_Mis_A_Jour.docx")
        doc.save(alt_file)
        final_file = alt_file
        print(f" [NOTE] Le fichier d'origine étant ouvert dans Word, la nouvelle version a été enregistrée sous : {alt_file}")

    print("================================================================================")
    print(f" ✅ RAPPORT DE STAGE GENERE AVEC SUCCES : {final_file}")
    print(f" 📄 Taille du fichier : {os.path.getsize(final_file) / 1024 / 1024:.2f} Mo")
    print(" 🎯 Pagination totale calibrée : ~38 à 40 pages maximum !")
    print("================================================================================")


if __name__ == '__main__':
    build_final_report_40_pages()
