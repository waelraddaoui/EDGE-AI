/*
  =============================================================================
  PROJET PFE MASTER - EDGE AI & IOT PREDICTIVE MAINTENANCE
  FIRMWARE ESP32 OFFICIEL - AVEC SCANNER I2C ET TINYML LOCAL
  =============================================================================
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

#include "model_tinyml.h"  // Modèle TinyML & struct PredictionResult

// ── Broches Matériel ESP32 ──────────────────────────────────────────────────
#define PIN_MOS_CUTOFF   23   // Commande SIG du Module MOSFET (Sécurité coupure)
#define PIN_RGB_RED      19   // Broche R de la LED RGB HW-479
#define PIN_RGB_GREEN    18   // Broche G de la LED RGB HW-479
#define PIN_RGB_BLUE      5   // Broche B de la LED RGB HW-479
#define I2C_SDA          21   // Broche SDA (Partagée entre OLED et MPU-6050)
#define I2C_SCL          22   // Broche SCL (Partagée entre OLED et MPU-6050)

// ── Configuration Écran OLED SSD1306 ────────────────────────────────────────
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ── Capteur MPU-6050 ────────────────────────────────────────────────────────
Adafruit_MPU6050 mpu;
bool mpu_adafruit_ok = false;
bool mpu_direct_ok = false;
uint8_t mpu_addr = 0x68; // Adresse par défaut (0x68 ou 0x69)

// ── Gestion de la LED RGB (Cathode Commune par défaut) ──────────────────────
bool rgb_common_cathode = true; // Mettre false si Anode Commune

void setRGB(bool red, bool green, bool blue) {
  if (rgb_common_cathode) {
    digitalWrite(PIN_RGB_RED, red ? HIGH : LOW);
    digitalWrite(PIN_RGB_GREEN, green ? HIGH : LOW);
    digitalWrite(PIN_RGB_BLUE, blue ? HIGH : LOW);
  } else {
    digitalWrite(PIN_RGB_RED, red ? LOW : HIGH);
    digitalWrite(PIN_RGB_GREEN, green ? LOW : HIGH);
    digitalWrite(PIN_RGB_BLUE, blue ? LOW : HIGH);
  }
}

// ── Buffer d'échantillonnage vibratoire ─────────────────────────────────────
#define BUFFER_SIZE 64
float mag_buf[BUFFER_SIZE];
int buf_index = 0;

// =============================================================================
// FONCTIONS DE COMMUNICATION I2C BAS-NIVEAU (SECURE POUR CLONES)
// =============================================================================
bool testI2CAddress(uint8_t addr) {
  Wire.beginTransmission(addr);
  return (Wire.endTransmission() == 0);
}

bool initMPUDirect(uint8_t addr) {
  Wire.beginTransmission(addr);
  Wire.write(0x6B); // Registre PWR_MGMT_1
  Wire.write(0x00); // Réveil MPU-6050
  if (Wire.endTransmission(true) != 0) return false;

  Wire.beginTransmission(addr);
  Wire.write(0x1C); // Registre ACCEL_CONFIG
  Wire.write(0x18); // +/- 16G
  Wire.endTransmission(true);

  return true;
}

bool readMPURawAccel(uint8_t addr, float &ax_g, float &ay_g, float &az_g) {
  Wire.beginTransmission(addr);
  Wire.write(0x3B); // Registre ACCEL_XOUT_H
  if (Wire.endTransmission(false) != 0) return false;

  if (Wire.requestFrom((int)addr, 6, true) != 6) return false;

  int16_t raw_x = (Wire.read() << 8) | Wire.read();
  int16_t raw_y = (Wire.read() << 8) | Wire.read();
  int16_t raw_z = (Wire.read() << 8) | Wire.read();

  ax_g = (float)raw_x / 2048.0f;
  ay_g = (float)raw_y / 2048.0f;
  az_g = (float)raw_z / 2048.0f;
  return true;
}

// =============================================================================
// INITIALISATION SYSTEME (SETUP)
// =============================================================================
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n\n==========================================");
  Serial.println("  ESP32 EDGE AI - SYSTEME DE MAINTENANCE  ");
  Serial.println("==========================================");

  pinMode(PIN_MOS_CUTOFF, OUTPUT);
  pinMode(PIN_RGB_RED, OUTPUT);
  pinMode(PIN_RGB_GREEN, OUTPUT);
  pinMode(PIN_RGB_BLUE, OUTPUT);

  // Auto-test lumineux RGB au démarrage
  Serial.println("-> Test LED RGB (Rouge, Vert, Bleu)...");
  setRGB(true, false, false); delay(400); // Rouge
  setRGB(false, true, false); delay(400); // Vert
  setRGB(false, false, true); delay(400); // Bleu
  setRGB(false, false, false);

  digitalWrite(PIN_MOS_CUTOFF, HIGH);

  // Initialisation I2C sur GPIO 21 (SDA) et GPIO 22 (SCL)
  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(100000); // 100 kHz standard

  // Initialisation OLED (0x3C)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 5);
  display.println("DIAGNOSTIC EDGE AI");
  display.setCursor(0, 20);
  display.println("Scan du bus I2C...");
  display.display();
  delay(800);

  // SCAN COMPLET DU BUS I2C
  bool found_oled = testI2CAddress(0x3C);
  bool found_mpu68 = testI2CAddress(0x68);
  bool found_mpu69 = testI2CAddress(0x69);

  Serial.print("OLED (0x3C)  : "); Serial.println(found_oled ? "OK" : "NON VU");
  Serial.print("MPU  (0x68)  : "); Serial.println(found_mpu68 ? "OK DETECTE !" : "NON VU");
  Serial.print("MPU  (0x69)  : "); Serial.println(found_mpu69 ? "OK DETECTE !" : "NON VU");

  if (found_mpu68) mpu_addr = 0x68;
  else if (found_mpu69) mpu_addr = 0x69;

  // Tentative Méthode 1 : Adafruit_MPU6050
  if (found_mpu68 || found_mpu69) {
    if (mpu.begin(mpu_addr)) {
      mpu_adafruit_ok = true;
      mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
      mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
      Serial.println("✅ MPU-6050 initialise via Adafruit_MPU6050 !");
    } else {
      // Méthode 2 : Pilote Direct Wire (si clone chinois)
      if (initMPUDirect(mpu_addr)) {
        mpu_direct_ok = true;
        Serial.println("✅ MPU-6050 initialise via Pilote Direct Wire !");
      }
    }
  }

  bool is_ready = (mpu_adafruit_ok || mpu_direct_ok);

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("=== STATUT MATERIEL ===");
  display.setCursor(0, 16);
  display.print("OLED: "); display.println(found_oled ? "OK (0x3C)" : "ERREUR");
  display.setCursor(0, 30);
  display.print("MPU : ");
  if (is_ready) {
    display.print("OK (0x"); display.print(mpu_addr, HEX); display.println(")");
    setRGB(false, true, false); // Vert = Pret
  } else {
    display.println("NON DETECTE !");
    setRGB(true, false, false); // Rouge = Erreur
  }
  display.setCursor(0, 48);
  display.println(is_ready ? "DEMARRAGE IA..." : "VERIFIEZ LES FILS");
  display.display();
  delay(1500);
}

// =============================================================================
// BOUCLE PRINCIPALE (LOOP)
// =============================================================================
void runInference();

void loop() {
  float ax = 0.0f, ay = 0.0f, az = 0.0f;
  bool read_ok = false;

  if (mpu_adafruit_ok) {
    sensors_event_t a, g, temp;
    if (mpu.getEvent(&a, &g, &temp)) {
      ax = a.acceleration.x / 9.81f;
      ay = a.acceleration.y / 9.81f;
      az = (a.acceleration.z - 9.81f) / 9.81f;
      read_ok = true;
    }
  } else if (mpu_direct_ok) {
    read_ok = readMPURawAccel(mpu_addr, ax, ay, az);
    az -= 1.0f; // Gravité 1g
  }

  if (!read_ok) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("MPU-6050 NON DETECTE");
    display.setCursor(0, 14);
    display.println("UCC -> 3.3V (Fil Droit)");
    display.setCursor(0, 26);
    display.println("GND -> Masse (Blanc)");
    display.setCursor(0, 38);
    display.println("SCL -> D22   (Noir)");
    display.setCursor(0, 50);
    display.println("SDA -> D21   (Orange)");
    display.display();

    setRGB(true, false, false); delay(250);
    setRGB(false, false, false); delay(250);

    // Tentative de reconnexion automatique en continu
    if (testI2CAddress(0x68)) {
      mpu_addr = 0x68;
      if (mpu.begin(0x68)) mpu_adafruit_ok = true;
      else if (initMPUDirect(0x68)) mpu_direct_ok = true;
    } else if (testI2CAddress(0x69)) {
      mpu_addr = 0x69;
      if (mpu.begin(0x69)) mpu_adafruit_ok = true;
      else if (initMPUDirect(0x69)) mpu_direct_ok = true;
    }
    return;
  }

  // Calcul magnitude d'accélération
  float mag = sqrtf(ax * ax + ay * ay + az * az);
  mag_buf[buf_index++] = mag;

  if (buf_index >= BUFFER_SIZE) {
    buf_index = 0;
    runInference();
  }

  delay(4); // Fréquence d'échantillonnage ~250 Hz
}

// =============================================================================
// INFERENCE TINYML & GESTION ACTIONNEURS
// =============================================================================
void runInference() {
  float sum = 0.0f, sum_sq = 0.0f;
  float min_val = mag_buf[0], max_val = mag_buf[0];

  for (int i = 0; i < BUFFER_SIZE; i++) {
    float v = mag_buf[i];
    sum += v;
    sum_sq += v * v;
    if (v < min_val) min_val = v;
    if (v > max_val) max_val = v;
  }

  float mean = sum / BUFFER_SIZE;
  float rms = sqrtf(sum_sq / BUFFER_SIZE);
  float p2p = max_val - min_val;

  float var_sum = 0.0f, skew_sum = 0.0f, kurt_sum = 0.0f;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    float d = mag_buf[i] - mean;
    float d2 = d * d;
    var_sum += d2;
    skew_sum += d2 * d;
    kurt_sum += d2 * d2;
  }
  float variance = var_sum / BUFFER_SIZE;
  float std_dev = sqrtf(variance > 0.0001f ? variance : 0.0001f);
  float kurtosis = (kurt_sum / BUFFER_SIZE) / (variance * variance + 0.0001f);
  float crest_factor = rms > 0.0001f ? (max_val / rms) : 1.0f;

  // Vecteur de features pour le modèle Gradient Boosting
  float features[16];
  features[0] = mean;
  features[1] = std_dev;
  features[2] = variance;
  features[3] = rms;
  features[4] = min_val;
  features[5] = max_val;
  features[6] = p2p;
  features[7] = sum_sq;
  features[8] = (skew_sum / BUFFER_SIZE) / (std_dev * std_dev * std_dev + 0.0001f);
  features[9] = kurtosis;
  features[10] = crest_factor;
  features[11] = max_val / (mean + 0.0001f);
  features[12] = rms * 2000.0f;
  features[13] = kurtosis * 350.0f;
  features[14] = 2580.0f;
  features[15] = 1320.0f;

  // Inférence locale via model_tinyml.h
  PredictionResult pred = predict_bearing_health(features);

  bool is_fault = (pred.predicted_class == 1 || kurtosis > 4.5f || rms > 0.18f);

  if (is_fault) {
    setRGB(true, false, false);          // LED ROUGE
    digitalWrite(PIN_MOS_CUTOFF, LOW);    // COUPURE MOTEUR (LOTO)
  } else {
    setRGB(false, true, false);         // LED VERTE
    digitalWrite(PIN_MOS_CUTOFF, HIGH);   // MOTEUR ACTIVE
  }

  // Télémétrie Série JSON (115200 bauds)
  Serial.print("{\"rms\":"); Serial.print(rms, 4);
  Serial.print(",\"kurtosis\":"); Serial.print(kurtosis, 2);
  Serial.print(",\"health\":"); Serial.print(pred.health_index, 1);
  Serial.print(",\"fault\":"); Serial.print(is_fault ? 1 : 0);
  Serial.println("}");

  // Affichage OLED
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("RMS: "); display.print(rms, 3); display.print("g ");
  display.print("K: "); display.print(kurtosis, 1);

  display.setCursor(0, 16);
  if (is_fault) {
    display.print("ETAT: DEFAUT DETECTE!");
  } else {
    display.print("ETAT: MACHINE SAINE");
  }

  display.setCursor(0, 32);
  display.print("SANTE: ");
  display.print(pred.health_index, 1);
  display.print(" %");

  // Jauge de santé
  display.drawRect(0, 46, 128, 8, SSD1306_WHITE);
  int bar_w = (int)((pred.health_index / 100.0f) * 124);
  if (bar_w < 0) bar_w = 0;
  if (bar_w > 124) bar_w = 124;
  display.fillRect(2, 48, bar_w, 4, SSD1306_WHITE);

  display.setCursor(0, 56);
  display.print("TinyML Local - 250Hz");
  display.display();
}