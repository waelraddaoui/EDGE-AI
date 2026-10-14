# Edge AI Predictive Maintenance on Raspberry Pi

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=111111)](frontend/)
[![Raspberry Pi](https://img.shields.io/badge/Edge%20device-Raspberry%20Pi-C51A4A?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)

An end-to-end industrial condition-monitoring system that detects bearing faults at the edge, explains its predictions, and gives maintenance teams a searchable technical assistant.

This project demonstrates applied **machine learning, signal processing, explainable AI, RAG, FastAPI, React, MQTT, and embedded deployment** in one production-minded workflow.

## What I built

- **Edge inference:** lightweight models for vibration-based anomaly and fault classification on Raspberry Pi, with latency and resource benchmarking.
- **Signal pipeline:** windowing, time-domain statistics, FFT features, preprocessing, training, evaluation, and reproducible saved models.
- **Explainability:** feature importance and healthy-baseline Z-scores to make predictions actionable for technicians.
- **RAG diagnostic assistant:** indexes technical documents, answers maintenance questions, and generates structured diagnostic reports.
- **Full-stack interface:** React dashboard backed by a FastAPI service for monitoring and diagnosis workflows.
- **IoT path:** Raspberry Pi and ESP32 components with MQTT streaming and a Wokwi simulation setup.

## Architecture

```text
Vibration signal -> preprocessing -> time / FFT features -> ML models
                                                       |
                                                       v
                         Raspberry Pi inference <- prediction + XAI
                                                       |
                                      MQTT / FastAPI / React dashboard
                                                       |
                                      RAG knowledge base -> diagnosis report
```

## Results and evidence

The repository includes the trained models, benchmark scripts, figures, and technical reports needed to inspect the work rather than treating it as a black-box demo.

- [Edge benchmark and deployment analysis](reports/edge_benchmark_report.md)
- [Model evaluation metrics](reports/model_evaluation_metrics.md)
- [Explainability analysis](reports/xai_analysis_report.md)
- [Edge decision matrix](reports/edge_decision_matrix.md)
- [Exploratory notebook](notebooks/01_exploration.ipynb)
- [Automated diagnostic report](reports/automated_diagnostic_report.md)

## Quick start

### Python environment

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the ML pipeline

```bash
python src/data_preparation.py
python src/feature_extraction.py
python src/train_models.py
python src/evaluate_models.py
```

### Run edge inference and the RAG assistant

```bash
python raspberry/inference_edge.py
python raspberry/benchmark_edge.py
python rag_agent/build_index.py
python rag_agent/ask_agent.py
```

### Run the web interface

```bash
cd frontend
npm install
npm run dev
```

The API entry point is `api/main.py`. See the source files for environment-specific hardware and service settings.

## Repository map

| Area | Purpose |
| --- | --- |
| `src/` | Data preparation, feature engineering, training, evaluation, and XAI |
| `raspberry/` | Edge inference, benchmarking, and MQTT streaming |
| `api/` | FastAPI endpoints and report generation |
| `frontend/` | React dashboard |
| `rag_agent/` | Document indexing, retrieval, Q&A, and diagnostics |
| `esp32_firmware/` and `wokwi/` | Embedded firmware and simulation |
| `models/` and `figures/` | Reusable artifacts and experiment outputs |
| `reports/` | Technical analysis, benchmarks, and project documentation |

## Technical keywords

`Python` `PyTorch` `scikit-learn` `XGBoost` `LightGBM` `FastAPI` `React` `RAG` `TF-IDF` `XAI` `FFT` `time-series` `predictive-maintenance` `Raspberry-Pi` `ESP32` `MQTT` `TinyML` `Docker-ready`

## Context

This project was developed as a final-year engineering internship project focused on explainable Edge AI for industrial predictive maintenance. It includes both the implementation and the educational case study used to communicate the engineering decisions.
