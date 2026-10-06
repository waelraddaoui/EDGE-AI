"""
src/train_models.py
-------------------
Module 3 : Entraînement des modèles IA légers pour la détection d'anomalies.

Entraîne et sauvegarde 5 modèles candidats :
1. Isolation Forest (Baseline non-supervisée)
2. Random Forest Légers (Supervisé)
3. Gradient Boosting / XGBoost Légers
4. Autoencodeur compact PyTorch (Reconstruction non-supervisée)
5. 1D-CNN compact PyTorch

Conforme aux exigences F3.1 à F3.7 du Cahier des Charges.
"""

import os
import numpy as np
import joblib

# Mettre PyTorch avant sklearn pour eviter le conflit OpenMP (Access Violation 0xC0000005)
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingClassifier


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(MODELS_DIR, exist_ok=True)

# -------------------------------------------------------------
# PyTorch Architectures (Autoencodeur & 1D-CNN)
# -------------------------------------------------------------
class CompactAutoencoder(nn.Module):
    def __init__(self, input_dim=16):
        super(CompactAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, input_dim)
        )
        
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class Compact1DCNN(nn.Module):
    def __init__(self, input_dim=16):
        super(Compact1DCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(1, 8, kernel_size=3, padding=1),
            nn.BatchNorm1d(8),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(8, 16, kernel_size=3, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(4)
        )
        self.fc = nn.Sequential(
            nn.Linear(16 * 4, 16),
            nn.ReLU(),
            nn.Linear(16, 2)
        )
        
    def forward(self, x):
        # x shape: (batch_size, 16) -> (batch_size, 1, 16)
        x = x.unsqueeze(1)
        feat = self.conv(x)
        feat = feat.view(feat.size(0), -1)
        out = self.fc(feat)
        return out

def train_all_models():
    print("=== Module 3 : Entrainement des Modeles IA Legers ===")
    
    split_data = np.load(os.path.join(DATA_PROCESSED_DIR, 'dataset_split.npz'))
    X_train = split_data['X_train']
    y_train = split_data['y_train']
    X_val = split_data['X_val']
    y_val = split_data['y_val']
    
    # -------------------------------------------------------------
    # 1. Isolation Forest (Non surveille - Entraine sur classe normale = 0)
    # -------------------------------------------------------------
    print("Entrainement 1/5 : Isolation Forest...")
    X_train_normal = X_train[y_train == 0]
    iso_forest = IsolationForest(n_estimators=50, contamination=0.01, random_state=42)
    iso_forest.fit(X_train_normal)
    joblib.dump(iso_forest, os.path.join(MODELS_DIR, 'isolation_forest.joblib'))
    
    # -------------------------------------------------------------
    # 2. Random Forest Leger
    # -------------------------------------------------------------
    print("Entrainement 2/5 : Random Forest Leger...")
    rf_model = RandomForestClassifier(n_estimators=30, max_depth=6, random_state=42)
    rf_model.fit(X_train, y_train)
    joblib.dump(rf_model, os.path.join(MODELS_DIR, 'random_forest.joblib'))
    
    # -------------------------------------------------------------
    # 3. XGBoost & LightGBM Optimisés pour l'Embarqué Edge AI
    # -------------------------------------------------------------
    print("Entrainement 3/5 : XGBoost & LightGBM Légers...")
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier

    xgb_model = XGBClassifier(n_estimators=30, max_depth=3, learning_rate=0.1, random_state=42, eval_metric='logloss')
    xgb_model.fit(X_train, y_train)
    joblib.dump(xgb_model, os.path.join(MODELS_DIR, 'xgboost.joblib'))

    lgb_model = LGBMClassifier(n_estimators=30, max_depth=3, learning_rate=0.1, random_state=42, verbose=-1)
    lgb_model.fit(X_train, y_train)
    joblib.dump(lgb_model, os.path.join(MODELS_DIR, 'lightgbm.joblib'))

    # Sauvegarde du modèle XGBoost à la place de gradient_boosting.joblib pour de meilleures performances
    joblib.dump(xgb_model, os.path.join(MODELS_DIR, 'gradient_boosting.joblib'))
    
    # -------------------------------------------------------------
    # 4. Autoencodeur Compact (PyTorch)
    # -------------------------------------------------------------
    print("Entrainement 4/5 : Autoencodeur Compact PyTorch...")
    autoencoder = CompactAutoencoder(input_dim=16)
    criterion_ae = nn.MSELoss()
    optimizer_ae = optim.Adam(autoencoder.parameters(), lr=0.01)
    
    train_normal_tensor = torch.tensor(X_train_normal, dtype=torch.float32)
    
    autoencoder.train()
    for epoch in range(40):
        optimizer_ae.zero_grad()
        recon = autoencoder(train_normal_tensor)
        loss = criterion_ae(recon, train_normal_tensor)
        loss.backward()
        optimizer_ae.step()
            
    torch.save(autoencoder.state_dict(), os.path.join(MODELS_DIR, 'autoencoder.pth'))
    
    autoencoder.eval()
    with torch.no_grad():
        recon_train = autoencoder(train_normal_tensor)
        errors = torch.mean((recon_train - train_normal_tensor) ** 2, dim=1).numpy()
        ae_threshold = float(np.percentile(errors, 95))
        
    np.save(os.path.join(MODELS_DIR, 'ae_threshold.npy'), np.array([ae_threshold]))
    
    # -------------------------------------------------------------
    # 5. 1D-CNN Compact (PyTorch)
    # -------------------------------------------------------------
    print("Entrainement 5/5 : 1D-CNN Compact PyTorch...")
    cnn_model = Compact1DCNN(input_dim=16)
    criterion_cnn = nn.CrossEntropyLoss()
    optimizer_cnn = optim.Adam(cnn_model.parameters(), lr=0.01)
    
    tensor_x = torch.tensor(X_train, dtype=torch.float32)
    tensor_y = torch.tensor(y_train, dtype=torch.long)
    
    cnn_model.train()
    for epoch in range(50):
        optimizer_cnn.zero_grad()
        out = cnn_model(tensor_x)
        loss = criterion_cnn(out, tensor_y)
        loss.backward()
        optimizer_cnn.step()
            
    torch.save(cnn_model.state_dict(), os.path.join(MODELS_DIR, 'cnn_1d.pth'))
    
    print("[OK] Tous les 5 modeles de detection d'anomalies ont ete entraines et sauvegardes.")

if __name__ == '__main__':
    train_all_models()
