import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="InsightUX - Auditoría IA",
    page_icon="🔍",
    layout="centered"
)

# --- ESTILOS CSS (Para ocultar elementos molestos y centrar) ---
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
st.header("Auditoría Web 360° con IA")
st.markdown("""
Obtén un diagnóstico profesional de tu sitio web en segundos.
Analizamos **Experiencia de Usuario (UX)**, **Conversión (CRO)** y **Posicionamiento (SEO)**.
""")

st.markdown("---")

# --- FORMULARIO ---
with st.form("analisis_form"):
    st.write("### 🚀 Comienza tu análisis gratuito")
    
    # Inputs
    col1, col2 = st.columns([2, 1])
    
    url_input = st.text_input(
        "Sitio Web", 
        placeholder="ejemplo.com", 
        help="No hace falta poner https://"
    )
    
    email_usuario = st.text_input(
        "Tu Correo Electrónico", 
        placeholder="nombre@tuempresa.com"
    )
    
    # Botón de envío (ancho completo)
    enviado = st.form_submit_button("✨ Auditar mi sitio ahora", type="primary")

# --- LÓGICA DE PROCESAMIENTO ---
if enviado:
    if not url_input or not email_usuario:
        st.warning("⚠️ Por favor, completa todos los campos para iniciar.")
    else:
        # --- 1. LIMPIEZA DE URL (La magia automática) ---
        url_final = url_input.strip() # Quita espacios
        if not url_final.startswith(('http://', 'https://')):
            url_final = 'https://' + url_final
            
        # --- 2. FEEDBACK VISUAL ---
        with st.status("🤖 Conectando con el Agente de IA...", expanded=True) as status:
            st.write("Escaneando estructura web...")
            
            # --- 3. ENVÍO DE DATOS ---
            # URL DE PRODUCCIÓN (Asegúrate de que sea la correcta sin -test)
            webhook_url = "https://n8n-testi.hopto.org/webhook/analisis-ux"
            
            datos = {
                "url": url_final,
                "email": email_usuario
            }
            
            try:
                respuesta = requests.post(webhook_url, json=datos)
                
                if respuesta.status_code == 200:
                    status.update(label="¡Análisis completado!", state="complete", expanded=False)
                    
                    # --- 4. MENSAJE DE ÉXITO AMIGABLE ---
                    st.success(f"✅ ¡Listo! Hemos enviado el reporte PDF a **{email_usuario}**.")
                    st.info("🕒 Podría tardar entre 1 y 2 minutos en llegar. Revisa tu carpeta de Spam por si acaso.")
                    
                    # Mostramos qué URL se analizó realmente (para confirmación visual)
                    st.caption(f"🔗 URL Analizada: {url_final}")
                    
                else:
                    status.update(label="Error de conexión", state="error")
                    st.error("Hubo un problema al conectar con el servidor. Intenta de nuevo en unos minutos.")
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Desarrollado por Lucas R. & Anto C. | Potenciador de Web</small>
    </div>
    """, 
    unsafe_allow_html=True
)




