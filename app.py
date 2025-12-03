import streamlit as st
import requests
import json
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (Para que se vea limpio y oculte marcas de agua) ---
st.markdown("""
<style>
    .stDeployButton {display:none;}
    h1 {color: #FF4B4B;}
    .stButton button {width: 100%; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 🔗 TU URL REAL (Ya configurada)
N8N_WEBHOOK_URL = "https://n8n-testi.hopto.org/webhook/analisis-ux"

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("🕵️ InsightUX")
    st.markdown("---")
    st.markdown("""
    **Pasos:**
    1.  🌐 Ingresa la web.
    2.  🎯 Define el perfil.
    3.  📩 Recibe el reporte.
    """)
    st.info("💡 **Tip:** El perfil 'Gen Z' detecta si tu diseño se siente antiguo.")
    st.caption("v.Stable | Powered by Gemini & n8n")

# --- ÁREA PRINCIPAL ---
st.title("Evaluador de Experiencia UX")
st.markdown("Diagnóstico de sitios web potenciado por Inteligencia Artificial.")
st.markdown("---") 

# --- FORMULARIO INTELIGENTE ---
# 1. Input de URL (Sin obligar a poner http)
url_input = st.text_input(
    "🔗 Sitio web a analizar", 
    placeholder="ejemplo.com",
    help="Puedes escribirlo con o sin https://"
)

col1, col2 = st.columns(2)

with col1:
    email_input = st.text_input("✉️ Tu correo", placeholder="tu@email.com")

with col2:
    persona_selected = st.selectbox(
        "🎭 Perfil del Auditor",
        options=[
            "Experto en UX (Crítico Técnico)",
            "Usuario Senior (+70 años, dificultad visual)",
            "Gen Z (Impaciente, escanea rápido)",
            "Comprador Impulsivo (Busca ofertas)",
            "Usuario Desconfiado (Busca seguridad legal)"
        ]
    )

st.write("") # Espacio separador
analyze_btn = st.button("🚀 Iniciar Auditoría", type="primary")

# --- LÓGICA DE PROCESAMIENTO ---
if analyze_btn:
    if not url_input:
        st.warning("⚠️ Por favor ingresa una URL.")
    elif not email_input:
        st.warning("⚠️ Falta el correo electrónico.")
    else:
        # CORRECCIÓN AUTOMÁTICA DE URL (Lo que pediste)
        url_final = url_input.strip()
        if not url_final.startswith("http"):
            url_final = "https://" + url_final

        # Spinner compatible (Funciona en todas las versiones)
        with st.spinner(f"🤖 El {persona_selected} está analizando {url_final}..."):
            try:
                # Simular espera visual
                time.sleep(1) 
                
                payload = {
                    "url": url_final,
                    "persona": persona_selected,
                    "email": email_input
                }

                # Envío de datos
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- RESPUESTAS ---
                if response.status_code == 200:
                    data = response.json()
                    # Extraer texto de cualquier formato que devuelva n8n
                    analisis_texto = data.get("output") or data.get("text") or data.get("message") or str(data)
                    
                    st.balloons() # ¡Festejo!
                    st.success("✅ ¡Análisis Completado!")
                    
                    with st.expander("📄 Leer reporte preliminar", expanded=True):
                        st.markdown(analisis_texto)
                    
                    st.info(f"📧 Enviando copia detallada a: {email_input}")

                elif response.status_code == 400:
                    st.error("🔒 El sitio tiene seguridad anti-robots. Intenta con otro.")
                
                elif response.status_code == 404:
                    st.error("❌ Error 404: El Webhook de n8n no está activo o la URL cambió.")

                else:
                    st.error(f"🔥 Error del servidor: {response.status_code}")

            except Exception as e:
                st.error(f"😱 Error de conexión: {str(e)}")




