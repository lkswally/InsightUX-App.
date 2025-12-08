import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="🕵️‍♀️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stDeployButton {display:none;}
    h1 {color: #FF4B4B;}
    .stButton button {width: 100%; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 🔗 URL DE PRODUCCIÓN DE N8N (PEGA TU URL AQUI)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/test-lucas"

# --- SIDEBAR ---
with st.sidebar:
    st.header("🕵️ InsightUX")
    st.markdown("---")
    st.markdown("""
    **Cómo funciona:**
    1. 🌐 Ingresa la URL.
    2. 🤖 IA analiza UX/UI.
    3. 📧 Recibes el reporte.
    """)
    st.caption("v.MVP 1.0 | Lucas Rojo")

# --- MAIN ---
st.title("Evaluador de Experiencia UX")
st.markdown("Auditoría de landing pages en tiempo real con IA.")
st.markdown("---") 

url_input = st.text_input("🔗 URL del sitio web", placeholder="reyesoft.com")
email_input = st.text_input("✉️ Tu correo electrónico", placeholder="lucas@ejemplo.com")

if st.button("🚀 Auditar Ahora", type="primary"):
    if not url_input or not email_input:
        st.warning("⚠️ Por favor completa URL y Email.")
    else:
        # Normalización de URL
        url_final = url_input.strip()
        if not url_final.startswith("http"):
            url_final = "https://" + url_final

        with st.spinner(f"🤖 Leyendo {url_final} y generando reporte..."):
            try:
                # Payload que espera tu n8n
                payload = {"url": url_final, "email": email_input}
                
                # Petición al Webhook
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- LÓGICA DE RESPUESTA ---
                if response.status_code == 200:
                    data = response.json()
                    # Intentamos obtener el texto de la respuesta
                    analisis = data.get("output", "Análisis completado (revisá tu email).")
                    
                    st.success("✅ ¡Auditoría Finalizada!")
                    st.balloons()
                    
                    # Mostrar resultado en pantalla
                    with st.expander("📄 Leer Reporte Aquí", expanded=True):
                        st.markdown(analisis)
                        
                elif response.status_code == 400:
                    st.error("🔒 No pudimos leer el sitio. Posible bloqueo de seguridad o URL inválida.")
                else:
                    st.error(f"⚠️ Error del sistema ({response.status_code}). Intenta más tarde.")
                    
            except Exception as e:
                st.error(f"Error de conexión: {e}")




