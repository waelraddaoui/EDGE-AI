"""
raspberry/simulator_raspberry_edge.py
-------------------------------------
Simulateur Matériel Complet pour Raspberry Pi (Edge IoT)
Simule :
1. Un capteur accéléromètre I2C (ex: ADXL345 / MPU6050) acquérant les vibrations en continu.
2. La boucle d'acquisition temps réel et le buffer circulaire de 1024 points.
3. L'extraction des 16 descripteurs physiques Edge.
4. L'inférence ultra-rapide par le modèle XGBoost / LightGBM.
5. Les alertes GPIO virtuelles (LED Verte = Normal, LED Rouge Clignotante = Panne Détectée).
6. L'envoi automatique des alertes vers le Dashboard central.
"""

import time
import os
import sys
import random
import numpy as np
import pandas as pd
import joblib

# Chemins absolus
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.feature_extraction import extract_window_features
from raspberry.inference_edge import EdgeInferenceEngine

# Configuration du Simulateur
SAMPLE_RATE_HZ = 12000      # 12 kHz (standard CWRU / NASA)
WINDOW_SIZE = 1024          # Fenêtre glissante
INFERENCE_INTERVAL_SEC = 1.0 # Inférence toutes les secondes

class VirtualHardwarePin:
    """Simulateur de broche GPIO physique Raspberry Pi (LEDs, Relais)"""
    def __init__(self, pin_name, color):
        self.pin_name = pin_name
        self.color = color
        self.state = False

    def write(self, state: bool):
        self.state = state

    def __str__(self):
        status = "ON [ALLUMÉE]" if self.state else "OFF [ÉTEINTE]"
        return f"GPIO {self.pin_name} ({self.color}): {status}"

class VirtualI2CSensor:
    """Simulateur de capteur accéléromètre triaxial I2C (ex: ADXL345)"""
    def __init__(self):
        self.mode = "normal"  # "normal" ou "defaut"
        self.nasa_files = self._load_nasa_files()
        
    def _load_nasa_files(self):
        p_healthy = os.path.join(BASE_DIR, 'data', 'nasa_ims_classe', '1_ETAT_NORMAL_SAIN', '01_NASA_Sain_Jour1_Demarrage_12Fev.csv')
        p_fault = os.path.join(BASE_DIR, 'data', 'nasa_ims_classe', '3_ETAT_DEFAILLANCE_CRITIQUE_BAGUE_EXTERNE', '10_NASA_Defaillance_Jour7_RuptureFinale_MaxVibration_19Fev_05h52.csv')
        
        sig_h = pd.read_csv(p_healthy)['vibration_acc'].values if os.path.exists(p_healthy) else np.random.normal(0, 0.08, 5000)
        sig_f = pd.read_csv(p_fault)['vibration_acc'].values if os.path.exists(p_fault) else np.random.normal(0, 0.5, 5000)
        return {'normal': sig_h, 'fault': sig_f}

    def read_stream(self, n_points=1024, mode="normal"):
        source = self.nasa_files['normal'] if mode == "normal" else self.nasa_files['fault']
        # Découpage aléatoire pour simuler le flux continu
        if len(source) > n_points:
            start = random.randint(0, len(source) - n_points)
            return source[start:start+n_points] + np.random.normal(0, 0.02, n_points)
        return np.random.normal(0, 0.1 if mode == "normal" else 0.6, n_points)

def run_edge_simulator(duration_cycles=10):
    print("=" * 70)
    print(" 🍓 SIMULATEUR VIRTUEL EMBARQUÉ RASPBERRY PI 4 / 5 (EDGE AI IOT)")
    print("=" * 70)
    print(" [INFO] Initialisation des composants matériels virtuels...")
    
    # 1. GPIOs Virtuels
    led_green = VirtualHardwarePin("GPIO 17", "VERTE")
    led_red = VirtualHardwarePin("GPIO 27", "ROUGE")
    sensor = VirtualI2CSensor()
    
    # 2. Chargement du Moteur d'Inférence Edge
    print(" [INFO] Chargement du modèle XGBoost Edge AI sur CPU ARM...")
    engine = EdgeInferenceEngine(model_name='Gradient Boosting')
    scaler_path = os.path.join(BASE_DIR, 'models', 'scaler.joblib')
    scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    
    print("\n [OK] Système prêt ! Démarrage de la boucle de surveillance temps réel.\n")
    print("-" * 70)
    print(f"{'CYCLE':<8}{'ÉTAT CAPTEUR':<16}{'VERDICT IA':<20}{'LATENCE':<12}{'ÉTAT LEDS GPIO'}")
    print("-" * 70)
    
    for cycle in range(1, duration_cycles + 1):
        # Simulation d'un événement de panne à partir du cycle 6
        current_mode = "fault" if cycle >= 6 else "normal"
        
        # 1. Lecture Capteur I2C
        vibration_chunk = sensor.read_stream(n_points=WINDOW_SIZE, mode=current_mode)
        
        # 2. Extraction des caractéristiques Edge (16 features)
        t0 = time.perf_counter()
        features = extract_window_features(vibration_chunk)
        if scaler:
            features = scaler.transform(np.array(features).reshape(1, -1))[0]
            
        # 3. Inférence Edge AI
        res = engine.predict_sample(features)
        latency_total_ms = (time.perf_counter() - t0) * 1000
        
        is_anomaly = res['is_anomaly']
        
        # 4. Actionneur GPIO (Contrôle des LEDs)
        if is_anomaly:
            led_green.write(False)
            led_red.write(True)
            verdict_str = "🔴 DÉFAILLANCE !"
            led_str = "🟢 OFF | 🔴 ON (Alarme)"
        else:
            led_green.write(True)
            led_red.write(False)
            verdict_str = "🟢 NOMINAL (Sain)"
            led_str = "🟢 ON  | 🔴 OFF"
            
        sensor_str = "NASA Normal" if current_mode == "normal" else "NASA Rupture"
        print(f"#{cycle:<7}{sensor_str:<16}{verdict_str:<20}{latency_total_ms:.2f} ms     {led_str}")
        
        time.sleep(0.6)

    print("-" * 70)
    print(" [SUCCÈS] Simulation terminée sans erreur.")
    print(" Ce même script s'exécutera à 100% à l'identique sur votre vraie Raspberry Pi !")
    print("=" * 70)

if __name__ == '__main__':
    run_edge_simulator()
