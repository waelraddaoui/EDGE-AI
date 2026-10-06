"""
run_all_tests.py
----------------
Script de Validation Global Tout-en-Un.
Exécute l'ensemble de la chaîne du projet pour vérifier le bon fonctionnement de tous les modules.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_command_step(step_num, title, command):
    print(f"\n==========================================================")
    print(f"  [Étape {step_num}/5] {title}")
    print(f"==========================================================")
    cmd = [sys.executable] + command.split()
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if res.returncode == 0:
        print(res.stdout)
        print(f"[OK] Étape {step_num} validée avec succès.")
    else:
        print(f"[ERREUR] Étape {step_num} a échoué :")
        print(res.stderr)
        sys.exit(1)

def main():
    print("==========================================================")
    print("   [START] TEST ET VALIDATION GLOBALE DU PROJET EDGE AI & RAG")
    print("==========================================================")
    
    run_command_step(1, "Data Preparation", "src/data_preparation.py")
    run_command_step(2, "Feature Extraction (16 Features FFT)", "src/feature_extraction.py")
    run_command_step(3, "Entrainement et Evaluation des Modeles IA", "src/train_models.py")
    run_command_step(4, "Benchmark Edge AI et Explicabilite XAI", "raspberry/benchmark_edge.py")
    run_command_step(5, "Agent RAG et Rapport de Diagnostic Automatique", "rag_agent/generate_diagnostic.py")

    print("\n==========================================================")
    print("   [SUCCESS] TOUTES LES ETAPES ONT ETE VALIDEES AVEC SUCCES !")
    print("==========================================================")

if __name__ == '__main__':
    main()
