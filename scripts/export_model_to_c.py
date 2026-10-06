import os
import joblib
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "gradient_boosting.joblib")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.joblib")
OUTPUT_HEADER = os.path.join(BASE_DIR, "esp32_firmware", "model_tinyml.h")

def tree_to_cpp(node):
    if "leaf" in node:
        return f"return {float(node['leaf']):.6f}f;"
    
    feat = int(node["split"].replace("f", ""))
    cond = float(node["split_condition"])
    
    # Children
    yes_child = None
    no_child = None
    for c in node["children"]:
        if c["nodeid"] == node["yes"]:
            yes_child = c
        elif c["nodeid"] == node["no"]:
            no_child = c
            
    yes_code = tree_to_cpp(yes_child)
    no_code = tree_to_cpp(no_child)
    
    return f"if (x[{feat}] < {cond:.6f}f) {{ {yes_code} }} else {{ {no_code} }}"

def export():
    print(f"Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    
    booster = model.get_booster()
    tree_dumps = booster.get_dump(dump_format="json")
    print(f"Extracted {len(tree_dumps)} trees from trained Gradient Boosting model.")
    
    lines = []
    lines.append("// =============================================================================")
    lines.append("// MODEL_TINYML.H - EXPORT C++ DU VRAI MODELE GRADIENT BOOSTING (XGBOOST)")
    lines.append("// Entraîné sur le dataset vibratoire CWRU (16 caractéristiques physiques)")
    lines.append("// Déployable 100% en local dans la mémoire Flash de l'ESP32")
    lines.append("// =============================================================================")
    lines.append("#ifndef MODEL_TINYML_H")
    lines.append("#define MODEL_TINYML_H")
    lines.append("")
    lines.append("#include <math.h>")
    lines.append("")
    lines.append("// 1. Paramètres de normalisation StandardScaler (16 features)")
    
    mean_str = ", ".join([f"{float(m):.6f}f" for m in scaler.mean_])
    scale_str = ", ".join([f"{float(s):.6f}f" for s in scaler.scale_])
    
    lines.append(f"const float SCALER_MEAN[16] = {{ {mean_str} }};")
    lines.append(f"const float SCALER_SCALE[16] = {{ {scale_str} }};")
    lines.append("")
    
    # Trees functions
    for i, t_json in enumerate(tree_dumps):
        node = json.loads(t_json)
        body = tree_to_cpp(node)
        lines.append(f"static inline float tree_{i}(const float* x) {{ {body} }}")
    
    lines.append("")
    lines.append("// 2. Fonction principale d'inférence TinyML")
    lines.append("struct PredictionResult {")
    lines.append("    int predicted_class;   // 0 = SAIN (Normal), 1 = DEFAUT (Bearing Fault)")
    lines.append("    float fault_prob;      // Probabilité de panne (0.0 à 1.0)")
    lines.append("    float health_index;    // Indice de Santé (0.0% à 100.0%)")
    lines.append("};")
    lines.append("")
    lines.append("inline PredictionResult predict_bearing_health(const float raw_features[16]) {")
    lines.append("    // A. Normalisation StandardScaler")
    lines.append("    float x[16];")
    lines.append("    for (int i = 0; i < 16; i++) {")
    lines.append("        x[i] = (raw_features[i] - SCALER_MEAN[i]) / SCALER_SCALE[i];")
    lines.append("    }")
    lines.append("")
    lines.append("    // B. Sommation des 30 arbres du Gradient Boosting")
    lines.append("    float raw_score = 0.0f;")
    for i in range(len(tree_dumps)):
        lines.append(f"    raw_score += tree_{i}(x);")
        
    lines.append("")
    lines.append("    // C. Fonction Sigmoïde logistique")
    lines.append("    float prob = 1.0f / (1.0f + expf(-raw_score));")
    lines.append("")
    lines.append("    PredictionResult res;")
    lines.append("    res.fault_prob = prob;")
    lines.append("    res.predicted_class = (prob >= 0.50f) ? 1 : 0;")
    lines.append("    res.health_index = (1.0f - prob) * 100.0f;")
    lines.append("    return res;")
    lines.append("}")
    lines.append("")
    lines.append("#endif // MODEL_TINYML_H")
    
    os.makedirs(os.path.dirname(OUTPUT_HEADER), exist_ok=True)
    with open(OUTPUT_HEADER, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Generated TinyML C++ header successfully: {OUTPUT_HEADER}")

if __name__ == "__main__":
    export()
