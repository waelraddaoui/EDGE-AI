"""
generate_pptx.py
----------------
Génère la présentation PowerPoint (.pptx) de checkpoint pour l'encadrant(e).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Thème de couleurs professionnel
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    LIGHT_BG = RGBColor(248, 250, 252)
    DARK_TEXT = RGBColor(30, 41, 59)
    GRAY_TEXT = RGBColor(100, 116, 139)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 232, 240)
    GREEN = RGBColor(22, 163, 74)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="STAGE DE FIN D'ÉTUDES"):
        # Fond clair
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()

        # En-tête bleu top line
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = BLUE
        top_line.line.fill.background()

        # Titre
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # SLIDE 1 : Titre
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    txBox = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "POINT D'AVANCEMENT & CHECKPOINT DU PROJET"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p2 = tf.add_paragraph()
    p2.text = "Développement d'un Système Autonome de Détection et Diagnostic d'Anomalies (Edge AI & RAG)"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Application à la maintenance prédictive des roulements à billes (Dataset CWRU)"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(10)

    # SLIDE 2 : Contexte & Objectifs
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Contexte Industrial & Objectifs du Projet")

    def add_card(slide, left, top, width, height, title, items):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        txBox = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = txBox.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE
        p_t.space_after = Pt(10)

        for item in items:
            p_i = tf.add_paragraph()
            p_i.text = f"• {item}"
            p_i.font.size = Pt(12)
            p_i.font.color.rgb = DARK_TEXT
            p_i.space_before = Pt(4)

    add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), "Problématique Industrielle", [
        "Les pannes non planifiées de roulements sur moteurs critiques coûtent très cher.",
        "Le streaming continu de signaux bruts vers le Cloud pose des problèmes de coût de bande passante et de confidentialité.",
        "Besoin d'une solution autonome directement implantable au pied de la machine."
    ])

    add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2), "Objectifs Réalisés", [
        "Déploiement Edge AI ultra-rapide (< 1 ms) pour une décision en temps réel.",
        "Extraction de 16 indicateurs physiques temporels et spectraux (FFT).",
        "Intégration d'un Assistant RAG d'explicabilité (Sentence-Transformers).",
        "Génération automatique de Rapports de Maintenance PDF."
    ])

    # SLIDE 3 : Dataset CWRU & Perturbations
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Dataset CWRU & Simulation de Perturbations Réelles")

    add_card(slide3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), "Composition du Jeu de Données CWRU", [
        "Roulement SKF 6205-2RS côté entraînement (Drive End).",
        "Vitesse de rotation : 1797 RPM (~29.95 Hz).",
        "Fréquence d'échantillonnage : 12 000 Hz.",
        "10 Scénarios : 1 Normal + 9 Anomalies (Bague Interne BPFI, Bague Externe BPFO, Bille BSF avec 3 sévérités).",
        "1 200 000 points temporels de vibrations."
    ])

    add_card(slide3, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2), "Bruitage & Perturbations Hybrides", [
        "Bruit Gaussien Blanc (SNR 12-15 dB) pour simuler l'environnement moteur.",
        "Dérive basse fréquence pour simuler l'échauffement thermique du capteur.",
        "Pertes de paquets / zéros (2%) pour simuler des micro-coupures IoT.",
        "Spikes impulsionnels pour simuler les parasites électriques d'usine."
    ])

    # SLIDE 4 : Traitement du Signal (Feature Engineering)
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Traitement du Signal & Extraction de Caractéristiques")

    add_card(slide4, Inches(0.8), Inches(1.5), Inches(11.6), Inches(5.2), "Découpage en Fenêtres & 16 Indicateurs Physiques", [
        "Fenêtrage glissant de 1024 points (~85 ms) avec 50% de chevauchement (2320 fenêtres d'apprentissage).",
        "12 Indicateurs Temporels & Statistiques : Moyenne, RMS, Variance, Min, Max, Peak-to-Peak, Énergie, Skewness, Kurtosis (chocs), Crest Factor, Impulse Factor.",
        "4 Indicateurs Fréquentiels FFT : Énergie Spectrale, Fréquence Dominante (Hz), Centre de Gravité Spectral (Centroid), Étalement Spectral.",
        "Standardisation StandardScaler (μ=0, σ=1) pour équilibrer les échelles de grandeurs."
    ])

    # SLIDE 5 : Benchmark des 5 Modèles IA
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Benchmark des Modèles IA & Modèle Vainqueur")

    add_card(slide5, Inches(0.8), Inches(1.5), Inches(11.6), Inches(5.2), "Résultats du Benchmark d'Inférence Edge AI", [
        " Gradient Boosting (Gagnant) : Latence 0.22 ms | Taille 30.6 KB | F1-Score 97.8% 🏆",
        " 1D-CNN Compact PyTorch : Latence 0.54 ms | Taille 11.3 KB | F1-Score 96.7%",
        " Random Forest Légers : Latence 1.22 ms | Taille 20.1 KB | F1-Score 99.4%",
        " Autoencodeur PyTorch : Latence 0.85 ms | Taille 15.2 KB | F1-Score 92.1%",
        " Isolation Forest : Latence 1.21 ms | Taille 573.3 KB | F1-Score 94.7%",
        "Conclusion : Le Gradient Boosting offre le meilleur compromis Vitesse/Taille/Précision pour le Raspberry Pi."
    ])

    # SLIDE 6 : Explicabilité XAI & Agent RAG
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Explicabilité XAI & Agent IA RAG Maintenance")

    add_card(slide6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), "Explicabilité XAI (Feature Importance)", [
        "Calcul en direct des contributions de chaque caractéristique physique.",
        "Visualisation sur le Dashboard (ex: 44.5% Kurtosis, 28.2% FFT, 14.8% RMS).",
        "Prouve au technicien la cause physique exacte de la prédiction."
    ])

    add_card(slide6, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2), "Agent RAG (Sentence-Transformers)", [
        "Indexation sémantique de 11 documents de référence (D1 à D11).",
        "Synthèse automatique d'un Plan d'Action de Maintenance.",
        "Gestion des salutations et des questions techniques ouvertes du technicien.",
        "Procédure de réparation détaillée étape par étape (Sécurité LOTO, graissage, chauffe par induction)."
    ])

    # SLIDE 7 : Architecture Logicielle & Dashboard React
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Architecture Logicielle & Interface Web (Dashboard)")

    add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), "Backend API (FastAPI)", [
        "FastAPI asynchrone ultra-rapide.",
        "Endpoints : /api/predict/simulate, /api/signal/sample, /api/chat, /api/report/pdf.",
        "Calcul du spectre FFT en direct (0-500 Hz)."
    ])

    add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2), "Frontend Dashboard (React + Vite)", [
        "Interface web moderne sombre type Salle de Contrôle Usine 4.0.",
        "Graphique du signal vibratoire temporel en temps réel.",
        "Graphique d'Analyse Spectrale FFT avec pics BPFI/BPFO/BSF.",
        "Barres de progression XAI & Chatbot RAG interactif."
    ])

    # SLIDE 8 : Génération de Rapports PDF
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Génération Automatique de Rapports PDF")

    add_card(slide8, Inches(0.8), Inches(1.5), Inches(11.6), Inches(5.2), "Rapport de Diagnostic de Maintenance Officiel", [
        "Module de génération PDF développé avec ReportLab (api/report_generator.py).",
        "Téléchargement en 1 clic depuis le Dashboard React (Bouton PDF Rapport).",
        "Contenu du rapport : Horodatage précis, métriques du modèle Gradient Boosting, score de confiance, explication physique RAG et tableau encadré des consignes de sécurité LOTO et de maintenance préventive."
    ])

    # SLIDE 9 : État d'Avancement & Prochaine Étape
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. État d'Avancement & Prochaine Étape (Matériel Réel)")

    add_card(slide9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), "Ce qui est 100% Terminé (Logiciel & IA)", [
        "Prétraitement et fenêtrage des données CWRU.",
        "Entraînement et benchmark des 5 modèles IA.",
        "Système RAG et explicabilité XAI.",
        "API FastAPI, Dashboard React et Rapports PDF."
    ])

    add_card(slide9, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2), "Prochaine Étape (Connexion Matérielle)", [
        "Raccordement physique de l'accéléromètre (ADXL335 / MPU6050).",
        "Connexion du convertisseur ADC (ADS1115) au Raspberry Pi.",
        "Déploiement de l'API sur le Raspberry Pi OS 64-bit pour validation sur banc de test."
    ])

    # SLIDE 10 : Conclusion
    slide10 = prs.slides.add_slide(blank_layout)
    bg10 = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = NAVY
    bg10.line.fill.background()

    txBox = slide10.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(11.3), Inches(3.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "MERCI POUR VOTRE ATTENTION"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Avez-vous des questions ou des remarques sur cet avancement ?"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(15)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Presentation_Stage_Checkpoint.pptx")
    prs.save(output_path)
    print(f"[OK] Présentation créée avec succès : {output_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()
