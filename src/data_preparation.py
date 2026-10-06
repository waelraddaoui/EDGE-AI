"""
src/data_preparation.py
------------------------
Module 1 : Gestion, préparation et documentation du jeu de données CWRU (Case Western Reserve University).

Ce script assure :
1. La génération / le téléchargement des signaux vibratoires bruts (Normal, Bague Interne, Bague Externe, Bille).
2. La création d'un dataset hybride perturbé (Bruit gaussien, Dérive lente, Pertes de paquets / Zéros, Pics d'impulsion).
3. La création d'une version réduite pédagogique (F1.7) pour les activités étudiantes et l'agent RAG.
4. La documentation et la sauvegarde des métadonnées du dataset (F1.5).

Conforme aux exigences F1.1 à F1.7 du Cahier des Charges.
"""

import os
import json
import numpy as np
import pandas as pd

# Chemins des répertoires
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DATA_PEDAGOGICAL_DIR = os.path.join(BASE_DIR, 'data', 'pedagogical_subset')

for directory in [DATA_RAW_DIR, DATA_PROCESSED_DIR, DATA_PEDAGOGICAL_DIR]:
    os.makedirs(directory, exist_ok=True)

# Paramètres physiques de simulation CWRU (Roulement 6205-2RS JSK, Échantillonnage 12 kHz, 1797 RPM)
FS = 12000  # Fréquence d'échantillonnage Hz
RPM = 1797  # Vitesse de rotation tr/min
FR = RPM / 60.0  # Fréquence de rotation ~29.95 Hz

# Fréquences mécaniques caractéristiques de défaut (CWRU Drive End)
BPFI = 5.4152 * FR  # Ball Pass Frequency Inner race ~ 162.2 Hz
BPFO = 3.5848 * FR  # Ball Pass Frequency Outer race ~ 107.4 Hz
BSF  = 2.357 * FR   # Ball Spin Frequency ~ 70.6 Hz
FTF  = 0.398 * FR   # Fundamental Train Frequency ~ 11.9 Hz

def generate_vibration_signal(fault_type='normal', severity='normal', duration_sec=10.0, seed=42):
    """
    Génère un signal vibratoire synthétique haute fidélité modélisant la physique des défauts CWRU.
    
    Parameters:
    -----------
    fault_type : str
        'normal', 'inner_race', 'outer_race', 'ball'
    severity : str
        'normal', '0.007', '0.014', '0.021'
    duration_sec : float
        Durée du signal en secondes.
    seed : int
        Graine aléatoire pour la reproductibilité.
        
    Returns:
    --------
    t : ndarray (Temps en s)
    acc : ndarray (Signal d'accélération vibratoire en g)
    """
    np.random.seed(seed)
    n_samples = int(FS * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)
    
    # Bruit de fond stochastique
    acc = np.random.normal(0, 0.05, n_samples)
    
    # Composante fondamentale de rotation (déséquilibre résiduel)
    acc += 0.08 * np.sin(2 * np.pi * FR * t)
    acc += 0.03 * np.sin(4 * np.pi * FR * t)
    
    if fault_type == 'normal':
        return t, acc
    
    # Facteur d'amplitude selon la sévérité
    severity_map = {'0.007': 1.0, '0.014': 1.8, '0.021': 2.5}
    amp_factor = severity_map.get(severity, 1.0)
    
    # Fréquence caractéristique d'impact
    if fault_type == 'inner_race':
        f_fault = BPFI
        resonance_freq = 3000.0  # Hz (Fréquence propre de résonance bague interne)
        damping = 800.0
        modulation = 1.0 + 0.4 * np.cos(2 * np.pi * FR * t)  # Modulation par la rotation de l'arbre
    elif fault_type == 'outer_race':
        f_fault = BPFO
        resonance_freq = 2500.0  # Hz
        damping = 600.0
        modulation = 1.0  # Défaut fixe par rapport à la charge
    elif fault_type == 'ball':
        f_fault = BSF
        resonance_freq = 2000.0  # Hz
        damping = 500.0
        modulation = 1.0 + 0.5 * np.cos(2 * np.pi * FTF * t)  # Modulation à la fréquence de la cage
    else:
        raise ValueError(f"Type de défaut non reconnu : {fault_type}")
        
    period = 1.0 / f_fault
    n_impacts = int(duration_sec / period)
    impact_times = np.arange(n_impacts) * period + np.random.normal(0, 0.02 * period, n_impacts)
    
    impact_samples = int(0.01 * FS)  # 10 ms d'impulsion
    t_impulse = np.linspace(0, 0.01, impact_samples, endpoint=False)
    base_impulse = np.exp(-damping * t_impulse) * np.sin(2 * np.pi * resonance_freq * t_impulse)
    
    for t_imp in impact_times:
        if t_imp <= 0 or t_imp >= duration_sec - 0.01:
            continue
        idx_start = int(t_imp * FS)
        mod_val = modulation[idx_start] if isinstance(modulation, np.ndarray) else float(modulation)
        imp = amp_factor * mod_val * base_impulse
        
        end_idx = min(idx_start + impact_samples, n_samples)
        actual_len = end_idx - idx_start
        acc[idx_start:end_idx] += imp[:actual_len]
            
    return t, acc

def add_synthetic_disturbances(signal, noise_snr_db=15, drift_amp=0.2, packet_loss_rate=0.02, spike_rate=0.001):
    """
    Ajoute des perturbations industrielles réalistes (bruit, dérive, pertes de données, pics impulsionnels).
    """
    noisy_signal = signal.copy()
    
    # 1. Bruit gaussien blanc selon le ratio SNR
    sig_power = np.mean(signal ** 2)
    noise_power = sig_power / (10 ** (noise_snr_db / 10.0))
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    noisy_signal += noise
    
    # 2. Dérive basse fréquence de ligne de base (ex: échauffement thermique capteur)
    t = np.linspace(0, len(signal)/FS, len(signal))
    drift = drift_amp * np.sin(2 * np.pi * 0.1 * t) + 0.05 * t
    noisy_signal += drift
    
    # 3. Pertes de paquets / zéros (déconnexion temporaire du flux IoT)
    mask = np.random.rand(len(signal)) < packet_loss_rate
    noisy_signal[mask] = 0.0
    
    # 4. Pics aberrants impulsionnels (parasite électrique)
    spikes_mask = np.random.rand(len(signal)) < spike_rate
    noisy_signal[spikes_mask] += np.random.choice([-1, 1], size=np.sum(spikes_mask)) * np.max(np.abs(signal)) * 3.0
    
    return noisy_signal

def build_dataset():
    """
    Construit le jeu de données CWRU complet, sa version hybride perturbée et sa version pédagogique réduite.
    """
    print("=== Module 1 : Génération & Préparation du Jeu de Données CWRU ===")
    
    scenarios = [
        ('normal', 'normal', 'Normal'),
        ('inner_race', '0.007', 'InnerRace_007'),
        ('inner_race', '0.014', 'InnerRace_014'),
        ('inner_race', '0.021', 'InnerRace_021'),
        ('outer_race', '0.007', 'OuterRace_007'),
        ('outer_race', '0.014', 'OuterRace_014'),
        ('outer_race', '0.021', 'OuterRace_021'),
        ('ball', '0.007', 'Ball_007'),
        ('ball', '0.014', 'Ball_014'),
        ('ball', '0.021', 'Ball_021'),
    ]
    
    duration = 10.0  # 10 secondes par scénario = 120 000 points par classe
    raw_dfs = []
    hybrid_dfs = []
    
    for seed, (fault_type, severity, label_name) in enumerate(scenarios, start=100):
        t, signal = generate_vibration_signal(fault_type, severity, duration_sec=duration, seed=seed)
        noisy_signal = add_synthetic_disturbances(signal, noise_snr_db=12)
        
        is_anomaly = 0 if fault_type == 'normal' else 1
        
        df_sub = pd.DataFrame({
            'time_s': np.round(t, 6),
            'vibration_acc': np.round(signal, 6),
            'label': label_name,
            'fault_type': fault_type,
            'severity': severity,
            'is_anomaly': is_anomaly
        })
        raw_dfs.append(df_sub)
        
        df_hyb = pd.DataFrame({
            'time_s': np.round(t, 6),
            'vibration_acc_noisy': np.round(noisy_signal, 6),
            'label': label_name,
            'fault_type': fault_type,
            'severity': severity,
            'is_anomaly': is_anomaly
        })
        hybrid_dfs.append(df_hyb)
            
    df_raw = pd.concat(raw_dfs, ignore_index=True)
    df_hybrid = pd.concat(hybrid_dfs, ignore_index=True)
    
    # 1. Sauvegarde du Dataset Brut CWRU
    raw_path = os.path.join(DATA_RAW_DIR, 'cwru_raw_signals.parquet')
    df_raw.to_parquet(raw_path, index=False)
    print(f"[OK] Dataset Brut CWRU sauvegarde : {raw_path} ({len(df_raw)} points)")
    
    # 2. Sauvegarde du Dataset Hybride Perturbe
    hybrid_path = os.path.join(DATA_RAW_DIR, 'cwru_hybrid_noisy.parquet')
    df_hybrid.to_parquet(hybrid_path, index=False)
    print(f"[OK] Dataset Hybride sauvegarde : {hybrid_path} ({len(df_hybrid)} points)")
    
    # 3. Sauvegarde du Dataset Pedagogique Reduit (F1.7)
    df_pedagogical = df_raw[df_raw['label'].isin(['Normal', 'InnerRace_014', 'OuterRace_014', 'Ball_014'])].copy()
    df_pedagogical = df_pedagogical[df_pedagogical['time_s'] <= 1.0]
    pedagogical_csv = os.path.join(DATA_PEDAGOGICAL_DIR, 'cwru_pedagogical_subset.csv')
    df_pedagogical.to_csv(pedagogical_csv, index=False)
    print(f"[OK] Dataset Pedagogique Reduit sauvegarde : {pedagogical_csv} ({len(df_pedagogical)} lignes)")
    
    # 4. Documentation des Metadonnees du Dataset (F1.5)
    metadata = {
        "dataset_name": "CWRU Bearing Vibration Dataset (Simulated & Hybrid)",
        "source": "Case Western Reserve University Bearing Data Center (Simulation conforme)",
        "sampling_frequency_hz": FS,
        "motor_speed_rpm": RPM,
        "rotation_frequency_hz": round(FR, 2),
        "characteristic_frequencies_hz": {
            "BPFI_inner_race": round(BPFI, 2),
            "BPFO_outer_race": round(BPFO, 2),
            "BSF_ball": round(BSF, 2),
            "FTF_cage": round(FTF, 2)
        },
        "total_samples_per_class": int(FS * duration),
        "classes": list(df_raw['label'].unique()),
        "columns": list(df_raw.columns),
        "limitations": [
            "Donnees simulees basees sur les equations physiques analytiques de CWRU.",
            "Signal mono-axe d'acceleration (Drive End).",
            "Ideal pour l'experimentation Edge AI et le prototypage rapide sur Raspberry Pi."
        ]
    }
    
    meta_path = os.path.join(DATA_RAW_DIR, 'dataset_metadata.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"[OK] Metadonnees documentees sauvegardees : {meta_path}")

if __name__ == '__main__':
    build_dataset()
