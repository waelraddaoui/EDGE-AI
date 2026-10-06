"""
rag_agent/ask_agent.py
----------------------
Séance 10 : Moteur de Recherche Documentaire RAG & Assistant Virtuel Maintenance.

Interroge la base documentaire (D1 à D8) via l'index TF-IDF / Cosine Similarity,
extrait les passages les plus pertinents et retourne une réponse structurée avec citations.

Conforme aux exigences F6.3 et F6.4 du Cahier des Charges.
"""

import os
import sys
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, 'rag_agent', 'rag_index.joblib')

class RAGAgent:
    def __init__(self):
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"Index RAG introuvable à {INDEX_PATH}. Exécutez rag_agent/build_index.py.")
            
        index_data = joblib.load(INDEX_PATH)
        self.df_chunks = index_data['df_chunks']
        self.vectorizer = index_data['vectorizer']
        self.tfidf_matrix = index_data['tfidf_matrix']

    def query(self, user_query, top_k=3):
        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.05:
                row = self.df_chunks.iloc[idx]
                results.append({
                    'doc_id': row['doc_id'],
                    'title': row['title'],
                    'chunk_id': row['chunk_id'],
                    'score': round(score, 4),
                    'text': row['text']
                })
                
        return results

    def answer_question(self, question):
        results = self.query(question, top_k=3)
        
        print(f"\n========================================================")
        print(f"  QUESTION : {question}")
        print(f"========================================================")
        
        if not results:
            print("Aucun document pertinent trouvé dans la base documentaire.")
            return
            
        print(f"\n--- Extraits de Référence Trouvés ({len(results)} sources) ---")
        for i, res in enumerate(results, 1):
            print(f"\n[Source {i}] Document : {res['doc_id']} | Score de pertinence : {res['score']}")
            print(f"Extrait :")
            print(res['text'][:350] + ("..." if len(res['text']) > 350 else ""))
            
        return results

def interactive_mode():
    agent = RAGAgent()
    print("=== Agent RAG Maintenance & Edge AI (Tapez 'exit' pour quitter) ===")
    
    test_queries = [
        "Quelle est la latence du Gradient Boosting sur Raspberry Pi ?",
        "Quelles sont les fréquences caractéristiques du roulement SKF 6205-2RS ?",
        "Comment le Kurtosis permet-il de détecter un défaut de bague interne ?"
    ]
    
    for q in test_queries:
        agent.answer_question(q)

if __name__ == '__main__':
    interactive_mode()
