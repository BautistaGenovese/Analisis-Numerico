import streamlit as st
from core import utils as ut

st.set_page_config(
    page_title='Roooty Lab',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# --- 1. DEFINICIÓN DE PÁGINAS ---
pagina_inicio = st.Page("inicio.py", title="Inicio", icon="🏠")
pagina_biseccion = st.Page("metodos/biseccion.py", title="Bisección", icon="📉", url_path="biseccion")
pagina_regula_falsi = st.Page("metodos/regula_falsi.py", title="Regula Falsi", icon="📐", url_path="regula-falsi")
pagina_newton = st.Page("metodos/newton.py", title="Newton", icon="🎢", url_path="newton")
pagina_secante = st.Page("metodos/secante.py", title="Secante", icon="🎯", url_path="secante")
pagina_punto_fijo = st.Page("metodos/punto_fijo.py", title="Punto Fijo", icon="📍", url_path="punto-fijo")
pagina_regresion = st.Page("metodos/regresion.py", title="Regresión", icon="📊", url_path="regresion")
pagina_comparacion = st.Page("metodos/comparacion.py", title="Comparación", icon="📈", url_path="comparacion")

# --- 2. NAVEGACIÓN OCULTA ---
todas_las_paginas = [
    pagina_inicio, pagina_biseccion, pagina_regula_falsi,
    pagina_newton, pagina_secante, pagina_punto_fijo,
    pagina_regresion, pagina_comparacion
]
nav = st.navigation(todas_las_paginas, position="hidden")

def cargar_css_externo(ruta_archivo):
    try:
        with open(ruta_archivo, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def main():
    # Carga todos los estilos desde tu archivo CSS
    cargar_css_externo("estilos.css")

    # --- 3. DIBUJADO DEL MENÚ LATERAL ---
    with st.sidebar:
        # Logo Corporativo
        st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 2rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 1rem;">
                <h1 style="margin: 0; font-weight: 800; color: #1a2b4c; font-size: 1.8rem; letter-spacing: -1px;">
                <b style = "display: inline; padding:0px 11px; margin-right:5px; background-color:#0f172a; border-radius:5px; color: #F0F8FF ">Σ</b> ROOOTY Lab</h1>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='color: #64748b; font-weight: bold; font-size: 0.8rem; margin-bottom: 0.8rem;'>NAVEGACIÓN</p>", unsafe_allow_html=True)
        st.page_link(pagina_inicio)

        st.markdown("<p style='color: #64748b; font-weight: bold; font-size: 0.8rem; margin-top: 1.5rem; margin-bottom: 0.8rem;'>MÉTODOS CERRADOS</p>", unsafe_allow_html=True)
        st.page_link(pagina_biseccion)
        st.page_link(pagina_regula_falsi)

        st.markdown("<p style='color: #64748b; font-weight: bold; font-size: 0.8rem; margin-top: 1.5rem; margin-bottom: 0.8rem;'>MÉTODOS ABIERTOS</p>", unsafe_allow_html=True)
        st.page_link(pagina_newton)
        st.page_link(pagina_secante)
        st.page_link(pagina_punto_fijo)

        st.markdown("<p style='color: #64748b; font-weight: bold; font-size: 0.8rem; margin-top: 1.5rem; margin-bottom: 0.8rem;'>HERRAMIENTAS</p>", unsafe_allow_html=True)
        st.page_link(pagina_regresion)
        st.page_link(pagina_comparacion)

        st.markdown("<hr style='border: 1px solid #f1f5f9; margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-weight: bold; font-size: 0.8rem; margin-bottom: 0.8rem;'>UTILIDADES</p>", unsafe_allow_html=True)
        ut.mostrar_menu_ajustes()

    # --- 4. EJECUCIÓN ---
    nav.run()

if __name__ == '__main__':
    main()
