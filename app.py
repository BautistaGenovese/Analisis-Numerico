import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import inicio, biseccion, secante, newton, punto_fijo, regresion

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    )

mostrar_tp = False

def main():

    st.title('App Análisis Numérico 📊')

    choice = st.segmented_control(
        "Selecciona el módulo:",
        options=["Inicio", "Bisección","Secante","Punto Fijo","Newton","Regresión"],
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
    elif choice == 'Punto Fijo':
        mostrar_tp = st.checkbox("Mostrar Consigna del TP")
        if mostrar_tp:
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
        punto_fijo.mostrar_info()
    elif choice == 'Newton':
        mostrar_tp = st.checkbox("Mostrar Consigna del TP")
        if mostrar_tp:
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
        newton.mostrar_info()
    elif choice == 'Regresión':
        mostrar_tp = st.checkbox("Mostrar Consigna del TP")
        if mostrar_tp:
            st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
        regresion.mostrar_info()
    
    else:
        inicio.inicio()
    
    # if "pagina_actual" not in st.session_state:
    #     st.session_state.pagina_actual = "Inicio"

    # if st.session_state.pagina_actual == "Inicio":
    #     inicio.inicio()

    # elif st.session_state.pagina_actual == "Bisección":
    # # Acá llamas a la función real que arma tu archivo biseccion.py
    #     biseccion.mostrar_info()

    # elif st.session_state.pagina_actual == "Secante":
    # # Acá llamas a la función real que arma tu archivo secante.py
    #     secante.mostrar_info()

    # elif st.session_state.pagina_actual == "Newton":
    # # Cambiá "mostrar_newton()" por el nombre real de tu función
    #     newton.mostrar_info()
    # elif st.session_state.pagina_actual == "Punto Fijo":
    # # Cambiá "mostrar_newton()" por el nombre real de tu función
    #     punto_fijo.mostrar_info()
if __name__ == '__main__':
    main()
