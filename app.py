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
            /* Estilo para mensajes de alerta más bonitos */
            .stAlert { padding: 1rem; border-radius: 10px; }
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
        placeholder="tu@email.com"
    )
    
    # Espacio
    st.write("")
    
    # Botón de envío
    enviado = st.form_submit_button("✨ Iniciar Análisis Ahora", type="primary")

# --- LÓGICA DE PROCESAMIENTO ---
if enviado:
    if not url_input or not email_usuario:
        st.warning("⚠️ Por favor, completa todos los campos para iniciar.")
    else:
        # Limpieza de URL
        url_final = url_input.strip()
        if not url_final.startswith(('http://', 'https://')):
            url_final = 'https://' + url_final
            
        # Simulación de carga (Feedback visual)
        with st.status("⚙️ Iniciando motores de análisis...", expanded=True) as status:
            st.write("Conectando con el servidor...")
            time.sleep(1)
            st.write("Validando URL...")
            
            # URL DE PRODUCCIÓN
            webhook_url = "https://n8n-testi.hopto.org/webhook/analisis-ux"
            
            datos = {
                "url": url_final,
                "email": email_usuario
            }
            
            try:
                respuesta = requests.post(webhook_url, json=datos)
                
                if respuesta.status_code == 200:
                    status.update(label="✅ ¡Solicitud procesada correctamente!", state="complete", expanded=True)
                    
                    # --- MENSAJE PRINCIPAL ---
                    st.success(f"""
                    **¡El sistema ha iniciado el análisis correctamente!** 🚀
                    
                    Hemos puesto en cola a **{url_final}**. Nuestro agente de IA está escaneando la web en este momento.
                    """)
                    
                    # --- ADVERTENCIA PROFESIONAL (Aquí manejamos el error de seguridad) ---
                    st.info(f"""
                    📧 **Revisa tu correo ({email_usuario}) en los próximos 2 minutos.**
                    
                    ---
                    ⚠️ **¿No recibes el PDF?** Si pasados 5 minutos no te llega el reporte, es muy probable que el sitio web tenga **bloqueos de seguridad anti-bots** (común en sitios de gobierno o bancos) que impiden nuestra auditoría externa.
                    """)
                    
                else:
                    status.update(label="Error de conexión", state="error", expanded=True)
                    st.error("Hubo un problema técnico al conectar. Por favor intenta más tarde.")
                    
            except Exception as e:
                st.error(f"Error de comunicación: {e}")

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






