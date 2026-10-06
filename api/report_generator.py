"""
api/report_generator.py
------------------------
Générateur de Rapports de Maintenance PDF pour l'analyse Edge AI & RAG.
Utilise ReportLab pour produire un document PDF professionnel 1-page.
"""

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_pdf_report(prediction_title="Anomaly Detected (Bague Interne)", confidence=99.5, latency_ms=0.22, rag_text=""):
    """
    Génère un flux d'octets PDF contenant le rapport de diagnostic de maintenance.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Couleurs personnalisées
    NAVY = colors.HexColor('#0F172A')
    BLUE = colors.HexColor('#2563EB')
    RED = colors.HexColor('#DC2626')
    GREEN = colors.HexColor('#16A34A')
    GRAY_BG = colors.HexColor('#F8FAFC')
    TEXT_DARK = colors.HexColor('#334155')

    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=NAVY,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=BLUE,
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK
    )

    elements = []

    # 1. En-tête du Rapport
    elements.append(Paragraph("RAPPORT DE DIAGNOSTIC - EDGE AI & MAINTENANCE 4.0", title_style))
    now_str = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    elements.append(Paragraph(f"Généré le : {now_str} | Système : CWRU Bearing Condition Monitoring | Unité : Moteur 01 (Drive End)", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=15))

    # 2. Tableau résumé du Diagnostic Edge AI
    is_anomaly = "Anomaly" in prediction_title or "Défaut" in prediction_title or "Bague" in prediction_title or "Bille" in prediction_title
    status_color = RED if is_anomaly else GREEN
    status_text = f"<b>{prediction_title.upper()}</b>"

    diag_table_data = [
        [
            Paragraph("<b>Modèle d'Inférence :</b>", body_style),
            Paragraph("Gradient Boosting (Optimisé Edge)", body_style),
            Paragraph("<b>Latence d'Inférence :</b>", body_style),
            Paragraph(f"{latency_ms} ms", body_style)
        ],
        [
            Paragraph("<b>Résultat Verdict :</b>", body_style),
            Paragraph(f"<font color='{status_color.hexval()}'>{status_text}</font>", body_style),
            Paragraph("<b>Confiance du Modèle :</b>", body_style),
            Paragraph(f"{confidence}%", body_style)
        ],
        [
            Paragraph("<b>Capteur d'acquisition :</b>", body_style),
            Paragraph("Accéléromètre 12 kHz (Drive End)", body_style),
            Paragraph("<b>Fréquence d'Échantillonnage :</b>", body_style),
            Paragraph("12 000 Hz", body_style)
        ]
    ]

    t = Table(diag_table_data, colWidths=[130, 150, 130, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    # 3. Explication Technique & Diagnostic RAG
    elements.append(Paragraph("1. Analyse Sémantique & Diagnostic Explicatif (RAG)", section_style))
    
    clean_rag = rag_text.replace('#', '').strip() if rag_text else "Aucun diagnostic complémentaire requis. Le système fonctionne dans ses paramètres spectraux normaux."
    elements.append(Paragraph(clean_rag, body_style))
    elements.append(Spacer(1, 15))

    # 4. Plan d'Action Recommandé pour l'Équipe de Maintenance
    elements.append(Paragraph("2. Recommandations & Plan d'Action Opérationnel", section_style))
    
    if is_anomaly:
        recs = [
            "<b>[Urgence Élevée]</b> Arrêter le moteur lors de la prochaine fenêtre de maintenance planifiée.",
            "<b>[Inspection Visuelle]</b> Démonter le roulement côté entraînement (Drive End, Modèle SKF 6205-2RS).",
            "<b>[Contrôle Vibratoire]</b> Vérifier si des pics caractéristiques aux fréquences BPFI/BPFO persistent après graissage.",
            "<b>[Remplacement]</b> Prévoir le remplacement préventif de la bague/du roulement pour éviter le grippage total."
        ]
    else:
        recs = [
            "<b>[Statut Normal]</b> Aucune action corrective immédiate n'est requise.",
            "<b>[Routine]</b> Poursuivre le suivi vibratoire continu en temps réel.",
            "<b>[Maintenance Préventive]</b> Vérifier la lubrification standard lors du prochain cycle trimestriel."
        ]

    rec_table_data = [[Paragraph(f"• {r}", body_style)] for r in recs]
    rec_table = Table(rec_table_data, colWidths=[540])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF2F2') if is_anomaly else colors.HexColor('#F0FDF4')),
        ('BOX', (0, 0), (-1, -1), 1, RED if is_anomaly else GREEN),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(rec_table)
    elements.append(Spacer(1, 20))

    # 5. Pied de Page
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    footer_text = "Projet Stage Edge AI & Maintenance Prédictive | Certifié par le Système de Surveillance Autonome sur Raspberry Pi"
    elements.append(Paragraph(f"<font color='#94A3B8' size=8>{footer_text}</font>", body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
