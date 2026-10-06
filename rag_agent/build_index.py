"""
rag_agent/build_index.py
------------------------
Séance 10 (Mise à jour) : Construction de l'Index Sémantique RAG (D1 à D8).

Indexe les documents en utilisant des plongements denses (Sentence-Transformers)
pour une compréhension sémantique de l'état de l'art.
"""

import os
import glob
import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'rag_agent', 'documents')
INDEX_PATH = os.path.join(BASE_DIR, 'rag_agent', 'rag_index.joblib')

def build_rag_index():
    print("=== Construction de l'Index RAG Sémantique (Sentence-Transformers) ===")
    
    doc_files = sorted(glob.glob(os.path.join(DOCS_DIR, '*.md')))
    if not doc_files:
        raise FileNotFoundError(f"Aucun document .md trouvé dans {DOCS_DIR}")
        
    chunks = []
    
    for file_path in doc_files:
        doc_id = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Découpage par sections (par titres ##)
        sections = content.split('\n## ')
        title = sections[0].strip('# ').split('\n')[0]
        
        for i, sec in enumerate(sections):
            sec_text = sec if i == 0 else "## " + sec
            sec_text = sec_text.strip()
            if len(sec_text) > 30:
                chunks.append({
                    'doc_id': doc_id,
                    'title': title,
                    'chunk_id': f"{doc_id}_sec_{i}",
                    'text': sec_text
                })
                
    df_chunks = pd.DataFrame(chunks)
    
    print("Chargement du modèle SentenceTransformer (cela peut prendre quelques instants lors du premier téléchargement)...")
    # Modèle léger, rapide et multilingue (parfait pour le français)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    print("Génération des embeddings denses pour les documents...")
    embeddings = model.encode(df_chunks['text'].tolist(), show_progress_bar=True)
    
    index_data = {
        'df_chunks': df_chunks,
        'model_name': 'paraphrase-multilingual-MiniLM-L12-v2',
        'embeddings': embeddings
    }
    
    joblib.dump(index_data, INDEX_PATH)
    print(f"[OK] Indexation sémantique de {len(df_chunks)} sections de documents terminée.")
    print(f"[OK] Index sauvegardé dans : {INDEX_PATH}")

if __name__ == '__main__':
    build_rag_index()
