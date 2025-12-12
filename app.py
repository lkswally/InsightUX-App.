import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA (MODO OSCURO FORZADO) ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="🕵️‍♀️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PREMIUM (DISEÑO DARK/PRO) ---
st.markdown("""
<style>
    /* Forzar fondo oscuro y texto claro */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Botones personalizados */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 12px;
        background-color: #FF4B4B; 
        color: white;
        border: none;
    }
    .stButton button:hover {
        background-color: #D43F3F;
        color: white;
    }

    /* Tarjetas del Equipo (Estilo Glassmorphism) */
    .team-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border: 1px solid #363945;
        margin-bottom: 10px;
    }
    .team-card h3 {
        color: #FF4B4B;
        margin: 0 0 5px 0;
        font-size: 1.2rem;
    }
    .team-card p {
        font-size: 0.9rem;
        color: #C0C0C0;
    }
    .team-card a {
        color: #4da6ff;
        text-decoration: none;
    }

    /* Caja del Reporte */
    .report-container {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
    
    /* Ocultar elementos de Streamlit */
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 🔗 URL PÚBLICA (CRUCIAL PARA QUE FUNCIONE EN LA NUBE)
# Apunta a tu VPS desde afuera
N8N_WEBHOOK_URL = "http://159.112.138.149:5678/webhook/test-lucas"

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094364.png", width=80)
    st.header("InsightUX Engine")
    st.markdown("---")
    st.info("""
    **🚀 Cómo funciona:**
    1. Ingresas la URL de tu Landing Page.
    2. Nuestra IA analiza UX, UI y Copywriting.
    3. Recibes un plan de mejora en tu email.
    """)
    st.caption("v2.0 Stable | Powered by n8n & Gemini")

# --- CABECERA ---
st.title("Evaluador de Experiencia UX 🚀")
st.markdown("""
<div style='background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B; margin-bottom: 30px;'>
    <strong>Diagnóstico IA:</strong> Descubre por qué tus visitas no se convierten en clientes. 
    Analizamos usabilidad, fricciones y psicología del usuario.
</div>
""", unsafe_allow_html=True)

# --- FORMULARIO ---
col1, col2 = st.columns([2, 1])
with col1:
    url_input = st.text_input("🔗 URL del sitio web", placeholder="tupagina.com")
with col2:
    email_input = st.text_input("✉️ Tu correo", placeholder="nombre@empresa.com")

# --- BOTÓN DE ACCIÓN ---
if st.button("🔍 AUDITAR AHORA", type="primary"):
    if not url_input or not email_input:
        st.warning("⚠️ Falta información. Por favor completa URL y Email.")
    else:
        # 1. Corrección automática de URL (Tu código favorito)
        url_final = url_input.strip()
        if not url_final.startswith(("http://", "https://")):
            url_final = "https://" + url_final

        # 2. Spinner de carga
        with st.spinner(f"📡 Conectando satélites... Escaneando {url_final}"):
            try:
                # Payload para n8n
                payload = {"url": url_final, "email": email_input}
                
                # Envío al servidor
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    analisis = data.get("output", "✅ Análisis enviado. Revisa tu correo.")
                    
                    st.success("¡Diagnóstico Exitoso!")
                    st.balloons()
                    
                    # Mostrar resultado lindo
                    st.markdown("### 📝 Resumen Ejecutivo")
                    st.markdown(f'<div class="report-container">{analisis}</div>', unsafe_allow_html=True)
                    st.info("📨 El reporte completo ha sido enviado a tu correo.")
                        
                elif response.status_code == 400:
                    st.error("🔒 No pudimos entrar al sitio. Verifica que la URL sea pública.")
                else:
                    st.error(f"⚠️ Error del servidor ({response.status_code}).")
                    
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")

# --- SECCIÓN EQUIPO (Mix Diseño Nuevo + Estética Dark) ---
st.markdown("---")
st.subheader("🤝 Expertos detrás de la IA")

col_team1, col_team2 = st.columns(2)

with col_team1:
    st.markdown("""
    <div class="team-card">
        <h3>Lucas Rojo</h3>
        <p style="font-weight: bold; color: #fff;">Technical Automation Architect</p>
        <p>Arquitectura de datos, integraciones API y desarrollo de soluciones No-Code.</p>
        <p>
            <a href="https://www.linkedin.com/in/lucas-rojo-54446214b/" target="_blank">🔗 LinkedIn</a> | 
            <a href="mailto:lksrojo86@gmail.com">✉️ Contacto</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_team2:
    st.markdown("""
    <div class="team-card">
        <h3>Antonella Calabro</h3>
        <p style="font-weight: bold; color: #fff;">Senior UX Auditor</p>
        <p>Estrategia de conversión (CRO), usabilidad y psicología del consumidor.</p>
        <p>
            <a href="https://www.linkedin.com/in/antonella-calabro/" target="_blank">🔗 LinkedIn</a> | 
            <a href="mailto:antonellacalabro@gmail.com">✉️ Contacto</a>
        </p>
    </div>
    """, unsafe_allow_html=True)









