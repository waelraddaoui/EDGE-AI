/*
  =============================================================================
  WOKWI SIMULATOR - EDGE AI PREDICTIVE MAINTENANCE EMBEDDED SYSTEM
  Projet : Surveillance Vibratoire & Détection d'Anomalies de Roulement
  Cible  : ESP32 / Raspberry Pi Pico (I2C MPU6050 + OLED 128x64 + GPIOs + Relais)
  =============================================================================
*/

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ── Configuration Écran OLED I2C ──────────────────────────────────────────
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ── Capteur Accéléromètre I2C ─────────────────────────────────────────────
Adafruit_MPU6050 mpu;

// ── Brochage GPIO ESP32 ───────────────────────────────────────────────────
#define PIN_LED_GREEN   18   // Voyant Nominal (Sain)
#define PIN_LED_YELLOW  19   // Voyant Alerte Précoce
#define PIN_LED_RED     23   // Voyant Panne Critique
#define PIN_RELAY        5   // Relais d'Arrêt d'Urgence (E-Stop Coupure Moteur)
#define PIN_BUZZER       4   // Alarme Sonore Industrielle
#define PIN_BTN_FAULT   15   // Bouton d'injection d'anomalie / choc mécanique

// ── Paramètres d'Échantillonnage et Buffers ───────────────────────────────
#define SAMPLE_BUFFER_SIZE 64
float samples[SAMPLE_BUFFER_SIZE];
int sampleIndex = 0;

// Variables dynamiques
unsigned long lastInferenceTime = 0;
bool faultInjected = false;

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n========================================================");
  Serial.println(" 🍓 DEMARRAGE DU SYSTEME EMBARQUE EDGE AI (WOKWI ESP32)");
  Serial.println("========================================================");

  // 1. Configuration des Broches GPIO
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_BTN_FAULT, INPUT_PULLUP);

  // Initialisation sorties
  digitalWrite(PIN_LED_GREEN, HIGH);
  digitalWrite(PIN_LED_YELLOW, LOW);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_RELAY, LOW);
  digitalWrite(PIN_BUZZER, LOW);

  // 2. Initialisation du Bus I2C (SDA=21, SCL=22)
  Wire.begin(21, 22);

  // 3. Initialisation Écran OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("❌ Erreur allocation SSD1306");
  } else {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(10, 15);
    display.println("EDGE AI BEARING");
    display.setCursor(10, 32);
    display.println("Modele : GradientBoost");
    display.setCursor(10, 48);
    display.println("Initialisation...");
    display.display();
    delay(1200);
  }

  // 4. Initialisation MPU6050
  if (!mpu.begin()) {
    Serial.println("⚠️ MPU6050 non detecte, simulation de signaux synthetiques activee.");
  } else {
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
    Serial.println("✅ Accélérateur MPU6050 calibre avec succes (Plage +/- 16g).");
  }

  Serial.println("✅ Moteur Edge AI pret. Debut de la surveillance en continu.\n");
}

void loop() {
  // A. Détection du bouton d'injection de défaut (bouton rouge Wokwi)
  if (digitalRead(PIN_BTN_FAULT) == LOW) {
    faultInjected = true;
  }

  // B. Lecture du signal vibratoire (MPU6050 ou onde simulée)
  sensors_event_t a, g, temp;
  float raw_val = 0.0;

  if (mpu.getEvent(&a, &g, &temp)) {
    // Calcul de l'amplitude résultante moins la gravité statique (1g = 9.81)
    float ax = a.acceleration.x;
    float ay = a.acceleration.y;
    float az = a.acceleration.z - 9.81;
    raw_val = sqrt(ax * ax + ay * ay + az * az) / 9.81; // Normalisé en G
  } else {
    // Simulation physique réaliste si capteur virtuel
    float t = millis() / 1000.0;
    raw_val = 0.08 * sin(2 * 3.14159 * 29.95 * t) + ((random(-50, 50)) / 1000.0);
  }

  // Injection d'impulsion si bouton appuyé
  if (faultInjected) {
    raw_val += (random(120, 250) / 100.0) * (sin(2 * 3.14159 * 107.4 * (millis() / 1000.0)));
  }

  samples[sampleIndex++] = raw_val;

  // C. Inférence Edge AI dès que le buffer est plein (toutes les ~250 ms)
  if (sampleIndex >= SAMPLE_BUFFER_SIZE) {
    sampleIndex = 0;
    processEdgeInference();
  }

  delay(5);
}

void processEdgeInference() {
  unsigned long t_start = micros();

  // 1. Extraction des caractéristiques physiques
  float sum = 0.0;
  float sum_sq = 0.0;
  float peak = 0.0;

  for (int i = 0; i < SAMPLE_BUFFER_SIZE; i++) {
    float val = samples[i];
    sum += val;
    sum_sq += val * val;
    if (abs(val) > peak) peak = abs(val);
  }

  float mean = sum / SAMPLE_BUFFER_SIZE;
  float variance = 0.0;
  float sum_quad = 0.0;

  for (int i = 0; i < SAMPLE_BUFFER_SIZE; i++) {
    float diff = samples[i] - mean;
    variance += diff * diff;
    sum_quad += diff * diff * diff * diff;
  }
  variance /= SAMPLE_BUFFER_SIZE;
  float std_dev = sqrt(variance);
  if (std_dev < 0.0001) std_dev = 0.0001;

  float rms = sqrt(sum_sq / SAMPLE_BUFFER_SIZE);
  float kurtosis = (sum_quad / SAMPLE_BUFFER_SIZE) / (variance * variance);
  float crest_factor = peak / (rms + 0.0001);

  // 2. Modèle de Décision Edge AI (Gradient Boosting émulation)
  int state = 0; // 0 = Nominal, 1 = Alerte, 2 = Panne Critique
  float health_index = 100.0;
  String iso_zone = "Zone A";
  String diagnostic_msg = "SAIN (NOMINAL)";

  if (faultInjected || kurtosis > 5.5 || rms > 0.28) {
    state = 2; // Défaut Critique (Bague externe BPFO ou Bague interne BPFI)
    health_index = max(15.0, 95.0 * exp(-0.45 * (kurtosis - 3.0)));
    iso_zone = "Zone D (Danger)";
    diagnostic_msg = "PANNE BPFO DETECTEE!";
  } else if (kurtosis > 3.8 || rms > 0.12) {
    state = 1; // Alerte précoce
    health_index = 72.5;
    iso_zone = "Zone C (Alerte)";
    diagnostic_msg = "DEGRADATION PRECOCE";
  } else {
    state = 0; // Normal
    health_index = 98.4;
    iso_zone = "Zone A (< 1.4 mm/s)";
    diagnostic_msg = "FONCTIONNEMENT NOMINAL";
  }

  unsigned long inference_us = micros() - t_start;

  // 3. Actionnement Matériel des Broches GPIO & Relais
  if (state == 0) {
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_YELLOW, LOW);
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_RELAY, LOW);       // Relais E-Stop Fermé / Sûr
    digitalWrite(PIN_BUZZER, LOW);
  } else if (state == 1) {
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_YELLOW, HIGH);
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_RELAY, LOW);
    digitalWrite(PIN_BUZZER, LOW);
  } else {
    // État Panne Critique : Alerte et Déclenchement de la Coupure
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_YELLOW, LOW);
    digitalWrite(PIN_LED_RED, (millis() / 250) % 2); // Clignotement
    digitalWrite(PIN_RELAY, HIGH);      // OUVERTURE DU RELAIS D'URGENCE (COUPURE MOTEUR LOTO)
    digitalWrite(PIN_BUZZER, HIGH);     // Alarme sonore active
  }

  // 4. Mise à jour de l'Écran OLED 128x64
  display.clearDisplay();
  
  // En-tête
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("EDGE AI: ");
  display.println(diagnostic_msg);

  // Ligne de séparation
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);

  // Métriques
  display.setCursor(0, 14);
  display.print("Kurtosis: ");
  display.print(kurtosis, 2);
  display.print(" (Norm=3)");

  display.setCursor(0, 24);
  display.print("RMS: ");
  display.print(rms, 3);
  display.print("g | CF: ");
  display.print(crest_factor, 1);

  display.setCursor(0, 34);
  display.print("Sante (HI): ");
  display.print((int)health_index);
  display.print("% | ");
  display.print(iso_zone.substring(0, 6));

  // Jauge graphique d'Indice de Santé (Progress Bar)
  display.drawRect(0, 45, 128, 7, SSD1306_WHITE);
  int barWidth = map((int)health_index, 0, 100, 0, 124);
  display.fillRect(2, 47, barWidth, 3, SSD1306_WHITE);

  // Statut Relais & Latence
  display.setCursor(0, 56);
  if (state == 2) {
    display.print("RELAIS: COUPURE ACTIF!");
  } else {
    display.print("RELAIS: OK | Lat: ");
    display.print(inference_us);
    display.print("us");
  }

  display.display();

  // 5. Télémétrie Série IoT (Format JSON compatible passerelle MQTT)
  Serial.print("{\"device\":\"ESP32_EDGE\",\"status\":\"");
  Serial.print(diagnostic_msg);
  Serial.print("\",\"HI\":");
  Serial.print(health_index);
  Serial.print(",\"kurtosis\":");
  Serial.print(kurtosis);
  Serial.print(",\"rms\":");
  Serial.print(rms);
  Serial.print(",\"relay\":");
  Serial.print(state == 2 ? 1 : 0);
  Serial.print(",\"lat_us\":");
  Serial.print(inference_us);
  Serial.println("}");

  // Réarmement automatique après 4 secondes de panne si bouton relâché
  if (faultInjected && digitalRead(PIN_BTN_FAULT) == HIGH) {
    static int resetCounter = 0;
    if (++resetCounter > 12) {
      faultInjected = false;
      resetCounter = 0;
      digitalWrite(PIN_BUZZER, LOW);
      digitalWrite(PIN_RELAY, LOW);
    }
  }
}
