import streamlit as st
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="InsightUX - Auditoría IA",
    page_icon="🔍",
    layout="centered"
)

# --- ESTILOS CSS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("🔍 InsightUX")
st.markdown("### Auditoría Técnica de UX, CRO y SEO")
st.markdown("""
Nuestro agente de IA analiza tu sitio web en tiempo real cruzando datos de:
* 🧠 **Experiencia de Usuario (Heurísticas)**
* 📈 **Potencial de Conversión (CRO)**
* 🔎 **Posicionamiento en Buscadores (SEO)**
""")

st.markdown("---")

# --- FORMULARIO ---
with st.form("analisis_form"):
    st.write("#### 🚀 Solicitar diagnóstico gratuito")
    
    col1, col2 = st.columns([2, 1])
    
    url_input = st.text_input(
        "Sitio Web", 
        placeholder="ejemplo.com", 
        help="Escribe el dominio (ej: saldo.com.ar)"
    )
    
    email_usuario = st.text_input(
        "¿Dónde enviamos el reporte?", 
        placeholder="nombre@tuempresa.com"
    )
    
    st.write("")
    enviado = st.form_submit_button("✨ Iniciar Análisis Ahora", type="primary")

# --- LÓGICA DE PROCESAMIENTO HÍBRIDA ---
if enviado:
    if not url_input or not email_usuario:
        st.warning("⚠️ Por favor, completa todos los campos para iniciar.")
    else:
        # Limpieza de URL
        url_final = url_input.strip()
        if not url_final.startswith(('http://', 'https://')):
            url_final = 'https://' + url_final
            
        # Feedback Visual de carga
        with st.status("⚙️ Conectando con el servidor...", expanded=True) as status:
            st.write("Validando URL y permisos de acceso...")
            
            # URL DE PRODUCCIÓN
            webhook_url = "https://n8n-testi.hopto.org/webhook/analisis-ux"
            
            datos = {
                "url": url_final,
                "email": email_usuario
            }
            
            try:
                # Esperamos la respuesta rápida del Scraper (máx 20 segundos)
                respuesta = requests.post(webhook_url, json=datos, timeout=20)
                
                # Intentamos leer el mensaje que manda n8n
                try:
                    mensaje_n8n = respuesta.json().get('message', 'Proceso finalizado.')
                except:
                    mensaje_n8n = "Respuesta del servidor recibida."

                # --- ESCENARIO 1: ÉXITO (Código 200 - Camino de arriba) ---
                if respuesta.status_code == 200:
                    status.update(label="✅ ¡Conexión Exitosa!", state="complete", expanded=True)
                    
                    st.success(f"**¡Excelente! {mensaje_n8n}**")
                    
                    st.markdown(f"""
                    El agente de IA ya está trabajando en tu reporte para **{url_final}**.
                    
                    📬 **Te llegará al correo ({email_usuario}) en aproximadamente 2 minutos.**
                    *(Puedes cerrar esta pestaña, el proceso continúa en la nube).*
                    """)
                
                # --- ESCENARIO 2: ERROR (Código 400 - Camino de abajo) ---
                elif respuesta.status_code >= 400:
                    status.update(label="🛑 No se pudo analizar", state="error", expanded=True)
                    
                    st.error(f"**Error de Lectura:** {mensaje_n8n}")
                    
                    st.info("""
                    **¿Por qué pasa esto?**
                    Es muy probable que el sitio tenga un **bloqueo de seguridad anti-bots** (común en sitios de gobierno o bancos) que impide nuestra auditoría automática.
                    """)
                    
            except Exception as e:
                status.update(label="Error técnico", state="error")
                st.error("El servidor está tardando en responder. Si el sitio es muy pesado, es posible que el reporte llegue igual a tu correo en unos minutos.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 12px;'>
        InsightUX © 2025 | Desarrollado por Antonella C. & Lucas R.<br>
        Potenciado por Google Gemini Pro
    </div>
    """, 
    unsafe_allow_html=True
)







