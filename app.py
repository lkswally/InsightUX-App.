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

# --- CSS DE ALTO IMPACTO (UX MEJORADA) ---
st.markdown("""
<style>
    /* 1. FONDO GLOBAL */
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. TÍTULO PRINCIPAL */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        text-align: center;
        padding-bottom: 20px;
        text-shadow: 0 0 30px rgba(255, 75, 75, 0.2);
    }
    
    h3 { color: #E0E0E0 !important; font-weight: 600; }

    /* 3. INPUTS Y SELECTS (OPTIMIZACIÓN DE TEXTO) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        
        /* AQUÍ ESTÁ LA MAGIA DEL CENTRADO */
        height: 60px !important;          /* Altura fija cómoda */
        padding-top: 0px !important;      /* Reset de padding */
        padding-bottom: 0px !important;   /* Reset de padding */
        padding-left: 20px !important;    /* Espacio a la izquierda */
        
        /* Texto interno */
        font-size: 1.25rem !important;    /* Texto más grande y legible */
        line-height: 60px !important;     /* Centrado vertical perfecto */
        display: flex;
        align-items: center;
    }

    /* --- TÍTULOS DE INPUTS (LABELS) MÁS GRANDES --- */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; 
        font-weight: 900 !important; /* Extra Negrita */
        font-size: 1.6rem !important; /* AUMENTADO */
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px !important; /* Más aire entre título y caja */
        display: flex;
        align-items: center;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }
    
    /* Barra lateral decorativa MÁS GRUESA */
    .stTextInput label::before, .stSelectbox label::before {
        content: '';
        display: inline-block;
        width: 10px;        /* Más gruesa */
        height: 32px;       /* Más alta */
        background: linear-gradient(180deg, #FF4B4B, #FF914D);
        margin-right: 15px;
        border-radius: 6px;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.8);
    }
    
    /* Ajuste para el texto dentro del Select (Dropdown) */
    .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        font-weight: 500;
        font-size: 1.2rem !important;
        line-height: 1.5 !important;
        align-self: center; /* Asegura centrado flex */
    }
    
    .stSelectbox div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }
    .stSelectbox svg { fill: #FF4B4B !important; }

    /* Focus */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 25px rgba(255, 75, 75, 0.35);
        background-color: rgba(255, 255, 255, 0.12) !important;
    }

    /* 4. BOTÓN DE ENVÍO */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 22px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 24px;
        font-weight: 900;
        margin-top: 35px;
        cursor: pointer;
        border-radius: 50px; 
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.5);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 40px rgba(255, 75, 75, 0.8);
    }

    /* 5. TARJETAS DEL EQUIPO (CELESTITA REPARADO) */
    .team-card {
        background: rgba(0, 194, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 194, 255, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        border-color: #00C2FF;
        box-shadow: 0 0 30px rgba(0, 194, 255, 0.2);
    }

    /* TÍTULO NOMBRE (Cian) */
    .team-card h4 {
        color: #00C2FF !important; 
        margin: 0 0 8px 0;
        font-weight: 800;
        font-size: 1.6rem;
        text-shadow: 0 0 15px rgba(0, 194, 255, 0.4);
    }
    
    .team-card p {
        color: #A0C0D0;
        font-size: 1rem;
        margin: 0 0 25px 0;
        font-weight: 500;
    }

    /* Enlace invisible para LinkedIn */
    .linkedin-link {
        text-decoration: none;
        display: block;
        margin-bottom: auto; /* Empuja hacia arriba */
        margin-top: auto;
    }

    /* BOTÓN EMAIL */
    .email-btn {
        background-color: transparent;
        color: #00C2FF;
        text-decoration: none;
        font-weight: bold;
        font-size: 1rem;
        border: 2px solid #00C2FF;
        padding: 10px 25px;
        border-radius: 50px;
        transition: all 0.3s;
        display: inline-block;
        margin-bottom: 10px;
    }
    .email-btn:hover {
        background-color: #00C2FF;
        color: #0e1117;
        box-shadow: 0 0 20px rgba(0, 194, 255, 0.8);
        font-weight: 900;
        transform: scale(1.05);
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
    "<p style='text-align: center; color: #BBB; font-size: 1.3rem; margin-bottom: 40px;'>Auditoría de Landing Pages potenciada por Inteligencia Artificial.</p>", 
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

# --- SECCIÓN EQUIPO (FINAL) ---
st.write("")
st.write("")
st.markdown("---")
st.markdown("<h3 style='text-align: center; margin-bottom: 50px; font-size: 2rem; color: #00C2FF !important; text-shadow: 0 0 20px rgba(0,194,255,0.3);'>Expertos detrás del Engine</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# --- CARD LUCAS ---
with col1:
    st.markdown("""
    <div class="team-card">
        <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank" class="linkedin-link">
            <h4>Lucas Rojo</h4>
            <p>Technical Automation Architect</p>
        </a>
        <a href="mailto:lksrojo86@gmail.com" class="email-btn">
            📩 Escribime
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- CARD ANTONELLA ---
with col2:
    st.markdown("""
    <div class="team-card">
        <a href="https://www.linkedin.com/in/antonella-calabro/" target="_blank" class="linkedin-link">
            <h4>Antonella Calabro</h4>
            <p>Senior UX Auditor</p>
        </a>
        <a href="mailto:antonellacalabro@gmail.com" class="email-btn">
            📩 Escribime
        </a>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")


