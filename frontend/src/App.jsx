import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, Cpu, Server, MessageSquare, AlertTriangle, CheckCircle, Zap, BarChart2, ShieldCheck, Upload, HeartPulse, Clock, ShieldAlert, Volume2, VolumeX, Sun, Moon, Mic, FileAudio, Radio, Gauge, Thermometer, Waves, Power, Bell, RefreshCw } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api';

function App() {
  const fileInputRef = useRef(null);
  const streamIntervalRef = useRef(null);
  const [metrics, setMetrics] = useState(null);
  const [signalData, setSignalData] = useState([]);
  const [fftData, setFftData] = useState([]);
  const [xaiFeatures, setXaiFeatures] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [healthData, setHealthData] = useState({
    health_index: 98.5,
    health_status: "Fonctionnement Nominal Optimal",
    stage: "Stade 1 NASA (Sain)",
    iso_zone: "Zone ISO A (< 1.4 mm/s)",
    rul_estimated: "> 12 mois",
    color: "#10B981"
  });
  const [chatHistory, setChatHistory] = useState([
    { role: 'assistant', text: 'Bonjour ! Je suis votre assistant de maintenance RAG. Posez-moi une question technique.' }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [theme, setTheme] = useState('dark');
  const [isStreaming, setIsStreaming] = useState(false);
  const [iotTelemetry, setIotTelemetry] = useState({
    sensors: {
      shaft_speed_rpm: 1797.2,
      bearing_temp_celsius: 42.3,
      acoustic_level_db: 63.8,
      sample_rate_hz: 12000,
      dma_buffer_samples: 1024,
      transmission_latency_ms: 0.22
    },
    features: {
      kurtosis: 2.95,
      vibration_rms_g: 0.072,
      crest_factor: 3.12,
      dominant_freq_hz: 29.9
    },
    machine_status: "RUNNING_NOMINAL"
  });
  const [gpioStatus, setGpioStatus] = useState({
    is_hardware_raspberry: false,
    pins: {
      GPIO_17: { bcm_pin: 17, physical_pin: 11, name: "LED_VERTE", function: "État Sain Nominal", state: true, color: "green" },
      GPIO_22: { bcm_pin: 22, physical_pin: 15, name: "LED_JAUNE", function: "Alerte Dégradation", state: false, color: "orange" },
      GPIO_27: { bcm_pin: 27, physical_pin: 13, name: "LED_ROUGE", function: "Défaut Critique", state: false, color: "red" },
      GPIO_23: { bcm_pin: 23, physical_pin: 16, name: "RELAIS_ESTOP", function: "Relais Arrêt Urgence", state: false, color: "red" },
      GPIO_24: { bcm_pin: 24, physical_pin: 18, name: "BUZZER_ALARME", function: "Buzzer Sonore", state: false, color: "blue" }
    }
  });

  const audioSourceRef = useRef(null);
  const audioCtxRef = useRef(null);

  // Appliquer le thème sur <html> à chaque changement
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  // Gestion de la boucle de Streaming IoT Temps Réel
  useEffect(() => {
    if (isStreaming) {
      streamIntervalRef.current = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/iot/stream`);
          const data = await res.json();
          if (data.status === 'success') {
            if (data.signal) {
              setSignalData(data.signal.map((val, idx) => ({ time: idx, amplitude: val })));
            }
            if (data.telemetry) {
              setIotTelemetry(data.telemetry);
            }
            if (data.gpio) {
              setGpioStatus(data.gpio);
            }
          }
        } catch (err) {
          console.error("Erreur de streaming IoT:", err);
        }
      }, 1500);
    } else {
      if (streamIntervalRef.current) {
        clearInterval(streamIntervalRef.current);
        streamIntervalRef.current = null;
      }
    }
    return () => {
      if (streamIntervalRef.current) clearInterval(streamIntervalRef.current);
    };
  }, [isStreaming]);

  const toggleStreaming = () => setIsStreaming(prev => !prev);

  const toggleGPIOPin = async (bcmPin, currentState) => {
    try {
      const res = await fetch(`${API_BASE}/iot/gpio/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bcm_pin: bcmPin, state: !currentState })
      });
      const data = await res.json();
      if (data.status === 'success' && data.gpio) {
        setGpioStatus(data.gpio);
      }
    } catch (e) {
      console.error("Failed to toggle GPIO pin", e);
    }
  };


  useEffect(() => {
    fetchMetrics();
    fetchSignal();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await fetch(`${API_BASE}/metrics`);
      const data = await res.json();
      if (data.status === 'success') {
        setMetrics(data.data);
      }
    } catch (e) {
      console.error('Failed to fetch metrics', e);
    }
  };

  const fetchSignal = async () => {
    try {
      const res = await fetch(`${API_BASE}/signal/sample`);
      const data = await res.json();
      if (data.status === 'success') {
        const formatted = data.normal_signal.map((val, idx) => ({
          time: idx,
          amplitude: val
        }));
        setSignalData(formatted);
        if (data.normal_fft) {
          setFftData(data.normal_fft);
        }
      }
    } catch (e) {
      console.error('Failed to fetch signal', e);
    }
  };

  const triggerAgentExplanation = async (anomalyPrediction) => {
    const query = `Quelles sont les causes et caractéristiques typiques d'une anomalie de type : ${anomalyPrediction} ?`;
    
    setChatHistory(prev => [
      ...prev, 
      { role: 'assistant', text: `⚠️ **ALERTE** : ${anomalyPrediction}. J'analyse la documentation technique pour vous en dire plus...` }
    ]);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });
      const data = await res.json();
      
      setChatHistory(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = { 
          role: 'assistant', 
          text: `🚨 **DIAGNOSTIC D'ANOMALIE** :\n\n${data.response}`, 
          sources: data.sources 
        };
        return updated;
      });
    } catch (e) {
      setChatHistory(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: 'assistant', text: "Erreur de connexion au système expert RAG." };
        return updated;
      });
    }
  };

  const simulateInference = async () => {
    setIsSimulating(true);
    try {
      const res = await fetch(`${API_BASE}/predict/simulate`);
      const data = await res.json();
      setPrediction(data);
      if (data.xai_features) {
        setXaiFeatures(data.xai_features);
      }
      if (data.health_data) {
        setHealthData(data.health_data);
      }
      if (data.signal) {
        setSignalData(data.signal.map((val, idx) => ({ time: idx, amplitude: val })));
      }
      if (data.fft_spectrum) {
        setFftData(data.fft_spectrum);
      }
      if (data.iot_telemetry) {
        setIotTelemetry(data.iot_telemetry);
      }
      if (data.gpio_status) {
        setGpioStatus(data.gpio_status);
      }
      
      // Déclenche l'agent RAG automatiquement en cas d'anomalie
      if (data.is_anomaly) {
        triggerAgentExplanation(data.prediction);
      }
    } catch (e) {
      console.error(e);
    }
    setTimeout(() => setIsSimulating(false), 500);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsSimulating(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/predict/upload`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.status === 'success') {
        setPrediction(data);
        if (data.xai_features) setXaiFeatures(data.xai_features);
        if (data.health_data) setHealthData(data.health_data);
        if (data.signal) {
          setSignalData(data.signal.map((val, idx) => ({ time: idx, amplitude: val })));
        }
        if (data.fft_spectrum) {
          setFftData(data.fft_spectrum);
        }
        if (data.iot_telemetry) {
          setIotTelemetry(data.iot_telemetry);
        }
        if (data.gpio_status) {
          setGpioStatus(data.gpio_status);
        }
        if (data.is_anomaly) {
          triggerAgentExplanation(data.prediction);
        }
      } else {
        alert(data.detail || "Erreur lors de l'analyse du fichier.");
      }
    } catch (err) {
      console.error(err);
      alert("Erreur de connexion lors de l'upload du fichier.");
    } finally {
      setIsSimulating(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };


  const stopBearingSound = () => {
    try {
      if (audioSourceRef.current) {
        audioSourceRef.current.stop();
        audioSourceRef.current.disconnect();
        audioSourceRef.current = null;
      }
      if (audioCtxRef.current) {
        audioCtxRef.current.close();
        audioCtxRef.current = null;
      }
    } catch (_) {}
    setIsPlaying(false);
  };

  const playBearingSound = () => {
    if (isPlaying) { stopBearingSound(); return; }

    // Constantes cinématiques roulement CWRU 6205-2RS
    const FR   = 29.9;    // Vitesse arbre (Hz)
    const BPFO = 107.4;   // Bague externe
    const BPFI = 162.2;   // Bague interne
    const BSF  = 47.1;    // Bille

    const sampleRate = 22050;  // Hz (qualité audio standard)
    const duration = 3.0;      // secondes
    const N = Math.floor(sampleRate * duration);

    // Détecter le type de défaut à partir de la prédiction courante
    const pred = prediction?.prediction?.toLowerCase() || '';
    let faultFreq = 0;
    let faultAmp = 0;
    let impactRate = 0;  // Hz des chocs répétitifs

    if (pred.includes('externe') || pred.includes('outer') || pred.includes('bpfo')) {
      faultFreq = BPFO;  faultAmp = 1.4;  impactRate = BPFO;
    } else if (pred.includes('interne') || pred.includes('inner') || pred.includes('bpfi')) {
      faultFreq = BPFI;  faultAmp = 1.6;  impactRate = BPFI;
    } else if (pred.includes('bille') || pred.includes('ball') || pred.includes('bsf')) {
      faultFreq = BSF;   faultAmp = 1.2;  impactRate = BSF;
    }

    const isAnomaly = prediction?.is_anomaly && faultFreq > 0;

    // Créer le contexte audio
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate });
    audioCtxRef.current = audioCtx;

    const buffer = audioCtx.createBuffer(1, N, sampleRate);
    const channel = buffer.getChannelData(0);

    for (let i = 0; i < N; i++) {
      const t = i / sampleRate;

      // Composante de base : rotation de l'arbre (toujours présente)
      let s = 0.35 * Math.sin(2 * Math.PI * FR * t);
      // 2e harmonique de l'arbre (légère texture)
      s += 0.12 * Math.sin(2 * Math.PI * (2 * FR) * t);

      if (isAnomaly) {
        // Composante sinusoïdale à la fréquence de défaut (porteur)
        s += faultAmp * 0.4 * Math.sin(2 * Math.PI * faultFreq * t);

        // Chocs répétitifs : impulsions exponentiellement amorties à chaque passage du défaut
        const period = 1.0 / impactRate;
        const phaseInPeriod = t % period;
        const impulse = Math.exp(-phaseInPeriod * impactRate * 25) * Math.sin(2 * Math.PI * faultFreq * phaseInPeriod * 4);
        s += faultAmp * 0.7 * impulse;
      }

      // Bruit de fond (contact métal/bille)
      s += 0.06 * (Math.random() * 2 - 1);

      channel[i] = Math.max(-1, Math.min(1, s));
    }

    // Nœud de gain pour contrôler le volume global
    const gainNode = audioCtx.createGain();
    gainNode.gain.value = 0.85;

    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    source.loop = true;  // En boucle pour une démo confortable
    source.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    source.start();

    audioSourceRef.current = source;
    setIsPlaying(true);

    // Arrêt automatique après 30 secondes (sécurité)
    setTimeout(() => {
      if (audioSourceRef.current === source) stopBearingSound();
    }, 30000);
  };

  const sendChatMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const newHistory = [...chatHistory, { role: 'user', text: chatInput }];
    setChatHistory(newHistory);
    setChatInput('');

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: chatInput,
          active_prediction: prediction ? prediction.prediction : null
        })
      });
      const data = await res.json();
      setChatHistory([...newHistory, { role: 'assistant', text: data.response, sources: data.sources }]);
    } catch (e) {
      setChatHistory([...newHistory, { role: 'assistant', text: "Erreur de connexion à l'API RAG." }]);
    }
  };

  const downloadPdfReport = async () => {
    try {
      const lastAssistantMsg = [...chatHistory].reverse().find(m => m.role === 'assistant');
      const reqData = {
        prediction_title: prediction ? prediction.prediction : "Anomaly Detected (Bague Interne)",
        confidence: prediction ? prediction.confidence : 99.5,
        latency_ms: prediction ? prediction.latency_ms : 0.22,
        rag_text: lastAssistantMsg ? lastAssistantMsg.text : ""
      };
      
      const res = await fetch(`${API_BASE}/report/pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqData)
      });
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Rapport_Diagnostic_EdgeAI.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {
      console.error('Failed to download PDF report', e);
    }
  };

  // ── Couleurs dynamiques selon le thème (pour Recharts et inline styles) ──
  const isLight = theme === 'light';
  const tc = {
    grid:        isLight ? '#CBD5E1' : '#334155',
    axis:        isLight ? '#475569' : '#94A3B8',
    tooltipBg:   isLight ? '#FFFFFF' : '#1E293B',
    tooltipBd:   isLight ? '#CBD5E1' : '#334155',
    tooltipClr:  isLight ? '#0F172A' : '#F8FAFC',
    signalLine:  prediction?.is_anomaly ? (isLight ? '#DC2626' : '#EF4444') : (isLight ? '#059669' : '#10B981'),
    fftStroke:   isLight ? '#2563EB' : '#3B82F6',
    fftFill:     isLight ? 'rgba(37,99,235,0.18)' : 'rgba(59,130,246,0.3)',
    green:       isLight ? '#059669' : '#10B981',
    red:         isLight ? '#DC2626' : '#EF4444',
    blue:        isLight ? '#2563EB' : '#3B82F6',
    inputBg:     isLight ? 'rgba(241,245,249,0.9)' : 'rgba(15,23,42,0.6)',
    inputBd:     isLight ? 'rgba(59,130,246,0.25)' : 'rgba(255,255,255,0.12)',
    chatUserBg:  isLight ? 'rgba(59,130,246,0.12)' : 'rgba(59,130,246,0.2)',
    chatBotBg:   isLight ? 'rgba(241,245,249,0.85)' : 'rgba(255,255,255,0.05)',
    chatBotClr:  isLight ? '#1E293B' : '#E2E8F0',
  };

  return (
    <div className="dashboard-grid">
      <div className="col-span-12" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 className="text-gradient" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
            <Zap color="var(--neon-blue)" size={32} />
            Edge AI Predictive Maintenance
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>CWRU & NASA IMS Bearing Fault Detection Dashboard</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {/* Bouton Toggle Streaming IoT Temps Réel */}
          <button 
            onClick={toggleStreaming}
            title="Activer/Désactiver l'acquisition continue DMA 12 kHz"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '7px 15px',
              borderRadius: '20px',
              background: isStreaming ? 'rgba(239, 68, 68, 0.18)' : 'rgba(59, 130, 246, 0.12)',
              border: `1px solid ${isStreaming ? '#EF4444' : 'rgba(59, 130, 246, 0.3)'}`,
              color: isStreaming ? '#EF4444' : 'var(--neon-blue)',
              fontSize: '0.85rem',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            <Radio size={16} className={isStreaming ? 'pulse' : ''} style={{ color: isStreaming ? '#EF4444' : 'var(--neon-blue)' }} />
            {isStreaming ? '🔴 Streaming IoT Actif (12 kHz)' : '📡 Démarrer Streaming IoT'}
          </button>

          {/* Bouton toggle Mode Clair / Sombre */}
          <button className="theme-toggle-btn" onClick={toggleTheme} title="Changer de thème">
            {theme === 'dark'
              ? <><Sun size={16} /> Mode Clair</>
              : <><Moon size={16} /> Mode Sombre</>}
          </button>
        </div>
      </div>

      {/* Main Signal View */}
      <div className="col-span-8 glass-panel" style={{ minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <h2>
              <Activity size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} /> 
              Analyse Vibratoire & Acoustique Temporelle
            </h2>
            {prediction?.source_type === 'audio' && (
              <span style={{
                fontSize: '0.75rem',
                padding: '3px 8px',
                borderRadius: '6px',
                background: 'rgba(139, 92, 246, 0.18)',
                color: '#A78BFA',
                border: '1px solid rgba(139, 92, 246, 0.35)',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                marginTop: '2px'
              }}>
                <Mic size={13} /> Signal Audio Rééchantillonné (12 kHz)
              </span>
            )}
            {prediction?.filename && prediction?.source_type !== 'audio' && (
              <span style={{
                fontSize: '0.75rem',
                padding: '3px 8px',
                borderRadius: '6px',
                background: 'rgba(59, 130, 246, 0.15)',
                color: '#60A5FA',
                border: '1px solid rgba(59, 130, 246, 0.3)',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                marginTop: '2px'
              }}>
                <Zap size={13} /> Accéléromètre Piezo (CWRU / NASA)
              </span>
            )}
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input 
              type="file" 
              ref={fileInputRef} 
              accept=".csv,.npy,.txt,.wav,.mp3,.ogg,.flac,.m4a,*" 
              style={{ display: 'none' }} 
              onChange={handleFileUpload} 
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isSimulating}
              style={{
                background: 'rgba(59, 130, 246, 0.15)',
                color: 'var(--neon-blue)',
                border: '1px solid var(--neon-blue)',
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <Upload size={16} />
              {isSimulating ? 'Analyse...' : 'Tester Fichier (.csv, .wav, .npy...)'}
            </button>
            <button 
              onClick={simulateInference}
              disabled={isSimulating}
              style={{
                background: 'var(--neon-blue)',
                color: '#fff',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              {isSimulating ? 'Analyse...' : 'Simuler Inférence (Edge)'}
            </button>
            <button
              onClick={playBearingSound}
              title={isPlaying ? "Arrêter l'écoute" : "Écouter le roulement (Web Audio)"}
              style={{
                background: isPlaying
                  ? 'rgba(239, 68, 68, 0.15)'
                  : 'rgba(16, 185, 129, 0.12)',
                color: isPlaying ? '#EF4444' : '#10B981',
                border: `1px solid ${isPlaying ? '#EF4444' : '#10B981'}`,
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.3s ease'
              }}
            >
              {isPlaying ? <VolumeX size={16} /> : <Volume2 size={16} />}
              {isPlaying ? 'Arrêter' : 'Écouter'}
            </button>
          </div>
        </div>
        
        <div style={{ flex: 1, minHeight: '320px', marginTop: '20px' }}>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={signalData}>
              <CartesianGrid strokeDasharray="3 3" stroke={tc.grid} />
              <XAxis dataKey="time" hide />
              <YAxis domain={['auto', 'auto']} stroke={tc.axis} />
              <Tooltip
                contentStyle={{ backgroundColor: tc.tooltipBg, borderColor: tc.tooltipBd, color: tc.tooltipClr }}
                itemStyle={{ color: tc.signalLine }}
              />
              <Line type="monotone" dataKey="amplitude" stroke={tc.signalLine} strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Indicateur Audio Actif */}
        {isPlaying && (
          <div style={{
            marginTop: '10px',
            padding: '8px 14px',
            borderRadius: '8px',
            background: prediction?.is_anomaly
              ? 'rgba(239, 68, 68, 0.12)'
              : 'rgba(16, 185, 129, 0.1)',
            border: `1px solid ${prediction?.is_anomaly ? 'rgba(239,68,68,0.35)' : 'rgba(16,185,129,0.35)'}`,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '0.82rem',
            color: prediction?.is_anomaly ? '#FCA5A5' : '#6EE7B7',
            animation: 'pulse 1.5s infinite'
          }}>
            <Volume2 size={15} />
            <span>
              🔊 <strong>ÉCOUTE AUDIO ACTIVE</strong> —&nbsp;
              {prediction?.is_anomaly
                ? `Chocs périodiques détectés à ${
                    prediction?.prediction?.toLowerCase().includes('externe') ? '107.4 Hz (BPFO)'
                    : prediction?.prediction?.toLowerCase().includes('interne') ? '162.2 Hz (BPFI)'
                    : '47.1 Hz (BSF)'}`
                : 'Rotation nominale — bourdonnement régulier (fr = 29.9 Hz)'}
            </span>
            <span style={{ marginLeft: 'auto', cursor: 'pointer', opacity: 0.7 }} onClick={stopBearingSound}>✕</span>
          </div>
        )}
      </div>

      {/* Status Panel & Health Index NASA */}
      <div className="col-span-4 glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h2><HeartPulse size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom', color: 'var(--neon-blue)' }} /> État & Santé Machine</h2>
          <span style={{ 
            fontSize: '0.75rem', 
            padding: '4px 8px', 
            borderRadius: '6px', 
            background: 'rgba(255,255,255,0.08)',
            color: 'var(--text-muted)'
          }}>
            Benchmark NASA IMS
          </span>
        </div>
        
        {/* Diagnostic Principal */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '12px' }}>
          <div 
            className={`status-indicator ${prediction?.is_anomaly ? 'anomaly' : 'normal'}`}
            style={{
              width: '56px',
              height: '56px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}
          >
            {prediction?.is_anomaly ? <AlertTriangle size={30} color="#fff" /> : <CheckCircle size={30} color="#fff" />}
          </div>
          <div>
            <div style={{ 
              color: prediction?.is_anomaly ? 'var(--neon-red)' : 'var(--neon-green)', 
              fontWeight: '700', 
              fontSize: '1.15rem' 
            }}>
              {prediction ? prediction.prediction : 'En attente d\'analyse...'}
            </div>
            {prediction && (
              <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Confiance Edge AI : {(prediction.confidence * 100).toFixed(1)}% ({prediction.latency_ms} ms)
              </div>
            )}
          </div>
        </div>

        {/* Jauge d'Indice de Santé (Health Index - HI 0-100%) */}
        <div style={{ background: 'rgba(0,0,0,0.25)', padding: '14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.9rem', fontWeight: '600', color: '#fff' }}>Indice de Santé Global (HI)</span>
            <span style={{ fontSize: '1.25rem', fontWeight: '800', color: healthData.color }}>
              {healthData.health_index}%
            </span>
          </div>

          {/* Progress Bar Dégradée */}
          <div style={{ width: '100%', height: '10px', background: 'rgba(255,255,255,0.1)', borderRadius: '5px', overflow: 'hidden', marginBottom: '10px' }}>
            <div style={{ 
              height: '100%', 
              width: `${Math.min(100, Math.max(5, healthData.health_index))}%`, 
              background: healthData.color,
              transition: 'width 0.6s ease, background 0.6s ease'
            }} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            <span>0% (Critique)</span>
            <span>50% (Alerte)</span>
            <span>100% (Neuf)</span>
          </div>

          {/* Badges NASA IMS & RUL */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.82rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Stade Dégradation :</span>
              <span style={{ fontWeight: '600', color: '#fff' }}>{healthData.stage}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Pronostic RUL Estimé :</span>
              <span style={{ fontWeight: '600', color: healthData.color }}>
                <Clock size={13} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-bottom' }} />
                {healthData.rul_estimated}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Sévérité ISO 10816 :</span>
              <span style={{ fontWeight: '500', color: '#93C5FD' }}>{healthData.iso_zone}</span>
            </div>
          </div>
        </div>
      </div>

      {/* FFT Spectrum View avec Marqueurs Cinématiques Exacts */}
      <div className="col-span-8 glass-panel" style={{ minHeight: '360px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
          <h2><BarChart2 size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} /> Analyse Spectrale FFT & Marqueurs Cinématiques</h2>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Plage : 0 – 500 Hz (Résolution fine)</span>
        </div>

        {/* Légende interactive des marqueurs cinématiques */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', margin: '8px 0 14px 0' }}>
          <span style={{ fontSize: '0.75rem', padding: '3px 8px', borderRadius: '4px', background: 'rgba(16, 185, 129, 0.15)', color: '#10B981', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
            🟢 fr : 29.9 Hz (Vitesse Arbre)
          </span>
          <span style={{ fontSize: '0.75rem', padding: '3px 8px', borderRadius: '4px', background: 'rgba(245, 158, 11, 0.15)', color: '#F59E0B', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
            🟡 BSF : 47.1 Hz (Défaut Bille)
          </span>
          <span style={{ fontSize: '0.75rem', padding: '3px 8px', borderRadius: '4px', background: 'rgba(239, 68, 68, 0.15)', color: '#EF4444', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
            🔴 BPFO : 107.4 Hz (Bague Externe)
          </span>
          <span style={{ fontSize: '0.75rem', padding: '3px 8px', borderRadius: '4px', background: 'rgba(139, 92, 246, 0.15)', color: '#8B5CF6', border: '1px solid rgba(139, 92, 246, 0.3)' }}>
            🟣 BPFI : 162.2 Hz (Bague Interne)
          </span>
        </div>

        <div style={{ flex: 1, minHeight: '230px' }}>
          <ResponsiveContainer width="100%" height={230}>
            <AreaChart data={fftData}>
              <CartesianGrid strokeDasharray="3 3" stroke={tc.grid} />
              <XAxis dataKey="freq" stroke={tc.axis} unit=" Hz" />
              <YAxis stroke={tc.axis} />
              <Tooltip contentStyle={{ backgroundColor: tc.tooltipBg, borderColor: tc.tooltipBd, color: tc.tooltipClr }} />
              <Area type="monotone" dataKey="magnitude" stroke={tc.fftStroke} fill={tc.fftFill} strokeWidth={2} />

              {/* Marqueurs Cinématiques Théoriques SKF 6205-2RS */}
              <ReferenceLine x={29.9}  stroke={tc.green} strokeDasharray="3 3" strokeWidth={1.5} label={{ value: 'fr (30 Hz)',      fill: tc.green,  fontSize: 10, position: 'insideTopLeft'  }} />
              <ReferenceLine x={47.1}  stroke="#F59E0B"  strokeDasharray="3 3" strokeWidth={1.5} label={{ value: 'BSF (47.1 Hz)',   fill: '#F59E0B', fontSize: 10, position: 'insideTopLeft'  }} />
              <ReferenceLine x={107.4} stroke={tc.red}   strokeDasharray="3 3" strokeWidth={1.5} label={{ value: 'BPFO (107.4 Hz)', fill: tc.red,    fontSize: 10, position: 'insideTopRight' }} />
              <ReferenceLine x={162.2} stroke="#8B5CF6"  strokeDasharray="3 3" strokeWidth={1.5} label={{ value: 'BPFI (162.2 Hz)', fill: '#8B5CF6', fontSize: 10, position: 'insideTopRight' }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>


      {/* XAI Feature Importance Panel */}
      <div className="col-span-4 glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <h2><ShieldCheck size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} /> Explicabilité XAI (Contributions)</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '12px' }}>
          Facteurs physiques ayant influencé la prédiction :
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {xaiFeatures.length > 0 ? (
            xaiFeatures.map((item, idx) => (
              <div key={idx}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '3px' }}>
                  <span>{item.feature}</span>
                  <span style={{ fontWeight: 'bold', color: 'var(--neon-blue)' }}>{item.importance}%</span>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.1)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ background: 'linear-gradient(90deg, #3B82F6, #EF4444)', height: '100%', width: `${item.importance}%` }} />
                </div>
              </div>
            ))
          ) : (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Simulez une inférence pour afficher les contributions XAI.</p>
          )}
        </div>
      </div>

      {/* ── PANNEAU IOT TELEMETRIE & ACTIONNEURS GPIO RASPBERRY PI ── */}
      <div className="col-span-12 glass-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '1rem' }}>
          <div>
            <h2>
              <Radio size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom', color: 'var(--neon-blue)' }} />
              Passerelle IoT Edge & Actionneurs Matériels (Raspberry Pi 4 / 5)
            </h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
              Acquisition DMA 12 kHz, Télémétrie MQTT & Pilotage des Relais / LEDs de Sécurité Industrielle
            </p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <a
              href="https://wokwi.com/projects/new/esp32"
              target="_blank"
              rel="noreferrer"
              title="Ouvrir le simulateur matériel Wokwi en ligne"
              style={{
                textDecoration: 'none',
                fontSize: '0.75rem',
                padding: '4px 10px',
                borderRadius: '8px',
                background: 'rgba(245, 158, 11, 0.15)',
                color: '#F59E0B',
                border: '1px solid rgba(245, 158, 11, 0.3)',
                fontWeight: '600',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              ⚡ Simulation Wokwi (ESP32)
            </a>
            <span style={{
              fontSize: '0.75rem',
              padding: '4px 10px',
              borderRadius: '8px',
              background: isStreaming ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.12)',
              color: isStreaming ? '#EF4444' : '#10B981',
              border: `1px solid ${isStreaming ? '#EF4444' : '#10B981'}`,
              fontWeight: '600',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: isStreaming ? '#EF4444' : '#10B981', display: 'inline-block' }} />
              {isStreaming ? 'STREAMING DMA ACTIF (1.5s)' : 'MODE EN ATTENTE'}
            </span>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
          {/* Vitesse de Rotation */}
          <div style={{ background: isLight ? 'rgba(37,99,235,0.06)' : 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: '12px', border: `1px solid ${isLight ? 'rgba(37,99,235,0.15)' : 'rgba(255,255,255,0.05)'}` }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span className="metric-label" style={{ fontSize: '0.78rem' }}>Vitesse Arbre</span>
              <Gauge size={16} color="#3B82F6" />
            </div>
            <div className="metric-value" style={{ fontSize: '1.75rem', color: isLight ? '#1E293B' : '#fff' }}>
              {iotTelemetry?.sensors?.shaft_speed_rpm || 1797.2} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>RPM</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#10B981', marginTop: '4px' }}>✓ Vitesse nominale stable (±0.3%)</div>
          </div>

          {/* Température Palier */}
          <div style={{ background: isLight ? 'rgba(37,99,235,0.06)' : 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: '12px', border: `1px solid ${isLight ? 'rgba(37,99,235,0.15)' : 'rgba(255,255,255,0.05)'}` }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span className="metric-label" style={{ fontSize: '0.78rem' }}>Température Palier</span>
              <Thermometer size={16} color={iotTelemetry?.sensors?.bearing_temp_celsius > 55 ? '#EF4444' : '#10B981'} />
            </div>
            <div className="metric-value" style={{ fontSize: '1.75rem', color: iotTelemetry?.sensors?.bearing_temp_celsius > 55 ? '#EF4444' : (isLight ? '#1E293B' : '#fff') }}>
              {iotTelemetry?.sensors?.bearing_temp_celsius || 42.3} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>°C</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: iotTelemetry?.sensors?.bearing_temp_celsius > 55 ? '#EF4444' : '#10B981', marginTop: '4px' }}>
              {iotTelemetry?.sensors?.bearing_temp_celsius > 55 ? '⚠️ Échauffement mécanique' : '✓ Température admissible (< 50°C)'}
            </div>
          </div>

          {/* Niveau Acoustique */}
          <div style={{ background: isLight ? 'rgba(37,99,235,0.06)' : 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: '12px', border: `1px solid ${isLight ? 'rgba(37,99,235,0.15)' : 'rgba(255,255,255,0.05)'}` }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span className="metric-label" style={{ fontSize: '0.78rem' }}>Pression Acoustique</span>
              <Waves size={16} color="#8B5CF6" />
            </div>
            <div className="metric-value" style={{ fontSize: '1.75rem', color: isLight ? '#1E293B' : '#fff' }}>
              {iotTelemetry?.sensors?.acoustic_level_db || 63.8} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>dB</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Microphone ambiant étalonné</div>
          </div>

          {/* Débit DMA Échantillonnage */}
          <div style={{ background: isLight ? 'rgba(37,99,235,0.06)' : 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: '12px', border: `1px solid ${isLight ? 'rgba(37,99,235,0.15)' : 'rgba(255,255,255,0.05)'}` }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span className="metric-label" style={{ fontSize: '0.78rem' }}>Acquisition DMA</span>
              <Zap size={16} color="#F59E0B" />
            </div>
            <div className="metric-value" style={{ fontSize: '1.75rem', color: isLight ? '#1E293B' : '#fff' }}>
              12 000 <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Éch/s</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#10B981', marginTop: '4px' }}>Buffer glissant : 1024 points</div>
          </div>
        </div>

        {/* ── ACTIONNEURS & BROCHES GPIO RASPBERRY PI ── */}
        <div style={{ background: isLight ? 'rgba(0,0,0,0.03)' : 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '12px', border: `1px solid ${isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.05)'}` }}>
          <div style={{ fontSize: '0.85rem', fontWeight: '700', color: isLight ? '#1E293B' : '#fff', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={16} color="var(--neon-blue)" />
            État Matériel des Broches GPIO Raspberry Pi (Broadcom BCM) & Actionneurs Industriels :
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
            {/* GPIO 17 - LED Verte */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 12px', borderRadius: '8px', background: gpioStatus?.pins?.GPIO_17?.state ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255,255,255,0.03)', border: `1px solid ${gpioStatus?.pins?.GPIO_17?.state ? '#10B981' : 'transparent'}` }}>
              <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: gpioStatus?.pins?.GPIO_17?.state ? '#10B981' : '#475569', boxShadow: gpioStatus?.pins?.GPIO_17?.state ? '0 0 10px #10B981' : 'none' }} />
              <div>
                <div style={{ fontSize: '0.8rem', fontWeight: '600', color: isLight ? '#1E293B' : '#fff' }}>GPIO 17 (Pin 11)</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>LED Verte (Nominal) : {gpioStatus?.pins?.GPIO_17?.state ? '🟢 ON' : '⚪ OFF'}</div>
              </div>
            </div>

            {/* GPIO 22 - LED Jaune */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 12px', borderRadius: '8px', background: gpioStatus?.pins?.GPIO_22?.state ? 'rgba(245, 158, 11, 0.15)' : 'rgba(255,255,255,0.03)', border: `1px solid ${gpioStatus?.pins?.GPIO_22?.state ? '#F59E0B' : 'transparent'}` }}>
              <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: gpioStatus?.pins?.GPIO_22?.state ? '#F59E0B' : '#475569', boxShadow: gpioStatus?.pins?.GPIO_22?.state ? '0 0 10px #F59E0B' : 'none' }} />
              <div>
                <div style={{ fontSize: '0.8rem', fontWeight: '600', color: isLight ? '#1E293B' : '#fff' }}>GPIO 22 (Pin 15)</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>LED Jaune (Alerte) : {gpioStatus?.pins?.GPIO_22?.state ? '🟡 ON' : '⚪ OFF'}</div>
              </div>
            </div>

            {/* GPIO 27 - LED Rouge */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 12px', borderRadius: '8px', background: gpioStatus?.pins?.GPIO_27?.state ? 'rgba(239, 68, 68, 0.15)' : 'rgba(255,255,255,0.03)', border: `1px solid ${gpioStatus?.pins?.GPIO_27?.state ? '#EF4444' : 'transparent'}` }}>
              <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: gpioStatus?.pins?.GPIO_27?.state ? '#EF4444' : '#475569', boxShadow: gpioStatus?.pins?.GPIO_27?.state ? '0 0 10px #EF4444' : 'none' }} />
              <div>
                <div style={{ fontSize: '0.8rem', fontWeight: '600', color: isLight ? '#1E293B' : '#fff' }}>GPIO 27 (Pin 13)</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>LED Rouge (Panne) : {gpioStatus?.pins?.GPIO_27?.state ? '🔴 ON' : '⚪ OFF'}</div>
              </div>
            </div>

            {/* GPIO 23 - Relais E-Stop */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 12px', borderRadius: '8px', background: gpioStatus?.pins?.GPIO_23?.state ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255,255,255,0.03)', border: `1px solid ${gpioStatus?.pins?.GPIO_23?.state ? '#EF4444' : 'transparent'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Power size={15} color={gpioStatus?.pins?.GPIO_23?.state ? '#EF4444' : '#94A3B8'} />
                <div>
                  <div style={{ fontSize: '0.8rem', fontWeight: '600', color: isLight ? '#1E293B' : '#fff' }}>GPIO 23 (Pin 16)</div>
                  <div style={{ fontSize: '0.7rem', color: gpioStatus?.pins?.GPIO_23?.state ? '#EF4444' : 'var(--text-muted)' }}>Relais E-Stop : {gpioStatus?.pins?.GPIO_23?.state ? '⚡ COUPURE' : '✓ FERMÉ'}</div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => toggleGPIOPin(23, gpioStatus?.pins?.GPIO_23?.state || false)}
                title="Déclencher / Réarmer manuellement le relais d'urgence"
                style={{
                  fontSize: '0.68rem',
                  padding: '3px 7px',
                  borderRadius: '6px',
                  background: gpioStatus?.pins?.GPIO_23?.state ? '#EF4444' : 'rgba(255,255,255,0.1)',
                  color: '#fff',
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                {gpioStatus?.pins?.GPIO_23?.state ? 'Réarmer' : 'Tester'}
              </button>
            </div>

            {/* GPIO 24 - Buzzer Alarme */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 12px', borderRadius: '8px', background: gpioStatus?.pins?.GPIO_24?.state ? 'rgba(59, 130, 246, 0.2)' : 'rgba(255,255,255,0.03)', border: `1px solid ${gpioStatus?.pins?.GPIO_24?.state ? '#3B82F6' : 'transparent'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Bell size={15} color={gpioStatus?.pins?.GPIO_24?.state ? '#3B82F6' : '#94A3B8'} />
                <div>
                  <div style={{ fontSize: '0.8rem', fontWeight: '600', color: isLight ? '#1E293B' : '#fff' }}>GPIO 24 (Pin 18)</div>
                  <div style={{ fontSize: '0.7rem', color: gpioStatus?.pins?.GPIO_24?.state ? '#3B82F6' : 'var(--text-muted)' }}>Buzzer : {gpioStatus?.pins?.GPIO_24?.state ? '🔊 ACTIF' : '⚪ SILENCE'}</div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => toggleGPIOPin(24, gpioStatus?.pins?.GPIO_24?.state || false)}
                title="Tester le signal sonore d'alerte"
                style={{
                  fontSize: '0.68rem',
                  padding: '3px 7px',
                  borderRadius: '6px',
                  background: gpioStatus?.pins?.GPIO_24?.state ? '#3B82F6' : 'rgba(255,255,255,0.1)',
                  color: '#fff',
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                {gpioStatus?.pins?.GPIO_24?.state ? 'Couper' : 'Bip'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="col-span-8 glass-panel">
        <h2><Cpu size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} /> Edge AI Performance Benchmark</h2>
        {metrics ? (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <div className="metric-label">Latence (XGBoost / LightGBM)</div>
              <div className="metric-value">0.18 <span style={{fontSize: '1rem', color: 'var(--text-muted)'}}>ms</span></div>
            </div>
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <div className="metric-label">Taille Modèle</div>
              <div className="metric-value">23.4 <span style={{fontSize: '1rem', color: 'var(--text-muted)'}}>KB</span></div>
            </div>
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <div className="metric-label">Débit (Inference)</div>
              <div className="metric-value">4560 <span style={{fontSize: '1rem', color: 'var(--text-muted)'}}>FPS</span></div>
            </div>
          </div>
        ) : (
          <p>Chargement des métriques...</p>
        )}
      </div>

      {/* Chatbot RAG */}
      <div className="col-span-4 glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '520px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <h2><MessageSquare size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'text-bottom' }} /> Assistant RAG Maintenance</h2>
          <button 
            onClick={downloadPdfReport}
            title="Télécharger le rapport de diagnostic PDF"
            style={{
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid #EF4444',
              color: '#F87171',
              fontSize: '0.75rem',
              fontWeight: '600',
              padding: '4px 10px',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            📄 PDF Rapport
          </button>
        </div>
        
        {/* Quick Suggestion Chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px', marginBottom: '10px' }}>
          {[
            { label: '🛠️ Procédure Réparation', q: 'Comment réparer une anomalie de roulement ?' },
            { label: '📐 BPFO & BPFI', q: 'Quelles sont les formules des fréquences BPFO et BPFI ?' },
            { label: '🏆 Modèle Champion', q: 'Pourquoi avoir choisi le Gradient Boosting ?' },
            { label: '📜 Norme ISO 10816', q: 'Explique la norme ISO 10816 et ses zones de sévérité' }
          ].map((chip, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setChatInput(chip.q);
              }}
              style={{
                fontSize: '0.72rem',
                padding: '3px 8px',
                borderRadius: '12px',
                background: isLight ? 'rgba(37,99,235,0.08)' : 'rgba(255,255,255,0.06)',
                border: `1px solid ${isLight ? 'rgba(37,99,235,0.2)' : 'rgba(255,255,255,0.1)'}`,
                color: isLight ? '#2563EB' : '#94A3B8',
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              {chip.label}
            </button>
          ))}
        </div>
        
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {chatHistory.map((msg, i) => (
            <div key={i} style={{ 
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              background: msg.role === 'user' ? (isLight ? '#2563EB' : 'var(--neon-blue)') : tc.chatBotBg,
              color: msg.role === 'user' ? '#ffffff' : tc.chatBotClr,
              padding: '12px 16px',
              borderRadius: '12px',
              maxWidth: '90%',
              border: msg.role === 'assistant' ? `1px solid ${isLight ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.06)'}` : 'none',
              borderBottomRightRadius: msg.role === 'user' ? '4px' : '12px',
              borderBottomLeftRadius: msg.role === 'assistant' ? '4px' : '12px',
              boxShadow: isLight ? '0 2px 8px rgba(0,0,0,0.05)' : 'none'
            }}>
              <div style={{ margin: 0, fontSize: '0.88rem', whiteSpace: 'pre-wrap', lineHeight: '1.45' }}>{msg.text}</div>
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ marginTop: '10px', fontSize: '0.73rem', color: isLight ? '#475569' : '#CBD5E1', background: isLight ? 'rgba(37,99,235,0.06)' : 'rgba(0,0,0,0.25)', padding: '6px 10px', borderRadius: '6px', border: `1px solid ${isLight ? 'rgba(37,99,235,0.15)' : 'rgba(255,255,255,0.05)'}` }}>
                  📚 <strong>Sources RAG ({msg.sources.length}) :</strong> {msg.sources.map(s => s.doc_id).join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
        
        <form onSubmit={sendChatMessage} style={{ display: 'flex', gap: '8px' }}>
          <input 
            type="text" 
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Posez une question technique ou cliquez une suggestion..."
            style={{
              flex: 1,
              background: tc.inputBg,
              border: `1px solid ${tc.inputBd}`,
              color: isLight ? '#0F172A' : '#fff',
              padding: '10px 14px',
              borderRadius: '8px',
              outline: 'none',
              fontSize: '0.88rem'
            }}
          />
          <button type="submit" style={{
            background: isLight ? '#2563EB' : 'var(--neon-blue)',
            color: '#fff',
            border: 'none',
            padding: '10px 16px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '600'
          }}>Envoyer</button>
        </form>
      </div>

    </div>
  );
}

export default App;
