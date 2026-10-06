import pandas as pd

# Define sheets and their columns exactly as requested in the document
sheets = {
    "1_Sources": ["Référence", "Métadonnées", "DOI", "Type de publication", "Évaluation par les pairs", "Lien officiel", "Sous-thème associé"],
    "2_Datasets": ["Référence", "Dataset", "Cas industriel", "Signal", "Variables", "Fréquence", "Labels", "Taille", "Conditions", "Tâche", "Avantages", "Limites", "Data leakage", "Edge", "XAI", "Robustesse", "[n]"],
    "3_Pretraitement": ["Référence", "Dataset", "Signal", "Nettoyage", "Normalisation", "Fenêtre", "Recouvrement", "Segmentation", "Features temporelles", "Features statistiques", "Features fréquentielles", "Signal brut", "Réduction", "Prévention fuite", "Impact", "Limites", "[n]"],
    "4_Modeles": ["Réf.", "Année", "Dataset", "Tâche", "Supervision", "Entrée", "Modèle", "Hyperparamètres", "Accuracy", "Precision", "Recall", "F1", "AUC", "Taille", "Paramètres", "Explicabilité", "Avantages", "Limites", "[n]"],
    "5_Deploiement_Edge": ["Réf.", "Cas", "Modèle", "Matériel", "Version", "RAM", "OS", "Runtime", "Format", "Entraînement", "Inférence", "Entrée", "Batch", "Optimisation", "Quantification", "Logs", "Code", "Limites", "[n]"],
    "6_Benchmark": ["Réf.", "Matériel", "Modèle", "Entrée", "Inférences", "Warm-up", "Outil", "Lat. moy.", "Médiane", "Max", "P95/P99", "Écart-type", "RAM", "CPU", "Taille", "Débit", "Énergie", "Métriques ML", "Limites", "[n]"],
    "7_Robustesse": ["Réf.", "Dataset", "Modèle", "Perturbation", "Niveau", "Référence", "Perf. initiale", "Perf. perturbée", "Perte abs.", "Perte rel.", "Recall", "Faux négatifs", "Mitigation", "Domain shift", "Limites", "[n]"],
    "8_XAI": ["Réf.", "Dataset", "Modèle", "Méthode XAI", "Intrinsèque/post-hoc", "Globale/locale", "Agnostique/spécifique", "Unité", "Feature", "Fenêtre", "Temps", "Fréquence", "Fidélité", "Stabilité", "Validation humaine", "Interprétation", "Limites", "[n]"],
    "9_RAG": ["Réf.", "Domaine", "Type", "Corpus", "Documents", "Chunking", "Embeddings", "Base", "Retrieval", "Reranking", "Agent", "Entrées ML", "Entrées XAI", "Sortie", "Citations", "Faithfulness", "Groundedness", "Hallucinations", "Validation", "Limites", "[n]"],
    "10_Gaps": ["Code", "Sous-thème", "Gap observé", "Références", "Nombre de travaux", "Importance", "Conséquence", "Réponse proposée", "Limite", "G1"],
    "11_Gaps_Contributions": ["Gap confirmé", "Preuve bibliographique", "Contribution envisagée", "Expérimentation", "Métriques", "Limite reconnue"],
    "12_References_IEEE": ["Réf.", "Citation IEEE"],
    "13_Fiches_Synthese": ["Sous-thème", "Nombre de publications analysées", "Approches dominantes", "Meilleurs résultats", "Résultats non comparables", "Convergences", "Contradictions", "Informations souvent absentes", "Limites communes", "Gap potentiel", "Preuves du gap", "Conséquence pour le projet", "Décision méthodologique", "Résultat retenu"],
    "14_Resultats_Globaux": ["Axe", "Résultat principal", "Approche dominante", "Limite principale", "Gap confirmé", "Décision pour le projet"]
}

# Create Excel file
with pd.ExcelWriter("Etat_de_l_art_Bibliographie.xlsx", engine="openpyxl") as writer:
    for sheet_name, columns in sheets.items():
        df = pd.DataFrame(columns=columns)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Excel file 'Etat_de_l_art_Bibliographie.xlsx' created successfully.")
