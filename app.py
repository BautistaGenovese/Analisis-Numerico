import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import inicio, biseccion, secante, newton, punto_fijo, regresion

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    layout='wide' # <--- ESTO EXPANDE LA APP A TODA LA PANTALLA
)

# --- CÓDIGO PARA OCULTAR LA BARRA SUPERIOR Y EL FOOTER ---
ocultar_menu_estilo = """
    <style>
    /* Oculta la barra superior */
    header {visibility: hidden;}
    
    /* Oculta el pie de página predeterminado de Streamlit (opcional) */
    footer {visibility: hidden;}
    
    /* Reduce el espacio en blanco que queda arriba */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    </style>
"""
st.markdown(ocultar_menu_estilo, unsafe_allow_html=True)
# ---------------------------------------------------------

mostrar_tp = False

def main():

    col1, col2 = st.columns(2)
    with col1:
        st.title('App Análisis Numérico 📊')
    with col2:
        choice = st.pills(
            "Selecciona el módulo:",
            options=["Inicio", "Bisección","Secante","Newton","Punto Fijo","Regresión"],
            default="Inicio",
            selection_mode='single'
        )
    if choice == 'Inicio' or choice is None:
        inicio.inicio()
    else:
        if st.checkbox("Mostrar Consigna del TP"):
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")

        st.divider()  # Línea divisoria para separar la selección del contenido

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
