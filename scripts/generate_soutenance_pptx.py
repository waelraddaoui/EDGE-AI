import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Colors
DARK_BLUE   = RGBColor(0x00, 0x2B, 0x55)
LIGHT_BLUE  = RGBColor(0x00, 0x78, 0xD7)
ORANGE      = RGBColor(0xFF, 0x6B, 0x00)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GREEN       = RGBColor(0x10, 0xA3, 0x5A)
RED_COLOR   = RGBColor(0xE5, 0x2B, 0x2B)

W = Inches(13.33)  # Widescreen 16:9
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]

def bg(slide, color):
    bg_fill = slide.background.fill
    bg_fill.solid()
    bg_fill.fore_color.rgb = color

def box(slide, left, top, width, height, fill_color=None, line_color=None, line_width=Pt(0)):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.line.width = line_width
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width if line_width else Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def txt(slide, text, left, top, width, height,
        size=20, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
        italic=False, wrap=True):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return txb

def header_bar(slide, title_text, subtitle_text=''):
    box(slide, 0, 0, W, Inches(1.3), fill_color=DARK_BLUE)
    txt(slide, title_text, Inches(0.4), Inches(0.12), Inches(12.5), Inches(0.65),
        size=28, bold=True, color=WHITE)
    if subtitle_text:
        txt(slide, subtitle_text, Inches(0.4), Inches(0.78), Inches(12.5), Inches(0.4),
            size=14, color=RGBColor(0xAA, 0xCC, 0xFF))
    box(slide, 0, Inches(1.25), W, Inches(0.06), fill_color=ORANGE)

def badge(slide, text, left, top, width=Inches(2.5), height=Inches(0.45), color=GREEN):
    box(slide, left, top, width, height, fill_color=color)
    txt(slide, text, left, top+Inches(0.03), width, height-Inches(0.06),
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

def footer(slide, slide_num, total=12):
    box(slide, 0, H-Inches(0.35), W, Inches(0.35), fill_color=DARK_BLUE)
    txt(slide, 'Soutenance de Stage PFE — Edge AI & IoT Predictive Maintenance — ESPRIM 2026',
        Inches(0.3), H-Inches(0.32), Inches(10), Inches(0.3),
        size=9, color=RGBColor(0xAA, 0xCC, 0xFF))
    txt(slide, f'{slide_num} / {total}', Inches(12.4), H-Inches(0.32), Inches(0.7), Inches(0.3),
        size=9, color=WHITE, align=PP_ALIGN.RIGHT)

# ── SLIDE 1 : TITRE ──
s1 = prs.slides.add_slide(BLANK)
bg(s1, DARK_BLUE)
box(s1, 0, 0, W, Inches(0.12), fill_color=ORANGE)
txt(s1, 'EDGE AI & MAINTENANCE PRÉDICTIVE IoT', Inches(0.5), Inches(1.0), Inches(12.3), Inches(1.2),
    size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s1, 'Surveillance Intelligente et Détection d\'Anomalies sur Roulements Industriels', Inches(0.5), Inches(2.2), Inches(12.3), Inches(0.6),
    size=22, bold=False, color=ORANGE, align=PP_ALIGN.CENTER)
box(s1, Inches(2.5), Inches(2.95), Inches(8.3), Inches(0.04), fill_color=LIGHT_BLUE)
txt(s1, 'TinyML sur ESP32 · Gradient Boosting · Explicabilité XAI · Agent RAG · Dashboard Temps Réel',
    Inches(0.5), Inches(3.2), Inches(12.3), Inches(0.5),
    size=15, italic=True, color=RGBColor(0xCC, 0xE4, 0xFF), align=PP_ALIGN.CENTER)

info = [('Étudiant', 'Soutenance Stage PFE'),
        ('Établissement', 'ESPRIM - Monastir'),
        ('Encadrante', 'Mme Amina Rouis'),
        ('Spécialité', 'Edge AI & IoT')]
for i, (label, val) in enumerate(info):
    x = Inches(0.6) + i * Inches(3.1)
    box(s1, x, Inches(4.5), Inches(2.9), Inches(1.0),
        fill_color=RGBColor(0x00, 0x38, 0x6A), line_color=LIGHT_BLUE, line_width=Pt(1))
    txt(s1, label, x+Inches(0.1), Inches(4.6), Inches(2.7), Inches(0.3),
        size=11, color=RGBColor(0x88, 0xBB, 0xFF))
    txt(s1, val, x+Inches(0.1), Inches(4.95), Inches(2.7), Inches(0.4),
        size=13, bold=True, color=WHITE)
box(s1, 0, H-Inches(0.35), W, Inches(0.35), fill_color=ORANGE)

# ── SLIDE 2 : CONTEXTE & PROBLEMATIQUE ──
s2 = prs.slides.add_slide(BLANK)
bg(s2, WHITE)
header_bar(s2, '1. Contexte & Problématique Industrielle', 'Transition de la maintenance corrective vers la maintenance prédictive 4.0')
box(s2, Inches(0.5), Inches(1.6), Inches(5.8), Inches(5.2),
    fill_color=RGBColor(0xFF, 0xF2, 0xF0), line_color=RED_COLOR, line_width=Pt(2))
txt(s2, '❌ Approches Conventionnelles', Inches(0.7), Inches(1.75), Inches(5.4), Inches(0.4),
    size=18, bold=True, color=RED_COLOR)
p_items = [
    '• Pannes de roulements non planifiées (arrêts d\'usines).',
    '• Maintenance corrective coûteuse (jusqu\'à 10x plus cher).',
    '• Envoi massif des données brutes vers le Cloud :',
    '   - Latence réseau inacceptable (> 500 ms).',
    '   - Coûts de bande passante et stockage prohibitifs.',
    '   - Dépendance totale à la connexion Internet.'
]
for i, p in enumerate(p_items):
    txt(s2, p, Inches(0.7), Inches(2.4)+i*Inches(0.65), Inches(5.4), Inches(0.55),
        size=13, color=RGBColor(0x55, 0x11, 0x11))

box(s2, Inches(6.9), Inches(1.6), Inches(5.9), Inches(5.2),
    fill_color=RGBColor(0xF0, 0xFF, 0xF4), line_color=GREEN, line_width=Pt(2))
txt(s2, '✅ Solution Développée : Edge AI & IoT', Inches(7.1), Inches(1.75), Inches(5.5), Inches(0.4),
    size=18, bold=True, color=GREEN)
s_items = [
    '• Traitement directement sur le nœud embarqué (Edge).',
    '• Inférence locale en ultra-basse latence (< 2 ms).',
    '• TinyML sur microcontrôleur ESP32 à coût dérisoire.',
    '• Coupure de sécurité automatique via actionneur MOSFET.',
    '• Explicabilité (XAI) pour assister les techniciens de terrain.',
    '• Agent RAG pour le diagnostic assisté par base documentaire.'
]
for i, s in enumerate(s_items):
    txt(s2, s, Inches(7.1), Inches(2.4)+i*Inches(0.65), Inches(5.5), Inches(0.55),
        size=13, color=RGBColor(0x00, 0x44, 0x15))
footer(s2, 2)

# ── SLIDE 3 : ARCHITECTURE GLOBALE ──
s3 = prs.slides.add_slide(BLANK)
bg(s3, WHITE)
header_bar(s3, '2. Architecture Globale du Système', 'Une chaîne complète intégrée de bout en bout')
layers = [
    ('NIVEAU 1 : CAPTEURS & EDGE', 'Accéléromètre MPU-6050 (12 kHz)\nDOIT ESP32 DevKit V1\nExtraction 16 features FFT en local\nTinyML C++ embarqué (0.02 ms)\nActionneur coupure MOSFET (GPIO 23)\nÉcran OLED SSD1306 (128x64)', ORANGE),
    ('NIVEAU 2 : PASSERELLE & ANALYSE', 'Serveur Edge Python / Raspberry Pi\nModèles Gradient Boosting & XGBoost\nBenchmark comparatif 5 architectures\nExplicabilité XAI (TreeSHAP)\nProtocole IoT MQTT & Télémétrie JSON', LIGHT_BLUE),
    ('NIVEAU 3 : SUPERVISION & IA', 'API REST FastAPI haute performance\nAgent RAG (MiniLM-L12 multilingue)\nBase de connaissances (16 docs ISO)\nDashboard Web interactif (React 19)\nGénération de rapports PDF officiels', GREEN)
]
for i, (title, body, col) in enumerate(layers):
    x = Inches(0.5) + i * Inches(4.2)
    box(s3, x, Inches(1.6), Inches(3.9), Inches(5.2),
        fill_color=RGBColor(0xF6, 0xFA, 0xFF), line_color=col, line_width=Pt(2))
    box(s3, x, Inches(1.6), Inches(3.9), Inches(0.6), fill_color=col)
    txt(s3, title, x+Inches(0.1), Inches(1.72), Inches(3.7), Inches(0.4),
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s3, body, x+Inches(0.2), Inches(2.4), Inches(3.5), Inches(4.2),
        size=13, color=DARK_BLUE, align=PP_ALIGN.LEFT)
footer(s3, 3)

# ── SLIDE 4 : DATASET & EXTRACTION DES 16 FEATURES ──
s4 = prs.slides.add_slide(BLANK)
bg(s4, WHITE)
header_bar(s4, '3. Prétraitement du Signal & Extraction des Caractéristiques', 'Du signal brut vibratoire aux signatures physiques de défaillance')
box(s4, Inches(0.5), Inches(1.6), Inches(4.2), Inches(5.2),
    fill_color=RGBColor(0xF0, 0xF4, 0xFF), line_color=LIGHT_BLUE, line_width=Pt(1.5))
txt(s4, '📊 Dataset de Référence CWRU', Inches(0.7), Inches(1.75), Inches(3.8), Inches(0.4),
    size=15, bold=True, color=DARK_BLUE)
c_text = [
    '• 1 200 000 points d\'accélération.',
    '• Fréquence d\'échantillonnage : 12 kHz.',
    '• 4 classes : Sain, Bague Interne (BPFI),',
    '  Bague Externe (BPFO), Bille (BSF).',
    '• Fenêtrage glissant : 1024 points (50% recouvrement).',
    '• 2 330 fenêtres extraites et normalisées (StandardScaler).'
]
for i, c in enumerate(c_text):
    txt(s4, c, Inches(0.7), Inches(2.4)+i*Inches(0.65), Inches(3.8), Inches(0.6),
        size=12, color=RGBColor(0x22, 0x22, 0x66))

box(s4, Inches(5.0), Inches(1.6), Inches(7.8), Inches(5.2),
    fill_color=RGBColor(0xFA, 0xFB, 0xFD), line_color=ORANGE, line_width=Pt(1.5))
txt(s4, '⚡ Les 16 Features Statistiques & Fréquentielles (FFT)', Inches(5.2), Inches(1.75), Inches(7.4), Inches(0.4),
    size=15, bold=True, color=ORANGE)
f_temp = "• Domaine Temporel : RMS, Variance, Écart-Type, Moyenne, Facteur de Crête, Kurtosis, Skewness, Min, Max, Peak-to-Peak, Énergie carrée."
f_freq = "• Domaine Fréquentiel : Énergie spectrale FFT, Fréquence dominante, Corrélations avec les fréquences caractéristiques de défaut (BPFO=107.4Hz, BPFI=162.2Hz, BSF=47.1Hz)."
txt(s4, f_temp, Inches(5.2), Inches(2.4), Inches(7.4), Inches(1.3), size=13, color=DARK_BLUE)
txt(s4, f_freq, Inches(5.2), Inches(3.8), Inches(7.4), Inches(1.3), size=13, color=DARK_BLUE)
badge(s4, 'Réduction de dimension : 1024 points bruts  ➔  16 variables clés ultra-légères',
      Inches(5.2), Inches(5.8), Inches(7.4), Inches(0.55), color=DARK_BLUE)
footer(s4, 4)

# ── SLIDE 5 : BENCHMARK COMPARATIF DES MODELES IA ──
s5 = prs.slides.add_slide(BLANK)
bg(s5, WHITE)
header_bar(s5, '4. Benchmark Comparatif des Modèles IA Edge', 'Évaluation rigoureuse sur banc d\'essai (Précision vs Ressources)')
headers = ['Modèle IA', 'F1-Score (Propre)', 'F1-Score (Bruité)', 'Latence (ms)', 'Taille Modèle', 'Empreinte RAM']
rows = [
    ('Gradient Boosting', '100 %', '100 % (après opt.)', '1.08 ms', '26.3 Ko', 'Faible'),
    ('Random Forest', '100 %', '99.6 %', '1.23 ms', '20.1 Ko', 'Très faible'),
    ('LightGBM', '100 %', '100 %', '1.54 ms', '23.4 Ko', 'Modérée'),
    ('Autoencodeur (PyTorch)', '99.5 %', '94.0 %', '0.19 ms', '4.6 Ko', '1.0 Mo'),
    ('1D-CNN Compact', '100 %', '90.7 %', '0.54 ms', '11.3 Ko', '0.24 Mo'),
    ('Isolation Forest', '100 %', '94.5 %', '1.14 ms', '573 Ko', '0.97 Mo')
]
widths = [Inches(3.2), Inches(2.0), Inches(2.0), Inches(1.8), Inches(1.8), Inches(1.8)]
x_start = Inches(0.4)
box(s5, x_start, Inches(1.6), sum(widths), Inches(0.5), fill_color=DARK_BLUE)
curr_x = x_start
for w, h in zip(widths, headers):
    txt(s5, h, curr_x+Inches(0.05), Inches(1.68), w-Inches(0.1), Inches(0.35),
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    curr_x += w

for r_idx, row in enumerate(rows):
    y = Inches(2.15) + r_idx * Inches(0.65)
    bg_row = RGBColor(0xFF, 0xF8, 0xEE) if r_idx == 0 else (RGBColor(0xF4, 0xF8, 0xFF) if r_idx % 2 == 1 else WHITE)
    box(s5, x_start, y, sum(widths), Inches(0.6), fill_color=bg_row, line_color=RGBColor(0xDD, 0xEE, 0xFF), line_width=Pt(0.5))
    curr_x = x_start
    for c_idx, (w, val) in enumerate(zip(widths, row)):
        col_c = ORANGE if (r_idx == 0 and c_idx == 0) else DARK_BLUE
        bld = True if (r_idx == 0 or c_idx == 0) else False
        txt(s5, val, curr_x+Inches(0.05), y+Inches(0.12), w-Inches(0.1), Inches(0.4),
            size=11, bold=bld, color=col_c, align=PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT)
        curr_x += w

box(s5, Inches(0.4), Inches(6.3), Inches(12.5), Inches(0.6), fill_color=RGBColor(0xE8, 0xF4, 0xFF), line_color=LIGHT_BLUE, line_width=Pt(1))
txt(s5, '🎯 Choix d\'implémentation : Le Gradient Boosting offre le compromis parfait entre précision (100%), compacité (26 Ko) et facilité de transpilation en C++ pur pour microcontrôleur.',
    Inches(0.6), Inches(6.38), Inches(12.1), Inches(0.5), size=12, bold=True, color=DARK_BLUE)
footer(s5, 5)

# ── SLIDE 6 : EXPLICABILITÉ XAI ──
s6 = prs.slides.add_slide(BLANK)
bg(s6, WHITE)
header_bar(s6, '5. Explicabilité de l\'IA (XAI) pour la Décision Industrielle', 'Rendre transparentes et justifiables les prédictions pour les opérateurs')
box(s6, Inches(0.5), Inches(1.6), Inches(5.8), Inches(5.2),
    fill_color=RGBColor(0xF9, 0xF6, 0xFF), line_color=RGBColor(0x6A, 0x1B, 0x9A), line_width=Pt(2))
txt(s6, '🔍 Approche TreeSHAP & Attribution', Inches(0.7), Inches(1.75), Inches(5.4), Inches(0.4),
    size=16, bold=True, color=RGBColor(0x4A, 0x14, 0x8C))
txt(s6, 'L\'algorithme SHAP calcule la contribution marginale de chaque caractéristique sur la décision finale :\n\n1. Kurtosis : Indicateur n°1 de choc mécanique (explique > 55% de la prédiction de panne).\n2. RMS : Indique la sévérité énergétique de la vibration.\n3. Pics Spectraux FFT : Confirment la cinématique interne du défaut.',
    Inches(0.7), Inches(2.4), Inches(5.4), Inches(4.2), size=13, color=DARK_BLUE)

box(s6, Inches(6.9), Inches(1.6), Inches(5.9), Inches(5.2),
    fill_color=RGBColor(0xF0, 0xFF, 0xF5), line_color=GREEN, line_width=Pt(2))
txt(s6, '⚙️ Diagnostic Physique Associé', Inches(7.1), Inches(1.75), Inches(5.5), Inches(0.4),
    size=16, bold=True, color=GREEN)
diag_phys = [
    '• BPFO (107.4 Hz) : Fissure sur bague externe.',
    '• BPFI (162.2 Hz) : Écaillage sur bague interne.',
    '• BSF (47.1 Hz) : Dégradation d\'une bille de roulement.',
    '• Kurtosis > 4.5 & RMS > 0.18g : Alarme rouge critique.',
    '• Indice de Santé (HI) calculé en continu de 0% à 100%.'
]
for i, d in enumerate(diag_phys):
    txt(s6, d, Inches(7.1), Inches(2.4)+i*Inches(0.7), Inches(5.5), Inches(0.6),
        size=13, bold=True if i == 4 else False, color=DARK_BLUE if i < 3 else (RED_COLOR if i == 3 else GREEN))
footer(s6, 6)

# ── SLIDE 7 : TINYML SUR ESP32 (HARDWARE) ──
s7 = prs.slides.add_slide(BLANK)
bg(s7, WHITE)
header_bar(s7, '6. Déploiement Matériel TinyML sur ESP32', 'Prototype autonome 100% temps réel et sans connexion Cloud')
cards = [
    ('Microcontrôleur DOIT ESP32', 'Xtensa Dual-Core 240 MHz\nFlash 4 Mo / SRAM 520 Ko\nTraitement local sans serveur'),
    ('Capteur MPU-6050 (GY-521)', 'Accéléromètre 3 axes (I2C)\nSDA: GPIO 21 / SCL: GPIO 22\nÉchantillonnage haute cadence'),
    ('Écran OLED SSD1306', 'Affichage 128x64 pixels\nJauge de santé dynamique\nAffichage RMS & Kurtosis'),
    ('Module Coupure MOSFET IRF520', 'Commande sur GPIO 23\nCoupure d\'urgence moteur (LOTO)\nSécurité machine proactive')
]
for i, (t_c, b_c) in enumerate(cards):
    col_i = i % 2
    row_i = i // 2
    x = Inches(0.5) + col_i * Inches(6.3)
    y = Inches(1.6) + row_i * Inches(2.4)
    box(s7, x, y, Inches(6.0), Inches(2.2), fill_color=RGBColor(0xF5, 0xF9, 0xFF), line_color=LIGHT_BLUE, line_width=Pt(1.5))
    txt(s7, t_c, x+Inches(0.2), y+Inches(0.15), Inches(5.6), Inches(0.4), size=14, bold=True, color=DARK_BLUE)
    txt(s7, b_c, x+Inches(0.2), y+Inches(0.65), Inches(5.6), Inches(1.4), size=12, color=RGBColor(0x33, 0x33, 0x66))

box(s7, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.5), fill_color=ORANGE)
txt(s7, '⚡ Modèle C++ pur transpilé (model_tinyml.h) : 30 arbres de décision exécutés en seulement 0.02 ms !',
    Inches(0.7), Inches(6.55), Inches(11.9), Inches(0.4), size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
footer(s7, 7)

# ── SLIDE 8 : AGENT RAG & RAPPORT DE DIAGNOSTIC ──
s8 = prs.slides.add_slide(BLANK)
bg(s8, WHITE)
header_bar(s8, '7. Agent IA / RAG & Assistant de Maintenance', 'Génération Augmentée par Récupération basée sur 16 documents techniques')
box(s8, Inches(0.5), Inches(1.6), Inches(6.0), Inches(5.2),
    fill_color=RGBColor(0xF4, 0xF8, 0xFF), line_color=LIGHT_BLUE, line_width=Pt(2))
txt(s8, '📚 Base Documentaire Technique', Inches(0.7), Inches(1.75), Inches(5.6), Inches(0.4),
    size=15, bold=True, color=DARK_BLUE)
rag_desc = [
    '• 16 documents normatifs et scientifiques indexés :',
    '  - Norme ISO 10816 (seuils de sévérité vibratoire).',
    '  - Fiches techniques cinématiques des roulements SKF.',
    '  - Guides de traitement du signal et détection de pannes.',
    '• Modèle d\'embedding multilingue performant :',
    '  sentence-transformers (MiniLM-L12).',
    '• Index vectoriel optimisé avec similarité cosinus.'
]
for i, rd in enumerate(rag_desc):
    txt(s8, rd, Inches(0.7), Inches(2.3)+i*Inches(0.55), Inches(5.6), Inches(0.5),
        size=12, color=DARK_BLUE)

box(s8, Inches(6.9), Inches(1.6), Inches(5.9), Inches(5.2),
    fill_color=RGBColor(0xF0, 0xFF, 0xF4), line_color=GREEN, line_width=Pt(2))
txt(s8, '🤖 Fonctionnalités de l\'Agent', Inches(7.1), Inches(1.75), Inches(5.5), Inches(0.4),
    size=15, bold=True, color=GREEN)
rag_f = [
    '• Chat interactif pour assister le technicien.',
    '• Analyse sémantique de la requête et contexte de panne.',
    '• Récupération précise des extraits documentaires pertinents.',
    '• Génération automatique d\'un rapport officiel de diagnostic (PDF / Markdown).',
    '• Recommandations d\'actions de maintenance corrective ciblées.'
]
for i, rf in enumerate(rag_f):
    txt(s8, rf, Inches(7.1), Inches(2.4)+i*Inches(0.68), Inches(5.5), Inches(0.6),
        size=12, color=RGBColor(0x00, 0x44, 0x15))
footer(s8, 8)

# ── SLIDE 9 : SUPERVISION DASHBOARD REACT & API FASTAPI ──
s9 = prs.slides.add_slide(BLANK)
bg(s9, WHITE)
header_bar(s9, '8. Dashboard Web Industriel & API REST', 'Interface de supervision temps réel moderne et réactive')
items_dash = [
    ('FastAPI Backend (Port 8000)', '• Endpoints REST haute performance.\n• Streaming télémétrique temps réel.\n• Documentation interactive OpenAPI / Swagger.', LIGHT_BLUE),
    ('Interface React 19 / Vite (Port 5173)', '• Graphiques vibratoires interactifs (Recharts).\n• Spectre FFT avec pics cinématiques en direct.\n• Jauge de santé machine et historique temporel.', GREEN),
    ('Streaming IoT & Alertes', '• Communication MQTT / Émulation bus local.\n• Déclenchement d\'alarmes sonores et visuelles.\n• Bouton d\'export PDF du rapport en 1 clic.', ORANGE)
]
for i, (title_d, text_d, col_d) in enumerate(items_dash):
    x = Inches(0.5) + i * Inches(4.2)
    box(s9, x, Inches(1.8), Inches(3.9), Inches(4.8), fill_color=RGBColor(0xFA, 0xFA, 0xFE), line_color=col_d, line_width=Pt(2))
    box(s9, x, Inches(1.8), Inches(3.9), Inches(0.6), fill_color=col_d)
    txt(s9, title_d, x+Inches(0.1), Inches(1.9), Inches(3.7), Inches(0.4), size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s9, text_d, x+Inches(0.2), Inches(2.6), Inches(3.5), Inches(3.8), size=13, color=DARK_BLUE)
footer(s9, 9)

# ── SLIDE 10 : VALIDATION & TESTS COMPLETS ──
s10 = prs.slides.add_slide(BLANK)
bg(s10, WHITE)
header_bar(s10, '9. Validation & Résultats des Tests', 'Un projet robuste, reproductible et validé à 100%')
tests = [
    ('Étape 1 : Préparation Dataset', 'Génération et split stratifié des signaux CWRU', '100% VALIDÉ'),
    ('Étape 2 : Extraction 16 Features', 'Calcul FFT, descripteurs temporels & scaler', '100% VALIDÉ'),
    ('Étape 3 : Entraînement 5 Modèles', 'Validation croisée & sauvegarde des poids IA', '100% VALIDÉ'),
    ('Étape 4 : Benchmark Edge & XAI', 'Mesure latence, RAM, TreeSHAP & profiler', '100% VALIDÉ'),
    ('Étape 5 : Agent RAG & Diagnostic', 'Indexation vectorielle et génération de rapport', '100% VALIDÉ'),
    ('Étape 6 : Firmware ESP32 TinyML', 'Inférence locale en C++, scanner I2C & OLED', '100% VALIDÉ')
]
for i, (t_title, t_desc, t_res) in enumerate(tests):
    y = Inches(1.6) + i * Inches(0.85)
    box(s10, Inches(0.5), y, Inches(12.3), Inches(0.75), fill_color=RGBColor(0xF6, 0xFB, 0xF7), line_color=GREEN, line_width=Pt(1))
    txt(s10, f'✅ {t_title}', Inches(0.7), y+Inches(0.15), Inches(4.5), Inches(0.45), size=14, bold=True, color=DARK_BLUE)
    txt(s10, t_desc, Inches(5.3), y+Inches(0.18), Inches(5.0), Inches(0.4), size=12, italic=True, color=RGBColor(0x55, 0x55, 0x55))
    badge(s10, t_res, Inches(10.5), y+Inches(0.15), Inches(2.1), Inches(0.45), color=GREEN)
footer(s10, 10)

# ── SLIDE 11 : BILAN PERSONNEL & PERSPECTIVES ──
s11 = prs.slides.add_slide(BLANK)
bg(s11, WHITE)
header_bar(s11, '10. Bilan du Stage & Perspectives d\'Évolution', 'Compétences acquises et ouvertures pour le futur')
box(s11, Inches(0.5), Inches(1.6), Inches(5.8), Inches(5.2),
    fill_color=RGBColor(0xF0, 0xF7, 0xFF), line_color=LIGHT_BLUE, line_width=Pt(2))
txt(s11, '🎓 Compétences Acquises & Apports', Inches(0.7), Inches(1.75), Inches(5.4), Inches(0.4),
    size=16, bold=True, color=DARK_BLUE)
c_acq = [
    '• Maîtrise de la chaîne complète Edge AI industrielle.',
    '• Traitement du signal vibratoire (FFT, filtrage, kurtosis).',
    '• Programmation bas-niveau en C++ embarqué (TinyML ESP32).',
    '• Développement Fullstack moderne (FastAPI, React 19).',
    '• Conception d\'agents IA spécialisés avec architecture RAG.',
    '• Rigueur méthodologique, documentation et gestion de projet.'
]
for i, ca in enumerate(c_acq):
    txt(s11, ca, Inches(0.7), Inches(2.4)+i*Inches(0.65), Inches(5.4), Inches(0.55),
        size=12, color=DARK_BLUE)

box(s11, Inches(6.9), Inches(1.6), Inches(5.9), Inches(5.2),
    fill_color=RGBColor(0xFF, 0xF9, 0xF2), line_color=ORANGE, line_width=Pt(2))
txt(s11, '🚀 Perspectives d\'Évolution', Inches(7.1), Inches(1.75), Inches(5.5), Inches(0.4),
    size=16, bold=True, color=ORANGE)
persp = [
    '• Déploiement multi-capteurs (acoustique + température + courant).',
    '• Intégration de la prédiction de Durée de Vie Résiduelle (RUL).',
    '• Déploiement en usine avec bus industriel (Modbus TCP / OPC-UA).',
    '• Optimisation matérielle via quantification INT8 avancée.',
    '• Valorisation académique sous forme de publication scientifique.'
]
for i, pe in enumerate(persp):
    txt(s11, pe, Inches(7.1), Inches(2.4)+i*Inches(0.65), Inches(5.5), Inches(0.55),
        size=12, color=DARK_BLUE)
footer(s11, 11)

# ── SLIDE 12 : CONCLUSION & QUESTIONS ──
s12 = prs.slides.add_slide(BLANK)
bg(s12, DARK_BLUE)
box(s12, 0, 0, W, Inches(0.12), fill_color=ORANGE)
txt(s12, 'MERCI POUR VOTRE ATTENTION', Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.2),
    size=46, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s12, 'Place aux Questions & Échanges avec la Professeure', Inches(0.5), Inches(2.8), Inches(12.3), Inches(0.8),
    size=24, color=ORANGE, align=PP_ALIGN.CENTER)
box(s12, Inches(2.5), Inches(3.8), Inches(8.3), Inches(0.04), fill_color=LIGHT_BLUE)
txt(s12, 'Démonstration interactive en direct prête à être présentée :\nDashboard Web (localhost:5173) · API REST (localhost:8000) · Prototype ESP32',
    Inches(0.5), Inches(4.2), Inches(12.3), Inches(1.0),
    size=16, italic=True, color=RGBColor(0xCC, 0xE4, 0xFF), align=PP_ALIGN.CENTER)
box(s12, 0, H-Inches(0.35), W, Inches(0.35), fill_color=ORANGE)

output_file = os.path.join(BASE_DIR, 'Soutenance_Stage_PFE_EdgeAI_ESPRIM_2026.pptx')
prs.save(output_file)
print(f"SUCCESS: {output_file}")
