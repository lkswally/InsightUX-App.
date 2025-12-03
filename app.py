import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
# Tu URL REAL (Recuperada de tus capturas)
N8N_WEBHOOK_URL = "https://n8n-testi.hopto.org/webhook/analisis-ux"

st.set_page_config(
    page_title="InsightUX - MVP",
    page_icon="🕵️‍♀️",
    layout="centered"
)

# --- INTERFAZ SIMPLE ---
st.title("🕵️‍♀️ InsightUX")
st.markdown("Diagnóstico de UX potenciado por IA. Ingresa tu sitio y recibe el reporte.")

st.divider()

# Formulario básico (Solo URL y Email)
url_input = st.text_input("🔗 URL del sitio web a analizar", placeholder="https://ejemplo.com")
email_input = st.text_input("✉️ Tu correo electrónico", placeholder="nombre@empresa.com")

if st.button("🚀 Analizar Sitio", type="primary"):
    if not url_input or not url_input.startswith("http"):
        st.error("⛔ Por favor ingresa una URL válida (con http:// o https://)")
    else:
        # Spinner clásico (compatible con todas las versiones)
        with st.spinner("⏳ Conectando con el servidor... esto puede tardar unos segundos."):
            try:
                # Payload simple (Sin personalidad)
                payload = {
                    "url": url_input,
                    "email": email_input
                }

                # Petición al servidor
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                if response.status_code == 200:
                    try:
                        data = response.json()
                        # Busca el texto en cualquier campo posible
                        resultado = data.get("output") or data.get("text") or data.get("message") or str(data)
                        
                        st.success("✅ ¡Análisis completado!")
                        st.markdown("### Resultado:")
                        st.markdown(resultado)
                    except:
                        st.success("✅ El análisis se envió correctamente.")
                        st.write(response.text)
                
                elif response.status_code == 400:
                    st.error("❌ El sitio web bloqueó el acceso (Seguridad Anti-Bot).")
                
                elif response.status_code == 500:
                    st.error("🔥 Error interno del servidor (Revisa n8n).")
                    
                else:
                    st.error(f"Error desconocido: {response.status_code}")

            except Exception as e:
                st.error(f"😱 No se pudo conectar: {str(e)}")




