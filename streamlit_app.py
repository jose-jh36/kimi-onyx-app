# KIMI ONYX VIP - INTERFAZ ESTILO KIMI NATIVO CON EFECTOS 3D PREMIUM
# Backend: Python/Streamlit + Frontend: React-inspired UI
# ============================================================================

import streamlit as st
from openai import OpenAI
import time
import json
import base64
import zipfile
import io
import os
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN INICIAL - ESTILO KIMI NATIVO PREMIUM
# ============================================================================

st.set_page_config(
    page_title="Kimi Onyx VIP",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PALETA DE COLORES - DISEÑO LUMINOSO Y MODERNO
# ============================================================================

COLORS = {
    'primary': '#4F46E5',      # Indigo premium
    'primary_light': '#818CF8', # Indigo claro
    'secondary': '#7C3AED',    # Violeta
    'accent': '#EC4899',       # Rosa vibrante
    'bg_primary': '#FAFAFA',   # Blanco roto (fondo principal)
    'bg_secondary': '#F3F4F6', # Gris muy claro
    'bg_card': '#FFFFFF',      # Blanco puro para cards
    'text_primary': '#111827', # Negro suave
    'text_secondary': '#6B7280', # Gris medio
    'text_muted': '#9CA3AF',   # Gris claro
    'border': '#E5E7EB',       # Borde sutil
    'shadow': 'rgba(0, 0, 0, 0.08)', # Sombra suave
    'gradient_start': '#667EEA', # Inicio gradiente
    'gradient_end': '#764BA2',   # Fin gradiente
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444'
}

# ============================================================================
# CATÁLOGO COMPLETO DE MODELOS (MANTENIDO IGUAL)
# ============================================================================

KIMI_MODELS = {
    "kimi-k2.5": {
        "name": "Kimi K2.5 Ultra",
        "id": "moonshotai/kimi-k2.5",
        "description": "Modelo multimodal más potente con capacidades agenticas avanzadas",
        "features": ["Vision", "Agentic", "Coding", "Long Context"],
        "badges": ["new", "vision", "ultra"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "⚡",
        "vip_level": 1,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-instruct": {
        "name": "Kimi K2.5 Instruct",
        "id": "moonshotai/kimi-k2.5-instruct",
        "description": "Variante instruct optimizada para seguimiento de instrucciones precisas",
        "features": ["Instruction Following", "Structured Output"],
        "badges": ["instruct", "agentic"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "📋",
        "vip_level": 1,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-long-context": {
        "name": "Kimi K2.5 Long Context",
        "id": "moonshotai/kimi-k2.5-long-context",
        "description": "Especializado en procesamiento de contextos extremadamente largos",
        "features": ["Long Context", "Document Analysis"],
        "badges": ["long-context"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "📚",
        "vip_level": 2,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-short-context": {
        "name": "Kimi K2.5 Short Context",
        "id": "moonshotai/kimi-k2.5-short-context",
        "description": "Optimizado para tareas de corto alcance con máxima velocidad",
        "features": ["Fast", "Efficient", "Low Latency"],
        "badges": ["fast"],
        "max_tokens": 4096,
        "context": "32K",
        "icon": "🏃",
        "vip_level": 1,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-extended-thinking": {
        "name": "Kimi K2.5 Extended Thinking",
        "id": "moonshotai/kimi-k2.5-extended-thinking",
        "description": "Modo de razonamiento extendido con cadena de pensamiento visible",
        "features": ["Deep Reasoning", "Chain-of-Thought"],
        "badges": ["reasoning", "thinking"],
        "max_tokens": 12288,
        "context": "256K",
        "icon": "🧠",
        "vip_level": 3,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-vision": {
        "name": "Kimi K2.5 Vision",
        "id": "moonshotai/kimi-k2.5-vision",
        "description": "Especialización máxima en análisis de imágenes y video",
        "features": ["Vision", "Image Analysis", "Video Understanding"],
        "badges": ["vision", "multimodal"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "👁️",
        "vip_level": 2,
        "category": "K2.5 Series"
    },
    "kimi-k2-instruct": {
        "name": "Kimi K2 Instruct",
        "id": "moonshotai/kimi-k2-instruct-0905",
        "description": "Modelo instruct de 1T parámetros optimizado para coding",
        "features": ["Coding", "Tool Use", "MoE Architecture"],
        "badges": ["coding", "moe"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "💻",
        "vip_level": 1,
        "category": "K2 Series"
    },
    "kimi-k2-thinking": {
        "name": "Kimi K2 Thinking",
        "id": "moonshotai/kimi-k2-thinking",
        "description": "Variante con razonamiento profundo y cadena de pensamiento",
        "features": ["Reasoning", "Long Context"],
        "badges": ["reasoning"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🤔",
        "vip_level": 2,
        "category": "K2 Series"
    },
    "kimi-k2-coder": {
        "name": "Kimi K2 Coder",
        "id": "moonshotai/kimi-k2-coder",
        "description": "Especialización en generación de código y debugging",
        "features": ["Coding", "Debugging", "Architecture"],
        "badges": ["coding", "dev"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "⌨️",
        "vip_level": 2,
        "category": "K2 Series"
    },
    "kimi-k2-math": {
        "name": "Kimi K2 Math",
        "id": "moonshotai/kimi-k2-math",
        "description": "Optimizado para razonamiento matemático y STEM",
        "features": ["Math", "Logic", "Theorem Proving"],
        "badges": ["math", "stem"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🔢",
        "vip_level": 2,
        "category": "K2 Series"
    },
    "kimi-k1.5": {
        "name": "Kimi K1.5 Logic",
        "id": "moonshotai/kimi-k1.5",
        "description": "Modelo de razonamiento multimodal comparable con OpenAI o1",
        "features": ["Math", "Logic", "Multimodal Reasoning"],
        "badges": ["reasoning", "advanced"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🎯",
        "vip_level": 2,
        "category": "K1.5 Series"
    },
    "kimi-k1.5-short": {
        "name": "Kimi K1.5 Short",
        "id": "moonshotai/kimi-k1.5-short",
        "description": "Variante corta para razonamiento rápido",
        "features": ["Fast Reasoning", "Quick Math"],
        "badges": ["fast", "reasoning"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "⚡",
        "vip_level": 1,
        "category": "K1.5 Series"
    },
    "kimi-k1.5-long": {
        "name": "Kimi K1.5 Long",
        "id": "moonshotai/kimi-k1.5-long",
        "description": "K1.5 con ventana de contexto extendida",
        "features": ["Long Context", "Deep Analysis"],
        "badges": ["long-context"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "📖",
        "vip_level": 2,
        "category": "K1.5 Series"
    },
    "kimi-vl": {
        "name": "Kimi-VL",
        "id": "moonshotai/kimi-vl",
        "description": "Modelo visión-lenguaje de 16B parámetros",
        "features": ["Vision", "Reasoning", "Agentic"],
        "badges": ["vision", "efficient"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "👀",
        "vip_level": 1,
        "category": "Vision Series"
    },
    "kimi-vl-thinking": {
        "name": "Kimi-VL Thinking",
        "id": "moonshotai/kimi-vl-thinking",
        "description": "Kimi-VL con capacidades de razonamiento profundo",
        "features": ["Vision", "Reasoning", "Thinking"],
        "badges": ["vision", "reasoning"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "🔮",
        "vip_level": 2,
        "category": "Vision Series"
    },
    "kimi-vl-pro": {
        "name": "Kimi-VL Pro",
        "id": "moonshotai/kimi-vl-pro",
        "description": "Versión profesional con máxima calidad de análisis visual",
        "features": ["Vision", "High Quality", "OCR"],
        "badges": ["vision", "pro"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🎨",
        "vip_level": 2,
        "category": "Vision Series"
    },
    "kimi-vl-a3b": {
        "name": "Kimi-VL A3B",
        "id": "moonshotai/kimi-vl-a3b",
        "description": "Optimizada para dispositivos edge y móviles",
        "features": ["Vision", "Edge", "Mobile"],
        "badges": ["vision", "mobile"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "📱",
        "vip_level": 1,
        "category": "Vision Series"
    },
    "kimi-linear": {
        "name": "Kimi Linear",
        "id": "moonshotai/kimi-linear",
        "description": "Arquitectura de atención lineal híbrida, 2.9x más rápido",
        "features": ["Fast", "Long Context", "1M Context"],
        "badges": ["speed", "efficient"],
        "max_tokens": 2048,
        "context": "1M",
        "icon": "🚀",
        "vip_level": 1,
        "category": "Linear Series"
    },
    "kimi-linear-pro": {
        "name": "Kimi Linear Pro",
        "id": "moonshotai/kimi-linear-pro",
        "description": "Versión profesional con contexto de 1M tokens",
        "features": ["Ultra Fast", "1M Context", "Enterprise"],
        "badges": ["speed", "enterprise"],
        "max_tokens": 4096,
        "context": "1M",
        "icon": "⚡",
        "vip_level": 2,
        "category": "Linear Series"
    },
    "kimi-linear-mini": {
        "name": "Kimi Linear Mini",
        "id": "moonshotai/kimi-linear-mini",
        "description": "Versión ligera para dispositivos con recursos limitados",
        "features": ["Ultra Fast", "Lightweight"],
        "badges": ["fast", "mini"],
        "max_tokens": 1024,
        "context": "256K",
        "icon": "💨",
        "vip_level": 1,
        "category": "Linear Series"
    },
    "kimi-audio": {
        "name": "Kimi Audio",
        "id": "moonshotai/kimi-audio",
        "description": "Modelo foundation de audio universal",
        "features": ["Audio", "Speech Recognition", "Voice Chat"],
        "badges": ["audio", "voice"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "🎵",
        "vip_level": 2,
        "category": "Audio Series"
    },
    "kimi-audio-asr": {
        "name": "Kimi Audio ASR",
        "id": "moonshotai/kimi-audio-asr",
        "description": "Especialización en Automatic Speech Recognition",
        "features": ["ASR", "Multilingual", "Transcription"],
        "badges": ["asr"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "🎤",
        "vip_level": 2,
        "category": "Audio Series"
    },
    "kimi-audio-tts": {
        "name": "Kimi Audio TTS",
        "id": "moonshotai/kimi-audio-tts",
        "description": "Text-to-Speech de alta calidad",
        "features": ["TTS", "Natural Voice", "Expressive"],
        "badges": ["tts", "voice"],
        "max_tokens": 4096,
        "context": "64K",
        "icon": "🔊",
        "vip_level": 2,
        "category": "Audio Series"
    },
    "kimi-dev": {
        "name": "Kimi Dev 72B",
        "id": "moonshotai/kimi-dev-72b",
        "description": "Especializado en coding y resolución de issues",
        "features": ["Coding", "Issue Resolution", "Development"],
        "badges": ["coding", "72b"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🛠️",
        "vip_level": 3,
        "category": "Dev Series"
    },
    "kimi-dev-plus": {
        "name": "Kimi Dev Plus",
        "id": "moonshotai/kimi-dev-plus",
        "description": "Versión mejorada con agente de software autónomo",
        "features": ["Autonomous Agent", "Code Review", "Testing"],
        "badges": ["agent", "autonomous"],
        "max_tokens": 8192,
        "context": "128K",
        "icon": "🤖",
        "vip_level": 3,
        "category": "Dev Series"
    },
    "kimi-moe-general": {
        "name": "Kimi MoE General",
        "id": "moonshotai/kimi-moe-general",
        "description": "Arquitectura MoE de propósito general",
        "features": ["General Purpose", "MoE", "Scalable"],
        "badges": ["moe"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🌐",
        "vip_level": 2,
        "category": "MoE Series"
    },
    "kimi-moe-coding": {
        "name": "Kimi MoE Coding",
        "id": "moonshotai/kimi-moe-coding",
        "description": "Especialización MoE para código a gran escala",
        "features": ["Coding", "MoE", "Scale"],
        "badges": ["moe", "coding"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "💾",
        "vip_level": 2,
        "category": "MoE Series"
    },
    "kimi-k1": {
        "name": "Kimi K1 (Legacy)",
        "id": "moonshotai/kimi-k1",
        "description": "Modelo base K1 con capacidades de razonamiento",
        "features": ["Reasoning", "Foundation"],
        "badges": ["legacy"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "📜",
        "vip_level": 1,
        "category": "Legacy Series"
    },
    "kimi-chat": {
        "name": "Kimi Chat (Legacy)",
        "id": "moonshotai/kimi-chat",
        "description": "Modelo de conversación original",
        "features": ["Chat", "Conversation"],
        "badges": ["legacy"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "💬",
        "vip_level": 1,
        "category": "Legacy Series"
    },
    "kimi-research": {
        "name": "Kimi Research (Beta)",
        "id": "moonshotai/kimi-research",
        "description": "Modelo experimental para investigación científica",
        "features": ["Research", "Scientific", "Academic"],
        "badges": ["beta", "research"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "🔬",
        "vip_level": 3,
        "category": "Experimental"
    },
    "kimi-legal": {
        "name": "Kimi Legal (Beta)",
        "id": "moonshotai/kimi-legal",
        "description": "Especialización en análisis legal y contratos",
        "features": ["Legal", "Contracts", "Compliance"],
        "badges": ["beta", "legal"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "⚖️",
        "vip_level": 3,
        "category": "Experimental"
    },
    "kimi-medical": {
        "name": "Kimi Medical (Beta)",
        "id": "moonshotai/kimi-medical",
        "description": "Orientado a análisis médico e investigación biomédica",
        "features": ["Medical", "Biomedical", "Clinical"],
        "badges": ["beta", "medical"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🏥",
        "vip_level": 3,
        "category": "Experimental"
    }
}

# ============================================================================
# CSS PERSONALIZADO - ESTILO KIMI NATIVO CON EFECTOS 3D PREMIUM
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Fondo principal con gradiente sutil y efecto 3D */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-attachment: fixed;
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Capa de glassmorphism sobre el fondo */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        z-index: -1;
    }}
    
    /* Header estilo Kimi nativo */
    .vip-header {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    
    .vip-logo {{
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }}
    
    .vip-badge {{
        background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['gradient_end']} 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Cards de Modelos con efectos 3D */
    .model-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        padding: 1.5rem;
    }}
    
    .model-card-vip {{
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.5) inset,
            0 20px 40px rgba(102, 126, 234, 0.1);
        transform-style: preserve-3d;
    }}
    
    .model-card-vip::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }}
    
    .model-card-vip:hover::before {{
        left: 100%;
    }}
    
    .model-card-vip:hover {{
        transform: translateY(-8px) rotateX(5deg) rotateY(5deg);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.8) inset,
            0 30px 60px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }}
    
    .model-card-vip.active {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(255, 255, 255, 0.95) 100%);
        border: 2px solid {COLORS['primary']};
        box-shadow: 
            0 0 30px rgba(102, 126, 234, 0.3),
            0 10px 40px rgba(0, 0, 0, 0.1);
    }}
    
    .model-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
    }}
    
    .model-name {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }}
    
    .model-desc {{
        font-size: 0.9rem;
        color: {COLORS['text_secondary']};
        line-height: 1.5;
        margin-bottom: 1rem;
    }}
    
    .model-meta {{
        display: flex;
        gap: 1rem;
        font-size: 0.8rem;
        color: {COLORS['text_muted']};
        font-weight: 500;
    }}
    
    .badge-vip {{
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    .badge-primary {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    .badge-secondary {{
        background: rgba(255, 255, 255, 0.8);
        color: {COLORS['primary']};
        border: 1px solid rgba(102, 126, 234, 0.2);
    }}
    
    /* Chat Interface estilo Kimi nativo */
    .chat-container {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        height: calc(100vh - 180px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.8) inset;
        backdrop-filter: blur(20px);
    }}
    
    .chat-messages {{
        flex: 1;
        overflow-y: auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }}
    
    .message {{
        max-width: 85%;
        padding: 1.25rem 1.75rem;
        border-radius: 20px;
        font-size: 0.95rem;
        line-height: 1.6;
        animation: messageSlide 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }}
    
    @keyframes messageSlide {{
        from {{ 
            opacity: 0; 
            transform: translateY(20px) scale(0.95); 
        }}
        to {{ 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }}
    }}
    
    .message-user {{
        align-self: flex-end;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 
            0 10px 30px rgba(79, 70, 229, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset;
    }}
    
    .message-assistant {{
        align-self: flex-start;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(229, 231, 235, 0.8);
        border-bottom-left-radius: 4px;
        color: {COLORS['text_primary']};
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.05),
            0 0 0 1px rgba(255, 255, 255, 0.8) inset;
    }}
    
    .message-model {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }}
    
    /* Input Area estilo Kimi nativo */
    .input-container {{
        padding: 1.5rem 2rem;
        background: rgba(255, 255, 255, 0.8);
        border-top: 1px solid rgba(229, 231, 235, 0.5);
        backdrop-filter: blur(10px);
    }}
    
    /* TEXTAREA estilo - Reemplaza al input para evitar envío con Enter */
    .stTextArea > div > div > textarea {{
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(229, 231, 235, 0.8) !important;
        border-radius: 16px !important;
        color: {COLORS['text_primary']} !important;
        padding: 1rem 1.25rem !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        resize: none !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.05),
            0 0 0 1px rgba(255, 255, 255, 0.5) inset !important;
        transition: all 0.3s ease !important;
        min-height: 60px !important;
        max-height: 200px !important;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 
            0 0 0 4px rgba(79, 70, 229, 0.1),
            0 4px 20px rgba(0, 0, 0, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: {COLORS['text_muted']} !important;
    }}
    
    /* BOTÓN ENVIAR ESTILO KIMI NATIVO - AHORA ES EL ÚNICO MÉTODO DE ENVÍO */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        box-shadow: 
            0 4px 15px rgba(79, 70, 229, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        transform: translateZ(0);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 8px 25px rgba(79, 70, 229, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.3) inset !important;
    }
    
    .stButton > button:active {{
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Botón de enviar específico - tamaño nativo Kimi */
    button[kind="primary"] {{
        height: 44px !important;
        min-width: 80px !important;
        border-radius: 10px !important;
    }}
    
    /* Workspace/Code Panel con efectos 3D */
    .workspace-panel {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        overflow: hidden;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.8) inset;
        backdrop-filter: blur(10px);
    }}
    
    .workspace-header {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
        padding: 1rem 1.25rem;
        border-bottom: 1px solid rgba(229, 231, 235, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .workspace-content {{
        padding: 1.25rem;
        max-height: 400px;
        overflow-y: auto;
        color: {COLORS['text_primary']};
        background: rgba(249, 250, 251, 0.8);
    }}
    
    /* Sidebar estilo moderno */
    .css-1d391kg {{
        background: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid rgba(229, 231, 235, 0.5) !important;
        backdrop-filter: blur(20px) !important;
    }}
    
    /* Scrollbar moderna */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.05);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['accent']} 100%);
    }}
    
    /* Utility classes */
    .text-primary {{ color: {COLORS['primary']} !important; }}
    .text-secondary {{ color: {COLORS['text_secondary']} !important; }}
    
    /* Loading Animation moderna */
    .loading-pulse {{
        display: inline-flex;
        gap: 4px;
    }}
    
    .loading-pulse span {{
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 50%;
        animation: pulse 1.4s infinite ease-in-out both;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
    }}
    
    .loading-pulse span:nth-child(1) {{ animation-delay: -0.32s; }}
    .loading-pulse span:nth-child(2) {{ animation-delay: -0.16s; }}
    
    @keyframes pulse {{
        0%, 80%, 100% {{ transform: scale(0); opacity: 0.5; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}
    
    /* Category Headers con efecto 3D */
    .category-header {{
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, transparent 100%);
        padding: 1rem 1.25rem;
        margin: 2rem 0 1.25rem 0;
        border-left: 4px solid {COLORS['primary']};
        border-radius: 0 12px 12px 0;
        font-weight: 700;
        color: {COLORS['primary']};
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
    }}
    
    /* Efectos de profundidad adicionales */
    .depth-1 {{ box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); }}
    .depth-2 {{ box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); }}
    .depth-3 {{ 
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.5) inset;
    }}
    
    /* Mobile Optimizations */
    @media (max-width: 768px) {{
        .model-grid {{
            grid-template-columns: 1fr;
            gap: 1rem;
            padding: 1rem;
        }}
        .message {{
            max-width: 95%;
            padding: 1rem 1.25rem;
        }}
        .vip-header {{
            padding: 0.75rem 1rem;
        }}
        .chat-container {{
            height: calc(100vh - 160px);
            border-radius: 20px;
        }}
    }}
    
    /* Efectos de glassmorphism adicionales */
    .glass {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Botones de acción secundarios */
    .btn-secondary {{
        background: rgba(255, 255, 255, 0.9) !important;
        color: {COLORS['text_primary']} !important;
        border: 1px solid rgba(229, 231, 235, 0.8) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }}
    
    .btn-secondary:hover {{
        background: rgba(255, 255, 255, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }}
    
    /* Indicador de que se debe usar el botón */
    .send-hint {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 500;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CLASES DE NEGOCIO - SIN CONTADORES
# ============================================================================

class KimiVIPChat:
    def __init__(self, model_key="kimi-k2-instruct"):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=st.secrets.get("NVIDIA_API_KEY", "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")
        )
        self.model_key = model_key
        self.model_info = KIMI_MODELS[model_key]
        self.model_id = self.model_info["id"]
    
    def chat(self, message, temperature=0.7, max_tokens=None):
        try:
            tokens = max_tokens or self.model_info["max_tokens"]
            
            system_prompt = f"""Eres {self.model_info['name']}, un asistente AI premium en Kimi Onyx VIP.
Características: {', '.join(self.model_info['features'])}
Responde de manera profesional, clara y concisa."""
            
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=temperature,
                max_tokens=tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    
    def generate_code(self, prompt, language="python"):
        code_prompt = f"""Genera código {language} de alta calidad para: {prompt}
Incluye comentarios profesionales y mejores prácticas.
Responde SOLO con el código, sin explicaciones adicionales."""
        
        return self.chat(code_prompt, temperature=0.3, max_tokens=4096)

class VIPZipGenerator:
    def __init__(self):
        self.templates = {
            'react': self._react_template,
            'python': self._python_template,
            'android': self._android_template
        }
    
    def _react_template(self, model_info):
        return f'''// Kimi Onyx VIP - React App
import React from 'react';
import {{ OpenAI }} from 'openai';

const client = new OpenAI({{
    baseURL: "https://integrate.api.nvidia.com/v1",
    apiKey: "YOUR_API_KEY",
    dangerouslyAllowBrowser: true
}});

export default function App() {{
    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600">
            <h1>{model_info['name']} Onyx VIP</h1>
        </div>
    );
}}'''

    def _python_template(self, model_info):
        return f'''# Kimi Onyx VIP - Python App
import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="YOUR_API_KEY"
)

st.title("🌙 {model_info['name']} Onyx VIP")

if prompt := st.chat_input("Mensaje..."):
    response = client.chat.completions.create(
        model="{model_info['id']}",
        messages=[{{"role": "user", "content": prompt}}],
        max_tokens={model_info['max_tokens']}
    )
    st.write(response.choices[0].message.content)
'''

    def _android_template(self, model_info):
        return f'''[app]
title = {model_info['name']} Onyx VIP
package.name = kimi.onyx.vip
version = 2.0.0
requirements = python3,kivy,openai
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
'''

    def generate_project(self, model_key, project_type='python'):
        model_info = KIMI_MODELS[model_key]
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            if project_type == 'react':
                zf.writestr('src/App.jsx', self._react_template(model_info))
                zf.writestr('package.json', json.dumps({
                    "name": f"kimi-onyx-{model_key}",
                    "version": "2.0.0",
                    "dependencies": {"react": "^18.2.0", "openai": "^4.0.0"}
                }, indent=2))
            elif project_type == 'android':
                zf.writestr('buildozer.spec', self._android_template(model_info))
                zf.writestr('main.py', self._python_template(model_info))
            else:
                zf.writestr('app.py', self._python_template(model_info))
                zf.writestr('requirements.txt', 'streamlit>=1.28.0\\nopenai>=1.6.0\\n')
            
            zf.writestr('README.md', f'''# 🌙 {model_info['name']} Onyx VIP

## Configuración
- **Modelo:** {model_info['id']}
- **Categoría:** {model_info['category']}
- **Contexto:** {model_info['context']}
- **Tokens:** {model_info['max_tokens']}

## Características
{chr(10).join(['- ' + f for f in model_info['features']])}

---
Generado por Kimi Onyx VIP
''')
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

# ============================================================================
# INICIALIZACIÓN DE ESTADO - SIN CONTADORES
# ============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "kimi-k2-instruct"
if 'chat_engine' not in st.session_state:
    st.session_state.chat_engine = KimiVIPChat(st.session_state.selected_model)
if 'zip_generator' not in st.session_state:
    st.session_state.zip_generator = VIPZipGenerator()
if 'workspace_code' not in st.session_state:
    st.session_state.workspace_code = "# Workspace listo para generar código..."
if 'show_workspace' not in st.session_state:
    st.session_state.show_workspace = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = "vip@kimi.com"
if 'chat_input_text' not in st.session_state:
    st.session_state.chat_input_text = ""

# ============================================================================
# HEADER VIP ESTILO KIMI
# ============================================================================

st.markdown(f"""
<div class="vip-header">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 1.75rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">🌙</span>
        <div>
            <div class="vip-logo">Kimi Onyx VIP</div>
            <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; font-weight: 500; letter-spacing: 0.05em;">Multi-Model AI Platform</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 0.85rem; color: {COLORS['text_secondary']}; font-weight: 500;">{st.session_state.user_email}</span>
        <span class="vip-badge">VIP ACCESS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# NAVEGACIÓN PRINCIPAL
# ============================================================================

menu = st.sidebar.radio(
    "Navegación",
    ["💬 Chat", "🎨 Modelos", "💻 Workspace", "📦 Exportar", "⚙️ Config"],
    label_visibility="collapsed"
)

# ============================================================================
# SECCIÓN: CHAT ESTILO KIMI NATIVO - SOLO BOTÓN PARA ENVIAR
# ============================================================================

if menu == "💬 Chat":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 Modelo Activo")
    
    models_by_category = {}
    for key, model in KIMI_MODELS.items():
        cat = model['category']
        if cat not in models_by_category:
            models_by_category[cat] = []
        models_by_category[cat].append((key, model))
    
    model_options = []
    for cat in sorted(models_by_category.keys()):
        for key, model in models_by_category[cat]:
            model_options.append((key, f"{model['icon']} [{cat}] {model['name']}"))
    
    current_index = next((i for i, (k, _) in enumerate(model_options) if k == st.session_state.selected_model), 0)
    
    selected_display = st.sidebar.selectbox(
        "Seleccionar modelo:",
        options=[m[1] for m in model_options],
        index=current_index
    )
    
    new_model = next(k for k, display in model_options if display == selected_display)
    
    if new_model != st.session_state.selected_model:
        st.session_state.selected_model = new_model
        st.session_state.chat_engine = KimiVIPChat(new_model)
        st.session_state.messages = []
        st.session_state.chat_input_text = ""  # Limpiar input al cambiar modelo
        st.rerun()
    
    current = KIMI_MODELS[st.session_state.selected_model]
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 12px; margin-top: 1rem; border: 1px solid rgba(229,231,235,0.5);">
        <strong style="color: {COLORS['primary']}; font-size: 1.1rem;">{current['name']}</strong><br>
        <small style="color: {COLORS['text_secondary']};">
        📏 {current['context']} contexto<br>
        🔢 {current['max_tokens']} tokens<br>
        ⭐ Nivel VIP-{current['vip_level']}
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    temperatura = st.sidebar.slider("Creatividad", 0.0, 1.0, 0.7, 0.1)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="color: white; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                💬 Chat con {current['icon']} {current['name']}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                css_class = "message-user" if msg['role'] == 'user' else "message-assistant"
                model_tag = f'<div class="message-model">{msg.get("model", "Kimi")}</div>' if msg['role'] == 'assistant' else ''
                
                st.markdown(f"""
                <div class="message {css_class}">
                    {model_tag}
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # ÁREA DE INPUT CON TEXTAREA (NO ENVÍA CON ENTER) + BOTÓN ENVIAR
        with st.container():
            # Usar textarea en lugar de text_input para evitar envío con Enter
            prompt = st.text_area(
                "Mensaje",
                value=st.session_state.chat_input_text,
                placeholder="Escribe tu mensaje aquí... (Usa el botón ➤ para enviar)",
                height=80,
                label_visibility="collapsed",
                key="chat_textarea"
            )
            
            # Botón enviar debajo del textarea
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown('<div class="send-hint">Presiona el botón ➤ para enviar tu mensaje</div>', unsafe_allow_html=True)
            with cols[1]:
                send = st.button("➤", use_container_width=True, type="primary")
            
            # Procesar envío SOLO cuando se presiona el botón
            if send and prompt and prompt.strip():
                # Guardar mensaje de usuario
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt.strip(),
                    "timestamp": datetime.now()
                })
                
                # Limpiar el input inmediatamente
                st.session_state.chat_input_text = ""
                
                # Generar respuesta
                with st.spinner(""):
                    st.markdown("""
                    <div class="loading-pulse">
                        <span></span><span></span><span></span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    response = st.session_state.chat_engine.chat(prompt.strip(), temperature=temperatura)
                    
                    # Detectar código para workspace
                    if "```" in response:
                        code_blocks = response.split("```")
                        for i, block in enumerate(code_blocks):
                            if i % 2 == 1:
                                lang = block.split('\n')[0] if block.split('\n')[0] else 'python'
                                code = '\n'.join(block.split('\n')[1:]) if block.split('\n')[0] else block
                                st.session_state.workspace_code = f"# {lang.upper()}\n{code}"
                    
                    # Agregar respuesta del asistente
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "model": current['name'],
                        "timestamp": datetime.now()
                    })
                
                # Forzar rerun para actualizar la interfaz y limpiar el textarea
                st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.6);">
            <h3 style="color: #111827; margin-bottom: 1.5rem; font-weight: 700;">⚡ Acciones Rápidas</h3>
        """, unsafe_allow_html=True)
        
        if st.button("🧹 Limpiar Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_input_text = ""
            st.rerun()
        
        if st.button("💻 Abrir Workspace", use_container_width=True):
            st.session_state.show_workspace = True
        
        st.markdown("---")
        st.markdown("### 🚀 Generar Código")
        code_type = st.selectbox("Tipo", ["Python", "React", "Android", "API"])
        code_prompt = st.text_area("Descripción", height=100, placeholder="Describe lo que necesitas...", key="code_gen_input")
        
        if st.button("✨ Generar", use_container_width=True):
            with st.spinner("Generando..."):
                lang_map = {"Python": "python", "React": "jsx", "Android": "kotlin", "API": "python"}
                generated = st.session_state.chat_engine.generate_code(code_prompt, lang_map[code_type])
                st.session_state.workspace_code = generated
                st.session_state.show_workspace = True
                st.success("¡Código generado!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# SECCIÓN: MODELOS CON EFECTOS 3D
# ============================================================================

elif menu == "🎨 Modelos":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-weight: 800; text-shadow: 0 4px 20px rgba(0,0,0,0.2); font-size: 2.5rem;">
            🎨 Catálogo de Modelos VIP
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; font-weight: 500;">
            32 modelos premium organizados por categoría
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    categories = {}
    for key, model in KIMI_MODELS.items():
        cat = model['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, model))
    
    for category in sorted(categories.keys()):
        st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
        
        models_in_cat = categories[category]
        cols = st.columns(3)
        
        for idx, (key, model) in enumerate(models_in_cat):
            with cols[idx % 3]:
                is_active = key == st.session_state.selected_model
                active_class = "active" if is_active else ""
                
                badges_html = "".join([f'<span class="badge-vip badge-primary">{b}</span>' if i == 0 else f'<span class="badge-vip badge-secondary">{b}</span>' for i, b in enumerate(model["badges"])])
                
                st.markdown(f"""
                <div class="model-card-vip {active_class}">
                    <div class="model-icon">{model['icon']}</div>
                    <div class="model-name">{model['name']}</div>
                    <div style="margin-bottom: 0.75rem;">{badges_html}</div>
                    <div class="model-desc">{model['description']}</div>
                    <div class="model-meta">
                        <span>📏 {model['context']}</span>
                        <span>🔢 {model['max_tokens']}</span>
                    </div>
                    <div style="margin-top: 0.75rem; font-size: 0.8rem; color: {COLORS['primary']}; font-weight: 600;">
                        ⭐ Nivel VIP-{model['vip_level']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Seleccionar", key=f"btn_{key}", use_container_width=True):
                    st.session_state.selected_model = key
                    st.session_state.chat_engine = KimiVIPChat(key)
                    st.session_state.messages = []
                    st.session_state.chat_input_text = ""
                    st.success(f"✅ {model['name']} seleccionado")
                    time.sleep(0.5)
                    st.rerun()

# ============================================================================
# SECCIÓN: WORKSPACE
# ============================================================================

elif menu == "💻 Workspace":
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: white; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">💻 Workspace de Desarrollo</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        edited_code = st.text_area(
            "Editor",
            value=st.session_state.workspace_code,
            height=500,
            label_visibility="collapsed"
        )
        
        if edited_code != st.session_state.workspace_code:
            st.session_state.workspace_code = edited_code
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <h3 style="color: #111827; margin-bottom: 1.5rem; font-weight: 700;">🎯 Acciones</h3>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copiar", use_container_width=True):
            st.code(st.session_state.workspace_code)
        
        if st.button("💾 Descargar", use_container_width=True):
            st.download_button(
                label="⬇️ Descargar archivo",
                data=st.session_state.workspace_code,
                file_name=f"onyx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                mime="text/plain",
                use_container_width=True
            )
        
        if st.button("🧹 Limpiar", use_container_width=True):
            st.session_state.workspace_code = "# Workspace limpio..."
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📦 Generar Proyecto")
        proj_type = st.selectbox("Tipo", ["Python", "React", "Android"])
        
        if st.button("⚡ Crear ZIP", use_container_width=True):
            zip_data = st.session_state.zip_generator.generate_project(
                st.session_state.selected_model,
                proj_type.lower()
            )
            st.download_button(
                label="⬇️ Descargar",
                data=zip_data,
                file_name=f"ONYX_{st.session_state.selected_model}_{proj_type.upper()}.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# SECCIÓN: EXPORTAR
# ============================================================================

elif menu == "📦 Exportar":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-weight: 800; text-shadow: 0 4px 20px rgba(0,0,0,0.2);">📦 Exportar Proyectos</h1>
    </div>
    """, unsafe_allow_html=True)
    
    model = KIMI_MODELS[st.session_state.selected_model]
    
    col1, col2, col3 = st.columns(3)
    
    export_cards = [
        ("🐍", "Python App", "Streamlit completa lista para ejecutar", "python"),
        ("⚛️", "React App", "Frontend moderno con diseño premium", "react"),
        ("📱", "Android APK", "Compila para Android con Buildozer", "android")
    ]
    
    for col, (icon, title, desc, ptype) in zip([col1, col2, col3], export_cards):
        with col:
            st.markdown(f"""
            <div class="model-card-vip" style="text-align: center;">
                <div class="model-icon" style="font-size: 3rem;">{icon}</div>
                <div class="model-name">{title}</div>
                <div class="model-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Generar {ptype.title()}", key=f"gen_{ptype}", use_container_width=True):
                zip_data = st.session_state.zip_generator.generate_project(
                    st.session_state.selected_model, ptype
                )
                st.download_button(
                    f"⬇️ Descargar {ptype.title()}",
                    data=zip_data,
                    file_name=f"ONYX_{model['name']}_{ptype.upper()}.zip",
                    mime="application/zip",
                    use_container_width=True
                )

# ============================================================================
# SECCIÓN: CONFIGURACIÓN - SIN ESTADÍSTICAS DE USO
# ============================================================================

else:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: white; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">⚙️ Configuración VIP</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <h3 style="color: #111827; margin-bottom: 1.5rem; font-weight: 700;">👤 Perfil</h3>
        """, unsafe_allow_html=True)
        
        new_email = st.text_input("Email VIP", value=st.session_state.user_email)
        if new_email != st.session_state.user_email:
            st.session_state.user_email = new_email
            st.success("Perfil actualizado")
        
        st.markdown("### 🔑 API Key")
        st.code("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"[:30] + "...", language="bash")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <h3 style="color: #111827; margin-bottom: 1.5rem; font-weight: 700;">📊 Información del Sistema</h3>
        """, unsafe_allow_html=True)
        
        total_models = len(KIMI_MODELS)
        categories_count = len(set(m['category'] for m in KIMI_MODELS.values()))
        
        st.metric("Total Modelos Disponibles", total_models)
        st.metric("Categorías", categories_count)
        st.metric("Nivel de Acceso", "VIP-3 (Ilimitado)")
        st.metric("Versión", "2.0.0 Premium")
        
        if st.button("🗑️ Limpiar historial de chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_input_text = ""
            st.success("Historial limpiado")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FOOTER ESTILO KIMI - SIN CONTADORES
# ============================================================================

st.markdown(f"""
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-top: 1px solid rgba(229, 231, 235, 0.5);
    padding: 1rem;
    text-align: center;
    font-size: 0.8rem;
    color: {COLORS['text_secondary']};
    z-index: 999;
    font-weight: 500;
">
    <span style="color: {COLORS['primary']}; font-weight: 700;">🌙 Kimi Onyx VIP</span> • 
    {len(KIMI_MODELS)} Modelos Premium • 
    {st.session_state.user_email} • 
    {datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
