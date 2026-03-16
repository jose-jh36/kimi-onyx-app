# ============================================================================
# KIMI ONYX VIP - UNIFIED MULTI-MODEL AI PLATFORM
# Backend: Python/Streamlit + Frontend: React-inspired UI
# ============================================================================

import streamlit as st
from openai import OpenAI
import time
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN INICIAL VIP
# ============================================================================

st.set_page_config(
    page_title="⚡ KIMI ONYX VIP | Multi-Model AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTES Y ESTILOS
# ============================================================================

NVIDIA_API_KEY = "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"

COLORS = {
    'gold': '#D4AF37',
    'gold_light': '#F4E4BC',
    'black': '#000000',
    'dark_gray': '#0a0a0a',
    'medium_gray': '#111111',
    'white': '#FFFFFF'
}

KIMI_MODELS = {
    "kimi-k2.5": {
        "name": "Kimi K2.5 Ultra",
        "id": "moonshotai/kimi-k2.5",
        "description": "Modelo multimodal más potente con capacidades agenticas.",
        "icon": "⚡",
        "category": "K2.5 Series",
        "max_tokens": 8192
    },
    "kimi-k2.5-instruct": {
        "name": "Kimi K2.5 Instruct",
        "id": "moonshotai/kimi-k2.5-instruct",
        "description": "Optimizado para seguimiento de instrucciones precisas.",
        "icon": "📋",
        "category": "K2.5 Series",
        "max_tokens": 8192
    },
    "kimi-k2-coder": {
        "name": "Kimi K2 Coder",
        "id": "moonshotai/kimi-k2-coder",
        "description": "Especialización en generación de código y debugging.",
        "icon": "⌨️",
        "category": "K2 Series",
        "max_tokens": 4096
    },
    "kimi-linear": {
        "name": "Kimi Linear",
        "id": "moonshotai/kimi-linear",
        "description": "Arquitectura híbrida, 2.9x más rápido.",
        "icon": "🚀",
        "category": "Linear Series",
        "max_tokens": 2048
    }
}

# ============================================================================
# LÓGICA DE SALUDO DINÁMICO
# ============================================================================

def get_vip_greeting():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "Buenos días"
    elif 12 <= hora < 19:
        return "Buenas tardes"
    else:
        return "Buenas noches"

# ============================================================================
# INICIALIZACIÓN DE ESTADO (CRÍTICO: SIEMPRE K2.5 ULTRA AL INICIO)
# ============================================================================

if 'messages' not in st.session_state: st.session_state.messages = []
if 'selected_model' not in st.session_state: st.session_state.selected_model = "kimi-k2.5"
if 'user_email' not in st.session_state: st.session_state.user_email = "josejhonnym53@gmail.com"
if 'workspace_code' not in st.session_state: st.session_state.workspace_code = "// Workspace VIP..."

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=NVIDIA_API_KEY)

# ============================================================================
# INTERFAZ Y NAVEGACIÓN
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background: {COLORS['black']}; color: {COLORS['white']}; }}
    .vip-header {{ background: rgba(212,175,55,0.1); border-bottom: 1px solid {COLORS['gold']}; padding: 1rem; text-align: center; }}
    .vip-logo {{ font-size: 1.8rem; font-weight: 900; color: {COLORS['gold']}; letter-spacing: 3px; }}
    .greeting-text {{ color: {COLORS['gold_light']}; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="vip-header"><div class="vip-logo">⚡ KIMI ONYX VIP</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 💎 {get_vip_greeting()}")
    st.markdown(f"**Usuario:** {st.session_state.user_email}")
    st.markdown("---")
    menu = st.radio("Menú Principal", ["💬 Chat VIP", "🎨 Catálogo", "💻 Workspace", "⚙️ Config"])
    
    st.markdown("---")
    model_options = {f"{m['icon']} {m['name']}": k for k, m in KIMI_MODELS.items()}
    current_idx = list(model_options.values()).index(st.session_state.selected_model)
    selection = st.selectbox("IA Activa:", list(model_options.keys()), index=current_idx)
    
    if model_options[selection] != st.session_state.selected_model:
        st.session_state.selected_model = model_options[selection]
        st.rerun()

# ============================================================================
# SECCIÓN: CHAT VIP
# ============================================================================

if menu == "💬 Chat VIP":
    model_info = KIMI_MODELS[st.session_state.selected_model]
    
    # Mensaje de Bienvenida Dinámico
    st.markdown(f'<p class="greeting-text">✨ {get_vip_greeting()}, bienvenido al núcleo Onyx.</p>', unsafe_allow_html=True)
    st.caption(f"Utilizando: {model_info['name']} ({model_info['category']})")

    # Contenedor de Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input Nativo
    if prompt := st.chat_input("Escribe tu comando..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                placeholder = st.empty()
                completion = client.chat.completions.create(
                    model=model_info["id"],
                    messages=[{"role": "system", "content": f"Eres {model_info['name']}. Saluda brevemente según sea {get_vip_greeting().lower()}."}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.7
                )
                response = completion.choices[0].message.content
                placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error de conexión VIP: {e}")

# ============================================================================
# SECCIÓN: CATÁLOGO
# ============================================================================

elif menu == "🎨 Catálogo":
    st.markdown("## 🎨 Selección de Potencia")
    cols = st.columns(2)
    for i, (k, m) in enumerate(KIMI_MODELS.items()):
        with cols[i % 2]:
            st.markdown(f"### {m['icon']} {m['name']}")
            st.write(m['description'])
            if st.button(f"Activar {m['name']}", key=k, use_container_width=True):
                st.session_state.selected_model = k
                st.rerun()

# ============================================================================
# SECCIÓN: WORKSPACE
# ============================================================================

elif menu == "💻 Workspace":
    st.markdown("## 💻 Editor de Código Onyx")
    st.session_state.workspace_code = st.text_area("Código Fuente", value=st.session_state.workspace_code, height=400)
    st.download_button("💾 Exportar Script", st.session_state.workspace_code, "script_vip.py")

# ============================================================================
# SECCIÓN: CONFIG
# ============================================================================

else:
    st.markdown("## ⚙️ Configuración del Sistema")
    st.session_state.user_email = st.text_input("Correo de Suscriptor", value=st.session_state.user_email)
    if st.button("🗑️ Limpiar Memoria de Chat"):
        st.session_state.messages = []
        st.success("Memoria purgada.")
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div style="position:fixed; bottom:0; left:0; right:0; background:rgba(0,0,0,0.9); padding:0.5rem; text-align:center; font-size:0.7rem; color:#555; border-top:1px solid #222;">
    ONYX VIP ENGINE | {get_vip_greeting()} | {datetime.now().year}
</div>
""", unsafe_allow_html=True)
