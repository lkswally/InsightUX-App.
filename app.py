import streamlit as st
import requests
import json
import time

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="InsightUX | Auditoría IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS DE ALTO IMPACTO (GLASSMORPHISM) ---
st.markdown("""
<style>
    /* 1. FONDO GLOBAL CON DEGRADADO */
    .stApp {
        background: rgb(14,17,23);
        background: linear-gradient(135deg, rgba(14,17,23,1) 0%, rgba(30,33,48,1) 100%);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. TÍTULOS CON GRADIENTE */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #E0E0E0 !important;
        font-weight: 600;
    }

    /* 3. INPUTS MODERNOS (Cajas de texto) */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border: 1px solid #FF4B4B !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.2);
    }
    .stTextInput label {
        color: #BBBBBB !important;
        font-size: 0.9rem;
    }

    /* 4. BOTÓN PRINCIPAL (NEÓN) */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        font-weight: bold;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 50px; /* Redondo */
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.6);
    }

    /* 5. TARJETAS DEL EQUIPO (CRISTAL) */
    .team-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 75, 75, 0.3);
    }
    .team-card h4 {
        color: white;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .team-card p {
        color: #888;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }
    .team-link {
        color: #FF4B4B;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        border: 1px solid #FF4B4B;
        padding: 5px 15px;
        border-radius: 20px;
        transition: all 0.3s;
    }
    .team-link:hover {
        background-color: #FF4B4B;
        color: white;
    }

    /* Ocultar elementos molestos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
</style>
""", unsafe_allow_html=True)

# 🔗 CONEXIÓN
N8N_WEBHOOK_URL = "http://159.112.138.149:5678/webhook/test-lucas"

# --- UI PRINCIPAL ---

# Espacio superior
st.write("")
st.write("")

st.title("InsightUX Engine ⚡")
st.markdown(
    "<p style='text-align: center; color: #BBB; font-size: 1.1rem;'>Auditoría de Landing Pages potenciada por Inteligencia Artificial.</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# --- FORMULARIO ---
# Usamos columnas para centrar un poco si la pantalla es muy ancha, 
# pero en '







