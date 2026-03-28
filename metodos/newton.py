import streamlit as st
from core import algoritmos, grafico, utils as ut



def mostrar_info():
    st.markdown("<h1 style='text-align: center;'>Método Newton</h1>", unsafe_allow_html=True)
    
    with st.expander("📖 ¿Cómo funciona el método de Newton-Raphson?"):
        st.markdown("""
        **Concepto básico:** Es uno de los métodos abiertos más rápidos y eficientes. Comienza en un punto inicial $x_0$ y traza una línea **tangente** a la curva en ese punto (utilizando la derivada). La intersección de esa tangente con el eje X nos da el siguiente punto $x_1$.
        
        **Fórmula de iteración:**
        """)
        st.latex(r"x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}")
        
        st.markdown("""
        **Intervalos permitidos y Condiciones:**
        * Solo requiere **un punto inicial** $x_0$.
        * La función debe ser derivable y debemos conocer su derivada $f'(x)$.
        * El punto inicial debe estar relativamente cerca de la raíz para asegurar que converja.
        """)
        st.warning(r"⚠️ **Restricción:** La derivada evaluada en el punto actual nunca debe ser cero ($f'(x_i) \neq 0$), ya que la línea tangente sería horizontal y nunca cruzaría el eje X.")
    
    with st.container(border=True):
        
        # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
        col_in, col_out = st.columns([1, 2], gap="large")

        with col_in:
            st.subheader("📥 Ingreso de datos")
            formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
            st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
            st.latex(ut.mostrar_formula(formula))
            st.divider()

            x_n = st.number_input('Ingresar valor inicial $(x_n)$',value=-10.0,step=2.0)
            
            err_exp = st.select_slider(
                    "Presición",
                    options=[1,2,3,4,5,6,7,8,9,10],
                    value=2,
                    format_func=lambda x: f"$10^{{{-int(x)}}}$"
                )
            err = 10**(-err_exp)
            
            st.divider()
            try:
                raiz, datos = algoritmos.newton(x_n, formula, err)
                if raiz is not None:
                    
                    inf_grafico = raiz - 5
                    sup_grafico = raiz + 5
                    
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                    
                    grafico_f = grafico.obtener_grafico(formula, raiz, inf_grafico, sup_grafico, key="graf_unico_newton", iteraciones=datos.obtener_datos() if mostrar_datos else None)
                    
                    ut.boton_descarga(
                        metodo='Newton',
                        formula=formula,
                        parametros=f"Tolerancia: 10^-{err_exp}",
                        raiz=raiz,
                        datos=datos.obtener_datos(),
                        fig=grafico_f
                        )
                    
            except Exception as e:
                raiz = None
                st.error(f'Error en la fórmula: {e}')
                st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')
        with col_out:
            # Si no eligió nada, muestra solo Newton
            if 'raiz' in locals() and raiz is not None:
                ut.mostrar_panel_resultados(raiz,datos.obtener_datos(),grafico_f)

            else:
                if 'raiz' in locals():
                    st.error('No se ha encontrado la raíz o no hay cambio de signo en el intervalo.')



    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def newton(x_n,f,err):
    
    # Calculo de la raíz
    iteracion=0
    while True:
        fa = ut.evaluar_f(f, x_n)
        derivada = str(sp.diff(f, 'x'))
        d_evaluada = round(ut.evaluar_f(derivada, x_n), 6)
        
        # Evitamos la división por cero si la derivada da 0
        if d_evaluada == 0:
            return None, datos
            
        x_n1 = x_n - (fa / d_evaluada)

        # Condición de corte
        if abs(ut.evaluar_f(f, x_n1)) <= 1e-12:
            return x_n1, datos
        
        # Condición de corte por si se estanca
        if abs(x_n1 - x_n) <= err:
            return x_n1, datos
        
        x_n=x_n1
        iteracion+=1''',
            "python")
