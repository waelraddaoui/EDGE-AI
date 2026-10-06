"""
raspberry/inference_edge.py
---------------------------
Séance 5 : Moteur d'Inférence Embarquée & Simulation IoT Streaming.

Simule l'acquisition en direct de signaux vibratoires (16 caractéristiques extraites),
les normalise avec le scaler sauvegardé, et exécute l'inférence en temps réel
avec journalisation JSON dans raspberry/logs/inference_stream.log.

Prend en charge :
- Isolation Forest
- Random Forest
- Gradient Boosting
- Autoencodeur Compact PyTorch
- 1D-CNN Compact PyTorch

Conforme aux exigences F4.1 à F4.4 du Cahier des Charges.
"""

import os
import sys
import time
import json
import numpy as np
import joblib
import torch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'raspberry', 'logs')

os.makedirs(LOGS_DIR, exist_ok=True)

# Import local architecture definitions
sys.path.append(os.path.join(BASE_DIR, 'src'))
try:
    from train_models import CompactAutoencoder, Compact1DCNN
except ImportError:
    import torch.nn as nn
    class CompactAutoencoder(nn.Module):
        def __init__(self, input_dim=16):
            super(CompactAutoencoder, self).__init__()
            self.encoder = nn.Sequential(nn.Linear(input_dim, 8), nn.ReLU(), nn.Linear(8, 4), nn.ReLU())
            self.decoder = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, input_dim))
        def forward(self, x):
            return self.decoder(self.encoder(x))

    class Compact1DCNN(nn.Module):
        def __init__(self, input_dim=16):
            super(Compact1DCNN, self).__init__()
            self.conv = nn.Sequential(
                nn.Conv1d(1, 8, kernel_size=3, padding=1), nn.BatchNorm1d(8), nn.ReLU(), nn.MaxPool1d(2),
                nn.Conv1d(8, 16, kernel_size=3, padding=1), nn.BatchNorm1d(16), nn.ReLU(), nn.AdaptiveAvgPool1d(4)
            )
            self.fc = nn.Sequential(nn.Linear(16 * 4, 16), nn.ReLU(), nn.Linear(16, 2))
        def forward(self, x):
            x = x.unsqueeze(1)
            feat = self.conv(x)
            feat = feat.view(feat.size(0), -1)
            return self.fc(feat)


class EdgeInferenceEngine:
    def __init__(self, model_name='Random Forest'):
        self.model_name = model_name
        self.scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.joblib'))
        self.model = None
        self.ae_threshold = None
        self._load_model()

    def _load_model(self):
        if self.model_name == 'Isolation Forest':
            self.model = joblib.load(os.path.join(MODELS_DIR, 'isolation_forest.joblib'))
        elif self.model_name == 'Random Forest':
            self.model = joblib.load(os.path.join(MODELS_DIR, 'random_forest.joblib'))
        elif self.model_name == 'Gradient Boosting':
            self.model = joblib.load(os.path.join(MODELS_DIR, 'gradient_boosting.joblib'))
        elif self.model_name == 'Autoencodeur':
            self.model = CompactAutoencoder(input_dim=16)
            self.model.load_state_dict(torch.load(os.path.join(MODELS_DIR, 'autoencoder.pth'), weights_only=False))
            self.model.eval()
            self.ae_threshold = float(np.load(os.path.join(MODELS_DIR, 'ae_threshold.npy'))[0])
        elif self.model_name == '1D-CNN':
            self.model = Compact1DCNN(input_dim=16)
            self.model.load_state_dict(torch.load(os.path.join(MODELS_DIR, 'cnn_1d.pth'), weights_only=False))
            self.model.eval()
        else:
            raise ValueError(f"Modèle inconnu : {self.model_name}")

    def predict_sample(self, features_1d):
        """
        Effectue l'inférence sur une seule fenêtre de caractéristiques (1D array len=16).
        Retourne : dict(is_anomaly=bool, score=float, latency_ms=float)
        """
        sample_batch = features_1d.reshape(1, -1)
        start_t = time.perf_counter()

        if self.model_name == 'Isolation Forest':
            pred_raw = self.model.predict(sample_batch)[0]
            is_anomaly = bool(pred_raw == -1)
            score = float(-self.model.score_samples(sample_batch)[0])
        elif self.model_name in ['Random Forest', 'Gradient Boosting']:
            pred_class = self.model.predict(sample_batch)[0]
            prob = self.model.predict_proba(sample_batch)[0, 1]
            is_anomaly = bool(pred_class == 1)
            score = float(prob)
        elif self.model_name == 'Autoencodeur':
            tensor_x = torch.tensor(sample_batch, dtype=torch.float32)
            with torch.no_grad():
                recon = self.model(tensor_x)
                rec_err = float(torch.mean((recon - tensor_x) ** 2).item())
            is_anomaly = bool(rec_err > self.ae_threshold)
            score = float(rec_err)
        elif self.model_name == '1D-CNN':
            tensor_x = torch.tensor(sample_batch, dtype=torch.float32)
            with torch.no_grad():
                logits = self.model(tensor_x)
                prob = float(torch.softmax(logits, dim=1)[0, 1].item())
                pred_class = int(torch.argmax(logits, dim=1)[0].item())
            is_anomaly = bool(pred_class == 1)
            score = float(prob)

        latency_ms = (time.perf_counter() - start_t) * 1000.0
        return {
            'is_anomaly': is_anomaly,
            'score': round(score, 4),
            'latency_ms': round(latency_ms, 4)
        }


def run_streaming_simulation(model_name='Random Forest', num_samples=100, delay_sec=0.01):
    print(f"=== Séance 5 : Inférence Edge Streaming [{model_name}] ===")
    split_data = np.load(os.path.join(DATA_PROCESSED_DIR, 'dataset_split.npz'))
    X_test = split_data['X_test']
    y_test = split_data['y_test']

    engine = EdgeInferenceEngine(model_name=model_name)
    log_file = os.path.join(LOGS_DIR, 'inference_stream.log')

    indices = np.random.choice(len(X_test), size=min(num_samples, len(X_test)), replace=False)
    latencies = []
    correct_count = 0

    with open(log_file, 'w', encoding='utf-8') as f_log:
        for idx, sample_id in enumerate(indices):
            x_sample = X_test[sample_id]
            true_label = int(y_test[sample_id])

            res = engine.predict_sample(x_sample)
            latencies.append(res['latency_ms'])

            pred_label = 1 if res['is_anomaly'] else 0
            if pred_label == true_label:
                correct_count += 1

            log_entry = {
                'sample_idx': idx,
                'sample_id': int(sample_id),
                'timestamp': time.time(),
                'model': model_name,
                'true_label': true_label,
                'predicted_anomaly': res['is_anomaly'],
                'confidence_score': res['score'],
                'latency_ms': res['latency_ms']
            }
            f_log.write(json.dumps(log_entry) + '\n')

            if delay_sec > 0:
                time.sleep(delay_sec)

    accuracy = (correct_count / len(indices)) * 100.0
    avg_lat = np.mean(latencies)
    p95_lat = np.percentile(latencies, 95)

    print(f"[OK] Simulation terminee ({len(indices)} echantillons).")
    print(f"   Accuracy en direct : {accuracy:.2f}%")
    print(f"   Latence moyenne    : {avg_lat:.3f} ms / fenetre")
    print(f"   Latence P95        : {p95_lat:.3f} ms / fenetre")
    print(f"   Log journalise dans : {log_file}")


if __name__ == '__main__':
    run_streaming_simulation(model_name='Random Forest', num_samples=100, delay_sec=0.001)
