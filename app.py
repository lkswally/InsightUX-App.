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

# --- CSS DE ALTO IMPACTO (CORREGIDO PARA EVITAR CORTES) ---
st.markdown("""
<style>
    /* 1. FONDO GLOBAL CON DEGRADADO */
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. TÍTULOS PRINCIPALES */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #E0E0E0 !important;
        font-weight: 600;
    }

    /* 3. INPUTS Y SELECTS (SOLUCIÓN AL TEXTO CORTADO) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        min-height: 45px !important; /* Altura mínima para que nada se corte */
        align-items: center !important;
    }

    /* ESTILOS DE LOS TÍTULOS DE LOS INPUTS (LABELS) */
    .stTextInput label, .stSelectbox label {
        color: #FFFFFF !important; /* Blanco Puro */
        font-weight: 700 !important; /* Negrita Fuerte */
        font-size: 1.1rem !important; /* Un poco más grande */
        letter-spacing: 0.5px;
        margin-bottom: 8px !important;
    }
    
    /* Texto dentro del selectbox seleccionado */
    .stSelectbox div[data-baseweb="select"] span {
        color: white !important;
        font-weight: 500;
        font-size: 1rem !important;
        white-space: normal !important; /* Permite que el texto baje si es largo */
        line-height: 1.2 !important;
    }
    
    /* Menú desplegable (Opciones) */
    .stSelectbox div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }
    
    /* Icono del dropdown */
    .stSelectbox svg { fill: #FF4B4B !important; }

    /* Efecto Focus */
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.2);
    }

    /* 4. BOTÓN PRINCIPAL (NEÓN) */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        font-weight: bold;
        margin-top: 15px;
        cursor: pointer;
        border-radius: 50px; 
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.6);
    }

    /* 5. TARJETAS DEL EQUIPO */
    .team-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 75, 75, 0.3);
    }
    .team-card h4 {
        color: white;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .team-card p {
        color: #888;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }
    .team-link {
        color: #FF4B4B;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        border: 1px solid #FF4B4B;
        padding: 5px 15px;
        border-radius: 20px;
        transition: all 0.3s;
    }
    .team-link:hover {
        background-color: #FF4B4B;
        color: white;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
</style>
""", unsafe_allow_html=True)

# 🔗 CONEXIÓN
N8N_WEBHOOK_URL = "http://159.112.138.149:5678/webhook/test-lucas"

# --- LÓGICA DE AUDIENCIAS (Texto Descriptivo) ---
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
    "<p style='text-align: center; color: #BBB; font-size: 1.1rem;'>Auditoría de Landing Pages potenciada por Inteligencia Artificial.</p>", 
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
    
    # --- SELECTOR DE AUDIENCIA CORREGIDO ---
    audiencia_seleccionada = st.selectbox(
        "👁️ Mira tu web con ojos de...",
        options=list(OPCIONES_AUDIENCIA.keys()),
        index=0 
    )
    
    st.write("")
    st.write("")
    
    # Botón de acción
    if st.button("🚀 INICIAR AUDITORÍA"):
        if not url_input or not email_input:
            st.warning("⚠️ Por favor completa todos los datos.")
        else:
            # Corrección de URL
            url_final = url_input.strip()
            if not url_final.startswith(("http://", "https://")):
                url_final = "https://" + url_final

            valor_generacion = OPCIONES_AUDIENCIA[audiencia_seleccionada]

            # --- UX: SPINNER CON MENSAJES ALEATORIOS ---
            mensajes_carga = [
                f"🧠 Adoptando personalidad de: {audiencia_seleccionada.split('(')[0]}...",
                "📡 Escaneando estructura y contenido...",
                "🕵️‍♀️ Investigando reputación de marca...",
                "🎨 Evaluando experiencia de usuario..."
            ]
            
            with st.spinner("Iniciando motores de IA..."):
                try:
                    # Simulación de pasos para mejor UX
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
                        
                        st.info(f"""
                        **📢 Importante:** Tu reporte simulará la visión de un usuario **{audiencia_seleccionada.split(' ')[1]}**.
                        
                        Llegará a tu email en unos minutos. Si tarda más de 10 min, verifica tu carpeta de Spam.
                        """)
                        
                    else:
                        # --- ERROR DE SERVIDOR ---
                        st.error(f"⚠️ Hubo un problema de conexión ({response.status_code}).")
                        st.markdown(f"El servidor no pudo procesar la solicitud. Intenta con otra URL o espera unos minutos.")

                except Exception as e:
                    st.error("❌ Error inesperado")
                    st.warning("Verifica tu conexión a internet o intenta más tarde.")

# --- SECCIÓN EQUIPO ---
st.write("")
st.write("")
st.markdown("---")
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Expertos detrás del Engine</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="team-card">
        <h4>Lucas Rojo</h4>
        <p>Technical Automation Architect</p>
        <a class="team-link" href="mailto:lksrojo86@gmail.com">Contactar</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="team-card">
        <h4>Antonella Calabro</h4>
        <p>Senior UX Auditor</p>
        <a class="team-link" href="mailto:antonellacalabro@gmail.com">Contactar</a>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
