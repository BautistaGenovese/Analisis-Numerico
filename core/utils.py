import math
import numpy as np
import re, io
from fpdf import FPDF
import streamlit as st
from core import grafico

def evaluar_f(formula, x=0):
    formula_python = formula.replace('^', '**').replace(',', '.')
    formula_python = re.sub(r'(\d)x', r'\1*x', formula_python)

    # 1. TRUNCAMIENTO DE LA ENTRADA (Si está activado)
    if st.session_state.get('simular_truncamiento', False):
        decs = st.session_state.get('decimales_trunc', 4)
        x = round(float(x), decs)

    # 2. MODO TRIGONOMETRÍA (Radianes o Grados)
    if st.session_state.get('trig_mode', 'Radianes') == 'Grados':
        # Si está en grados, convertimos el valor a radianes antes de pasárselo a Numpy
        sin_func = lambda val: np.sin(np.radians(val))
        cos_func = lambda val: np.cos(np.radians(val))
        tan_func = lambda val: np.tan(np.radians(val))
    else:
        sin_func = np.sin
        cos_func = np.cos
        tan_func = np.tan

    entorno_seguro = {
        'x': x, 'np': np,
        'sin': sin_func, 'sen': sin_func, 'cos': cos_func, 'tan': tan_func,
        'exp': np.exp, 'log': np.log, 'e': np.e, 'pi': np.pi, 'π': np.pi
    }

    try:
        resultado = eval(formula_python, entorno_seguro)
        
        # 3. TRUNCAMIENTO DE LA SALIDA (Si está activado)
        if st.session_state.get('simular_truncamiento', False):
            resultado = round(float(resultado), decs)
            
        return resultado
        
    except SyntaxError:
        raise ValueError("Error de sintaxis. Verifica que la fórmula esté completa.")
    except NameError as e:
        var = str(e).split("'")[1] if "'" in str(e) else str(e)
        raise ValueError(f"Término no reconocido: '{var}'. Usa solo la 'x'.")
    except ZeroDivisionError:
        raise ValueError("División por cero detectada.")
    except Exception as e:
        raise ValueError(f"Error matemático: {e}")

def mostrar_formula(formula):
    f = formula.replace('**','^').replace('sen','sin').replace('.', ',')

    f = re.sub(r'\((.*?)\)/\(?([a-zA-Z0-9.x\s\+\-\*]+)\)?', r'\\frac{\1}{\2}', f)

    f = re.sub(r'\^\((.*?)\)', r'^{\1}', f)
    
    f = re.sub(r'(\d)x',r'\1*x',f)

    funciones = r'(sin|cos|exp|log|pi)'
    
    f = re.sub(funciones, r'\\\1', f)

    f = f.replace('*', r' \cdot ')

    return f'f(x) = {f}'

def calcular_error(actual, anterior):
    """Calcula el error según la preferencia del usuario en st.session_state"""
    tipo = st.session_state.get('tipo_error', 'Absoluto')
    
    # Prevenir división por cero en errores relativos
    if actual == 0 and tipo != "Absoluto":
        return abs(actual - anterior) 
        
    if tipo == "Absoluto":
        return abs(actual - anterior)
    elif tipo == "Relativo":
        return abs((actual - anterior) / actual)
    elif tipo == "Porcentual":
        return abs((actual - anterior) / actual) * 100
    
    return abs(actual - anterior) # Fallback por las dudas

def restablecer_ajustes():
    st.session_state.trig_mode = 'Radianes'
    st.session_state.tipo_error = 'Absoluto'
    st.session_state.max_iters = 100
    st.session_state.cero_maquina = 1e-12
    st.session_state.limite_infinito = 1e6
    st.session_state.simular_truncamiento = False
    st.session_state.mostrar_pdf = False
    if 'decimales_trunc' in st.session_state:
        st.session_state.decimales_trunc = 4

def mostrar_menu_ajustes():
    """Renderiza el menú flotante de configuraciones globales"""
    
    # Inicializamos valores por defecto la primera vez que se abre la app
    defaults = {
        'trig_mode': 'Radianes', 'tipo_error': 'Absoluto', 
        'max_iters': 100, 'cero_maquina': 1e-12, 'limite_infinito': 1e6, 
        'simular_truncamiento': False, 'mostrar_pdf': False
    }
    for llave, valor in defaults.items():
        if llave not in st.session_state:
            st.session_state[llave] = valor

    with st.popover("⚙️", width='stretch'):
        st.markdown("### 🛠️ Configuración Global")

        st.divider()
        st.write("**🧮 Motor Matemático**")
        
        # 3. MAGIA DE STREAMLIT: Usamos 'key' en vez del signo '='
        st.radio("Trigonometría", ["Radianes", "Grados"], horizontal=True, key="trig_mode",help="Define cómo se evalúan las funciones como sin(x) o cos(x). En el ámbito académico y en la programación, el estándar matemático es usar Radianes.")
        st.selectbox("Criterio de Parada (Error)", ["Absoluto", "Relativo", "Porcentual"], key="tipo_error",help="Define la fórmula para calcular el error. El 'Absoluto' mide la distancia directa entre iteraciones. El 'Relativo' y 'Porcentual' escalan esa diferencia según el tamaño de la raíz, ideal para números muy gigantes o microscópicos.")
        
        st.divider()
        st.write("**🛑 Límites y Tolerancias**")
        st.number_input("Límite de Iteraciones", min_value=10, max_value=1000, step=10, key="max_iters", help="El freno de emergencia. Si un método (como Punto Fijo) queda atrapado en un bucle infinito porque no converge, el programa abortará al alcanzar esta cantidad de pasos.")
        
        st.select_slider(
            "Tolerancia de 'Cero Exacto'",
            options=[1e-6, 1e-9, 1e-12, 1e-15],
            format_func=lambda x: f"$10^{{{int(math.log10(x))}}}$",
            key="cero_maquina",
            help="Define qué tan cerca del cero debe estar f(x) para considerarlo un éxito. Si la función arroja un número menor a este valor microscópico, el programa asume que tocó el eje X."
        )
        
        st.select_slider(
            "Umbral de Divergencia",
            options=[1e6, 1e15, 1e50, 1e100],
            format_func=lambda x: f"$10^{{{int(math.log10(x))}}}$",
            key="limite_infinito",
            help="El límite de explosión para los métodos abiertos. Si en algún paso la variable x supera este número gigantesco, el programa asume que el método se descontroló hacia el infinito y aborta para evitar un error de desbordamiento (Overflow)."
        )
        
        st.divider()
        st.write("**🧪 Simulación Avanzada**")
        # El toggle también usa key
        st.toggle("Simular Aritmética Finita", key="simular_truncamiento", help="Activa el 'Modo Calculadora Antigua'. En lugar de usar la precisión total de la computadora, recorta artificialmente los decimales en cada paso para demostrar cómo el error de propagación arruina los cálculos.")
        
        if st.session_state.simular_truncamiento:
            # Inicializamos su valor si no existe
            if 'decimales_trunc' not in st.session_state:
                st.session_state.decimales_trunc = 4
            st.slider("Cifras decimales a retener", 2, 8, key="decimales_trunc",help="Cantidad de decimales que sobrevivirán en cada operación matemática. Bajalo a 2 o 3 para forzar a que métodos precisos como Newton fallen miserablemente.")
            
        st.divider()
        st.write("**📄 Documentación**")
        st.toggle("Mostrar consigna del TP", key="mostrar_pdf")
        
        st.divider()
        st.button("🧹 Limpiar Caché", width='stretch', on_click=st.cache_data.clear)
            
        st.button("♻️ Restablecer Valores", width='stretch', on_click=restablecer_ajustes)     

@st.cache_data(show_spinner=False)
def generar_pdf_reporte(metodo, formula, parametros, raiz, historial_dict, fig):
    pdf = FPDF()
    pdf.add_page()
    
    # --- 1. TÍTULO Y FUENTE ESTÉTICA ---
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(30, 136, 229) # Azul Rooty
    pdf.cell(0, 10, "Reporte de Análisis Numérico - Rooty", new_x="LMARGIN", new_y="NEXT", align="C")
    
    # Línea separadora
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(8)

    # --- 2. DATOS DEL PROBLEMA ---
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(60, 60, 60) 
    pdf.cell(0, 8, f"Método de {metodo}: f(x) = {formula}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Parámetros: {parametros}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(39, 174, 96) # Verde éxito
    pdf.cell(0, 10, f"Raíz encontrada: x = {raiz:.6f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # --- 3. EL GRÁFICO ---
    if fig is not None:
        img_bytes = fig.to_image(format="png", width=800, height=400, scale=2)
        imagen_virtual = io.BytesIO(img_bytes)
        pdf.image(imagen_virtual, w=190)
        pdf.ln(8) 

    # --- 4. LA TABLA PREMIUM (CON ÍNDICES) ---
    if historial_dict:
        # Extraemos las columnas originales (ej: 'x[i]')
        columnas_orig = list(historial_dict.keys())
        
        # Limpiamos los nombres para el PDF (Cambia 'x[i]' por 'x_i')
        columnas_limpias = [col.replace("[i]", "_i") for col in columnas_orig]
        
        # Sumamos 1 al número de columnas para hacerle lugar al índice "Iter"
        num_cols = len(columnas_orig) + 1 
        ancho_col = 190 / num_cols 
        
        # Diseño del Encabezado
        pdf.set_fill_color(30, 136, 229)
        pdf.set_text_color(255, 255, 255)
        pdf.set_draw_color(30, 136, 229) 
        pdf.set_font("helvetica", "B", 11)
        
        # Agregamos la primera columna a mano: "Iter"
        pdf.cell(ancho_col, 8, "Iter", border=1, align="C", fill=True)
        # Agregamos el resto de las columnas limpias
        for col_nombre in columnas_limpias:
            pdf.cell(ancho_col, 8, col_nombre, border=1, align="C", fill=True)
        pdf.ln()

        # Diseño de las Filas
        pdf.set_text_color(40, 40, 40) 
        pdf.set_draw_color(220, 220, 220) 
        pdf.set_font("helvetica", "", 10)
        
        num_filas = len(historial_dict[columnas_orig[0]])
        for i in range(num_filas):
            
            # Protección de Salto de Página
            if pdf.get_y() > 270:
                pdf.add_page()
                pdf.set_fill_color(30, 136, 229)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("helvetica", "B", 11)
                pdf.cell(ancho_col, 8, "Iter", border=1, align="C", fill=True)
                for col_nombre in columnas_limpias:
                    pdf.cell(ancho_col, 8, col_nombre, border=1, align="C", fill=True)
                pdf.ln()
                pdf.set_text_color(40, 40, 40)
                pdf.set_font("helvetica", "", 10)

            # Efecto Cebra
            if i % 2 == 0:
                pdf.set_fill_color(248, 248, 248) 
            else:
                pdf.set_fill_color(255, 255, 255) 
                
            # 1. Imprimimos el número de iteración (0, 1, 2...)
            pdf.cell(ancho_col, 8, str(i), border="LR", align="C", fill=True)
            
            # 2. Imprimimos los datos de la fila
            for col_orig in columnas_orig:
                valor = historial_dict[col_orig][i]
                texto = f"{valor:.6f}" if isinstance(valor, float) else str(valor)
                pdf.cell(ancho_col, 8, texto, border="LR", align="C", fill=True)
            pdf.ln()
            
        # Línea final de la tabla
        pdf.cell(ancho_col * num_cols, 0, "", border="T")

    return bytes(pdf.output())

def boton_descarga(metodo, formula, parametros, raiz, datos, fig):
    if st.button('Generar reporte en PDF',key='generar_repo',type='secondary', icon='📝'):
        # Generamos el PDF en crudo (los bytes)
        with st.spinner('Generando reporte PDF...',show_time=True):
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

def mostrar_panel_resultados(raiz, datos, grafico_f):       
    st.space('small')
    st.success(f'Raíz encontrada en: $x \\approx {raiz:.6f}$')
    # Gráfico
    with st.spinner(text='Generando grafica...'):
        grafico.dibujar(grafico_f)
    
    # Expander para la tabla
    with st.expander("Ver tabla de iteraciones"):
        st.dataframe(datos,width='stretch',hide_index=False)

