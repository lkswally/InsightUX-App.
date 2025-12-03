import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
# ⚠️ IMPORTANTE: Reemplaza esto con tu URL del Webhook de n8n (Production URL preferiblemente)
N8N_WEBHOOK_URL = "https://tu-n8n-server.com/webhook/..." 

# Configuración de la página (título, icono, layout)
st.set_page_config(
    page_title="InsightUX - Análisis IA",
    page_icon="🕵️‍♀️",
    layout="centered"
)

# --- ENCABEZADO ---
st.title("🕵️‍♀️ InsightUX")
st.markdown("""
**Tu analista de Experiencia de Usuario (UX) potenciado por IA.**
Ingresa una URL, elige quién quieres que audite el sitio y recibe un informe detallado.
""")

st.divider()

# --- FORMULARIO DE ENTRADA ---
col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input("🔗 URL del sitio web a analizar", placeholder="https://ejemplo.com")

with col2:
    # NUEVO: Selector de Personalidad
    persona_selected = st.selectbox(
        "🎭 ¿Quién audita?",
        options=[
            "Experto en UX (Técnico y crítico)",
            "Usuario Senior (+70 años, dificultad visual)",
            "Gen Z (Impaciente, escanea rápido)",
            "Comprador Impulsivo (Busca ofertas)",
            "Abogado (Busca términos legales y confianza)"
        ],
        index=0 # Por defecto selecciona la primera opción
    )

analyze_btn = st.button("🚀 Analizar Sitio", type="primary", use_container_width=True)

# --- LÓGICA DE PROCESAMIENTO ---
if analyze_btn:
    if not url_input:
        st.warning("⚠️ Por favor, ingresa una URL válida para comenzar.")
    elif not url_input.startswith("http"):
        st.error("⛔ La URL debe comenzar con http:// o https://")
    else:
        # Mostramos un spinner mientras n8n trabaja
        with st.spinner(f"🤖 El {persona_selected} está visitando el sitio... (Esto puede tardar unos segundos)"):
            try:
                # Preparamos los datos para enviar a n8n
                payload = {
                    "url": url_input,
                    "persona": persona_selected
                }

                # Enviamos la petición al Webhook
                response = requests.post(N8N_WEBHOOK_URL, json=payload)

                # --- MANEJO DE RESPUESTAS (Según lo que configuramos en el IF) ---
                
                # Caso 1: Error del Scraper (Configuramos código 400 en n8n)
                if response.status_code == 400:
                    try:
                        error_data = response.json()
                        st.error(f"❌ **No pudimos leer el sitio:** {error_data.get('message', 'Bloqueo de seguridad detectado.')}")
                        st.info("Intenta con otra URL o verifica que el sitio sea público.")
                    except:
                        st.error("❌ Error 400: El sitio bloqueó el acceso, pero no recibimos mensaje detallado.")

                # Caso 2: Éxito (Código 200)
                elif response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Dependiendo de cómo








