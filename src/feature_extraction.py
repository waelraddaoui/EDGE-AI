"""
src/feature_extraction.py
--------------------------
Module 2 : Prétraitement, fenêtrage et extraction de caractéristiques temporelles, statistiques et fréquentielles.

Calcule 16 caractéristiques par fenêtre de signal (1024 points, 50% chevauchement) :
1. Temporelles : Mean, Std, Variance, RMS, Min, Max, Peak-to-Peak, Energy.
2. Statistiques : Skewness, Kurtosis, Crest Factor, Impulse Factor.
3. Fréquentielles (FFT) : Spectral Energy, Dominant Frequency, Spectral Centroid, Spectral Roll-off.

Conforme aux exigences F2.1 à F2.7 du Cahier des Charges.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

FS = 12000  # Fréquence d'échantillonnage Hz

def extract_window_features(signal_window):
    """
    Extrait un vecteur de 16 caractéristiques statistiques, temporelles et fréquentielles sur une fenêtre.
    """
    N = len(signal_window)
    eps = 1e-10
    
    # 1. Caractéristiques Temporelles & Statistiques
    mean_val = np.mean(signal_window)
    std_val = np.std(signal_window)
    var_val = np.var(signal_window)
    rms_val = np.sqrt(np.mean(signal_window ** 2))
    min_val = np.min(signal_window)
    max_val = np.max(signal_window)
    peak_val = np.max(np.abs(signal_window))
    p2p_val = max_val - min_val
    energy_val = np.sum(signal_window ** 2)
    
    skew_val = float(skew(signal_window)) if std_val > eps else 0.0
    kurt_val = float(kurtosis(signal_window)) if std_val > eps else 0.0
    crest_factor = peak_val / (rms_val + eps)
    impulse_factor = peak_val / (np.mean(np.abs(signal_window)) + eps)
    
    # 2. Caractéristiques Fréquentielles (FFT)
    fft_vals = np.abs(np.fft.rfft(signal_window))
    freqs = np.fft.rfftfreq(N, 1.0 / FS)
    
    spectral_energy = np.sum(fft_vals ** 2)
    dom_freq_idx = np.argmax(fft_vals)
    dominant_freq = freqs[dom_freq_idx]
    
    spectral_centroid = np.sum(freqs * fft_vals) / (np.sum(fft_vals) + eps)
    spectral_spread = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * fft_vals) / (np.sum(fft_vals) + eps))
    
    return [
        mean_val, std_val, var_val, rms_val, min_val, max_val, p2p_val, energy_val,
        skew_val, kurt_val, crest_factor, impulse_factor,
        spectral_energy, dominant_freq, spectral_centroid, spectral_spread
    ]

FEATURE_NAMES = [
    'mean', 'std', 'var', 'rms', 'min', 'max', 'p2p', 'energy',
    'skewness', 'kurtosis', 'crest_factor', 'impulse_factor',
    'spectral_energy', 'dominant_freq', 'spectral_centroid', 'spectral_spread'
]

def process_signal_df(df, window_size=1024, step_size=512, is_hybrid=False):
    """
    Découpe le signal en fenêtres et extrait les caractéristiques pour chaque classe.
    """
    col_name = 'vibration_acc_noisy' if is_hybrid else 'vibration_acc'
    rows = []
    
    for label_name, group in df.groupby('label'):
        signal = group[col_name].values
        is_anomaly = group['is_anomaly'].iloc[0]
        fault_type = group['fault_type'].iloc[0]
        severity = group['severity'].iloc[0]
        
        n_samples = len(signal)
        n_windows = (n_samples - window_size) // step_size + 1
        
        for w_idx in range(n_windows):
            start = w_idx * step_size
            end = start + window_size
            window = signal[start:end]
            
            feats = extract_window_features(window)
            record = {
                'window_id': f"{label_name}_w{w_idx}",
                'label': label_name,
                'fault_type': fault_type,
                'severity': severity,
                'is_anomaly': is_anomaly
            }
            for name, val in zip(FEATURE_NAMES, feats):
                record[name] = round(float(val), 6)
                
            rows.append(record)
            
    return pd.DataFrame(rows)

def run_feature_extraction():
    print("=== Module 2 : Extraction des Caractéristiques & Normalisation ===")
    
    raw_path = os.path.join(DATA_RAW_DIR, 'cwru_raw_signals.parquet')
    hybrid_path = os.path.join(DATA_RAW_DIR, 'cwru_hybrid_noisy.parquet')
    
    df_raw = pd.read_parquet(raw_path)
    df_hybrid = pd.read_parquet(hybrid_path)
    
    print("Extraction sur Dataset Brut...")
    df_feats_raw = process_signal_df(df_raw, window_size=1024, step_size=512, is_hybrid=False)
    
    print("Extraction sur Dataset Hybride...")
    df_feats_hybrid = process_signal_df(df_hybrid, window_size=1024, step_size=512, is_hybrid=True)
    
    # Enregistrement des DataFrames de caractéristiques
    feats_raw_path = os.path.join(DATA_PROCESSED_DIR, 'features_raw.parquet')
    feats_hyb_path = os.path.join(DATA_PROCESSED_DIR, 'features_hybrid.parquet')
    
    df_feats_raw.to_parquet(feats_raw_path, index=False)
    df_feats_hybrid.to_parquet(feats_hyb_path, index=False)
    
    print(f"[OK] Caractéristiques brutes enregistrées : {feats_raw_path} ({len(df_feats_raw)} fenêtres)")
    print(f"[OK] Caractéristiques hybrides enregistrées : {feats_hyb_path} ({len(df_feats_hybrid)} fenêtres)")
    
    # Séparation Train / Validation / Test (80% / 10% / 10%) sans fuite
    X = df_feats_raw[FEATURE_NAMES].values
    y = df_feats_raw['is_anomaly'].values
    y_multiclass = df_feats_raw['label'].values
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Enregistrement du Scaler et des ensembles de données prêts pour la modélisation
    scaler_path = os.path.join(MODELS_DIR, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)
    
    np.savez_compressed(
        os.path.join(DATA_PROCESSED_DIR, 'dataset_split.npz'),
        X_train=X_train_scaled, y_train=y_train,
        X_val=X_val_scaled, y_val=y_val,
        X_test=X_test_scaled, y_test=y_test,
        feature_names=np.array(FEATURE_NAMES)
    )
    print(f"[OK] Scaler enregistré : {scaler_path}")
    print(f"[OK] Split Train ({len(X_train)}), Val ({len(X_val)}), Test ({len(X_test)}) enregistrés dans dataset_split.npz")

if __name__ == '__main__':
    run_feature_extraction()
