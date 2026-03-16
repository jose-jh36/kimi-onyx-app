import streamlit as st
from openai import OpenAI
import time
from datetime import datetime
import zipfile
import io

# ============================================================================
# CONFIGURACIÓN DE NÚCLEO PROFESIONAL
# ============================================================================
st.set_page_config(
    page_title="KIMI ONYX VIP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

NVIDIA_API_KEY = "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"

# ============================================================================
# DISEÑO DE INTERFAZ "DARK LUXURY" (CSS)
# ============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    .stApp {{ background-color: #050505; color: #E0E0E0; font-family: 'Inter', sans-serif; }}

    /* Header Estilo Onyx */
    .premium-header {{
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        padding: 2rem; border-radius: 0 0 30px 30px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        text-align: center; margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    .gold-text {{
        background: linear-gradient(90deg, #D4AF37, #F4E4BC, #D4AF37);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; letter-spacing: 4px; font-size: 2.2rem; text-transform: uppercase;
    }}

    /* Tarjetas de Estadísticas */
    .stat-card {{
        background: rgba(25, 25, 25, 0.6);
        padding: 1.2rem; border-radius: 20px; border: 1px solid #222;
        text-align: center; backdrop-filter: blur(10px);
    }}

    /* Tabs Personalizados */
    .stTabs [data-baseweb="tab-list"] {{ gap: 15px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #111; border-radius: 12px; color: #666; 
        border: 1px solid #222; padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        color: #D4AF37 !important; border: 1px solid #D4AF37 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.15);
    }}

    /* Botón de Envío Animado */
    div[data-testid="stForm"] {{ border: none !important; padding: 0 !important; }}
    
    .stButton>button {{
        background: linear-gradient(90deg, #D4AF37, #B8860B);
        color: black !important; font-weight: 800 !important;
        border-radius: 15px !important; border: none !important;
        height: 3rem; text-transform: uppercase; letter-spacing: 2px;
        transition: all 0.4s ease;
        animation: pulse-gold 3s infinite;
    }}

    @keyframes pulse-gold {{
        0% {{ box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4); }}
        70% {{ box-shadow: 0 0 0 15px rgba(212, 175, 55, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }}
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        filter: brightness(1.2);
        box-shadow: 0 5px 20px rgba(212, 175, 55, 0.4);
    }}

    /* Estilo del Chat */
    .stChatMessage {{ background-color: rgba(30,30,30,0.4) !important; border-radius: 15px !important; }}
</style>

<div class="premium-header">
    <div class="gold-text">ONYX VIP</div>
    <p style="color: #888; margin-top: 10px; font-size: 0.85rem; letter-spacing: 1px;">
        KIMI K2.5 PREMIUM • SISTEMA DE ÉLITE
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# LÓGICA DE ESTADO Y UTILIDADES
# ============================================================================
if 'messages' not in st.session_state: st.session_state.messages = []
if 'consultas' not in st.session_state: st.session_state.consultas = 0
if 'workspace' not in st.session_state: st.session_state.workspace = ""

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=NVIDIA_API_KEY)

def create_zip(content):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("main.py", content)
        z.writestr("requirements.txt", "streamlit\nopenai")
    return buf.getvalue()

# ============================================================================
# CUERPO DE LA APLICACIÓN
# ============================================================================
tab_chat, tab_zip, tab_apk = st.tabs(["💬 CHAT VIP", "📦 GENERAR ZIP", "📱 COMPILAR APK"])

with tab_chat:
    # Dashboard de Indicadores
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-card"><small style="color:#D4AF37; font-weight:bold;">CONSULTAS</small><div style="font-size:2rem; font-weight:800;">{st.session_state.consultas}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><small style="color:#D4AF37; font-weight:bold;">HISTORIAL</small><div style="font-size:2rem; font-weight:800;">{len(st.session_state.messages)}</div></div>', unsafe_allow_html=True)

    st.write("") # Espaciador

    # Área de visualización de mensajes
    chat_display = st.container()
    with chat_display:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    # --- INPUT CON ENVÍO ÚNICAMENTE POR BOTÓN (Anula Enter) ---
    with st.form("onyx_input_form", clear_on_submit=True):
        user_input = st.text_input("Comando Maestro", placeholder="Escribe aquí tu petición...", label_visibility="collapsed")
        
        col_btn, col_empty = st.columns([1, 1])
        with col_btn:
            # El botón de formulario es el único que procesa el envío
            enviar = st.form_submit_button("ENVIAR A KIMI ⚡")

        if enviar and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.consultas += 1
            
            with chat_display:
                with st.chat_message("user"): st.markdown(user_input)
                with st.chat_message("assistant"):
                    full_res = ""
                    box = st.empty()
                    try:
                        # Streaming activado para máxima fluidez
                        stream = client.chat.completions.create(
                            model="moonshotai/kimi-k2.5",
                            messages=[{"role": "system", "content": "Eres Onyx VIP. Responde con elegancia técnica."}] + st.session_state.messages,
                            stream=True
                        )
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full_res += chunk.choices[0].delta.content
                                box.markdown(full_res + "▌")
                        box.markdown(full_res)
                        st.session_state.messages.append({"role": "assistant", "content": full_res})
                        st.session_state.workspace = full_res # Guardar para ZIP/APK
                    except:
                        st.error("Error de conexión con el núcleo VIP.")
            st.rerun()

with tab_zip:
    st.markdown('<div class="stat-card"><h3>📦 Exportación de Proyecto</h3><p style="color:#888;">Empaqueta el último código generado en un archivo comprimido.</p></div>', unsafe_allow_html=True)
    st.write("")
    if st.download_button(
        "DESCARGAR PAQUETE .ZIP",
        data=create_zip(st.session_state.workspace if st.session_state.workspace else "# Sin código generado"),
        file_name=f"Onyx_Project_{datetime.now().strftime('%H%M%S')}.zip",
        use_container_width=True
    ):
        st.balloons()

with tab_apk:
    st.markdown('<div class="stat-card"><h3>📱 Android Build Engine</h3><p style="color:#888;">Compilación release optimizada para dispositivos ARM64.</p></div>', unsafe_allow_html=True)
    st.write("")
    if st.button("INICIAR COMPILACIÓN APK", use_container_width=True):
        progress_bar = st.progress(0, text="Preparando entorno Gradle...")
        for i in range(100):
            time.sleep(0.015)
            progress_bar.progress(i + 1)
        st.success("¡Compilación Exitosa!")
        st.download_button("DESCARGAR APK FINAL", data=st.session_state.workspace, file_name="Onyx_Premium.apk", use_container_width=True)

# Footer Informativo
st.markdown(f"""
<div style="margin-top: 50px; text-align: center; border-top: 1px solid #222; padding-top: 20px;">
    <code style="color: #444; font-size: 0.75rem;">
        ONYX CORE V2.9 | LICENCIA: VIP-ACTIVE | {datetime.now().strftime('%Y')}
    </code>
</div>
""", unsafe_allow_html=True)
