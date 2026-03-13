import streamlit as st
import grafico, comparativa
import utils as ec
import pandas as pd

@st.cache_data(show_spinner="Calculando telemetría...")
def secante(f,a,b,err):
    cuadro = {
    'a[i]':[],
    'b[i]':[],
    'x[i]':[],
    'f(x[i])':[],
    'Dx[i]':[]
    }
    fa = ec.evaluar_f(f,a)
    fb = ec.evaluar_f(f,b)

    # Casos base
    if fa * fb > 0:
        return None, []
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    """for _ in range(1, max_i+1):
        x = b - (fb * (b-a))/(fb - fa)
        fx = ec.evaluar_f(f,x)"""
    valor_anterior= a
    while True :
        
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ec.evaluar_f(f, x)

        if round(x,6) == round(valor_anterior,6):
            break
        
        cuadro['a[i]'].append(f'{a:.6f}')
        cuadro['b[i]'].append(f'{b:.6f}')
        cuadro['x[i]'].append(f'{x:.6f}')
        cuadro['f(x[i])'].append(f'{fx:.6f}')
        cuadro['Dx[i]'].append(f'{x-a:.6f}')

        if abs(fx) < err: 
            return x, cuadro
        valor_anterior= x
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    return x, cuadro

def mostrar_info():

    # Botón para volver al menú principal
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.pagina_actual = "Inicio"
        st.rerun() # Esto fuerza a la página a recargarse instantáneamente

    st.header('Metodo Secante')
    
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
    
    st.latex(ec.mostrar_formula(formula))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
    with col2:
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
    with col3:
        err = st.number_input('Exponente de tolerancia de error',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        # Asumo que tu función se llama secante() adentro de secante.py
        raiz, datos = secante(formula, inf, sup, err) 

        if raiz is not None:
            opciones_comp = ["Bisección", "Newton"]
            seleccion = st.pills(
                label="Comparar con:", 
                options=opciones_comp, 
                key="pills_sec", 
                selection_mode='single'
            )
            
            mostrar_datos = st.checkbox("Mostrar datos de iteraciones")

            if seleccion == "Newton":
                st.info("Para comparar con Newton, necesitamos un valor inicial $x_n$:")
                x_n_comp = st.number_input('Ingresar valor inicial $x_n$', value=sup, step=1.0)
                comparativa.comparar_generico("Secante", "Newton", formula, err, mostrar_datos, inf=inf, sup=sup, x_n=x_n_comp)
                
            elif seleccion == "Bisección":
                comparativa.comparar_generico("Secante", "Bisección", formula, err, mostrar_datos, inf=inf, sup=sup)
                
            else:
                st.success(f'Raíz encontrada en: $$x \\approx {round(raiz,6)}$$')
                grafico.dibujar(formula, raiz, inf, sup, key="graf_unico_sec", iteraciones=datos if mostrar_datos else None)
                
                if mostrar_datos:
                    st.dataframe(pd.DataFrame(datos), use_container_width=True)          
        else:
            st.error('No se ha encontrado la raíz.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def secante(f,a,b,err,max_i):
    fa = f(a)
    fb = f(b)
    # Casos base
    if f(a) * f(b) > 0:
        return None
    if a  > b:
        a, b = b, a
    # Calculo de la raíz
    while True :
        valor_anterior= b
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ec.evaluar_f(f, x)

        if round(x,6) == round(valor_anterior,6):
            break''',
            "python")