# KIMI ONYX VIP - UNIFIED MULTI-MODEL AI PLATFORM
# Backend: Python/Streamlit + Frontend: React-inspired UI
# API KEY INCLUIDA: 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
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
# CONFIGURACIÓN INICIAL VIP
# ============================================================================

st.set_page_config(
    page_title="⚡ KIMI ONYX VIP | Multi-Model AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CONSTANTES VIP
# ============================================================================

NVIDIA_API_KEY = "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"

# Paleta de colores Onyx VIP
COLORS = {
    'gold': '#D4AF37',
    'gold_light': '#F4E4BC',
    'black': '#000000',
    'dark_gray': '#0a0a0a',
    'medium_gray': '#111111',
    'light_gray': '#333333',
    'white': '#FFFFFF',
    'accent': '#667EEA'
}

# ============================================================================
# CATÁLOGO COMPLETO DE MODELOS KIMI (VIP EDITION - TODOS LOS MODELOS)
# ============================================================================

KIMI_MODELS = {
    "kimi-k2.5": {
        "name": "Kimi K2.5 Ultra",
        "id": "moonshotai/kimi-k2.5",
        "description": "Modelo multimodal más potente con capacidades agenticas avanzadas, soporte de visión y modos Instant/Thinking",
        "features": ["Vision", "Agentic", "Coding", "Long Context", "Multimodal"],
        "badges": ["new", "vision", "ultra", "multimodal"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "⚡",
        "vip_level": 1,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-instruct": {
        "name": "Kimi K2.5 Instruct",
        "id": "moonshotai/kimi-k2.5-instruct",
        "description": "Variante instruct optimizada para seguimiento de instrucciones precisas y tareas estructuradas",
        "features": ["Instruction Following", "Structured Output", "Agentic", "Tool Use"],
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
        "description": "Especializado en procesamiento de contextos extremadamente largos hasta 256K tokens",
        "features": ["Long Context", "Document Analysis", "RAG", "Memory"],
        "badges": ["long-context", "memory"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "📚",
        "vip_level": 2,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-short-context": {
        "name": "Kimi K2.5 Short Context",
        "id": "moonshotai/kimi-k2.5-short-context",
        "description": "Optimizado para tareas de corto alcance con máxima velocidad y eficiencia",
        "features": ["Fast", "Efficient", "Quick Tasks", "Low Latency"],
        "badges": ["fast", "efficient"],
        "max_tokens": 4096,
        "context": "32K",
        "icon": "🏃",
        "vip_level": 1,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-extended-thinking": {
        "name": "Kimi K2.5 Extended Thinking",
        "id": "moonshotai/kimi-k2.5-extended-thinking",
        "description": "Modo de razonamiento extendido con cadena de pensamiento visible y profundidad máxima",
        "features": ["Deep Reasoning", "Chain-of-Thought", "Analysis", "Research"],
        "badges": ["reasoning", "thinking", "deep"],
        "max_tokens": 12288,
        "context": "256K",
        "icon": "🧠",
        "vip_level": 3,
        "category": "K2.5 Series"
    },
    "kimi-k2.5-vision": {
        "name": "Kimi K2.5 Vision",
        "id": "moonshotai/kimi-k2.5-vision",
        "description": "Especialización máxima en análisis de imágenes, video y contenido visual multimodal",
        "features": ["Vision", "Image Analysis", "Video Understanding", "OCR", "Visual Reasoning"],
        "badges": ["vision", "multimodal", "visual"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "👁️",
        "vip_level": 2,
        "category": "K2.5 Series"
    },
    "kimi-k2-instruct": {
        "name": "Kimi K2 Instruct",
        "id": "moonshotai/kimi-k2-instruct-0905",
        "description": "Modelo instruct de 1T parámetros (32B activos), optimizado para coding y agentes",
        "features": ["Coding", "Tool Use", "Reasoning", "MoE Architecture"],
        "badges": ["coding", "pro", "moe"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "💻",
        "vip_level": 1,
        "category": "K2 Series"
    },
    "kimi-k2-thinking": {
        "name": "Kimi K2 Thinking",
        "id": "moonshotai/kimi-k2-thinking",
        "description": "Variante con razonamiento profundo, cadena de pensamiento y hasta 256K contexto",
        "features": ["Reasoning", "Long Context", "Chain-of-Thought", "Analysis"],
        "badges": ["reasoning", "thinking"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🤔",
        "vip_level": 2,
        "category": "K2 Series"
    },
    "kimi-k2-coder": {
        "name": "Kimi K2 Coder",
        "id": "moonshotai/kimi-k2-coder",
        "description": "Especialización en generación de código, debugging y arquitectura de software",
        "features": ["Coding", "Debugging", "Architecture", "Multiple Languages"],
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
        "description": "Optimizado para razonamiento matemático, resolución de problemas y teoría",
        "features": ["Math", "Logic", "Theorem Proving", "STEM"],
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
        "description": "Modelo de razonamiento multimodal comparable con OpenAI o1 en matemáticas y coding",
        "features": ["Math", "Logic", "Multimodal Reasoning", "Competition Level"],
        "badges": ["reasoning", "math", "advanced"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🎯",
        "vip_level": 2,
        "category": "K1.5 Series"
    },
    "kimi-k1.5-short": {
        "name": "Kimi K1.5 Short",
        "id": "moonshotai/kimi-k1.5-short",
        "description": "Variante corta de K1.5 para razonamiento rápido sin pérdida de calidad",
        "features": ["Fast Reasoning", "Quick Math", "Efficient Logic"],
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
        "description": "K1.5 con ventana de contexto extendida para análisis profundo de documentos",
        "features": ["Long Context", "Deep Analysis", "Document Reasoning"],
        "badges": ["long-context", "reasoning"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "📖",
        "vip_level": 2,
        "category": "K1.5 Series"
    },
    "kimi-vl": {
        "name": "Kimi-VL",
        "id": "moonshotai/kimi-vl",
        "description": "Modelo de visión-lenguaje de 16B parámetros (3B activos) para razonamiento multimodal",
        "features": ["Vision", "Reasoning", "Agentic", "Efficient"],
        "badges": ["vision", "efficient", "lightweight"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "👀",
        "vip_level": 1,
        "category": "Vision Series"
    },
    "kimi-vl-thinking": {
        "name": "Kimi-VL Thinking",
        "id": "moonshotai/kimi-vl-thinking",
        "description": "Variante de Kimi-VL con capacidades de razonamiento profundo integrado",
        "features": ["Vision", "Reasoning", "Thinking", "Deep Analysis"],
        "badges": ["vision", "reasoning", "thinking"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "🔮",
        "vip_level": 2,
        "category": "Vision Series"
    },
    "kimi-vl-pro": {
        "name": "Kimi-VL Pro",
        "id": "moonshotai/kimi-vl-pro",
        "description": "Versión profesional de visión-lenguaje con máxima calidad de análisis visual",
        "features": ["Vision", "High Quality", "Professional", "OCR", "Charts"],
        "badges": ["vision", "pro", "quality"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🎨",
        "vip_level": 2,
        "category": "Vision Series"
    },
    "kimi-vl-a3b": {
        "name": "Kimi-VL A3B",
        "id": "moonshotai/kimi-vl-a3b",
        "description": "Variante A3B optimizada para dispositivos edge y aplicaciones móviles",
        "features": ["Vision", "Edge", "Mobile", "Lightweight", "Fast"],
        "badges": ["vision", "edge", "mobile"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "📱",
        "vip_level": 1,
        "category": "Vision Series"
    },
    "kimi-linear": {
        "name": "Kimi Linear",
        "id": "moonshotai/kimi-linear",
        "description": "Arquitectura de atención lineal híbrida, 48B parámetros (3B activos), 2.9x más rápido",
        "features": ["Fast", "Long Context", "Efficient", "Hybrid Attention"],
        "badges": ["new", "speed", "efficient"],
        "max_tokens": 2048,
        "context": "1M",
        "icon": "🚀",
        "vip_level": 1,
        "category": "Linear Series"
    },
    "kimi-linear-pro": {
        "name": "Kimi Linear Pro",
        "id": "moonshotai/kimi-linear-pro",
        "description": "Versión profesional con contexto de 1M tokens y máxima velocidad de procesamiento",
        "features": ["Ultra Fast", "1M Context", "Professional", "Enterprise"],
        "badges": ["speed", "enterprise", "pro"],
        "max_tokens": 4096,
        "context": "1M",
        "icon": "⚡",
        "vip_level": 2,
        "category": "Linear Series"
    },
    "kimi-linear-mini": {
        "name": "Kimi Linear Mini",
        "id": "moonshotai/kimi-linear-mini",
        "description": "Versión ligera de Linear para tareas rápidas y dispositivos con recursos limitados",
        "features": ["Ultra Fast", "Lightweight", "Mobile", "Efficient"],
        "badges": ["fast", "mini", "mobile"],
        "max_tokens": 1024,
        "context": "256K",
        "icon": "💨",
        "vip_level": 1,
        "category": "Linear Series"
    },
    "kimi-audio": {
        "name": "Kimi Audio",
        "id": "moonshotai/kimi-audio",
        "description": "Modelo foundation de audio universal: reconocimiento, comprensión, chat voz-a-texto",
        "features": ["Audio", "Speech Recognition", "Audio Understanding", "Voice Chat"],
        "badges": ["audio", "speech", "voice"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "🎵",
        "vip_level": 2,
        "category": "Audio Series"
    },
    "kimi-audio-asr": {
        "name": "Kimi Audio ASR",
        "id": "moonshotai/kimi-audio-asr",
        "description": "Especialización en Automatic Speech Recognition con soporte multilingüe",
        "features": ["ASR", "Multilingual", "Transcription", "Real-time"],
        "badges": ["asr", "transcription"],
        "max_tokens": 2048,
        "context": "64K",
        "icon": "🎤",
        "vip_level": 2,
        "category": "Audio Series"
    },
    "kimi-audio-tts": {
        "name": "Kimi Audio TTS",
        "id": "moonshotai/kimi-audio-tts",
        "description": "Text-to-Speech de alta calidad con voces naturales y expresivas",
        "features": ["TTS", "Natural Voice", "Expressive", "Multilingual"],
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
        "description": "Especializado en coding y resolución de issues, 72B parámetros, SOTA en SWE-bench",
        "features": ["Coding", "Issue Resolution", "Development", "Debugging", "Architecture"],
        "badges": ["coding", "dev", "sota", "72b"],
        "max_tokens": 4096,
        "context": "128K",
        "icon": "🛠️",
        "vip_level": 3,
        "category": "Dev Series"
    },
    "kimi-dev-plus": {
        "name": "Kimi Dev Plus",
        "id": "moonshotai/kimi-dev-plus",
        "description": "Versión mejorada de Kimi Dev con capacidades de agente de software autónomo",
        "features": ["Autonomous Agent", "Code Review", "Refactoring", "Testing"],
        "badges": ["agent", "autonomous", "dev"],
        "max_tokens": 8192,
        "context": "128K",
        "icon": "🤖",
        "vip_level": 3,
        "category": "Dev Series"
    },
    "kimi-moe-general": {
        "name": "Kimi MoE General",
        "id": "moonshotai/kimi-moe-general",
        "description": "Arquitectura MoE de propósito general con 1T parámetros totales",
        "features": ["General Purpose", "MoE", "Efficient", "Scalable"],
        "badges": ["moe", "general"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🌐",
        "vip_level": 2,
        "category": "MoE Series"
    },
    "kimi-moe-coding": {
        "name": "Kimi MoE Coding",
        "id": "moonshotai/kimi-moe-coding",
        "description": "Especialización MoE para generación y análisis de código a gran escala",
        "features": ["Coding", "MoE", "Scale", "Multiple Languages"],
        "badges": ["moe", "coding", "scale"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "💾",
        "vip_level": 2,
        "category": "MoE Series"
    },
    "kimi-k1": {
        "name": "Kimi K1 (Legacy)",
        "id": "moonshotai/kimi-k1",
        "description": "Modelo base K1, predecesor de K1.5 con capacidades de razonamiento sólidas",
        "features": ["Reasoning", "Foundation", "Reliable"],
        "badges": ["legacy", "foundation"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "📜",
        "vip_level": 1,
        "category": "Legacy Series"
    },
    "kimi-chat": {
        "name": "Kimi Chat (Legacy)",
        "id": "moonshotai/kimi-chat",
        "description": "Modelo de conversación original, base de la serie Kimi",
        "features": ["Chat", "Conversation", "Foundation"],
        "badges": ["legacy", "chat"],
        "max_tokens": 2048,
        "context": "128K",
        "icon": "💬",
        "vip_level": 1,
        "category": "Legacy Series"
    },
    "kimi-research": {
        "name": "Kimi Research (Beta)",
        "id": "moonshotai/kimi-research",
        "description": "Modelo experimental para investigación científica y análisis académico",
        "features": ["Research", "Scientific", "Academic", "Analysis"],
        "badges": ["beta", "research", "experimental"],
        "max_tokens": 8192,
        "context": "256K",
        "icon": "🔬",
        "vip_level": 3,
        "category": "Experimental"
    },
    "kimi-legal": {
        "name": "Kimi Legal (Beta)",
        "id": "moonshotai/kimi-legal",
        "description": "Especialización en análisis legal, contratos y documentación jurídica",
        "features": ["Legal", "Contracts", "Compliance", "Analysis"],
        "badges": ["beta", "legal", "domain"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "⚖️",
        "vip_level": 3,
        "category": "Experimental"
    },
    "kimi-medical": {
        "name": "Kimi Medical (Beta)",
        "id": "moonshotai/kimi-medical",
        "description": "Orientado a análisis médico, investigación biomédica y terminología clínica",
        "features": ["Medical", "Biomedical", "Clinical", "Research"],
        "badges": ["beta", "medical", "domain"],
        "max_tokens": 4096,
        "context": "256K",
        "icon": "🏥",
        "vip_level": 3,
        "category": "Experimental"
    }
}

# ============================================================================
# CSS PERSONALIZADO ONYX VIP
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    * {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, {COLORS['dark_gray']} 50%, {COLORS['medium_gray']} 100%);
        color: {COLORS['white']};
    }}
    
    .vip-header {{
        background: linear-gradient(90deg, rgba(212,175,55,0.1) 0%, rgba(0,0,0,0) 100%);
        border-bottom: 1px solid rgba(212,175,55,0.3);
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        backdrop-filter: blur(10px);
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    .vip-logo {{
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['gold_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }}
    
    .vip-badge {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, #B8941F 100%);
        color: {COLORS['black']};
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
    }}
    
    .model-card-vip {{
        background: linear-gradient(145deg, rgba(17,17,17,0.9) 0%, rgba(10,10,10,0.9) 100%);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
    }}
    
    .model-card-vip.active {{
        border-color: {COLORS['gold']};
        background: linear-gradient(145deg, rgba(212,175,55,0.1) 0%, rgba(17,17,17,0.9) 100%);
    }}
    
    .message {{
        max-width: 80%;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }}
    
    .message-user {{
        align-self: flex-end;
        background: linear-gradient(135deg, rgba(212,175,55,0.2) 0%, rgba(212,175,55,0.1) 100%);
        border-right: 3px solid {COLORS['gold']};
    }}
    
    .message-assistant {{
        align-self: flex-start;
        background: rgba(255,255,255,0.05);
        border-left: 3px solid {COLORS['accent']};
    }}

    .category-header {{
        background: linear-gradient(90deg, rgba(212,175,55,0.15) 0%, transparent 100%);
        padding: 0.8rem 1rem;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid {COLORS['gold']};
        font-weight: 700;
        color: {COLORS['gold']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CLASES DE NEGOCIO
# ============================================================================

class KimiVIPChat:
    def __init__(self, model_key="kimi-k2-instruct"):
        self.client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=NVIDIA_API_KEY)
        self.model_key = model_key
        self.model_info = KIMI_MODELS[model_key]
        self.total_queries = 0
        self.session_start = datetime.now()
    
    def chat(self, message, temperature=0.7, max_tokens=None):
        self.total_queries += 1
        try:
            tokens = max_tokens or self.model_info["max_tokens"]
            system_prompt = f"Eres {self.model_info['name']} de KIMI ONYX VIP. Responde de manera profesional."
            completion = self.client.chat.completions.create(
                model=self.model_info["id"],
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

class VIPZipGenerator:
    def generate_project(self, model_key, project_type='python'):
        model_info = KIMI_MODELS[model_key]
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('app.py', f"# Proyecto {project_type}\n# Modelo: {model_info['name']}")
            zf.writestr('README.md', f"# Onyx VIP Project\nGenerated for {st.session_state.user_email}")
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

# ============================================================================
# INICIALIZACIÓN DE ESTADO
# ============================================================================

if 'messages' not in st.session_state: st.session_state.messages = []
if 'selected_model' not in st.session_state: st.session_state.selected_model = "kimi-k2-instruct"
if 'chat_engine' not in st.session_state: st.session_state.chat_engine = KimiVIPChat(st.session_state.selected_model)
if 'zip_generator' not in st.session_state: st.session_state.zip_generator = VIPZipGenerator()
if 'workspace_code' not in st.session_state: st.session_state.workspace_code = "// Workspace VIP..."
if 'user_email' not in st.session_state: st.session_state.user_email = "josejhonnym53@gmail.com"

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"""
<div class="vip-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 2rem;">⚡</span>
        <div><div class="vip-logo">KIMI ONYX VIP</div></div>
    </div>
    <div><span class="vip-badge">VIP ACCESS</span></div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# NAVEGACIÓN
# ============================================================================

menu = st.sidebar.radio("Menú", ["💬 Chat", "🎨 Modelos", "💻 Workspace", "📦 Exportar", "⚙️ Config"], label_visibility="collapsed")

# ============================================================================
# SECCIÓN: CHAT (Modificada para quitar contadores y ensanchar layout)
# ============================================================================

if menu == "💬 Chat":
    # Selector de modelo en sidebar
    st.sidebar.markdown("### 🤖 Modelo Activo")
    model_list = [(k, f"{m['icon']} {m['name']}") for k, m in KIMI_MODELS.items()]
    selected_display = st.sidebar.selectbox("Modelo:", [m[1] for m in model_list], 
                                          index=[m[0] for m in model_list].index(st.session_state.selected_model))
    new_model = next(k for k, d in model_list if d == selected_display)
    
    if new_model != st.session_state.selected_model:
        st.session_state.selected_model = new_model
        st.session_state.chat_engine = KimiVIPChat(new_model)
        st.session_state.messages = []
        st.rerun()

    current = KIMI_MODELS[st.session_state.selected_model]
    
    # Layout Ajustado: Columna 1 más ancha, Columna 2 sin métricas
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"### 💬 Chat con {current['icon']} {current['name']}")
        for msg in st.session_state.messages:
            css = "message-user" if msg['role'] == 'user' else "message-assistant"
            st.markdown(f'<div class="message {css}">{msg["content"]}</div>', unsafe_allow_html=True)
        
        with st.container():
            cols = st.columns([6, 1])
            prompt = cols[0].text_input("", placeholder="Escribe tu mensaje VIP...", key="chat_input", label_visibility="collapsed")
            if (cols[1].button("➤") or prompt) and prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = st.session_state.chat_engine.chat(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    with col2:
        st.markdown("### ⚡ Acciones")
        if st.button("🧹 Limpiar Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 Generar")
        code_prompt = st.text_area("Tarea rápida", height=100)
        if st.button("✨ Ejecutar", use_container_width=True):
            st.session_state.workspace_code = st.session_state.chat_engine.chat(f"Genera código para: {code_prompt}")
            st.success("Enviado al Workspace")

# ============================================================================
# SECCIÓN: MODELOS
# ============================================================================

elif menu == "🎨 Modelos":
    st.markdown("## 🎨 Catálogo de Modelos VIP")
    cats = sorted(list(set(m['category'] for m in KIMI_MODELS.values())))
    for cat in cats:
        st.markdown(f'<div class="category-header">{cat}</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        cat_models = [(k, v) for k, v in KIMI_MODELS.items() if v['category'] == cat]
        for i, (k, m) in enumerate(cat_models):
            with cols[i % 3]:
                active = "active" if k == st.session_state.selected_model else ""
                st.markdown(f"""<div class="model-card-vip {active}">
                    <div style="font-size:1.5rem">{m['icon']}</div>
                    <div style="font-weight:700; color:{COLORS['gold']}">{m['name']}</div>
                    <div style="font-size:0.8rem; color:#888">{m['description']}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("Activar", key=k, use_container_width=True):
                    st.session_state.selected_model = k
                    st.session_state.chat_engine = KimiVIPChat(k)
                    st.rerun()

# ============================================================================
# SECCIÓN: WORKSPACE
# ============================================================================

elif menu == "💻 Workspace":
    st.markdown("## 💻 Editor VIP")
    st.session_state.workspace_code = st.text_area("Código", value=st.session_state.workspace_code, height=450)
    if st.button("💾 Descargar .py"):
        st.download_button("Click aquí", st.session_state.workspace_code, "app_vip.py")

# ============================================================================
# SECCIÓN: EXPORTAR
# ============================================================================

elif menu == "📦 Exportar":
    st.markdown("## 📦 Exportar Proyecto")
    ptype = st.selectbox("Formato", ["Python", "React", "Android"])
    if st.button("⚡ Generar Paquete"):
        zip_data = st.session_state.zip_generator.generate_project(st.session_state.selected_model, ptype)
        st.download_button("⬇️ Descargar ZIP", zip_data, f"PROYECTO_VIP_{ptype}.zip")

# ============================================================================
# SECCIÓN: CONFIGURACIÓN (Modificada para quitar métricas/contadores)
# ============================================================================

else:
    st.markdown("## ⚙️ Configuración VIP")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 Perfil")
        st.session_state.user_email = st.text_input("Email", value=st.session_state.user_email)
        st.markdown("### 🔑 API")
        st.code(f"{NVIDIA_API_KEY[:25]}...", language="text")
    with col2:
        st.markdown("### 🛠️ Preferencias")
        st.toggle("Modo Ultra Rapidez", value=True)
        st.info("Nivel de Acceso: VIP-3 (Ilimitado)")
        if st.button("🗑️ Resetear Aplicación"):
            st.session_state.messages = []
            st.success("Sistema reiniciado")

# ============================================================================
# FOOTER (Simplificado)
# ============================================================================

st.markdown(f"""
<div style="position:fixed; bottom:0; left:0; right:0; background:rgba(0,0,0,0.9); padding:0.8rem; text-align:center; font-size:0.7rem; color:#555; border-top:1px solid #222;">
    <span style="color:{COLORS['gold']}">KIMI ONYX VIP</span> | {st.session_state.user_email} | {datetime.now().year}
</div>
<div style="height:50px"></div>
""", unsafe_allow_html=True)
