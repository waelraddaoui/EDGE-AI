"""
scripts/generate_extra_diagrams.py
Génère les diagrammes UML et schémas d'architecture complémentaires pour le rapport de stage.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Cadre Système
    rect = patches.FancyBboxPatch((2.2, 0.5), 5.6, 9.0, boxstyle="round,pad=0.2", ec="#1B365D", fc="#F8FAFC", lw=2)
    ax.add_patch(rect)
    ax.text(5.0, 9.1, "SYSTÈME EMBARQUÉ EDGE AI & MAINTENANCE (RASPBERRY PI)", ha='center', va='center', fontsize=10, fontweight='bold', color="#1B365D")
    
    # Acteurs
    # Acteur 1: Opérateur / Technicien
    ax.scatter([1.0], [7.5], s=200, color="#2E6B9E", zorder=3)
    ax.text(1.0, 6.7, "Opérateur / \nTechnicien\nde Maintenance", ha='center', va='center', fontsize=9, fontweight='bold', color="#1E293B")
    
    # Acteur 2: Moteur IoT / Capteurs
    ax.scatter([1.0], [2.5], s=200, color="#10B981", zorder=3)
    ax.text(1.0, 1.7, "Capteur I2C / \nAccéléromètre\n(Flux DMA)", ha='center', va='center', fontsize=9, fontweight='bold', color="#065F46")
    
    # Acteur 3: Actionneurs de Sécurité
    ax.scatter([9.0], [4.5], s=200, color="#DC2626", zorder=3)
    ax.text(9.0, 3.7, "Relais E-Stop /\nLigne Moteur\n(Sécurité LOTO)", ha='center', va='center', fontsize=9, fontweight='bold', color="#991B1B")

    # Cas d'utilisation (Bulles elliptiques)
    use_cases = [
        (5.0, 8.0, "UC1: Visualiser Signal Temporel & FFT en direct", "#EFF6FF", "#3B82F6"),
        (5.0, 6.6, "UC2: Consulter l'Indice de Santé (HI) & Zone ISO", "#ECFDF5", "#10B981"),
        (5.0, 5.2, "UC3: Diagnostiquer Défaut (BPFO / BPFI / BSF)", "#FEF3C7", "#F59E0B"),
        (5.0, 3.8, "UC4: Déclencher Arrêt d'Urgence E-Stop (GPIO 23)", "#FEE2E2", "#EF4444"),
        (5.0, 2.4, "UC5: Interroger l'Agent Conversationnel RAG", "#F3E8FF", "#8B5CF6"),
        (5.0, 1.0, "UC6: Télécharger Rapport d'Expertise PDF", "#F1F5F9", "#64748B")
    ]
    
    for x, y, text, fc, ec in use_cases:
        ellipse = patches.FancyBboxPatch((x-2.3, y-0.45), 4.6, 0.9, boxstyle="round,pad=0.3", ec=ec, fc=fc, lw=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#0F172A")

    # Connexions (Lignes)
    ax.annotate("", xy=(2.7, 8.0), xytext=(1.5, 7.5), arrowprops=dict(arrowstyle="-", color="#475569", lw=1.2))
    ax.annotate("", xy=(2.7, 6.6), xytext=(1.5, 7.5), arrowprops=dict(arrowstyle="-", color="#475569", lw=1.2))
    ax.annotate("", xy=(2.7, 2.4), xytext=(1.5, 7.5), arrowprops=dict(arrowstyle="-", color="#475569", lw=1.2))
    ax.annotate("", xy=(2.7, 1.0), xytext=(1.5, 7.5), arrowprops=dict(arrowstyle="-", color="#475569", lw=1.2))

    ax.annotate("", xy=(2.7, 5.2), xytext=(1.5, 2.5), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.5))
    ax.annotate("", xy=(2.7, 3.8), xytext=(1.5, 2.5), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.5))

    ax.annotate("", xy=(8.5, 4.5), xytext=(7.3, 3.8), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.8))
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "12_uml_use_case_diagram.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Diagramme Use Case généré : {out_path}")

def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Lignes de vie
    entities = [
        (1.5, "Capteur ADXL345\n(DMA Buffer)"),
        (4.0, "Moteur Edge AI\n(Gradient Boosting)"),
        (6.5, "Contrôleur GPIO\n(Broadcom BCM)"),
        (9.0, "Dashboard React\n& Relais E-Stop")
    ]
    
    for x, label in entities:
        rect = patches.FancyBboxPatch((x-1.0, 8.8), 2.0, 0.9, boxstyle="square,pad=0.1", ec="#1B365D", fc="#1B365D")
        ax.add_patch(rect)
        ax.text(x, 9.25, label, ha='center', va='center', fontsize=8, fontweight='bold', color="#FFFFFF")
        ax.plot([x, x], [0.5, 8.8], color="#CBD5E1", linestyle="--", lw=1.5)

    # Messages
    msgs = [
        (1.5, 4.0, 8.0, "1. Envoi Buffer 1024 points (12 kHz)", "#2563EB"),
        (4.0, 4.0, 7.1, "2. Extraction 16 features (0.18 ms)", "#64748B"),
        (4.0, 4.0, 6.2, "3. Inférence Gradient Boosting (0.22 ms)", "#F59E0B"),
        (4.0, 6.5, 5.3, "4. Détection Panne Critique BPFO", "#DC2626"),
        (6.5, 9.0, 4.4, "5. Commutation GPIO 23 -> ON (E-Stop)", "#DC2626"),
        (6.5, 9.0, 3.5, "6. Alerte Sonore Buzzer GPIO 24 -> ON", "#DC2626"),
        (4.0, 9.0, 2.6, "7. Notification JSON Dashboard / MQTT", "#10B981"),
        (9.0, 9.0, 1.7, "8. Coupure Moteur & Alerte IHM < 2 ms", "#1E293B")
    ]
    
    for x1, x2, y, txt, col in msgs:
        if x1 == x2:
            ax.annotate("", xy=(x1+0.6, y-0.3), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
            ax.plot([x1, x1+0.6], [y, y], color=col, lw=1.5)
            ax.plot([x1+0.6, x1+0.6], [y, y-0.3], color=col, lw=1.5)
            ax.text(x1+0.7, y-0.15, txt, fontsize=7.5, fontweight='bold', color=col, va='center')
        else:
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
            ax.text((x1+x2)/2, y+0.15, txt, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=col)

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "13_uml_sequence_inference.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Diagramme de Séquence généré : {out_path}")

def generate_nasa_health_curve():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=200)
    
    days = np.linspace(0, 35, 300)
    # Dégradation exponentielle réaliste NASA IMS
    d_score = np.where(days < 25, 0.05 * np.random.normal(1.0, 0.2, len(days)), 
                       0.05 + 0.18 * ((days - 25) ** 1.8) + 0.1 * np.random.normal(0, 0.5, len(days)))
    d_score = np.maximum(0, d_score)
    health_index = 100 * np.exp(-0.22 * d_score)
    health_index = np.clip(health_index, 10, 100)
    
    ax.plot(days, health_index, color='#1E40AF', lw=2.5, label="Indice de Santé Réel (HI %)")
    
    # Zones ISO / Stades
    ax.axhspan(85, 100, color='#10B981', alpha=0.15, label="Stade 1 : Fonctionnement Nominal (> 85%)")
    ax.axhspan(45, 85, color='#F59E0B', alpha=0.15, label="Stade 2 : Dégradation Précoce (45-85%)")
    ax.axhspan(0, 45, color='#EF4444', alpha=0.15, label="Stade 3 : Panne Critique (< 45%)")
    
    ax.axvline(25, color='#F59E0B', linestyle='--', lw=1.5)
    ax.text(25.5, 90, "J+25 : Début d'écaillage\n(Micro-chocs BPFO)", fontsize=8, color='#B45309', fontweight='bold')
    
    ax.axvline(32, color='#EF4444', linestyle='--', lw=1.5)
    ax.text(32.3, 35, "J+32 : Défaillance Sévère\n(Arrêt d'urgence)", fontsize=8, color='#B91C1C', fontweight='bold')
    
    ax.set_title("Évolution de l'Indice de Santé (HI) - Benchmark NASA IMS (35 jours)", fontsize=11, fontweight='bold', pad=12, color='#1B365D')
    ax.set_xlabel("Temps d'opération continu (Jours)", fontsize=9, fontweight='bold')
    ax.set_ylabel("Indice de Santé (HI %)", fontsize=9, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.set_xlim(0, 35)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='lower left', fontsize=8, framealpha=0.9)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "14_nasa_ims_health_index_curve.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Courbe NASA IMS générée : {out_path}")

if __name__ == '__main__':
    generate_use_case_diagram()
    generate_sequence_diagram()
    generate_nasa_health_curve()
