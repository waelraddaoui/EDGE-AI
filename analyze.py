import pandas as pd
import sys

def analyze_excel(filepath):
    try:
        xls = pd.ExcelFile(filepath)
        sheets = xls.sheet_names
        
        total_rows = 0
        missing_count = 0
        sheets_info = []
        
        for sheet in sheets:
            df = pd.read_excel(filepath, sheet_name=sheet)
            rows = len(df)
            total_rows += rows
            
            # Count occurrences of "Non rapporté"
            missing_in_sheet = df.astype(str).apply(lambda x: x.str.contains("Non rapport", case=False, na=False)).sum().sum()
            missing_count += missing_in_sheet
            
            sheets_info.append(f"  - {sheet}: {rows} lignes")
            
        return {
            "sheets": sheets,
            "total_rows_across_sheets": total_rows,
            "missing_keyword_count": missing_count,
            "sheets_info": "\n".join(sheets_info)
        }
    except Exception as e:
        return {"error": str(e)}

file_user = r'c:\Users\marie\Desktop\Projets\Stage antigravity\etat_de_l_art_complet_rempli.xlsx'
file_agent = r'c:\Users\marie\Desktop\Projets\Stage antigravity\Etat_de_l_art_Bibliographie.xlsx'

res_user = analyze_excel(file_user)
res_agent = analyze_excel(file_agent)

def print_res(name, res):
    print(f"=== {name} ===")
    if "error" in res:
        print("Erreur:", res["error"])
        return
    print(f"Nombre de feuilles: {len(res['sheets'])}")
    print(f"Total des lignes de données (toutes feuilles confondues): {res['total_rows_across_sheets']}")
    print(f"Mentions 'Non rapporté dans la publication': {res['missing_keyword_count']}")
    print(res['sheets_info'])
    print()

print_res("Fichier de l'étudiant (etat_de_l_art_complet_rempli.xlsx)", res_user)
print_res("Fichier généré par l'Agent (Etat_de_l_art_Bibliographie.xlsx)", res_agent)
