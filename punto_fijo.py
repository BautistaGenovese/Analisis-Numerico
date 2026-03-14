import streamlit as st
import grafico
import utils as ec
import pandas as pd

@st.cache_data(show_spinner="Calculando iteraciones...")
def punto_fijo (g,x0,max_i=100):
    cuadro={
        'x[i]':[],
        'g(x[i])':[],
        'Error Absoluto': []
    }
    x_actual= x0
    i=0
    while i < max_i:
        try:
            x_nuevo=ec.evaluar_f(g, x_actual)

            error_actual= abs(x_nuevo - x_actual)

            cuadro['x[i]'].append(f'{x_actual:.6f}')
            cuadro['g(x[i])'].append(f'{x_nuevo:.6f}')
            cuadro['Error Absoluto'].append(f'{error_actual:.6f}')

            if round(x_nuevo, 6) == round(x_actual, 6):
                return x_nuevo, cuadro, True
            
            if error_actual > 1e6:
                return x_nuevo, cuadro, False
            
            x_actual = x_nuevo
            
        except Exception as e:
            return None, cuadro, False
        
    return x_actual, cuadro, False

def mostrar_info():
    st.header('Metodo Punto Fijo')
    # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        st.info("""
        Para este método, debes ingresar la función ya despejada $$g(x)$$. 
        Recuerda que estamos buscando la raíz de $f(x) = 0$ resolviendo $x = g(x)$.
        """)
        
        formula_g = st.text_input('Escribe tu función despejada $g(x)$:', value='(x + 2)**(0.5)')
        st.caption("Ejemplo: Si tu $f(x) = x^2 - x - 2 = 0$, una forma de $g(x)$ es `(x + 2)**0.5` o `(x**2 - 2)`.")
        
        st.latex('g(x)'+ec.mostrar_formula(formula_g)[4:])
    
        c1, c2 = st.columns(2)
        with c1:
            x_inicial = st.number_input('Ingresar punto de inicio $$(x_0)$$', value=1.0, step=0.5)
        with c2:
            err_input = st.number_input('Tolerancia de error $E = 10^{-n}$', value=4, min_value=1, max_value=10)
            err = 10**(-err_input)
        
        try:
            raiz, datos, converge = punto_fijo(formula_g, x_inicial, err)
            
            if raiz is not None:
                mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                if not converge:
                    st.error('El método DIVERGIÓ o no alcanzó la tolerancia requerida.')
                    st.warning(f'Último valor calculado: $x = {round(raiz, 6)}$')

        except Exception as e:
            st.error(f'Error al procesar la fórmula: {e}')

    with col_out:
        st.space('small')
        if 'raiz' in locals() and raiz is not None and converge:
            st.success(f'El método CONVERGIÓ. Raíz aproximada: $$x ≈ {round(raiz,6)}$$')
            # Dibujamos el gráfico
            grafico.dibujar(
                f=formula_g, 
                raiz=raiz, 
                inf=raiz-5,
                sup=raiz+5,
                key="grafico_pf", 
                iteraciones=datos if mostrar_datos else None
            )
            # Expander para la tabla
            with st.expander("Ver tabla de iteraciones"):
                st.dataframe(pd.DataFrame(datos), use_container_width=True)
        else:
            st.error('Ocurrió un error matemático durante el cálculo (probablemente la función divergió hacia el infinito o hay raíces complejas).')
                


    st.divider()
    st.header('Lógica en Python (Punto Fijo)')
    st.code('''
def punto_fijo(g, x_actual, tolerancia):
    while True:
        # Evaluamos x en la función g
        x_nuevo = g(x_actual)
        
        # Comparamos los 6 decimales
        if round(x_nuevo, 6) == round(x_actual, 6):
            return x_nuevo
            
        # El resultado se vuelve la nueva entrada
        x_actual = x_nuevo
    ''', "python") 
        
