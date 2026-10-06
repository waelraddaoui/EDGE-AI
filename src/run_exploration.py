"""
src/run_exploration.py
----------------------
Module 1 & 2 : Analyse exploratoire des signaux et fenêtrage temporel.
Génère le notebook 'notebooks/01_exploration.ipynb' et enregistre les figures scientifiques dans 'figures/'.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'notebooks')

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def run_exploration():
    print("=== Séance 2 : Analyse Exploratoire & Visualisation des Signaux CWRU ===")
    
    # 1. Chargement des signaux
    raw_path = os.path.join(DATA_RAW_DIR, 'cwru_raw_signals.parquet')
    hybrid_path = os.path.join(DATA_RAW_DIR, 'cwru_hybrid_noisy.parquet')
    
    df_raw = pd.read_parquet(raw_path)
    df_hybrid = pd.read_parquet(hybrid_path)
    
    print(f"Dataset Brut charge : {df_raw.shape}")
    print(f"Dataset Hybride charge : {df_hybrid.shape}")
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # -------------------------------------------------------------
    # Figure 1 : Signaux Temporels Bruts par Etat de Fonctionnement
    # -------------------------------------------------------------
    labels_to_plot = ['Normal', 'InnerRace_014', 'OuterRace_014', 'Ball_014']
    colors = ['#2ca02c', '#d62728', '#ff7f0e', '#1f77b4']
    
    fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
    fig.suptitle('Signaux Vibratoires Bruts CWRU (Accélération en g) - Sampling 12 kHz', fontsize=14, fontweight='bold')
    
    for ax, label_name, color in zip(axes, labels_to_plot, colors):
        subset = df_raw[(df_raw['label'] == label_name) & (df_raw['time_s'] <= 0.2)]
        ax.plot(subset['time_s'], subset['vibration_acc'], color=color, linewidth=1.0, label=label_name)
        ax.set_ylabel('Acc (g)', fontsize=10)
        ax.legend(loc='upper right', frameon=True)
        ax.set_ylim(-4, 4)
        
    axes[-1].set_xlabel('Temps (s)', fontsize=11)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURES_DIR, '01_raw_signals_time_domain.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[OK] Figure 1 generee : {fig1_path}")
    
    # -------------------------------------------------------------
    # Figure 2 : Comparaison Signal Propre vs Perturbé (Dataset Hybride)
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    fig.suptitle('Impact des Perturbations Industrielles sur le Signal Vibratoire (Bague Interne 0.014")', fontsize=13, fontweight='bold')
    
    sub_raw = df_raw[(df_raw['label'] == 'InnerRace_014') & (df_raw['time_s'] <= 0.5)]
    sub_hyb = df_hybrid[(df_hybrid['label'] == 'InnerRace_014') & (df_hybrid['time_s'] <= 0.5)]
    
    ax1.plot(sub_raw['time_s'], sub_raw['vibration_acc'], color='#d62728', label='Signal Brut (Propre)')
    ax1.set_ylabel('Acc (g)')
    ax1.legend(loc='upper right')
    
    ax2.plot(sub_hyb['time_s'], sub_hyb['vibration_acc_noisy'], color='#9467bd', label='Signal Hybride (Bruit + Dérive + Pertes)')
    ax2.set_ylabel('Acc (g)')
    ax2.set_xlabel('Temps (s)')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    fig2_path = os.path.join(FIGURES_DIR, '02_hybrid_disturbances_comparison.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[OK] Figure 2 generee : {fig2_path}")
    
    # -------------------------------------------------------------
    # Figure 3 : Principe du Fenêtrage Temporel Glissant
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 4))
    sub_norm = df_raw[(df_raw['label'] == 'Normal') & (df_raw['time_s'] <= 0.2)]
    ax.plot(sub_norm['time_s'], sub_norm['vibration_acc'], color='#2ca02c', alpha=0.7, label='Signal continu')
    
    # Fenêtre 1 (0 à 1024 points ~ 0.085s)
    ax.axvspan(0.0, 1024/12000, color='blue', alpha=0.2, label='Fenêtre N (1024 pts)')
    # Fenêtre 2 (512 à 1536 points ~ 0.042s à 0.128s)
    ax.axvspan(512/12000, 1536/12000, color='orange', alpha=0.2, label='Fenêtre N+1 (Recouvrement 50%)')
    
    ax.set_title('Principe de Fenêtrage Glissant (Taille W=1024 points, Pas S=512 points)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Acc (g)')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    fig3_path = os.path.join(FIGURES_DIR, '03_windowing_illustration.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[OK] Figure 3 generee : {fig3_path}")
    
    # -------------------------------------------------------------
    # Création du Notebook Jupyter 01_exploration.ipynb (Format JSON)
    # -------------------------------------------------------------
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Notebook 01 : Analyse Exploratoire du Dataset CWRU\n",
                    "Ce notebook présente l'analyse exploratoire des signaux vibratoires bruts du dataset CWRU, la comparaison avec le dataset hybride perturbé, et le principe du fenêtrage temporel."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "import json\n",
                    "\n",
                    "# Chargement des métadonnées\n",
                    "with open('../data/raw/dataset_metadata.json', 'r') as f:\n",
                    "    meta = json.load(f)\n",
                    "print('Métadonnées :', json.dumps(meta, indent=2))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Visualisation des Signaux Bruts par Classe"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df_raw = pd.read_parquet('../data/raw/cwru_raw_signals.parquet')\n",
                    "df_raw.head()"
                ]
            }
        ],
        "metadata": {
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    nb_path = os.path.join(NOTEBOOKS_DIR, '01_exploration.ipynb')
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_content, f, indent=2)
    print(f"[OK] Notebook cree : {nb_path}")

if __name__ == '__main__':
    run_exploration()
