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

# --- CSS DE ALTO IMPACTO (MODO ULTRA) ---
st.markdown("""
<style>
    /* 1. FONDO GLOBAL */
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. TÍTULO GIGANTE */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        text-align: center;
        padding-bottom: 10px;
    }
    
    h3 { color: #E0E0E0 !important; font-weight: 600; }

    /* 3. INPUTS Y SELECTS */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        min-height: 50px !important;
        font-size: 1.1rem !important;
    }

    /* --- TÍTULOS DE INPUTS DESTACADOS (NUEVO DISEÑO) --- */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; 
        font-weight: 900 !important; /* Extra Negrita */
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px !important;
        
        /* Decoración visual */
        display: flex;
        align-items: center;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Agregamos una barrita de neón al lado del título */
    .stTextInput label::before, .stSelectbox label::before {
        content: '';
        display: inline-block;
        width: 6px;
        height: 20px;
        background: #FF4B4B;
        margin-right: 10px;
        border-radius: 4px;
        box-shadow: 0 0 10px #FF4B4B;
    }
    
    /* Texto dentro del select */
    .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        font-weight: 500;
        font-size: 1.1rem !important;
    }
    
    /* Dropdown menú */
    .stSelectbox div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }
    .stSelectbox svg { fill: #FF4B4B !important; }

    /* Focus */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
    }

    /* 4. BOTÓN DE ENVÍO */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 18px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 20px;
        font-weight: 800;
        margin-top: 20px;
        cursor: pointer;
        border-radius: 50px; 
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.7);
    }

    /* 5. TARJETAS DEL EQUIPO (DUAL ACTION) */
    .team-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .team-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 75, 75, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    /* Enlace a LinkedIn (Toda la parte superior) */
    .linkedin-area {
        text-decoration: none;
        color: inherit;
        display: block;
        margin-bottom: 15px;
    }
    .linkedin-area:hover h4 { color: #0077b5; } /* Azul LinkedIn al pasar mouse */

    .team-card h4 {
        color: white;
        margin-bottom: 5px;
        font-weight: 800;
        font-size: 1.3rem;
        transition: color 0.3s;
    }
    .team-card p {
        color: #AAA;
        font-size: 0.95rem;
    }
    
    /* BOTÓN EMAIL */
    .email-btn {
        background-color: transparent;
        color: #FF4B4B;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        border: 2px solid #FF4B4B; 
        padding: 10px 20px;
        border-radius: 50px;
        transition: all 0.3s;
        display: inline-block;
        margin-top: auto; /* Empuja el botón al fondo */
    }
    .email-btn:hover {
        background-color: #FF4B4B;
        color: white;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
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

# --- SECCIÓN EQUIPO ---
st.write("")
st.write("")
st.markdown("---")
st.markdown("<h3 style='text-align: center; margin-bottom: 40px; font-size: 1.8rem;'>Expertos detrás del Engine</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# --- CARD LUCAS ---
with col1:
    st.markdown("""
    <div class="team-card">
        <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank" class="linkedin-area">
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
        <a href="https://www.linkedin.com/in/antonella-calabro/" target="_blank" class="linkedin-area">
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
