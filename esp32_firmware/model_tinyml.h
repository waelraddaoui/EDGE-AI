// =============================================================================
// MODEL_TINYML.H - EXPORT C++ DU VRAI MODELE GRADIENT BOOSTING (XGBOOST)
// Entraîné sur le dataset vibratoire CWRU (16 caractéristiques physiques)
// Déployable 100% en local dans la mémoire Flash de l'ESP32
// =============================================================================
#ifndef MODEL_TINYML_H
#define MODEL_TINYML_H

#include <math.h>

// 1. Paramètres de normalisation StandardScaler (16 features)
const float SCALER_MEAN[16] = { 0.009501f, 0.356652f, 0.151476f, 0.356880f, -1.627642f, 1.900601f, 3.528243f, 155.279722f, 0.435249f, 7.049099f, 5.145694f, 9.281147f, 79593.063836f, 2249.616500f, 2580.949885f, 1323.930141f };
const float SCALER_SCALE[16] = { 0.008582f, 0.155808f, 0.109765f, 0.155812f, 0.794793f, 0.906557f, 1.697196f, 112.492034f, 0.185540f, 3.398629f, 0.930200f, 2.588337f, 57645.411219f, 834.426955f, 289.772185f, 199.623451f };

static inline float tree_0(const float* x) { if (x[13] < -0.378730f) { return -0.945558f; } else { return 0.110353f; } }
static inline float tree_1(const float* x) { if (x[13] < -0.378730f) { return -0.436853f; } else { return 0.109135f; } }
static inline float tree_2(const float* x) { if (x[13] < -0.378730f) { return -0.318361f; } else { return 0.108042f; } }
static inline float tree_3(const float* x) { if (x[13] < -0.378730f) { return -0.258763f; } else { return 0.107057f; } }
static inline float tree_4(const float* x) { if (x[13] < -0.378730f) { return -0.222285f; } else { return 0.106165f; } }
static inline float tree_5(const float* x) { if (x[13] < -0.378730f) { return -0.197546f; } else { return 0.105352f; } }
static inline float tree_6(const float* x) { if (x[13] < -0.378730f) { return -0.179653f; } else { return 0.104608f; } }
static inline float tree_7(const float* x) { if (x[13] < -0.378730f) { return -0.166120f; } else { return 0.103922f; } }
static inline float tree_8(const float* x) { if (x[13] < -0.378730f) { return -0.155543f; } else { return 0.103285f; } }
static inline float tree_9(const float* x) { if (x[13] < -0.378730f) { return -0.147064f; } else { return 0.102689f; } }
static inline float tree_10(const float* x) { if (x[13] < -0.378730f) { return -0.140126f; } else { return 0.102128f; } }
static inline float tree_11(const float* x) { if (x[13] < -0.378730f) { return -0.134353f; } else { return 0.101595f; } }
static inline float tree_12(const float* x) { if (x[13] < -0.378730f) { return -0.129480f; } else { return 0.101084f; } }
static inline float tree_13(const float* x) { if (x[13] < -0.378730f) { return -0.125314f; } else { return 0.100590f; } }
static inline float tree_14(const float* x) { if (x[13] < -0.378730f) { return -0.121713f; } else { return 0.100107f; } }
static inline float tree_15(const float* x) { if (x[13] < -0.378730f) { return -0.118566f; } else { return 0.099630f; } }
static inline float tree_16(const float* x) { if (x[13] < -0.378730f) { return -0.115789f; } else { return 0.099156f; } }
static inline float tree_17(const float* x) { if (x[13] < -0.378730f) { return -0.113315f; } else { return 0.098680f; } }
static inline float tree_18(const float* x) { if (x[13] < -0.378730f) { return -0.111091f; } else { return 0.098198f; } }
static inline float tree_19(const float* x) { if (x[13] < -0.378730f) { return -0.109072f; } else { return 0.097705f; } }
static inline float tree_20(const float* x) { if (x[13] < -0.378730f) { return -0.107221f; } else { return 0.097199f; } }
static inline float tree_21(const float* x) { if (x[13] < -0.378730f) { return -0.105509f; } else { return 0.096675f; } }
static inline float tree_22(const float* x) { if (x[13] < -0.378730f) { return -0.103911f; } else { return 0.096129f; } }
static inline float tree_23(const float* x) { if (x[13] < -0.378730f) { return -0.102403f; } else { return 0.095559f; } }
static inline float tree_24(const float* x) { if (x[13] < -0.378730f) { return -0.100969f; } else { return 0.094960f; } }
static inline float tree_25(const float* x) { if (x[13] < -0.378730f) { return -0.099590f; } else { return 0.094331f; } }
static inline float tree_26(const float* x) { if (x[13] < -0.378730f) { return -0.098254f; } else { return 0.093667f; } }
static inline float tree_27(const float* x) { if (x[13] < -0.378730f) { return -0.096948f; } else { return 0.092965f; } }
static inline float tree_28(const float* x) { if (x[13] < -0.378730f) { return -0.095662f; } else { return 0.092223f; } }
static inline float tree_29(const float* x) { if (x[13] < -0.378730f) { return -0.094386f; } else { return 0.091439f; } }

// 2. Fonction principale d'inférence TinyML
struct PredictionResult {
    int predicted_class;   // 0 = SAIN (Normal), 1 = DEFAUT (Bearing Fault)
    float fault_prob;      // Probabilité de panne (0.0 à 1.0)
    float health_index;    // Indice de Santé (0.0% à 100.0%)
};

inline PredictionResult predict_bearing_health(const float raw_features[16]) {
    // A. Normalisation StandardScaler
    float x[16];
    for (int i = 0; i < 16; i++) {
        x[i] = (raw_features[i] - SCALER_MEAN[i]) / SCALER_SCALE[i];
    }

    // B. Sommation des 30 arbres du Gradient Boosting
    float raw_score = 0.0f;
    raw_score += tree_0(x);
    raw_score += tree_1(x);
    raw_score += tree_2(x);
    raw_score += tree_3(x);
    raw_score += tree_4(x);
    raw_score += tree_5(x);
    raw_score += tree_6(x);
    raw_score += tree_7(x);
    raw_score += tree_8(x);
    raw_score += tree_9(x);
    raw_score += tree_10(x);
    raw_score += tree_11(x);
    raw_score += tree_12(x);
    raw_score += tree_13(x);
    raw_score += tree_14(x);
    raw_score += tree_15(x);
    raw_score += tree_16(x);
    raw_score += tree_17(x);
    raw_score += tree_18(x);
    raw_score += tree_19(x);
    raw_score += tree_20(x);
    raw_score += tree_21(x);
    raw_score += tree_22(x);
    raw_score += tree_23(x);
    raw_score += tree_24(x);
    raw_score += tree_25(x);
    raw_score += tree_26(x);
    raw_score += tree_27(x);
    raw_score += tree_28(x);
    raw_score += tree_29(x);

    // C. Fonction Sigmoïde logistique
    float prob = 1.0f / (1.0f + expf(-raw_score));

    PredictionResult res;
    res.fault_prob = prob;
    res.predicted_class = (prob >= 0.50f) ? 1 : 0;
    res.health_index = (1.0f - prob) * 100.0f;
    return res;
}

#endif // MODEL_TINYML_H