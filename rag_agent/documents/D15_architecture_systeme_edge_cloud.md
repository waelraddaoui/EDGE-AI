# Document D15 : Architecture Complète du Système Edge AI, Backend FastAPI et Frontend React

## Vue d'Ensemble de l'Architecture Système
Le projet implémente une chaîne complète de maintenance prédictive Industrie 4.0 fonctionnant 100% en local sur **Raspberry Pi** :

```
[Capteurs IoT / Fichiers Audio & Vibrations]
                    │
                    ▼
[Moteur d'Inférence Edge AI sur Raspberry Pi]
  • Extraction 16 caractéristiques temporelles & FFT (0.18 ms)
  • Modèle Champion : Gradient Boosting (latence 0.218 ms, RAM 3.8 Mo)
  • Moteur XAI : Importance des variables & Z-scores
  • Moteur Pronostic : Indice de Santé (NASA IMS) + RUL
                    │
                    ▼ (Appel REST asynchrone)
[Serveur Backend FastAPI (Python)]
  • Endpoints : /api/predict/upload, /api/predict/simulate, /api/chat, /api/report/pdf
  • Agent RAG Sémantique (Sentence-Transformers MiniLM-L12-v2)
  • Générateur de rapports PDF professionnels (ReportLab)
                    │
                    ▼ (WebSockets / HTTP JSON)
[Interface Utilisateur React 19 + Vite]
  • Design Glassmorphism Dual (Mode Sombre / Mode Clair)
  • Visualisation FFT avec 4 Marqueurs Cinématiques (fr, BPFO, BPFI, BSF)
  • Lecteur Web Audio API (Écoute acoustique du roulement en temps réel)
  • Chatbot RAG interactif avec mémoire de diagnostic
```

## Caractéristiques Techniques et Spécifications Matérielles
- **Cible Matérielle** : Raspberry Pi 4 Model B (Quad-core ARM Cortex-A72 @ 1.5 GHz, 4 Go RAM, OS Raspberry Pi OS 64-bit).
- **Consommation Électrique** : 3.4 Watts en pleine inférence (idéal pour alimentation solaire ou PoE industriel).
- **Empreinte Mémoire** : Modèle exporté Joblib < 1.2 Mo, mémoire vive totale requise < 45 Mo.
- **Latence d'Inférence** : **0.218 ms** (plus de 4500 prédictions par seconde possible en continu).
- **Disponibilité Réseau** : Fonctionnement **100% autonome et offline** (aucune dépendance au cloud ou à une connexion Internet).
