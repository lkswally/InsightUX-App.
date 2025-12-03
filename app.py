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

# --- ESTILOS CSS (Para limpiar la vista) ---
st.markdown("""
<style>
    .stDeployButton {display:none;}
    h1 {color: #FF4B4B;}
</style>
""", unsafe_allow_html=True)

# ⚠️ TU WEBHOOK AQUÍ (Revisa que sea el correcto)
N8N_WEBHOOK_URL = "https://tu-n8n-server.com/webhook/..." 

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("🕵️ InsightUX")
    st.markdown("---")
    st.markdown("""
    **Pasos:**
    1.  🌐 Pega la URL.
    2.  🎯 Elige el perfil.
    3.  📩 Recibe el reporte.
    """)
    st.info("💡 Tip: El perfil 'Gen Z' detecta si tu sitio se ve antiguo.")
    st.caption("v1.5 | Powered by Gemini & n8n")

# --- ÁREA PRINCIPAL ---
st.title("Evaluador de Experiencia UX")
st.markdown("Diagnóstico de sitios web potenciado por Inteligencia Artificial.")
st.markdown("---") # Línea divisoria para separar el título del formulario

# --- FORMULARIO (Sin el borde que daba error) ---
st.subheader("🛠️ Configuración del Análisis")

url_input = st.text_input(
    "🔗 URL del sitio web", 
    placeholder="https://www.tusitio.com"
)

col1, col2 = st.columns(2)

with col1:
    email_input = st.text_input("✉️ Tu correo electrónico", placeholder="tu@email.com")

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

st.write("") # Espacio
analyze_btn = st.button("🚀 Iniciar Auditoría", type="primary", use_container_width=True)

# --- LÓGICA ---
if analyze_btn:
    if not url_input or not email_input:
        st.warning("⚠️ Faltan datos: URL o Email.")
    elif not url_input.startswith("http"):
        st.error("⛔ La URL debe comenzar con http:// o https://")
    else:
        # Usamos st.spinner que es compatible con TODAS las versiones
        with st.spinner(f"🤖 El {persona_selected} está analizando el sitio..."):
            try:
                # Simular proceso visual (espera 1 seg)
                time.sleep(1)
                
                payload = {
                    "url": url_input,
                    "persona": persona_selected,
                    "email": email_input
                }

                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    analisis_texto = data.get("output") or data.get("text") or str(data)
                    
                    st.success("✅ ¡Reporte Generado Exitosamente!")
                    st.balloons() # ¡Un poco de fiesta visual!
                    
                    st.markdown("### 📝 Resumen del Análisis")
                    with st.expander("Leer reporte completo", expanded=True):
                        st.markdown(analisis_texto)
                    
                    st.info(f"📧 Se ha enviado una copia a: {email_input}")

                elif response.status_code == 400:
                    st.error("❌ El sitio web bloqueó nuestro acceso (Seguridad Anti-Bot).")
                
                else:
                    st.error(f"🔥 Error del servidor (Código {response.status_code})")

            except Exception as e:
                st.error(f"😱 Error de conexión: {str(e)}")



