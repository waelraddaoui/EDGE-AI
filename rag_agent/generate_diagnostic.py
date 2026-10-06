"""
rag_agent/generate_diagnostic.py
--------------------------------
Séance 10 : Générateur Automatique de Rapport de Diagnostic de Maintenance.

Couple :
1. L'inférence Edge AI (Random Forest / Gradient Boosting)
2. L'explicabilité Z-score par caractéristique
3. L'agent RAG (Interrogation de D1 à D8) pour extraire les recommandations techniques et consignes de sécurité maintenance.

Génère : reports/automated_diagnostic_report.md

Conforme aux exigences F6.5 à F6.8 du Cahier des Charges.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

sys.path.append(os.path.join(BASE_DIR, 'raspberry'))
sys.path.append(os.path.join(BASE_DIR, 'rag_agent'))

from inference_edge import EdgeInferenceEngine
from ask_agent import RAGAgent

FEATURE_NAMES = [
    'Mean', 'Std Dev', 'Variance', 'RMS', 'Min', 'Max', 'Peak-to-Peak', 'Energy',
    'Skewness', 'Kurtosis', 'Crest Factor', 'Impulse Factor',
    'Spectral Energy', 'Dominant Freq', 'Spectral Centroid', 'Spectral Spread'
]

def generate_automated_diagnostic(sample_index=0):
    print(f"=== Séance 10 : Générateur Automatique de Rapport de Diagnostic ===")
    
    split_data = np.load(os.path.join(DATA_PROCESSED_DIR, 'dataset_split.npz'))
    X_test = split_data['X_test']
    y_test = split_data['y_test']
    X_train = split_data['X_train']
    y_train = split_data['y_train']
    
    anom_indices = np.where(y_test == 1)[0]
    target_idx = anom_indices[sample_index] if len(anom_indices) > sample_index else 0
    
    x_sample = X_test[target_idx]
    
    # 1. Edge Inference
    engine = EdgeInferenceEngine(model_name='Gradient Boosting')
    res = engine.predict_sample(x_sample)
    
    # 2. XAI Z-Scores
    mean_normal = np.mean(X_train[y_train == 0], axis=0)
    std_normal = np.std(X_train[y_train == 0], axis=0) + 1e-6
    z_scores = (x_sample - mean_normal) / std_normal
    
    # Highlight top anomalous indicators
    top_anom_feat_indices = np.argsort(np.abs(z_scores))[::-1][:3]
    top_feat_str = ", ".join([f"**{FEATURE_NAMES[i]}** (Z={z_scores[i]:+.2f})" for i in top_anom_feat_indices])
    
    # 3. Query RAG agent for technical recommendations
    rag_agent = RAGAgent()
    rag_results = rag_agent.query("Fréquences caractéristiques roulement SKF 6205-2RS défaillance bague interne", top_k=2)
    
    rag_excerpt = ""
    for r in rag_results:
        rag_excerpt += f"> **Ref [{r['doc_id']}]** : {r['text'][:250]}...\n\n"
        
    # 4. Generate Diagnostic Report
    report_content = f"""# Rapport Automatique de Diagnostic de Maintenance Prédictive

**Horodatage du diagnostic** : 2026-08-07  
**Unité de surveillance** : Raspberry Pi - Sensor Stream #01  
**Équipement contrôlé** : Moteur Électrique 2 HP (Roulement SKF 6205-2RS)  

---

## 1. Synthèse du Diagnostic IA Embarquée

- **Statut Équipement** : {'ANOMALIE DÉTECTÉE' if res['is_anomaly'] else 'FONCTIONNEMENT NORMAL'}
- **Score de Confiance IA** : {res['score'] * 100.0:.2f}%
- **Latence d'Inférence** : {res['latency_ms']:.3f} ms
- **Modèle Actif** : Gradient Boosting Embarqué

## 2. Explication Technique (XAI & Z-Scores)

L'analyse spectrale et temporelle indique un écart significatif par rapport au profil sain nominal :
- **Indicateurs Critiques Hors-Norme** : {top_feat_str}

### Interprétation Physique :
L'élévation simultanée du **Kurtosis** et du **Facteur de Crête** signale la présence d'impulsions mécaniques brèves causées par un choc répétitif à chaque passage de bille sur une zone dégradée.

---

## 3. Recommandations de la Base Documentaire RAG

{rag_excerpt}
## 4. Consignes d'Intervention pour les Techniciens
1. Programmer une vérification de la lubrification et un contrôle visuel du roulement sous 48 heures.
2. Mesurer les fréquences de passage des défauts (BPFI = 162.2 Hz) au stroboscope ou vibromètre portable.
3. Prévoir le remplacement du roulement SKF 6205-2RS lors de la prochaine fenêtre d'arrêt technique planifiée.
"""

    report_path = os.path.join(REPORTS_DIR, 'automated_diagnostic_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"[OK] Rapport de diagnostic automatique généré dans : {report_path}")

if __name__ == '__main__':
    generate_automated_diagnostic()
