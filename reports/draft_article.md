# Draft d'Article Scientifique : Explainable Edge AI and RAG-Enabled Diagnostic Agent for Industrial Bearing Fault Detection on Raspberry Pi

**Abstract**—In Industry 4.0 applications, real-time vibration fault detection for rotating machinery requires high detection accuracy, sub-millisecond inference latency, resource efficiency, and model explainability. Traditional cloud-based predictive maintenance approaches suffer from bandwidth saturation, privacy risks, and latency overheads. This paper presents an end-to-end framework integrating ultra-lightweight Machine Learning and Deep Learning architectures on a Raspberry Pi single-board computer, combined with Explainable AI (XAI) feature attribution and a Retrieval-Augmented Generation (RAG) diagnostic agent. Evaluated on the Case Western Reserve University (CWRU) bearing dataset, our experimental results demonstrate that lightweight Gradient Boosting achieves a 100% clean F1-score and 0.9781 hybrid perturbed F1-score with an inference latency of 0.218 ms per window (4,560 windows/sec throughput) and a memory footprint of only 30.6 KB. Furthermore, our XAI module highlights Kurtosis and RMS as primary physical indicators, while the RAG agent generates automated actionable maintenance reports.

**Keywords**—Edge AI, Fault Diagnosis, Bearing Vibrations, XAI, RAG, Raspberry Pi, Predictive Maintenance.

---

## I. Introduction
Bearing failures in induction motors account for over 40% of mechanical breakdowns in industrial plants. Real-time condition monitoring using vibration sensors allows early detection of localized bearing defects (inner race, outer race, ball faults). However, streaming high-frequency raw vibration data (12 kHz–48 kHz) to cloud servers introduces latency bottlenecks and high operational costs.

Edge AI addresses these challenges by processing signals locally on low-cost hardware such as the Raspberry Pi. This paper contributes:
1. A lightweight feature extraction pipeline capturing 16 time-domain, shape, and FFT spectral metrics.
2. A comprehensive resource-aware benchmark comparing 5 lightweight AI models on embedded hardware.
3. An XAI attribution module explaining local anomaly decisions via Z-score shifts and feature importances.
4. A RAG-enabled maintenance assistant automatically generating technical diagnostic reports.

---

## II. Methodology & Embedded Architecture

### A. Dataset & Windowing
Vibration signals from SKF 6205-2RS bearings are sliced into 1024-point sliding windows. Synthetic perturbations (Gaussian noise, packet loss, sensor drift) are introduced to evaluate edge robustness.

### B. Feature Engineering
Sixteen features are extracted per window:
- **Time-Domain**: Mean, Std Dev, Variance, RMS, Min, Max, Peak-to-Peak, Energy.
- **Form/Impulse**: Skewness, Kurtosis, Crest Factor, Impulse Factor.
- **Frequency-Domain (FFT)**: Spectral Energy, Dominant Frequency, Spectral Centroid, Spectral Spread.

---

## III. Experimental Results & Embedded Benchmark

Table I summarizes the empirical performance metrics across models:

**TABLE I: Performance and Resource Profiling Comparison**

| Model | Accuracy | F1 Clean | F1 Perturbed | Latency (ms) | Throughput (fps) | Disk Size (KB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **1.0000** | **1.0000** | **0.9781** | **0.218** | **4,560.9** | **30.6** |
| **1D-CNN Compact** | 1.0000 | 1.0000 | 0.9666 | 0.536 | 1,848.6 | 11.3 |
| **Random Forest** | 1.0000 | 1.0000 | 0.9945 | 1.217 | 820.6 | 20.1 |
| **Isolation Forest** | 1.0000 | 1.0000 | 0.9474 | 1.214 | 822.6 | 573.3 |

---

## IV. Explainability (XAI) and RAG Agent Integration
XAI feature importance confirms that **Kurtosis** and **RMS** exhibit Z-score spikes exceeding **+4.5 std** during inner race defect occurrences (BPFI = 162.2 Hz). The TF-IDF RAG agent queries an indexed knowledge base (SKF technical datasheets D1–D8) to produce automated diagnostic summary reports with prescriptive maintenance steps.

---

## V. Conclusion
The proposed Edge AI system delivers real-time, explainable, and autonomous bearing fault diagnosis on Raspberry Pi hardware, bridging the gap between embedded Machine Learning and industrial maintenance decision support.
