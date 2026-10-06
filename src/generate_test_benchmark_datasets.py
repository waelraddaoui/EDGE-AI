"""
src/generate_test_benchmark_datasets.py
---------------------------------------
Générateur de Datasets de Test Avancés pour la Validation du Modèle Edge AI :
1. Dataset NASA IMS Benchmark (Simulation Run-to-Failure en 3 stades de dégradation)
2. Dataset Synthétique IA Multi-Conditions (Variations de vitesse, bruits extrêmes, défauts combinés)

Produit des fichiers CSV prêts à être testés dans l'interface web Dashboard.
"""

import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NASA_DIR = os.path.join(BASE_DIR, 'data', 'nasa_ims_dataset')
DATA_AI_DIR = os.path.join(BASE_DIR, 'data', 'ai_synthetic_dataset')

os.makedirs(DATA_NASA_DIR, exist_ok=True)
os.makedirs(DATA_AI_DIR, exist_ok=True)

FS = 12000  # Fréquence d'échantillonnage standard (12 kHz)
DURATION_SEC = 1.0  # 1 seconde par fichier (12 000 points)
N_POINTS = int(FS * DURATION_SEC)
TIME = np.linspace(0, DURATION_SEC, N_POINTS, endpoint=False)

def generate_nasa_dataset():
    print("--> Génération du Benchmark Dataset NASA IMS (Run-to-Failure)...")
    
    # 1. NASA Stage 1 : Fonctionnement Sain Initial (Healthy Baseline)
    # Vitesse stable 2000 RPM (~33.3 Hz), bruit de fond mécanique faible
    f_rot = 33.33
    acc_healthy = 0.4 * np.sin(2 * np.pi * f_rot * TIME) + \
                  0.15 * np.sin(2 * np.pi * 2 * f_rot * TIME) + \
                  np.random.normal(0, 0.08, N_POINTS)
    
    df_healthy = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_healthy, 5),
        'stage': 'Stage 1 - Healthy Baseline',
        'expected_status': 'Normal'
    })
    df_healthy.to_csv(os.path.join(DATA_NASA_DIR, 'nasa_stage1_healthy_baseline.csv'), index=False)
    
    # 2. NASA Stage 2 : Défaut Naissant / Micro-fissuration (Incipient Defect)
    # Apparition de micro-chocs non destructifs, Kurtosis en hausse, RMS stable
    f_bpfo = 107.4
    shocks_incipient = np.zeros(N_POINTS)
    period_samples = int(FS / f_bpfo)
    for idx in range(0, N_POINTS, period_samples):
        length = min(80, N_POINTS - idx)
        decay = np.exp(-np.linspace(0, 4, length))
        shocks_incipient[idx:idx+length] += 1.8 * decay * np.sin(2 * np.pi * 2200 * TIME[:length])
        
    acc_incipient = 0.5 * np.sin(2 * np.pi * f_rot * TIME) + shocks_incipient + np.random.normal(0, 0.15, N_POINTS)
    
    df_incipient = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_incipient, 5),
        'stage': 'Stage 2 - Incipient Micro-Defect',
        'expected_status': 'Anomaly Detected (Bague Externe)'
    })
    df_incipient.to_csv(os.path.join(DATA_NASA_DIR, 'nasa_stage2_incipient_defect.csv'), index=False)

    # 3. NASA Stage 3 : Rupture Sévère & Écaillage (Severe Degradation)
    # Chocs violents à haute amplitude, modulation d'amplitude forte, bruit intense
    shocks_severe = np.zeros(N_POINTS)
    for idx in range(0, N_POINTS, period_samples):
        length = min(150, N_POINTS - idx)
        decay = np.exp(-np.linspace(0, 2.5, length))
        shocks_severe[idx:idx+length] += 5.2 * decay * np.sin(2 * np.pi * 2200 * TIME[:length])
        
    acc_severe = 0.8 * np.sin(2 * np.pi * f_rot * TIME) + shocks_severe + np.random.normal(0, 0.45, N_POINTS)
    
    df_severe = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_severe, 5),
        'stage': 'Stage 3 - Severe Flaking & Breakdown',
        'expected_status': 'Anomaly Detected (Bague Externe)'
    })
    df_severe.to_csv(os.path.join(DATA_NASA_DIR, 'nasa_stage3_severe_breakdown.csv'), index=False)
    print("   [OK] 3 fichiers NASA IMS créés dans data/nasa_ims_dataset/")

def generate_ai_synthetic_dataset():
    print("--> Génération du Dataset Synthétique IA Multi-Conditions...")
    
    # 1. AI Synthetic : Vitesse Variable & Régime Transitoire (1500 à 1800 RPM)
    speed_curve = np.linspace(25.0, 30.0, N_POINTS)  # Fréquence de rotation variant de 25 à 30 Hz
    phase = 2 * np.pi * np.cumsum(speed_curve) / FS
    acc_var_speed = 0.6 * np.sin(phase) + np.random.normal(0, 0.12, N_POINTS)
    
    df_var = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_var_speed, 5),
        'condition': 'Variable Speed Non-Stationary',
        'expected_status': 'Normal'
    })
    df_var.to_csv(os.path.join(DATA_AI_DIR, 'ai_synthetic_variable_speed_normal.csv'), index=False)

    # 2. AI Synthetic : Défaut Bague Interne sous Bruit Extrême d'Usine (SNR 5 dB)
    f_bpfi = 162.2
    shocks_bpfi = np.zeros(N_POINTS)
    period_bpfi = int(FS / f_bpfi)
    for idx in range(0, N_POINTS, period_bpfi):
        length = min(100, N_POINTS - idx)
        decay = np.exp(-np.linspace(0, 3.5, length))
        # Modulation par la rotation d'arbre (caractéristique physique bague interne)
        mod = 1.0 + 0.6 * np.sin(2 * np.pi * 30.0 * idx / FS)
        shocks_bpfi[idx:idx+length] += 4.0 * mod * decay * np.sin(2 * np.pi * 2800 * TIME[:length])
        
    noise_heavy = np.random.normal(0, 0.85, N_POINTS)  # Fort bruit industriel
    acc_noisy_bpfi = shocks_bpfi + noise_heavy
    
    df_bpfi = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_noisy_bpfi, 5),
        'condition': 'Heavy Industrial Noise (SNR 5dB) + BPFI',
        'expected_status': 'Anomaly Detected (Bague Interne)'
    })
    df_bpfi.to_csv(os.path.join(DATA_AI_DIR, 'ai_synthetic_heavy_noise_inner_race.csv'), index=False)

    # 3. AI Synthetic : Défaut de Bille avec Échauffement Thermique (Ball Spin BSF ~71 Hz)
    f_bsf = 70.6
    shocks_bsf = np.zeros(N_POINTS)
    period_bsf = int(FS / f_bsf)
    for idx in range(0, N_POINTS, period_bsf):
        length = min(120, N_POINTS - idx)
        decay = np.exp(-np.linspace(0, 3.0, length))
        shocks_bsf[idx:idx+length] += 3.2 * decay * np.sin(2 * np.pi * 1800 * TIME[:length])
        
    thermal_drift = 0.5 * np.sin(2 * np.pi * 0.8 * TIME)  # Dérive basse fréquence capteur
    acc_bsf = shocks_bsf + thermal_drift + np.random.normal(0, 0.2, N_POINTS)
    
    df_bsf = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_bsf, 5),
        'condition': 'Ball Defect (BSF) + Sensor Thermal Drift',
        'expected_status': 'Anomaly Detected (Défaut de Bille)'
    })
    df_bsf.to_csv(os.path.join(DATA_AI_DIR, 'ai_synthetic_ball_fault_thermal_drift.csv'), index=False)

    # 4. AI Synthetic : Défaut Combiné Complexe (Bague Interne + Bague Externe)
    f_bpfo = 107.4
    shocks_bpfo = np.zeros(N_POINTS)
    period_bpfo = int(FS / f_bpfo)
    for idx in range(0, N_POINTS, period_bpfo):
        length = min(80, N_POINTS - idx)
        decay = np.exp(-np.linspace(0, 4, length))
        shocks_bpfo[idx:idx+length] += 2.0 * decay * np.sin(2 * np.pi * 2200 * TIME[:length])
        
    acc_compound = shocks_bpfi * 0.7 + shocks_bpfo * 1.5 + np.random.normal(0, 0.3, N_POINTS)
    df_comp = pd.DataFrame({
        'time_sec': np.round(TIME, 6),
        'vibration_acc': np.round(acc_compound, 5),
        'condition': 'Compound Fault (Inner + Outer Races)',
        'expected_status': 'Anomaly Detected (Bague Interne)'
    })
    df_comp.to_csv(os.path.join(DATA_AI_DIR, 'ai_synthetic_compound_fault.csv'), index=False)
    print("   [OK] 4 fichiers Synthétiques IA créés dans data/ai_synthetic_dataset/")

if __name__ == '__main__':
    generate_nasa_dataset()
    generate_ai_synthetic_dataset()
    print("\n[SUCCÈS] Tous les datasets de test ont été générés avec succès !")
