import streamlit as st
import base64
import os
import inicio, biseccion

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    )

def mostrar_pdf_estilizado(base64_pdf):
    
    # CSS para que el PDF se vea pro
    pdf_style = """
    <div style="
        border: 1px solid #d1d5db; 
        border-radius: 12px; 
        overflow: hidden;
        margin-bottom: 20px;">
        <iframe src="data:application/pdf;base64,{}" width="100%" height="800" style="border:none;"></iframe>
    </div>
    """.format(base64_pdf)
    
    st.markdown(pdf_style, unsafe_allow_html=True)

def main():

    st.title('App Análisis Numérico 📊')

    choice = st.segmented_control(
        "Selecciona el módulo:",
        options=["Inicio", "Bisección"],
        default="Inicio"
    )
    
    mostrar_tp = st.checkbox("Mostrar Consigna del TP")
    
    ruta_pdf = "archivos/Consigna Tp 1 inf tele.pdf"

    if os.path.exists(ruta_pdf):
        with open(ruta_pdf, "rb") as f:
            # Convertimos el PDF a un formato base64
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        if mostrar_tp:
            mostrar_pdf_estilizado(base64_pdf)
    else:
        st.error(f"⚠️ No se encontró el archivo en: {ruta_pdf}")
        st.info("Asegurate de que la carpeta 'archivos' esté en el mismo lugar que tu app.py")

    if choice == 'Inicio':
        inicio.inicio()
    elif choice == 'Bisección':
        biseccion.mostrar_info()

if __name__ == '__main__':
    main()
