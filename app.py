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

# --- ESTILOS CSS (Look Pro y correcciones de visualización) ---
st.markdown("""
<style>
    .stDeployButton {display:none;}
    h1 {color: #FF4B4B;}
    .stButton button {width: 100%; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 🔗 TU URL REAL DE PRODUCCIÓN
N8N_WEBHOOK_URL = "https://n8n-testi.hopto.org/webhook/analisis-ux"

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("🕵️ InsightUX")
    st.markdown("---")
    st.markdown("""
    **Cómo funciona:**
    1.  🌐 Ingresa la URL del sitio.
    2.  ✉️ Coloca tu email.
    3.  🤖 Recibe la auditoría automática.
    """)
    st.info("ℹ️ El sistema detectará si el sitio tiene bloqueos de seguridad.")
    st.caption("v.Stable | Powered by Gemini & n8n")

# --- ÁREA PRINCIPAL ---
st.title("Evaluador de Experiencia UX")
st.markdown("Diagnóstico de sitios web potenciado por Inteligencia Artificial.")
st.markdown("---") 

# --- FORMULARIO SIMPLIFICADO ---
url_input = st.text_input(
    "🔗 Sitio web a analizar", 
    placeholder="ejemplo.com",
    help="El sistema corregirá automáticamente si falta http://"
)

email_input = st.text_input("✉️ Tu correo electrónico", placeholder="tu@email.com")

st.write("") # Espaciador visual
analyze_btn = st.button("🚀 Iniciar Auditoría", type="primary")

# --- LÓGICA DE PROCESAMIENTO ---
if analyze_btn:
    # 1. Validaciones básicas
    if not url_input:
        st.warning("⚠️ Por favor ingresa una URL.")
    elif not email_input:
        st.warning("⚠️ Falta el correo electrónico.")
    else:
        # 2. Corrección automática de URL
        url_final = url_input.strip()
        if not url_final.startswith("http"):
            url_final = "https://" + url_final

        # 3. Ejecución con Feedback Visual
        with st.spinner(f"🤖 Analizando {url_final}... (Esto puede tardar unos segundos)"):
            try:
                # Payload LIMPIO (Sin personalidad, solo lo esencial)
                payload = {
                    "url": url_final,
                    "email": email_input
                }

                # Llamada al Webhook
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- MANEJO DE ERRORES Y RESPUESTAS ---
                
                # CASO 1: ÉXITO (200)
                if response.status_code == 200:
                    data = response.json()
                    # Buscar el texto en cualquier variable que devuelva n8n
                    analisis_texto = data.get("output") or data.get("text") or data.get("message") or str(data)
                    
                    st.success("✅ ¡Análisis Completado!")
                    st.balloons()
                    
                    with st.expander("📄 Ver Reporte Preliminar", expanded=True):
                        st.markdown(analisis_texto)
                    
                    st.info(f"📧 Enviando copia detallada a: {email_input}")

                # CASO 2: ANTI-SCRAPER / BLOQUEO (400)
                elif response.status_code == 400:
                    st.error("🔒 ACCESO DENEGADO: El sitio web tiene protección anti-robots.")
                    st.warning("El scraper no pudo leer el contenido. Intenta con otro sitio web.")
                
                # CASO 3: ERROR DE SERVIDOR / API (500)
                elif response.status_code == 500:
                    st.error("🔥 Error del Servidor (500).")
                    st.markdown("""
                    **Posibles causas:**
                    * Bloqueo de facturación en Google Cloud (API Key suspendida).
                    * Fallo interno en el flujo de n8n.
                    """)

                # CASO 4: NO ENCONTRADO (404)
                elif response.status_code == 404:
                    st.error("❌ Error 404: No se encuentra el Webhook.")
                    st.caption("Verifica que el flujo esté ACTIVO (interruptor verde) en n8n.")

                else:
                    st.error(f"⚠️ Error inesperado: Código {response.status_code}")

            except Exception as e:
                st.error(f"😱 Error de conexión: {str(e)}")





