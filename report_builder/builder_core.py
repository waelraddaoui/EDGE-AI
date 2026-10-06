"""
generate_pfe_report_40p_master.py
---------------------------------
Script Maître de Génération du Rapport de Stage de Fin d'Études (PFE)
Structure exacte en 5 Grands Chapitres conforme aux standards académiques universitaires (ESPRIM).
Calibré pour une pagination cible de 38 à 40 pages maximum avec 12 figures intégrées,
10 tableaux stylisés, formules mathématiques et cahier de tests complet.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
OUTPUT_FILE = os.path.join(BASE_DIR, "Rapport_PFE_EdgeAI_40Pages_Final.docx")

def setup_document_styles(doc=None):
    """Configuration helper for document styles."""
    pass


# Charte Graphique "Executive Academic"
COLOR_NAVY = RGBColor(27, 54, 93)       # #1B365D - Titres principaux, en-têtes
COLOR_STEEL = RGBColor(46, 107, 158)    # #2E6B9E - Titres secondaires
COLOR_CHARCOAL = RGBColor(45, 55, 72)   # #2D3748 - Sous-titres
COLOR_BODY = RGBColor(34, 34, 34)       # #222222 - Texte principal
COLOR_MUTED = RGBColor(100, 116, 139)   # #64748B - Métadonnées / Légendes
COLOR_GREEN = RGBColor(16, 185, 129)    # #10B981 - Succès / Champion
COLOR_RED = RGBColor(220, 38, 38)       # #DC2626 - Alerte

HEX_NAVY = "1B365D"
HEX_STEEL = "2E6B9E"
HEX_LIGHT_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_title_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    
    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run.font.size = Pt(17)
        run.font.color.rgb = COLOR_NAVY
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(5)
        run.font.size = Pt(13.5)
        run.font.color.rgb = COLOR_STEEL
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = COLOR_CHARCOAL
        
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY
    return p

def add_callout(doc, title, text, box_type="info"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    border_color = HEX_NAVY if box_type == "info" else ("10B981" if box_type == "success" else "DC2626")
    set_cell_background(cell, HEX_LIGHT_BG)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    r_t = p.add_run(f"📌 {title}\n")
    r_t.bold = True
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(10)
    r_t.font.color.rgb = COLOR_NAVY if box_type == "info" else (COLOR_GREEN if box_type == "success" else COLOR_RED)
    
    r_b = p.add_run(text)
    r_b.font.name = 'Calibri'
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = COLOR_BODY
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_table_styled(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # En-tête
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if col_widths and i < len(col_widths):
            cell.width = col_widths[i]
            
    # Lignes
    for r_idx, row_data in enumerate(data):
        row = tbl.rows[r_idx + 1]
        bg = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=110, right=110)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_BODY
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
                
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(6)

def add_figure_image(doc, img_filename, caption, width=Inches(5.6)):
    img_path = os.path.join(FIGURES_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(f"Figure — {caption}")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED
    else:
        print(f"[WARN] Image introuvable : {img_path}")

print("Module de génération de rapport 40p prêt.")
