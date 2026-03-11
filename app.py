import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import inicio, biseccion, secante

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    )
mostrar_tp = False

def main():

    st.title('App Análisis Numérico 📊')

    choice = st.segmented_control(
        "Selecciona el módulo:",
        options=["Inicio", "Bisección","Secante"],
        default="Inicio",
        selection_mode='single'
    )

    if choice == 'Bisección':
        mostrar_tp = st.checkbox("Mostrar Consigna del TP")
        if mostrar_tp:
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
        biseccion.mostrar_info()
    elif choice == 'Secante':
        mostrar_tp = st.checkbox("Mostrar Consigna del TP")
        if mostrar_tp:
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
        secante.mostrar_info()
    else:
        inicio.inicio()

if __name__ == '__main__':
    main()
