import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────────────────────
# 1. GENERER LE FICHIER PPTX IMPORTABLE DANS CANVA
# ─────────────────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Couleurs
DARK_BLUE = RGBColor(0x00, 0x2B, 0x55)
LIGHT_BLUE = RGBColor(0x00, 0x78, 0xD7)
ORANGE = RGBColor(0xFF, 0x6B, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x10, 0xA3, 0x5A)
RED = RGBColor(0xDC, 0x26, 0x26)

bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = WHITE

# Helper Box
def add_box(s, l, t, w, h, fill=None, line=None, lw=Pt(1)):
    shape = s.shapes.add_shape(1, l, t, w, h)
    shape.line.width = lw
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
    else:
        shape.line.fill.background()
    return shape

def add_txt(s, text, l, t, w, h, size=14, bold=False, color=DARK_BLUE, align=PP_ALIGN.LEFT):
    txb = s.shapes.add_textbox(l, t, w, h)
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txb

# Top accent bar
add_box(slide, Inches(0.5), Inches(0.4), Inches(12.33), Inches(0.04), fill=LIGHT_BLUE)
add_txt(slide, "03", Inches(0.5), Inches(0.5), Inches(1.5), Inches(0.4), size=14, bold=True, color=LIGHT_BLUE)
add_txt(slide, "Données CWRU, 4 Classes & Gestion du Déséquilibre", Inches(0.5), Inches(0.85), Inches(12.3), Inches(0.6), size=26, bold=True, color=DARK_BLUE)

# COLONNE 1 : Le Dataset & 4 Classes
add_box(slide, Inches(0.5), Inches(1.6), Inches(3.8), Inches(5.2), fill=RGBColor(0xF5, 0xF9, 0xFF), line=LIGHT_BLUE, lw=Pt(1.5))
add_txt(slide, "1,2 M", Inches(0.8), Inches(1.8), Inches(3.2), Inches(0.8), size=44, bold=True, color=LIGHT_BLUE)
add_txt(slide, "points vibratoires · 12 kHz", Inches(0.8), Inches(2.6), Inches(3.2), Inches(0.4), size=14, bold=True, color=DARK_BLUE)

c1_text = (
    "4 Classes Physiques :\n\n"
    "• Normal (Machine saine)\n"
    "• Bague interne (BPFI - 162.2 Hz)\n"
    "• Bague externe (BPFO - 107.4 Hz)\n"
    "• Élément roulant (BSF - 47.1 Hz)\n\n"
    "2 330 fenêtres extraites de 1024 points (FFT + 16 features)."
)
add_txt(slide, c1_text, Inches(0.8), Inches(3.1), Inches(3.2), Inches(3.4), size=12, color=DARK_BLUE)

# COLONNE 2 : Le Défi du Déséquilibre
add_box(slide, Inches(4.7), Inches(1.6), Inches(3.8), Inches(5.2), fill=RGBColor(0xFF, 0xF5, 0xF5), line=RED, lw=Pt(1.5))
add_txt(slide, "⚠️ PROBLÉMATIQUE", Inches(5.0), Inches(1.8), Inches(3.2), Inches(0.4), size=14, bold=True, color=RED)
add_txt(slide, "Déséquilibre des Classes", Inches(5.0), Inches(2.2), Inches(3.2), Inches(0.5), size=20, bold=True, color=DARK_BLUE)

c2_text = (
    "En milieu industriel réel :\n\n"
    "• La machine est saine > 95% du temps.\n"
    "• Les pannes sont critiques mais rares.\n"
    "• Les données de défauts sont minoritaires.\n\n"
    "❌ Risque majeur :\n"
    "Un modèle standard apprendrait à prédire toujours 'Sain' avec 95% d'accuracy trompeuse tout en ignorant la panne fatale !"
)
add_txt(slide, c2_text, Inches(5.0), Inches(2.8), Inches(3.2), Inches(3.7), size=12, color=RGBColor(0x44, 0x11, 0x11))

# COLONNE 3 : Solutions Appliquées
add_box(slide, Inches(8.9), Inches(1.6), Inches(3.9), Inches(5.2), fill=RGBColor(0xF0, 0xFF, 0xF4), line=GREEN, lw=Pt(1.5))
add_txt(slide, "✅ SOLUTIONS APPLIQUÉES", Inches(9.2), Inches(1.8), Inches(3.3), Inches(0.4), size=14, bold=True, color=GREEN)
add_txt(slide, "Équilibrage & Robustesse", Inches(9.2), Inches(2.2), Inches(3.3), Inches(0.5), size=20, bold=True, color=DARK_BLUE)

c3_text = (
    "1. Fenêtrage glissant avec overlap 50% :\n"
    "   Multiplication des fenêtres de 1024 points (stride 512) sur les signaux de pannes.\n\n"
    "2. Split Stratifié (80% / 10% / 10%) :\n"
    "   Préservation stricte du ratio de chaque classe dans Train, Validation et Test.\n\n"
    "3. Data Augmentation Hybride :\n"
    "   Injection de bruit gaussien et dérives pour enrichir les pannes.\n\n"
    "4. Évaluation par F1-Score (100%) :\n"
    "   Métrique insensible au déséquilibre (vs simple Accuracy)."
)
add_txt(slide, c3_text, Inches(9.2), Inches(2.8), Inches(3.3), Inches(3.7), size=11.5, color=RGBColor(0x00, 0x44, 0x15))

# Footer
add_txt(slide, "EDGE AI · MAINTENANCE PRÉDICTIVE IoT", Inches(0.5), Inches(7.0), Inches(5.0), Inches(0.3), size=9, color=RGBColor(0x88, 0x88, 0x88))
add_txt(slide, "03", Inches(12.0), Inches(7.0), Inches(0.8), Inches(0.3), size=9, color=RGBColor(0x88, 0x88, 0x88), align=PP_ALIGN.RIGHT)

pptx_out = os.path.join(BASE_DIR, 'Diapositive_Donnees_Desequilibre.pptx')
prs.save(pptx_out)
print(f"PPTX créé : {pptx_out}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. GENERER UNE IMAGE HAUTE RESOLUTION PNG POUR CANVA (1920 x 1080)
# ─────────────────────────────────────────────────────────────────────────────
w_px, h_px = 1920, 1080
img = Image.new('RGB', (w_px, h_px), color='#FFFFFF')
draw = ImageDraw.Draw(img)

# Ligne d'accent bleue en haut
draw.rectangle([(80, 50), (1840, 56)], fill='#0078D7')

try:
    font_cat = ImageFont.truetype('arial.ttf', 24)
    font_title = ImageFont.truetype('arialbd.ttf', 44)
    font_big = ImageFont.truetype('arialbd.ttf', 72)
    font_h2 = ImageFont.truetype('arialbd.ttf', 26)
    font_body = ImageFont.truetype('arial.ttf', 20)
    font_body_bold = ImageFont.truetype('arialbd.ttf', 20)
    font_footer = ImageFont.truetype('arial.ttf', 16)
except:
    font_cat = font_title = font_big = font_h2 = font_body = font_body_bold = font_footer = ImageFont.load_default()

draw.text((80, 68), "03", fill='#0078D7', font=font_cat)
draw.text((80, 105), "Données CWRU, 4 Classes & Traitement du Déséquilibre", fill='#002B55', font=font_title)

# COLONNE 1
draw.rounded_rectangle([(80, 200), (620, 960)], radius=16, fill='#F5F9FF', outline='#0078D7', width=3)
draw.text((120, 240), "1,2 M", fill='#0078D7', font=font_big)
draw.text((120, 330), "points vibratoires · 12 kHz", fill='#002B55', font=font_h2)
c1_p = [
    "4 Classes Physiques :",
    "",
    "• Normal (Machine saine)",
    "• Bague interne (BPFI - 162.2 Hz)",
    "• Bague externe (BPFO - 107.4 Hz)",
    "• Élément roulant (BSF - 47.1 Hz)",
    "",
    "Échantillonnage :",
    "2 330 fenêtres temporelles",
    "de 1024 points (FFT + 16 features)",
    "sur banc d'essais CWRU."
]
y_c1 = 390
for line in c1_p:
    draw.text((120, y_c1), line, fill='#002B55', font=font_body_bold if ("Classes" in line or "Échantillonnage" in line) else font_body)
    y_c1 += 34

# COLONNE 2
draw.rounded_rectangle([(670, 200), (1210, 960)], radius=16, fill='#FFF5F5', outline='#DC2626', width=3)
draw.text((710, 240), "⚠️ LE DÉFI INDUSTRIEL", fill='#DC2626', font=font_h2)
draw.text((710, 280), "Déséquilibre des Classes", fill='#002B55', font=font_title)
c2_p = [
    "En fonctionnement réel :",
    "• La machine est saine > 95% du temps.",
    "• Les défauts sont rares et critiques.",
    "• Les données d'anomalies sont",
    "  fortement sous-représentées.",
    "",
    "❌ Risque majeur :",
    "Un algorithme naïf prédirait",
    "toujours 'Sain' avec 95% d'accuracy,",
    "mais raterait 100% des pannes !",
    "",
    "L'Accuracy est donc trompeuse."
]
y_c2 = 360
for line in c2_p:
    draw.text((710, y_c2), line, fill='#551111', font=font_body_bold if ("réel" in line or "Risque" in line) else font_body)
    y_c2 += 34

# COLONNE 3
draw.rounded_rectangle([(1260, 200), (1840, 960)], radius=16, fill='#F0FFF4', outline='#10A35A', width=3)
draw.text((1300, 240), "✅ SOLUTIONS APPLIQUÉES", fill='#10A35A', font=font_h2)
draw.text((1300, 280), "Méthodes de Correction", fill='#002B55', font=font_title)
c3_p = [
    "1. Fenêtrage glissant (Overlap 50%) :",
    "   Multiplication des fenêtres (stride 512)",
    "   sur les signaux de pannes.",
    "",
    "2. Split Stratifié (80/10/10) :",
    "   Maintien strict des proportions de chaque",
    "   classe dans Train, Val et Test.",
    "",
    "3. Data Augmentation Hybride :",
    "   Injection de bruit gaussien et perturbations",
    "   pour renforcer les classes minoritaires.",
    "",
    "4. Validation F1-Score (100%) :",
    "   Métrique insensible au déséquilibre."
]
y_c3 = 350
for line in c3_p:
    draw.text((1300, y_c3), line, fill='#004415', font=font_body_bold if ("1." in line or "2." in line or "3." in line or "4." in line) else font_body)
    y_c3 += 33

# Footer
draw.text((80, 1020), "EDGE AI · MAINTENANCE PRÉDICTIVE IoT", fill='#888888', font=font_footer)
draw.text((1800, 1020), "03", fill='#888888', font=font_footer)

png_out = os.path.join(BASE_DIR, 'Diapositive_Donnees_Desequilibre.png')
img.save(png_out, quality=95)
print(f"IMAGE PNG créée : {png_out}")
