"""
raspberry/gpio_controller.py
----------------------------
Contrôleur Matériel & Virtuel des Broches GPIO du Raspberry Pi 4 / 5.
Gère les actionneurs industriels et voyants d'état :
- GPIO 17 (Pin 11) : LED Verte (Fonctionnement Sain / Nominal)
- GPIO 22 (Pin 15) : LED Jaune / Orange (Alerte Dégradation Précoce)
- GPIO 27 (Pin 13) : LED Rouge (Panne Critique / Alerte Immédiate)
- GPIO 23 (Pin 16) : Relais d'Arrêt d'Urgence (Coupure Ligne Moteur)
- GPIO 24 (Pin 18) : Buzzer Piézoélectrique d'alarme sonore

Fonctionne de manière transparente en mode Réel (Raspberry Pi OS) ou Émulé (Windows/Linux/Mac).
"""

import os
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [GPIO] %(message)s")

# Détection de l'environnement physique Raspberry Pi
IS_RASPBERRY_PI = False
try:
    with open('/proc/cpuinfo', 'r') as f:
        cpuinfo = f.read().lower()
        if 'raspberry' in cpuinfo or 'bcm' in cpuinfo:
            import RPi.GPIO as GPIO
            IS_RASPBERRY_PI = True
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            logging.info("🍓 Environnement Raspberry Pi physique détecté. Pilote RPi.GPIO activé.")
except Exception:
    IS_RASPBERRY_PI = False
    logging.info("💻 Environnement de Développement détecté. Émulateur GPIO Virtuel activé.")


class PinDefinition:
    def __init__(self, bcm_pin: int, physical_pin: int, name: str, function: str, active_high: bool = True):
        self.bcm_pin = bcm_pin
        self.physical_pin = physical_pin
        self.name = name
        self.function = function
        self.active_high = active_high
        self.state = False
        self.last_updated = time.time()


class GPIOController:
    """Gestionnaire centralisé des entrées/sorties tout-ou-rien (TOR) industrielles."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPIOController, cls).__new__(cls)
            cls._instance._init_pins()
        return cls._instance

    def _init_pins(self):
        self.pins = {
            17: PinDefinition(17, 11, "LED_VERTE", "Voyant État Sain (Nominal)"),
            22: PinDefinition(22, 15, "LED_JAUNE", "Voyant Alerte Précoce"),
            27: PinDefinition(27, 13, "LED_ROUGE", "Voyant Défaut Critique"),
            23: PinDefinition(23, 16, "RELAIS_ESTOP", "Relais Coupure Moteur d'Urgence"),
            24: PinDefinition(24, 18, "BUZZER_ALARME", "Buzzer Alerte Sonore")
        }
        
        if IS_RASPBERRY_PI:
            for pin in self.pins.keys():
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                
        # État initial : LED Verte allumée (Machine sous tension, saine)
        self.set_pin(17, True)

    def set_pin(self, bcm_pin: int, state: bool) -> bool:
        if bcm_pin not in self.pins:
            logging.warning(f"Broche BCM {bcm_pin} non configurée.")
            return False
            
        self.pins[bcm_pin].state = state
        self.pins[bcm_pin].last_updated = time.time()
        
        if IS_RASPBERRY_PI:
            val = GPIO.HIGH if state else GPIO.LOW
            GPIO.output(bcm_pin, val)
            
        return True

    def get_status(self) -> dict:
        """Retourne l'état complet de toutes les broches pour l'API REST et le Dashboard."""
        return {
            "is_hardware_raspberry": IS_RASPBERRY_PI,
            "timestamp": time.time(),
            "pins": {
                f"GPIO_{p.bcm_pin}": {
                    "bcm_pin": p.bcm_pin,
                    "physical_pin": p.physical_pin,
                    "name": p.name,
                    "function": p.function,
                    "state": p.state,
                    "color": "green" if p.bcm_pin == 17 else ("orange" if p.bcm_pin == 22 else ("red" if p.bcm_pin in [27, 23] else "blue"))
                }
                for p in self.pins.values()
            }
        }

    def update_from_diagnostic(self, is_anomaly: bool, health_index: float, prediction_text: str = ""):
        """
        Met à jour automatiquement les voyants et relais en fonction du diagnostic Edge AI :
        - HI >= 85% : Vert ON, Jaune OFF, Rouge OFF, Relais OFF
        - 50% <= HI < 85% : Vert OFF, Jaune ON, Rouge OFF, Relais OFF
        - HI < 50% : Vert OFF, Jaune OFF, Rouge ON, Relais ON (Coupure automatique)
        """
        if not is_anomaly or health_index >= 85.0:
            self.set_pin(17, True)   # LED Verte ON
            self.set_pin(22, False)  # LED Jaune OFF
            self.set_pin(27, False)  # LED Rouge OFF
            self.set_pin(23, False)  # Relais E-Stop Normal
            self.set_pin(24, False)  # Buzzer OFF
        elif health_index >= 45.0:
            self.set_pin(17, False)  # LED Verte OFF
            self.set_pin(22, True)   # LED Jaune ON
            self.set_pin(27, False)  # LED Rouge OFF
            self.set_pin(23, False)  # Relais OFF
            self.set_pin(24, False)  # Buzzer OFF
        else:
            self.set_pin(17, False)  # LED Verte OFF
            self.set_pin(22, False)  # LED Jaune OFF
            self.set_pin(27, True)   # LED Rouge ON
            self.set_pin(23, True)   # Relais E-Stop ACTIVE (Sécurité)
            self.set_pin(24, True)   # Buzzer ON

    def cleanup(self):
        if IS_RASPBERRY_PI:
            GPIO.cleanup()
