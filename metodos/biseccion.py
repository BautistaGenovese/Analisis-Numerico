import streamlit as st
from core import algoritmos, grafico, utils as ut

def mostrar_info():
    st.markdown("""
    <h1 style='text-align: center;
    background: linear-gradient(90deg, #36d1dc, #5b86e5);
    -webkit-background-clip: text;
    color: transparent;'>
    🔍 Método de Bisección
    </h1>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 ¿Cómo funciona el método de Bisección?"):
            st.markdown("""
            **Concepto básico:** Es un método de búsqueda cerrada que se basa en el **Teorema del Valor Intermedio**. Consiste en dividir repetidamente a la mitad un intervalo conocido que contiene la raíz, acercándose paso a paso al valor exacto.
            
            **Fórmula de iteración (Punto medio):**
            """)
            st.latex(r"x_i = \frac{a + b}{2}")
            
            st.markdown("""
            **Intervalos permitidos y Condiciones:**
            * Se requiere un intervalo inicial cerrado $[a, b]$.
            * La función $f(x)$ debe ser continua en dicho intervalo.
            """)
            st.info(r"💡 **Condición de Cambio de Signo:** Obligatoriamente, la función debe cambiar de signo en los extremos del intervalo, es decir: $f(a) \cdot f(b) < 0$.")
       
    with st.container(border=True):
        
        # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
        col_in, col_out = st.columns([1, 2], gap="large")

        with col_in:
            st.subheader("📥 Ingreso de datos")

            formula = st.text_input('Función f(x):', value='x**2 + 11*x - 6')
            st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
            
            st.latex(ut.mostrar_formula(formula))

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                inf = st.number_input('Valor inicial a', value=-10.0)

            with col2:
                sup = st.number_input('Valor final b', value=10.0)


            err_exp = st.select_slider(
                    "Presición",
                    options=[1,2,3,4,5,6,7,8,9,10],
                    value=2,
                    format_func=lambda x: f"$10^{{{-int(x)}}}$"
                )
            err = 10**(-err_exp)
            
            st.divider()
            
            # Realizamos el cálculo aquí para saber si habilitar las opciones
            try:
                raiz, datos = algoritmos.biseccion(formula, inf, sup, err)
                if raiz is not None:
                    # Usamos un Toggle (interruptor) para prender/apagar los puntos
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                    
                    grafico_f = grafico.obtener_grafico(formula, raiz, inf, sup, key="graf_bis", iteraciones=datos.obtener_datos() if mostrar_datos else None)
                    
                    ut.boton_descarga(
                        metodo='Bisección',
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
def biseccion(a,b,err):
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
    
        x = (a + b) / 2
        fx = f(x)
        
        # Frena cuando el resultado es demasiado cercano al cero
        if abs(fx) < 1e-12: 
            return x, datos
            
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