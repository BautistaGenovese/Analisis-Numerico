import streamlit as st
from core import grafico, comparativa, utils as ut
from core.historial import Historial

@st.cache_data(show_spinner="Calculando telemetría...")
def biseccion(f,a,b,err):
    
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]','Error Absoluto'])
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)

    # Casos base
    if fa * fb >= 0:
        return None, datos
    if a > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    x_anterior=a
    iteracion=0
    while iteracion < 100:
        
        x=(a+b)/2
        fx=ut.evaluar_f(f,x)
        err_abs = abs(b-a)/2
        
        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a),
            'Error Absoluto':err_abs
        })

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
        
        x_anterior=x
        iteracion+=1

    return x, datos

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
            st.latex(ut.mostrar_formula(formula))

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                inf = st.number_input('Valor inicial a', value=-10.0)

            with col2:
                sup = st.number_input('Valor final b', value=10.0)

            st.divider()

            err_exp = st.slider('Precisión (n en 10⁻ⁿ)', 1, 10, 2)
            err = 10**(-err_exp)
            
            
            # Realizamos el cálculo aquí para saber si habilitar las opciones
            try:
                raiz, datos = biseccion(formula, inf, sup, err)
                if raiz is not None:
                    # Usamos un Toggle (interruptor) para prender/apagar los puntos
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                    # seleccion = st.pills(
                    #     label="Comparar con:", 
                    #     options=["Newton", "Secante"], 
                    #     key="pills_bis", 
                    #     selection_mode='single'
                    # )
                    
                    # if seleccion == "Newton":
                    #     st.info("Para comparar con Newton, necesitamos un valor inicial $x_n$:")
                    #     x_n_comp = st.number_input('Ingresar valor inicial $x_n$', value=(inf+sup)/2, step=1.0)
                        
            except Exception as e:
                raiz = None
                st.error(f'Error en la fórmula: {e}')
                st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

        # --- ZONA DE GRÁFICOS Y RESULTADOS ---
        with col_out:
            # Verifica si existe la raíz antes de mostrar opciones adicionales
            if 'raiz' in locals() and raiz is not None:
                
                # if seleccion == "Newton":
                #     comparativa.comparar_generico("Bisección", "Newton", formula, err, mostrar_datos, inf=inf, sup=sup, x_n=x_n_comp)
                # elif seleccion == "Secante":
                #     comparativa.comparar_generico("Bisección", "Secante", formula, err, mostrar_datos, inf=inf, sup=sup)
                # else:
                #     st.space('small')
                #     st.success(f'Raíz encontrada en: $x \\approx {round(raiz,6)}$')
                #     # Gráfico
                #     grafico.dibujar(formula, raiz, inf, sup, key="graf_unico_bis", iteraciones=datos.obtener_datos() if mostrar_datos else None)
                    
                    
                #     # Expander para la tabla
                #     with st.expander("Ver tabla de iteraciones"):
                #         st.table(datos.obtener_dataframe())
                
                st.space('small')
                st.success(f'Raíz encontrada en: $x \\approx {raiz:.6f}$')
                # Gráfico
                grafico.dibujar(formula, raiz, inf, sup, key="graf_unico_bis", iteraciones=datos.obtener_datos() if mostrar_datos else None)
                
                
                # Expander para la tabla
                with st.expander("Ver tabla de iteraciones"):
                    st.table(datos.obtener_dataframe())
                    
                    
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