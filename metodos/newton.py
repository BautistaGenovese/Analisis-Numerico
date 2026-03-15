import streamlit as st
import sympy as sp
import pandas as pd
from core import grafico, comparativa, utils as ec

def newton(x_n,f,err):
   # Creamos el diccionario para guardar las iteraciones
    cuadro = {
        'x[i]': [],
        'f(x[i])': [],
        "f'(x[i])": [],
        'x[i+1]': []
    }
    
    while True:
        fa = ec.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ec.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, cuadro
            
        x_n1 = round(x_n - fa / d_evaluada, 6)

        # Guardamos los datos de esta vuelta en el cuadro
        cuadro['x[i]'].append(x_n)
        cuadro['f(x[i])'].append(fa)
        cuadro["f'(x[i])"].append(d_evaluada)
        cuadro['x[i+1]'].append(x_n1)

        # Condición de corte
        if abs(ec.evaluar_f(f, x_n1)) <= err:
            return x_n1, cuadro
        
        # Condición de corte por si se estanca
        if x_n == x_n1:
            return x_n1, cuadro
        
        x_n = x_n1

def mostrar_info():

    st.header('Metodo de Newton')

    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")

    st.latex(ec.mostrar_formula(formula))

    col1, col2 = st.columns(2)
    with col1:
        x_n = st.number_input('Ingresar valor inicial $x_n$',value=-10.0,step=2.0)
    with col2:
        err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    
        
    try:
        raiz, datos = newton(x_n, formula, err)

        if raiz is not None:
            # 1. Pastillitas de selección única para comparar
            opciones_comp = ["Bisección", "Secante"]
            seleccion = st.pills(
                label="Comparar con:", 
                options=opciones_comp, 
                key="pills_newton", 
                selection_mode='single' # ¡Solo deja elegir uno a la vez!
            )
            
            # 2. El checkbox de los datos bien separadito abajo
            mostrar_datos = st.checkbox("Mostrar datos de iteraciones")

            # 3. Lógica de comparación
            if seleccion: # Si eligió alguna de las opciones
                st.info(f"Para comparar con {seleccion}, necesitamos un intervalo inicial:")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    inf = st.number_input('Ingresar intervalo inferior', value=x_n - 5.0, step=1.0)
                with col_c2:
                    sup = st.number_input('Ingresar intervalo superior', value=x_n + 5.0, step=1.0)

                comparativa.comparar_generico("Newton", seleccion, formula, err, mostrar_datos, x_n=x_n, inf=inf, sup=sup)

            else: # Si no eligió nada, muestra solo Newton
                st.success(f'Raíz encontrada en: $$x \\approx {round(raiz,6)}$$')
                inf_grafico = raiz - 5
                sup_grafico = raiz + 5
                grafico.dibujar(formula, raiz, inf_grafico, sup_grafico, key="graf_unico_newton", iteraciones=datos if mostrar_datos else None)
                
                if mostrar_datos:
                    st.dataframe(pd.DataFrame(datos), use_container_width=True)          
        else:
            st.error('No se ha encontrado la raíz o la derivada se hizo cero.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')


    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def newton(x_n,f,err):
    
    while True:
        fa = ec.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ec.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, cuadro
            
        x_n1 = round(x_n - fa / d_evaluada, 6)

        # Condición de corte
        if abs(ec.evaluar_f(f, x_n1)) <= err:
            return x_n1, cuadro
        
        # Condición de corte por si se estanca
        if x_n == x_n1:
            return x_n1, cuadro
        
        x_n = x_n1''',
            "python")
