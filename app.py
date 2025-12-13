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

# --- CSS DE ALTO IMPACTO (FIX TEXTO INVISIBLE) ---
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

    /* 3. INPUTS Y SELECTS (CORRECCIÓN DE VISIBILIDAD) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important; /* Ajustado para que el texto no se escape */
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        min-height: 50px !important;
    }

    /* --- FUERZA BRUTA PARA QUE EL TEXTO DEL SELECT SEA BLANCO --- */
    .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        fill: white !important;
        font-weight: 500;
    }
    
    .stSelectbox div[data-baseweb="select"] * {
        color: white !important; /* Asegura que cualquier elemento interno sea blanco */
    }

    /* TÍTULOS DE INPUTS (LABELS) CON NEÓN */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; 
        font-weight: 800 !important; 
        font-size: 1.3rem !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px !important;
        display: flex !important;
        align-items: center !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }

    .stTextInput label::before, .stSelectbox label::before {
        content: '';
        display: block;
        width: 6px;
        height: 24px;
        background: linear-gradient(180deg, #FF4B4B, #FF914D);
        margin-right: 12px;
        border-radius: 4px;
        box-shadow: 0 0 12px rgba(255, 75, 75, 0.8);
    }

    /* Menú desplegable */
    .stSelectbox div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }
    .stSelectbox svg { fill: #FF4B4B !important; }

    /* Focus */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.35);
        background-color: rgba(255, 255, 255, 0.12) !important;
    }

    /* 4. BOTÓN DE ENVÍO */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 20px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 20px;
        font-weight: 800;
        margin-top: 30px;
        cursor: pointer;
        border-radius: 50px; 
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 8px 30px rgba(255, 75, 75, 0.7);
    }

    /* 5. TARJETAS DEL EQUIPO */
    .team-card {
        background: rgba(0, 194, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 194, 255, 0.3);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        height: 250px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .team-card:hover {
        transform: translateY(-5px);
        border-color: #00C2FF;
        box-shadow: 0 0 30px rgba(0, 194, 255, 0.2);
    }
    .team-card a { text-decoration: none !important; }
    .team-card h4 {
        color: #00C2FF !important; 
        margin: 0 0 5px 0;
        font-weight: 800;
        font-size: 1.5rem;
        text-shadow: 0 0 10px rgba(0, 194, 255, 0.3);
    }
    .team-card p {
        color: #A0C0D0;
        font-size: 0.95rem;
        margin: 0 0 25px 0;
    }
    .email-btn {
        background-color: transparent;
        color: #00C2FF !important;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        border: 2px solid #00C2FF;
        padding: 8px 25px;
        border-radius: 50px;
        transition: all 0.3s;
        display: inline-block;
    }
    .email-btn:hover {
        background-color: #00C2FF;
        color: #0e1117 !important;
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
    "<p style='text-align: center; color: #BBB; font-size: 1.2rem; margin-bottom: 40px;'>Auditoría de Landing Pages potenciada por Inteligencia Artificial.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# --- FORMULARIO ---
col_form, _ = st.columns([1, 0.01]) 

with col_form:
    url_input = st.text_input("🔗 URL DEL SITIO WEB", placeholder="ejemplo.com.ar")
    st.write("") 
    
    email_input = st.text_input("✉️ TU CORREO ELECTRÓNICO", placeholder="tu@email.com")
    st.write("")
    
    audiencia_seleccionada = st.selectbox(
        "👁️ MIRA TU WEB CON OJOS DE...",
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
                        # --- ÉXITO ---
                        st.balloons()
                        st.success("✅ ¡Solicitud enviada con éxito!")
                        st.info(f"**📢 Importante:** Tu reporte simulará la visión de un usuario **{audiencia_seleccionada.split(' ')[1]}**. Llegará a tu email en unos minutos.")
                        
                    elif response.status_code == 400:
                        # --- ERROR DE LECTURA (ANTI-BOT) ---
                        st.error("🛡️ No pudimos leer este sitio web.")
                        st.warning("Es probable que la página tenga bloqueos de seguridad que impiden el análisis automático. Intenta con otra URL.")
                        
                    else:
                        # --- OTROS ERRORES ---
                        st.error(f"⚠️ Hubo un problema de conexión ({response.status_code}).")

                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")

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
        <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank" style="text-decoration:none;">
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
        <a href="https://www.linkedin.com/in/antonella-calabro/" target="_blank" style="text-decoration:none;">
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


