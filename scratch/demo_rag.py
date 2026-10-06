"""
scratch/demo_rag.py
-------------------
Démonstration interactive en direct de l'Agent IA / RAG et du Générateur de Diagnostic.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'rag_agent'))

from ask_agent import RAGAgent
from generate_diagnostic import generate_automated_diagnostic

def run_demo():
    print("==================================================================")
    print("   [RAG] DEMONSTRATION INTERACTIVE : AGENT IA / RAG & DIAGNOSTIC")
    print("==================================================================\n")
    
    agent = RAGAgent()
    
    questions = [
        "Quel est le meilleur modèle Edge AI pour Raspberry Pi et pourquoi ?",
        "Quelles sont les fréquences caractéristiques BPFI et BPFO du roulement SKF 6205-2RS ?",
        "Pourquoi le Kurtosis et le Crest Factor augmentent-ils lors d'une anomalie ?"
    ]
    
    for idx, q in enumerate(questions, 1):
        print(f"\n--- [Test {idx}/3] Interrogation RAG ---")
        agent.answer_question(q)
        
    print("\n\n==================================================================")
    print("   [DIAGNOSTIC] GENERATION EN DIRECT D'UN RAPPORT AUTOMATIQUE")
    print("==================================================================\n")
    
    generate_automated_diagnostic(sample_index=0)

if __name__ == '__main__':
    run_demo()
