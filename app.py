import streamlit as st
import inicio
from metodos import biseccion, secante, newton, punto_fijo, regresion

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    layout='wide'
)

# --- CSS LIGERO (Rendimiento optimizado) ---
estilo_seguro = """
    <style>
    /* Ocultar barra superior por defecto */
    header {visibility: hidden !important;}
    
    /* Espaciado del contenido para que no choque con el footer */
    .block-container {
        padding-top: 2rem !important; 
        padding-bottom: 6rem !important; 
    }

    /* FOOTER OPTIMIZADO (Color sólido, sin blur que cause lag) */
    .mi-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1A1C24; /* Color oscuro sólido */
        color: #888888;
        text-align: center;
        padding: 12px 0;
        font-size: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 999;
    }
    .mi-footer a { color: #1E88E5; text-decoration: none; font-weight: bold; }
    .mi-footer a:hover { text-decoration: underline; }
    </style>

    <div class="mi-footer">
        Desarrollado con ❤️ por el Grupo de Análisis Numérico | 
        <a href="https://github.com/BautistaGenovese/Analisis-Numerico" target="_blank">Ver código en GitHub</a>
    </div>
"""
st.markdown(estilo_seguro, unsafe_allow_html=True)
# -----------------------------------------

def main():
    # ==========================================
    # NAVBAR NATIVA CON RECUADRO
    # ==========================================
    with st.container(border=True): # Esto le da el marco lindo a la navbar
        # vertical_alignment="center" centra el texto con los botones!
        col_logo, col_nav = st.columns([1, 2], vertical_alignment="center") 
        
        with col_logo:
            st.markdown("<h3 style='margin: 0;'>📊 Análisis Numérico</h3>", unsafe_allow_html=True)
            
        with col_nav:
            choice = st.pills(
                "Navegación",
                options=["Inicio", "Bisección", "Secante", "Newton", "Punto Fijo", "Regresión"],
                default="Inicio",
                selection_mode='single',
                label_visibility="collapsed"
            )

    # Espacio separador
    st.write("") 

    # ==========================================
    # CONTENIDO DE LA APP
    # ==========================================
    if choice == 'Inicio' or choice is None:
        inicio.inicio()
    else:
        if st.checkbox("📄 Mostrar Consigna del TP"):
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf") 

        if choice == 'Bisección':
            biseccion.mostrar_info()
        elif choice == 'Secante':
            secante.mostrar_info()
        elif choice == 'Punto Fijo':
            punto_fijo.mostrar_info()
        elif choice == 'Newton':
            newton.mostrar_info()
        elif choice == 'Regresión':
            regresion.mostrar_info()

if __name__ == '__main__':
    main()