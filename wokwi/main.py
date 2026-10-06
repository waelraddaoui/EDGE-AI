"""
WOKWI EMBEDDED EDGE AI - MICROPYTHON VERSION
Pour Raspberry Pi Pico ou ESP32 sur https://wokwi.com
"""

import time
import math
from machine import Pin, I2C

# Broches GPIO
led_green = Pin(18, Pin.OUT)
led_yellow = Pin(19, Pin.OUT)
led_red = Pin(23, Pin.OUT)
relay = Pin(5, Pin.OUT)
buzzer = Pin(4, Pin.OUT)
btn_fault = Pin(15, Pin.IN, Pin.PULL_UP)

# État initial
led_green.value(1)
led_yellow.value(0)
led_red.value(0)
relay.value(0)
buzzer.value(0)

print("🍓 Moteur MicroPython Edge AI Démarre sur Wokwi...")

def extract_features(buffer):
    N = len(buffer)
    mean = sum(buffer) / N
    variance = sum((x - mean) ** 2 for x in buffer) / N
    std = math.sqrt(variance) if variance > 0 else 0.0001
    rms = math.sqrt(sum(x ** 2 for x in buffer) / N)
    peak = max(abs(x) for x in buffer)
    kurtosis = (sum((x - mean) ** 4 for x in buffer) / N) / (variance ** 2 + 1e-6)
    crest_factor = peak / (rms + 1e-6)
    return {"mean": mean, "rms": rms, "kurtosis": kurtosis, "crest_factor": crest_factor}

buffer = []
sample_count = 64

while True:
    t = time.ticks_ms() / 1000.0
    fault = (btn_fault.value() == 0) # Bouton enfoncé
    
    # Simulation du signal d'arbre à 30 Hz
    sig = 0.08 * math.sin(2 * math.pi * 30 * t)
    if fault:
        # Injection du pic de bague externe BPFO (107.4 Hz) + chocs
        sig += 1.8 * math.sin(2 * math.pi * 107.4 * t)
        
    buffer.append(sig)
    
    if len(buffer) >= sample_count:
        t0 = time.ticks_us()
        feat = extract_features(buffer)
        t_lat = time.ticks_diff(time.ticks_us(), t0)
        buffer = []
        
        k = feat["kurtosis"]
        rms = feat["rms"]
        
        if fault or k > 5.5 or rms > 0.25:
            # Panne Critique (BPFO)
            status = "CRITICAL_FAULT_BPFO"
            hi = 22.0
            led_green.value(0)
            led_yellow.value(0)
            led_red.value(1)
            relay.value(1) # E-Stop Coupure
            buzzer.value(1)
        elif k > 3.8 or rms > 0.12:
            # Alerte Dégradation
            status = "WARNING_INCIPIENT"
            hi = 68.0
            led_green.value(0)
            led_yellow.value(1)
            led_red.value(0)
            relay.value(0)
            buzzer.value(0)
        else:
            # Nominal
            status = "NOMINAL_HEALTHY"
            hi = 98.2
            led_green.value(1)
            led_yellow.value(0)
            led_red.value(0)
            relay.value(0)
            buzzer.value(0)
            
        print('{{"device":"MICROPYTHON_EDGE","status":"{}","HI":{:.1f},"kurtosis":{:.2f},"rms":{:.3f},"lat_us":{}}}'.format(
            status, hi, k, rms, t_lat
        ))
        
    time.sleep_ms(5)
