import streamlit as st
from core import algoritmos, grafico, utils as ut


def mostrar_info():
    st.markdown("<h1 style='text-align: center;'>Método de Punto Fijo</h1>", unsafe_allow_html=True)
    
    with st.expander("📖 ¿Cómo funciona el método de Punto Fijo?"):
        st.markdown("""
        **Concepto básico:** Este método transforma la ecuación original de búsqueda de raíces $f(x) = 0$ en una ecuación equivalente de la forma $x = g(x)$. Se toma un valor inicial, se evalúa en $g(x)$, y el resultado se convierte en la entrada para la siguiente iteración. Visualmente, buscamos el punto donde la curva $g(x)$ se cruza con la recta $y = x$.
        
        **Fórmula de iteración:**
        """)
        st.latex(r"x_{i+1} = g(x_i)")
        
        st.markdown("""
        **Intervalos permitidos y Condiciones:**
        * Requiere **un valor inicial** $x_0$.
        * Debes ser capaz de despejar una $x$ de tu función original $f(x)$ para crear $g(x)$.
        """)
        st.info(r"💡 **Criterio de Convergencia:** Para que el método no diverja hacia el infinito, la curva de $g(x)$ debe ser 'suave' cerca de la raíz. Matemáticamente, el valor absoluto de su derivada debe ser menor a 1: $|g'(x)| < 1$.")
    
    with st.container(border=True):
        
        # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
        col_in, col_out = st.columns([1, 2], gap="large")

        with col_in:
            st.subheader("📥 Ingreso de datos")
            
            modo = st.radio(
                "¿Cómo deseas ingresar la función?",
                ["Ingresar g(x) despejada (Recomendado)", "Generar g(x) automáticamente a partir de f(x)"],
                help="El método automático usa la transformación trivial g(x) = x - f(x), pero suele divergir con facilidad."
            )
            
            if modo == "Ingresar g(x) despejada (Recomendado)":
                formula_g = st.text_input('Escribe tu función despejada $g(x)$:', value='(x + 2)**(0.5)')
                st.latex('g(x)' + ut.mostrar_formula(formula_g)[4:])
            else:
                
                formula_f = st.text_input('Escribe tu función original $f(x)$:', value='x**2 - x - 2')
                st.caption("Transformación aplicada: $g(x) = x - f(x)$")
                st.latex(ut.mostrar_formula(formula_f))
                
                # Generamos automáticamente el string de la nueva función g(x)
                formula_g = f"x - ({formula_f})"
                st.latex(f"g(x) = x - ({ut.mostrar_formula(formula_f)[7:]})") # Mostramos cómo quedó

            st.divider()
            
            x_inicial = st.number_input('Ingresar punto de inicio $$(x_0)$$', value=1.0, step=0.5)

            err_exp = st.select_slider(
                    "Presición",
                    options=[1,2,3,4,5,6,7,8,9,10],
                    value=2,
                    format_func=lambda x: f"$10^{{{-int(x)}}}$"
                )
            err = 10**(-err_exp)
            
            st.divider()
            
            try:
                raiz, datos = algoritmos.punto_fijo(formula_g, x_inicial, err)
                
                if raiz is not None:
                    
                    inf_grafico = raiz - 5
                    sup_grafico = raiz + 5
                    
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                
                    grafico_func = grafico.obtener_grafico(
                        f=formula_g, 
                        raiz=raiz, 
                        inf=inf_grafico,
                        sup=sup_grafico,
                        key='graf Punto Fijo', 
                        iteraciones=datos.obtener_datos() if mostrar_datos else None
                    )
                    
                    ut.boton_descarga(
                        metodo='Bisección',
                        formula=formula_g,
                        parametros=f"Tolerancia: 10^-{err_exp}",
                        raiz=raiz,
                        datos=datos.obtener_datos(),
                        fig=grafico_func
                    )
                        
            except Exception as e:
                st.error(f'Error al procesar la fórmula: {e}')

        with col_out:
            st.space('small')
            if 'raiz' in locals() and raiz is not None:
                ut.mostrar_panel_resultados(raiz,datos.obtener_datos(),grafico_func)
            else:
                st.error('Ocurrió un error matemático durante el cálculo (probablemente la función divergió hacia el infinito o hay raíces complejas).')

    st.divider()
    st.header('Lógica en Python (Punto Fijo)')
    st.code('''
def punto_fijo (x0, err):
    
    x_actual=x0
    iteracion=0
    while iteracion < 100:
        try:
            x_nuevo = g(x_actual)
            # |x_(i+1) - x_i|
            error_abs = abs(x_nuevo - x_actual)

            # Sale si el error absoluto es demasiado grande
            if error_abs > 1e6:
                return x_nuevo
            
            # |x_(i+1) - x_i| <= ε
            if error_abs <= err:
                return x_nuevo
            
            x_actual = x_nuevo
            
        except Exception:
            return None
        iteracion+=1  
                 
    return x_actual
    ''', "python") 
        
