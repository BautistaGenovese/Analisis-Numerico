import streamlit as st
import grafico, comparativa
import utils as ec
import pandas as pd

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
        
        cuadro['a[i]'].append(a)
        cuadro['b[i]'].append(b)
        cuadro['x[i]'].append(x)
        cuadro['f(x[i])'].append(fx)
        cuadro['Dx[i]'].append(x-a)

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
        raiz, datos = secante(formula,inf,sup,err)
        
        if raiz is not None:
            comparar = st.checkbox("Comparar con Bisección")
            
            if comparar:
                comparativa.comparar_sec_bis(formula,inf,sup,err)
            else:
                st.success(f'Raíz encontrada en: $$x ≈ {round(raiz,6)}$$')

                grafico.dibujar(formula, raiz, inf, sup,key="grafico_unico")
                    
                mostrar_datos = st.checkbox("Mostrar datos de iteraciones")
                
                if mostrar_datos:
                    st.dataframe(pd.DataFrame(datos))
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