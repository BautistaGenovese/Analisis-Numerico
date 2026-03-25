import streamlit as st
from core import algoritmos, grafico, utils as ut

def mostrar_info():
    st.markdown("<h1 style='text-align: center;'>Método Secante</h1>", unsafe_allow_html=True)
    
    with st.expander("📖 ¿Cómo funciona el método de la Secante?"):
        st.markdown("""
        **Concepto básico:** Es un método abierto que aproxima la raíz trazando una línea recta (secante) que pasa por dos puntos evaluados en la función. Donde esta línea cruza el eje $X$, se obtiene el nuevo punto para la siguiente iteración. Es una alternativa excelente cuando calcular la derivada es muy complejo.
        
        **Fórmula de iteración:**
        """)
        st.latex(r"x_{i+1} = x_i - f(x_i) \cdot \frac{x_i - x_{i-1}}{f(x_i) - f(x_{i-1})}")
        
        st.markdown("""
        **Intervalos permitidos y Condiciones:**
        * Requiere **dos puntos iniciales** $x_0$ y $x_1$, preferentemente cercanos a la raíz buscada.
        * A diferencia de la bisección, **no es obligatorio** que la raíz esté encerrada entre estos dos puntos, aunque ayuda a la convergencia.
        """)
        st.warning(r"⚠️ **Restricción:** Para evitar la división por cero, las evaluaciones de los puntos no pueden ser iguales: $f(x_i) \neq f(x_{i-1})$.")
    
    with st.container(border=True):
    
        # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
        col_in, col_out = st.columns([1, 2], gap="large")
        with col_in:
            st.subheader("📥 Ingreso de datos")
            formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
            st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
            st.latex(ut.mostrar_formula(formula))
            st.divider()
        
            c1, c2 = st.columns(2)
            with c1:
                inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
            with c2:
                sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
            err_exp = st.slider('Precisión ($n$ en $10^{-n}$)', 1, 10, 2)
            err = 10**(-err_exp)
            st.divider()
            
            try:
                # Asumo que tu función se llama secante() adentro de secante.py
                raiz, datos = algoritmos.secante(formula, inf, sup, err) 
                if raiz is not None:
                    
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")

                    grafico_f = grafico.obtener_grafico(formula, raiz, inf, sup, key="graf_sec", iteraciones=datos.obtener_datos() if mostrar_datos else None
                    )
                    
                    ut.boton_descarga(
                        metodo='Secante',
                        formula=formula,
                        parametros=f"Intervalo [{inf}, {sup}], Tolerancia: 10^-{err_exp}",
                        raiz=raiz,
                        datos=datos.obtener_datos(),
                        fig=grafico_f
                        )
                    
            except Exception as e:
                raiz = None
                st.error(f'Error en la fórmula: {e}')
                st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

        # --- ZONA DE GRÁFICOS Y RESULTADOS ---
        with col_out:
            # Verifica si existe la raíz antes de mostrar opciones adicionales
            if 'raiz' in locals() and raiz is not None:
                ut.mostrar_panel_resultados(raiz=raiz,datos=datos.obtener_datos(),grafico_f=grafico_f)
                
            else:
                if 'raiz' in locals():
                    st.error('No se ha encontrado la raíz o no hay cambio de signo en el intervalo.')


    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def secante(a,b,err):
    fa = f(a)
    fb = f(b)
    
    # Casos base
    if fa * fb >= 0:
        return None
    if a > b:
        a, b = b, a
        fa, fb = fb, fa

    # Calculo de la raíz
    x_anterior = a
    iteracion = 0
    
    while iteracion < 100:
    
        x = b - (fb * (b - a)) / (fb - fa)
        fx = f(x)
        
        # Frena si es que la diferencia entre las derivadas es cercana al cero
        if abs(fb - fa) < 1e-12:
            return None
        
        # Frena cuando el resultado es demasiado cercano al cero
        if abs(fx) < 1e-12: 
            return x
            
        # Cierra el ciclo cuando la diferencia entre cada iteración es minima
        if abs(x - x_anterior) < err:
            break
            
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
            
        x_anterior = x
        iteracion += 1
        
    return x''',
            "python")