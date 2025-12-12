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
    .stButton button {width: 100%; border-radius: 8px; font-weight: bold; padding: 10px;}
    .report-container {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;}
    .team-card {background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;}
</style>
""", unsafe_allow_html=True)

# 🔗 URL DEL WEBHOOK DE N8N
# Si estás dentro del mismo servidor (Docker), usa la IP interna: http://172.17.0.1:5678...
# Si estás probando desde tu PC local, usa la IP pública: http://159.112.138.149:5678...
N8N_WEBHOOK_URL = "http://172.17.0.1:5678/webhook/test-lucas"

# --- SIDEBAR (INFORMACIÓN) ---
with st.sidebar:
    st.header("🕵️ InsightUX Engine")
    st.markdown("---")
    st.info("""
    **Proceso de Auditoría:**
    1. 🌐 **Escaneo:** Leemos la estructura de tu sitio.
    2. 🧠 **Análisis IA:** Detectamos fricciones UX/UI.
    3. 🚀 **Estrategia:** Generamos un plan de acción.
    """)
    
    st.markdown("---")
    st.caption("Developed by Lucas Rojo | Powered by n8n & LLMs")

# --- MAIN HEADER ---
st.title("Evaluador de Experiencia UX")
st.markdown("### 🚀 Auditoría de Landing Pages con Inteligencia Artificial")
st.markdown("Obtén un diagnóstico crítico de tu sitio web y descubre por qué no estás convirtiendo más visitas en clientes.")
st.markdown("---") 

# --- FORMULARIO DE ENTRADA ---
col1, col2 = st.columns([2, 1])
with col1:
    url_input = st.text_input("🔗 URL del sitio web", placeholder="ejemplo.com.ar")
with col2:
    email_input = st.text_input("✉️ Tu correo", placeholder="tu@email.com")

# --- LÓGICA DE EJECUCIÓN ---
if st.button("🔍 Iniciar Auditoría Técnica", type="primary"):
    if not url_input or not email_input:
        st.warning("⚠️ Por favor completa la URL y tu Email para enviarte el reporte.")
    else:
        # 1. Normalización de URL (El parche mágico)
        url_final = url_input.strip()
        if not url_final.startswith(("http://", "https://")):
            url_final = "https://" + url_final

        # 2. Feedback visual al usuario
        with st.spinner(f"⚡ Conectando con InsightUX Engine... Analizando {url_final}"):
            try:
                # Payload para n8n
                payload = {"url": url_final, "email": email_input}
                
                # Petición al Webhook
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- RESPUESTA ---
                if response.status_code == 200:
                    data = response.json()
                    # Si n8n devuelve texto, lo mostramos. Si no, mensaje default.
                    analisis = data.get("output", "✅ Análisis enviado exitosamente a tu correo.")
                    
                    st.success("¡Diagnóstico Completado!")
                    st.balloons()
                    
                    # Mostrar resultado preliminar en pantalla
                    st.markdown("### 📄 Resultado Preliminar")
                    st.markdown(f'<div class="report-container">{analisis}</div>', unsafe_allow_html=True)
                    st.info("📨 Se ha enviado un reporte detallado en PDF/HTML a tu casilla de correo.")
                        
                elif response.status_code == 400:
                    st.error("🔒 No pudimos acceder al sitio. Verifica que la URL sea correcta y pública.")
                else:
                    st.error(f"⚠️ Error de comunicación con el motor IA ({response.status_code}).")
                    
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")

# --- PIE DE PÁGINA: EQUIPO ---
st.markdown("---")
st.subheader("🤝 Conoce al Equipo InsightUX")
st.markdown("Detrás de esta herramienta combinamos la **potencia técnica** con la **psicología del usuario**.")

col_team1, col_team2 = st.columns(2)

with col_team1:
    st.markdown("""
    <div class="team-card">
        <h3>Lucas Rojo</h3>
        <p style="color: #666; font-weight: bold;">Technical Automation Architect</p>
        <p style="font-size: 14px;">Especialista en












