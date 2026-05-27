import streamlit as st
import requests
import time

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
<style>
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

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

    h3 {
        color: #E0E0E0 !important;
        font-weight: 600;
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    div[data-baseweb="popover"] {
        background-color: #1E2130 !important;
        border: 1px solid #444 !important;
    }

    div[data-baseweb="menu"] li {
        color: white !important;
    }

    .stTextInput label,
    .stSelectbox label {
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

    .stTextInput label::before,
    .stSelectbox label::before {
        content: '';
        display: block;
        width: 6px;
        height: 24px;
        background: linear-gradient(180deg, #FF4B4B, #FF914D);
        margin-right: 12px;
        border-radius: 4px;
        box-shadow: 0 0 12px rgba(255, 75, 75, 0.8);
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 18px;
        font-weight: 800;
        cursor: pointer;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.7);
        color: #fff !important;
    }

    .team-wrapper {
        max-width: 430px;
        margin: 0 auto;
    }

    .team-card {
        background: rgba(0, 194, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 194, 255, 0.3);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        transition: all 0.3s ease;
        min-height: 230px;
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

    .team-card a {
        text-decoration: none !important;
    }

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

# --- CONEXIÓN ---
# En Streamlit Cloud, configurar en Manage app → Settings → Secrets:
# N8N_WEBHOOK_URL = "http://159.112.138.149:5678/webhook/insightux-audit"
N8N_WEBHOOK_URL = st.secrets.get(
    "N8N_WEBHOOK_URL",
    "http://159.112.138.149:5678/webhook/insightux-audit"
)

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

_, col_main, _ = st.columns([0.1, 0.8, 0.1])

with col_main:
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

    c1, c2, c3 = st.columns([0.2, 0.6, 0.2])

    with c2:
        boton_submit = st.button("🚀 INICIAR AUDITORÍA")

    st.markdown("<br>", unsafe_allow_html=True)

    if boton_submit:
        if not url_input or not email_input:
            st.warning("⚠️ Por favor completa todos los datos.")
        elif "@" not in email_input or "." not in email_input:
            st.warning("⚠️ Revisá el correo electrónico ingresado.")
        else:
            url_final = url_input.strip()

            if not url_final.startswith(("http://", "https://")):
                url_final = "https://" + url_final

            valor_generacion = OPCIONES_AUDIENCIA[audiencia_seleccionada]

            mensajes_carga = [
                f"🧠 Adoptando personalidad de: {audiencia_seleccionada.split('(')[0]}...",
                "📡 Escaneando estructura y contenido...",
                "🕵️‍♀️ Investigando huella digital pública...",
                "📚 Comparando contra heurísticas UX/CRO...",
                "🎨 Preparando el informe..."
            ]

            with st.spinner("Iniciando motores de IA..."):
                try:
                    for msg in mensajes_carga:
                        st.info(msg)
                        time.sleep(0.7)

                    payload = {
                        "url": url_final,
                        "email": email_input.strip(),
                        "generacion": valor_generacion
                    }

                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        json=payload,
                        timeout=180
                    )

                    if response.status_code == 200:
                        st.balloons()
                        st.markdown(f"""
                        <div style="background-color: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #dcfce7; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px;">
                            <h3 style="margin:0; color: #22c55e !important;">✅ Auditoría enviada con éxito</h3>
                            <p style="margin-top: 10px; font-size: 1.1rem;">El análisis se generó con foco en <strong>{audiencia_seleccionada}</strong>.</p>
                            <p style="font-size: 0.9rem; opacity: 0.8;">Revisá tu email en unos minutos.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    elif response.status_code == 400:
                        st.error("🛡️ No pudimos leer este sitio web.")
                        try:
                            data = response.json()
                            mensaje = data.get(
                                "message",
                                "Puede que la página tenga bloqueos anti-bot, requiera JavaScript o no devuelva contenido suficiente."
                            )
                        except Exception:
                            mensaje = "Puede que la página tenga bloqueos anti-bot, requiera JavaScript o no devuelva contenido suficiente."

                        st.warning(mensaje)
                        st.info("Probá con una URL pública, real y accesible. Ejemplo: https://saldo.com.ar")

                    elif response.status_code in [502, 503, 504]:
                        st.error("⚠️ El motor de análisis está temporalmente saturado.")
                        st.warning("Probá nuevamente en unos minutos. Puede haber alta demanda en Gemini o en algún servicio intermedio.")

                    else:
                        detalle = response.text[:500] if response.text else "Sin detalle disponible."
                        st.error(f"⚠️ Hubo un problema de conexión ({response.status_code}).")
                        st.code(detalle)

                except requests.exceptions.Timeout:
                    st.error("⏳ El análisis tardó más de lo esperado.")
                    st.warning("Puede que el workflow siga procesando. Revisá tu correo o intentá nuevamente en unos minutos.")

                except requests.exceptions.ConnectionError:
                    st.error("❌ No se pudo conectar con el backend de auditoría.")
                    st.warning("Revisá que el workflow de n8n esté activo y que la URL productiva sea correcta.")

                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")

# --- SECCIÓN EQUIPO ---
st.write("")
st.write("")
st.markdown("---")
st.markdown(
    "<h3 style='text-align: center; margin-bottom: 50px; font-size: 2rem; color: #00C2FF !important; text-shadow: 0 0 20px rgba(0,194,255,0.3);'>Experto detrás del Engine</h3>",
    unsafe_allow_html=True
)

st.markdown("""
<div class="team-wrapper">
    <div class="team-card">
        <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank" style="text-decoration:none;">
            <h4>Lucas Rojo</h4>
            <p>Technical Automation Architect</p>
        </a>
        <a href="mailto:lksrojo86@gmail.com" class="email-btn">
            📩 Escribime
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
