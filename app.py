import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="InsightUX - Evaluador", page_icon="🔍")

# Título y Bajada
st.title("🔍 InsightUX")
st.subheader("Evaluador de Madurez UX Automatizado")
st.write("Ingresa la URL de tu sitio web y recibe un diagnóstico preliminar de experiencia de usuario basado en IA.")

# --- FORMULARIO ---
with st.form("analisis_form"):
    # Inputs del usuario
    url_objetivo = st.text_input("URL del sitio web a analizar", placeholder="https://ejemplo.com")
    email_usuario = st.text_input("Tu correo electrónico (para enviarte el reporte)", placeholder="nombre@empresa.com")
    
    # Botón de envío
    enviado = st.form_submit_button("🚀 Analizar mi sitio")

# --- LÓGICA DE ENVÍO ---
if enviado:
    if not url_objetivo or not email_usuario:
        st.warning("⚠️ Por favor, completa todos los campos.")
    else:
        st.info("⏳ Enviando datos al cerebro (n8n)...")
        
        # 1. TU URL DE N8N (La Test URL que copiaste)
        webhook_url = "https://n8n-testi.hopto.org/webhook-test/analisis-ux"
        
        # 2. El paquete de datos a enviar (JSON)
        datos = {
            "url": url_objetivo,
            "email": email_usuario
        }
        
        try:
            # 3. Enviar la petición POST a n8n
            respuesta = requests.post(webhook_url, json=datos)
            
            if respuesta.status_code == 200:
                st.success("✅ ¡Conexión Exitosa! n8n recibió los datos.")
                st.json(datos) # Te muestra en pantalla qué envió
            else:
                st.error(f"❌ Error al conectar con n8n: {respuesta.status_code}")
                
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

# Footer simple
st.markdown("---")

st.caption("InsightUX MVP - Powered by LucasR & AntoC")




