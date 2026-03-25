import numpy as np
import re, io
from fpdf import FPDF
import streamlit as st
from core import grafico

def evaluar_f(formula,x=0):
    formula_python = formula.replace('^','**')
    
    formula_python = re.sub(r'(\d)x',r'\1*x',formula_python)

    return eval(formula_python, {
        'x':x,
        'np':np,
        'sin':np.sin,
        'sen':np.sin,
        'cos':np.cos,
        'exp':np.exp,
        'log':np.log,
        'e': np.e,
        'pi': np.pi
    })

def mostrar_formula(formula):
    f = formula.replace('**','^').replace('sen','sin')

    f = re.sub(r'\((.*?)\)/\(?([a-zA-Z0-9.x\s\+\-\*]+)\)?', r'\\frac{\1}{\2}', f)

    f = re.sub(r'\^\((.*?)\)', r'^{\1}', f)
    
    f = re.sub(r'(\d)x',r'\1*x',f)

    funciones = r'(sin|cos|exp|log|pi)'
    
    f = re.sub(funciones, r'\\\1', f)

    f = f.replace('*', r' \cdot ')

    return f'f(x) = {f}'

def generar_pdf_reporte(metodo, formula, parametros, raiz, historial_dict, fig):
    pdf = FPDF()
    pdf.add_page()
    
    # --- 1. TEXTOS Y TÍTULOS (Lo que ya tenías) ---
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Reporte de Análisis Numérico - Rooty", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, f"Método de {metodo}: f(x) = {formula}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Parámetros: {parametros}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(39, 174, 96) 
    pdf.cell(0, 10, f"Raíz: x = {raiz:.6f}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0) 
    pdf.ln(5)

    # --- 2. LA MAGIA DE KALEIDO (LA FOTO) ---
    if fig is not None:
        # A. Le decimos a Plotly que escupa los bytes de la imagen (scale=2 mejora la calidad)
        img_bytes = fig.to_image(format="png", width=800, height=400, scale=2)
        
        # B. Metemos esos bytes en un "tupperware" virtual para engañar a FPDF
        imagen_virtual = io.BytesIO(img_bytes)
        
        # C. Estampamos la imagen en el PDF. w=190 ocupa todo el ancho de la hoja A4
        pdf.image(imagen_virtual, w=190)
        pdf.ln(5) # Dejamos un margencito abajo de la foto

    # --- 3. LA TABLA DE ITERACIONES ---
    if historial_dict:
        columnas = list(historial_dict.keys())
        num_cols = len(columnas)
        ancho_col = 190 / num_cols if num_cols > 0 else 190
        
        pdf.set_font("helvetica", "B", 10)
        for col in columnas:
            pdf.cell(ancho_col, 8, str(col), border=1, align="C")
        pdf.ln()

        pdf.set_font("helvetica", "", 9)
        num_filas = len(historial_dict[columnas[0]])
        for i in range(num_filas):
            for col in columnas:
                valor = historial_dict[col][i]
                texto = f"{valor:.6f}" if isinstance(valor, float) else str(valor)
                pdf.cell(ancho_col, 8, texto, border=1, align="C")
            pdf.ln()

    # --- 4. EL RETORNO SEGURO ---
    # Usamos bytes() para que Streamlit no llore con el bytearray
    return bytes(pdf.output())

def boton_descarga(metodo, formula, parametros, raiz, datos, fig):
    if st.button('Generar reporte en PDF',key='generar_repo',type='secondary', icon='📝'):
        # Generamos el PDF en crudo (los bytes)
        with st.spinner('Generando reporte PDF...'):
            pdf_bytes = generar_pdf_reporte(
                metodo=metodo,
                formula=formula,
                parametros=parametros,
                raiz=raiz,
                historial_dict=datos,
                fig=fig
            )
        st.download_button(
            label="Descargar Reporte en PDF",
            data=pdf_bytes,
            file_name=f"Reporte_{metodo}_{raiz:.4f}.pdf",
            mime="application/pdf",
            type="primary", # Lo pinta del color principal de tu app
            icon="📄"
        )

def mostrar_panel_resultados(raiz, datos, grafico_f, converge=True):       
    st.space('small')
    if converge:
        st.success(f'Raíz encontrada en: $x \\approx {raiz:.6f}$')
        # Gráfico
        with st.spinner(text='Generando grafica...'):
            grafico.dibujar(grafico_f)
        
        # Expander para la tabla
        with st.expander("Ver tabla de iteraciones"):
            st.table(datos)
    else:
        st.error('El método DIVERGIÓ o no alcanzó la tolerancia requerida.')
        st.warning(f'Último valor calculado: $x \\approx {raiz:.6f}$')
