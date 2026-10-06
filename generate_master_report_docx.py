"""
generate_master_report_docx.py
------------------------------
Script Maître de Génération du Rapport de Stage de Fin d'Études d'Ingénieur (> 40 pages).
Assemble l'ensemble des modules, applique la charte graphique académique,
intègre les 11 figures et 16 tableaux, et génère le fichier .docx final.
"""

import os
import sys
import docx

# Ajouter le répertoire racine au sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from report_builder.styles import setup_document_styles
from report_builder.front_matter import (
    add_title_page, add_acknowledgements, add_abstract,
    add_table_of_contents, add_lists_and_acronyms
)
from report_builder.intro_chap1_2 import (
    add_introduction, add_chapter_1, add_chapter_2
)
from report_builder.chap3_4_5 import (
    add_chapter_3, add_chapter_4, add_chapter_5
)
from report_builder.chap6_7_8_9 import (
    add_chapter_6, add_chapter_7, add_chapter_8, add_chapter_9
)
from report_builder.back_matter import (
    add_conclusion, add_bibliography, add_annexes
)

OUTPUT_FILE = os.path.join(BASE_DIR, "Rapport_de_Stage_EdgeAI_Raspberry_Complet.docx")

def build_complete_report():
    print("================================================================================")
    print("   DÉMARRAGE DE LA GÉNÉRATION DU RAPPORT DE STAGE D'INGÉNIEUR (> 40 PAGES)")
    print("================================================================================")
    
    doc = docx.Document()
    
    # 1. Configuration des styles et marges
    print("-> [1/6] Configuration des styles, marges A4 et en-têtes...")
    setup_document_styles(doc)
    
    # 2. Sections liminaires (Front Matter)
    print("-> [2/6] Génération de la page de garde, remerciements, résumés, sommaire et glossaire...")
    add_title_page(doc)
    add_acknowledgements(doc)
    add_abstract(doc)
    add_table_of_contents(doc)
    add_lists_and_acronyms(doc)
    
    # 3. Introduction et Chapitres 1 & 2 (Contexte et État de l'art Q1)
    print("-> [3/6] Rédaction de l'Introduction Générale, Chapitre 1 et Chapitre 2...")
    add_introduction(doc)
    add_chapter_1(doc)
    add_chapter_2(doc)
    
    # 4. Chapitres 3, 4 & 5 (Features, Modèles IA, Benchmark Edge Raspberry Pi)
    print("-> [4/6] Rédaction des Chapitres 3, 4 et 5 (Signal, IA, Benchmark Edge)...")
    add_chapter_3(doc)
    add_chapter_4(doc)
    add_chapter_5(doc)
    
    # 5. Chapitres 6, 7, 8 & 9 (XAI, RAG, Full-Stack Dashboard, Cas Pédagogique)
    print("-> [5/6] Rédaction des Chapitres 6, 7, 8 et 9 (XAI, RAG, Dashboard, TP Ingénieur)...")
    add_chapter_6(doc)
    add_chapter_7(doc)
    add_chapter_8(doc)
    add_chapter_9(doc)
    
    # 6. Conclusion Générale, Références IEEE & Annexes
    print("-> [6/6] Rédaction de la Conclusion Générale, Références IEEE et Annexes...")
    add_conclusion(doc)
    add_bibliography(doc)
    add_annexes(doc)
    
    # Sauvegarde du document Word
    print(f"\n-> Enregistrement du document final dans : {OUTPUT_FILE} ...")
    doc.save(OUTPUT_FILE)
    print(f"[SUCCÈS] Document généré et sauvegardé avec succès !")
    
    # Audit des statistiques du document
    verify_document_statistics(doc)

def verify_document_statistics(doc):
    print("\n================================================================================")
    print("   AUDIT ET VÉRIFICATION STATISTIQUE DU RAPPORT GÉNÉRÉ")
    print("================================================================================")
    
    total_paragraphs = len(doc.paragraphs)
    total_tables = len(doc.tables)
    
    total_words = 0
    for p in doc.paragraphs:
        total_words += len(p.text.split())
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    total_words += len(p.text.split())
                    
    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    
    # Estimation réaliste du nombre de pages sous Word :
    # Un document académique avec 11 figures pleines pages/demi-pages, 16 tableaux riches,
    # sauts de page avant chaque chapitre, interligne 1.15 et marges 2.5cm
    # compte environ 280 à 320 mots par page moyenne.
    # 11 figures représentent environ 6 à 8 pages équivalentes.
    # 16 tableaux représentent environ 7 à 9 pages équivalentes.
    # Les pages liminaires (Garde, Remerciements, Résumé, Sommaire, Listes, Acronymes) occupent 7 pages dédiées.
    # Le texte seul (~14 000 mots) représente ~30 à 35 pages.
    estimated_pages = 7 + int(total_words / 450) + int(11 * 0.6) + int(total_tables * 0.45)
    
    print(f"• Nombre total de paragraphes rédigés : {total_paragraphs}")
    print(f"• Nombre total de tableaux stylisés insérés : {total_tables}")
    print(f"• Nombre total de mots : {total_words:,} mots")
    print(f"• Taille du fichier .docx généré : {file_size_kb:.1f} KB")
    print(f"• Estimation minimale du nombre de pages sous Microsoft Word : {estimated_pages} pages")
    print("================================================================================")
    
    if estimated_pages >= 40:
        print(f"[CONFORME] L'exigence de volume (minimum 40 pages) est pleinement satisfaite ({estimated_pages} pages estimées) !")
    else:
        print(f"[ATTENTION] Le volume estimé est de {estimated_pages} pages.")

if __name__ == '__main__':
    build_complete_report()
