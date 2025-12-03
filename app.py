import streamlit as st
import requests
import json
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="🕵️‍♀️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (Para mantener el look "Pro" sin errores) ---
st.markdown("""
<style>
    .stDeployButton {display:none;}
    h1 {color: #FF4B4B;}
    .stButton button {width: 100%; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 🔗 TU URL REAL
N8N_WEBHOOK_URL = "https://n8n-testi.hopto.org/webhook/analisis-ux"

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("🕵️ InsightUX")
    st.markdown("---")
    st.markdown("""
    **Instrucciones:**
    1.  🌐 Ingresa la URL del sitio.
    2.  ✉️ Pon tu email.
    3.  🚀 Inicia la auditoría.
    """)
    st.info("ℹ️ El sistema detectará automáticamente si el sitio permite ser analizado.")
    st.caption("v.Stable | Powered by Gemini & n8n")

# --- ÁREA PRINCIPAL ---
st.title("Evaluador de Experiencia UX")
st.markdown("Diagnóstico de sitios web potenciado por Inteligencia Artificial.")
st.markdown("---") 

# --- FORMULARIO SIMPLE ---
url_input = st.text_input(
    "🔗 Sitio web a analizar", 
    placeholder="ejemplo.com",
    help="Puedes escribirlo con o sin https://"
)

email_input = st.text_input("✉️ Tu correo electrónico", placeholder="tu@email.com")

st.write("") # Espacio
analyze_btn = st.button("🚀 Iniciar Auditoría", type="primary")

# --- LÓGICA DE PROCESAMIENTO ---
if analyze_btn:
    if not url_input:
        st.warning("⚠️ Por favor ingresa una URL.")
    elif not email_input:
        st.warning("⚠️ Falta el correo electrónico.")
    else:
        # 1. Corrección inteligente de URL
        url_final = url_input.strip()
        if not url_final.startswith("http"):
            url_final = "https://" + url_final

        # 2. Ejecución
        with st.spinner(f"🤖 Analizando {url_final}..."):
            try:
                # Payload LIMPIO (Solo lo necesario)
                payload = {
                    "url": url_final,
                    "email": email_input
                }

                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- MANEJO DE RESPUESTAS ---
                
                # ÉXITO (200)
                if response.status_code == 200:
                    data = response.json()
                    analisis_texto = data.get("output") or data.get("text") or data.get("message") or str(data)
                    
                    st.success("✅ ¡Análisis Completado!")
                    
                    with st.expander("📄 Leer reporte completo", expanded=True):
                        st.markdown(analisis_texto)
                    
                    st.info(f"📧 Se ha enviado una copia a: {email_input}")

                # ERROR ANTI-SCRAPER (400)
                elif response.status_code == 400:
                    st.error("🔒 BLOQUEO DETECTADO: Este sitio web tiene protección anti-robots y no permite ser analizado.")
                    st.caption("Intenta con otro sitio o verifica que sea público.")
                
                # ERROR DE SERVIDOR (500)
                elif response.status_code == 500:
                    st.error("🔥 Error interno en n8n. (Probablemente por bloqueo de API de Google o fallo en el flujo).")

                # ERROR DE CONEXIÓN (404)
                elif response.status_code == 404:
                    st.error("❌ No se encuentra el Webhook. Verifica que el flujo esté ACTIVO en n8n.")

                else:
                    st.error(f"⚠️ Error inesperado: {response.status_code}")

            except Exception as e:
                st.error(f"😱 Error de conexión: {str(e)}")




