import streamlit as st
import requests
import json
import time

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS DE ALTO IMPACTO (MODO FINAL) ---
st.markdown("""
<style>
    /* 1. FONDO GLOBAL */
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. TÍTULO PRINCIPAL (GIGANTE) */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 4rem !important; /* Aumentado */
        text-align: center;
        padding-bottom: 15px;
        text-shadow: 0 0 30px rgba(255, 75, 75, 0.2);
    }
    
    h3 { color: #E0E0E0 !important; font-weight: 600; }

    /* 3. INPUTS Y SELECTS */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        min-height: 55px !important;
        font-size: 1.2rem !important;
    }

    /* --- TÍTULOS DE INPUTS (LABELS) CON BARRA NEÓN --- */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; 
        font-weight: 900 !important; /* Extra Negrita */
        font-size: 1.4rem !important; /* AÚN MÁS GRANDE */
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    /* La barra lateral roja/naranja */
    .stTextInput label::before, .stSelectbox label::before {
        content: '';
        display: inline-block;
        width: 7px;
        height: 24px;
        background: linear-gradient(180deg, #FF4B4B, #FF914D);
        margin-right: 12px;
        border-radius: 4px;
        box-shadow: 0 0 12px rgba(255, 75, 75, 0.8);
    }
    
    /* Dropdown y Texto */
    .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        font-weight: 500;
        font-size: 1.1rem !important;
    }
    .stSelectbox div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }
    .stSelectbox svg { fill: #FF4B4B !important; }

    /* Focus (Borde Rojo al escribir) */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
    }

    /* 4. BOTÓN DE ENVÍO (ROJO GRADIENTE) */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 20px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 22px;
        font-weight: 800;
        margin-top: 25px;
        cursor: pointer;
        border-radius: 50px; 
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.7);
    }

    /* 5. TARJETAS DEL EQUIPO (ESTILO CELESTITA / CYAN) */
    .team-card {
        background: rgba(0, 194, 255, 0.03); /* Fondo azulado muy sutil */
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 194, 255, 0.2); /* Borde Celestita */
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        border-color: #00C2FF; /* Celestita Brillante */
        box-shadow: 0 0 25px rgba(0, 194, 255, 0.2);
    }

    /* Contenedor Flex para alinear contenido */
    .team-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 100%;
        min-height: 180px;
    }

    /* Zona Superior (LinkedIn) */
    .linkedin-area {
        text-decoration: none;
        color: inherit;
        display: block;
        width: 100%;
    }
    .linkedin-area:hover h4 { color: #00C2FF; } /* Título se pone celeste */

    .team-card h4 {
        color: white;
        margin: 0 0 5px 0;
        font-weight: 800;
        font-size: 1.4rem;
        transition: color 0.3s;
    }
    .team-card p {
        color: #A0C0D0; /* Gris azulado */
        font-size: 0.95rem;
        margin: 0;
    }
    
    /* BOTÓN EMAIL (ESTILO CELESTITA) */
    .email-btn {
        background-color: transparent;
        color: #00C2FF; /* Texto Celestita */
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        border: 2px solid #00C2FF; /* Borde Celestita */
        padding: 10px 25px;
        border-radius: 50px;
        transition: all 0.3s;
        display: inline-block;
        margin-top: 20px;
    }
    .email-btn:hover {
        background-color: #00C2FF;
        color: #0e1117; /* Texto oscuro al hacer hover */
        box-shadow: 0 0 15px rgba(0, 194, 255, 0.6);
        font-weight: 900;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
</style>
""", unsafe_allow_html=True)

# 🔗 CONEXIÓN
N8N_WEBHOOK_URL = "http://159.112.138.149:5678/webhook/test-lucas"

# --- LÓGICA DE AUDIENCIAS ---
OPCIONES_AUDIENCIA = {
    "🌎 Público General (Estándar)": "general",
    "📸 Gen Z (Visual, Rápido y Móvil)": "gen_z",
    "💻 Millennials (UX, Reseñas y Social)": "millennials",
    "📊 Gen X (Datos Claros y Eficiencia)": "gen_x",
    "🛡️ Boomers (Seguridad y Letra Grande)": "baby_boomers"
}

# --- UI PRINCIPAL ---

st.write("")
st.write("")

st.title("InsightUX Engine ⚡")
st.markdown(
    "<p style='text-align: center; color: #BBB; font-size: 1.2rem; margin-bottom: 30px;'>Auditoría de Landing Pages potenciada por Inteligencia Artificial.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# --- FORMULARIO ---
col_form, _ = st.columns([1, 0.01]) 

with col_form:
    url_input = st.text_input("🔗 URL del sitio web", placeholder="ejemplo.com.ar")
    st.write("") 
    
    email_input = st.text_input("✉️ Tu correo electrónico", placeholder="tu@email.com")
    st.write("")
    
    audiencia_seleccionada = st.selectbox(
        "👁️ Mira tu web con ojos de...",
        options=list(OPCIONES_AUDIENCIA.keys()),
        index=0 
    )
    
    st.write("")
    st.write("")
    
    if st.button("🚀 INICIAR AUDITORÍA"):
        if not url_input or not email_input:
            st.warning("⚠️ Por favor completa todos los datos.")
        else:
            url_final = url_input.strip()
            if not url_final.startswith(("http://", "https://")):
                url_final = "https://" + url_final

            valor_generacion = OPCIONES_AUDIENCIA[audiencia_seleccionada]

            mensajes_carga = [
                f"🧠 Adoptando personalidad de: {audiencia_seleccionada.split('(')[0]}...",
                "📡 Escaneando estructura y contenido...",
                "🕵️‍♀️ Investigando reputación de marca...",
                "🎨 Evaluando experiencia de usuario..."
            ]
            
            with st.spinner("Iniciando motores de IA..."):
                try:
                    for msg in mensajes_carga:
                        time.sleep(0.7)
                        
                    payload = {
                        "url": url_final, 
                        "email": email_input,
                        "generacion": valor_generacion
                    }
                    
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)

                    if response.status_code == 200:
                        st.balloons()
                        st.success("✅ ¡Solicitud enviada con éxito!")
                        st.info(f"**📢 Importante:** Tu reporte simulará la visión de un usuario **{audiencia_seleccionada.split(' ')[1]}**. Llegará a tu email en unos minutos.")
                    else:
                        st.error(f"⚠️ Hubo un problema de conexión ({response.status_code}).")

                except Exception as e:
                    st.error("❌ Error inesperado")

# --- SECCIÓN EQUIPO (CELESTITA) ---
st.write("")
st.write("")
st.markdown("---")
st.markdown("<h3 style='text-align: center; margin-bottom: 40px; font-size: 1.8rem; color: #00C2FF !important;'>Expertos detrás del Engine</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# --- CARD LUCAS ---
with col1:
    st.markdown("""
    <div class="team-card">
        <div class="team-card-container">
            <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank" class="linkedin-area">
                <h4>Lucas Rojo</h4>
                <p>Technical Automation Architect</p>
            </a>
            
            <div>
                <a href="mailto:lksrojo86@gmail.com" class="email-btn">
                    📩 Escribime
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CARD ANTONELLA ---
with col2:
    st.markdown("""
    <div class="team-card">
        <div class="team-card-container">
            <a href="https://www.linkedin.com/in/antonella-calabro/" target="_blank" class="linkedin-area">
                <h4>Antonella Calabro</h4>
                <p>Senior UX Auditor</p>
            </a>
            
            <div>
                <a href="mailto:antonellacalabro@gmail.com" class="email-btn">
                    📩 Escribime
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

