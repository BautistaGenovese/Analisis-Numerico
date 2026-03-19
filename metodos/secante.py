import streamlit as st
from core import grafico, comparativa, utils as ut
from core.historial import Historial

@st.cache_data(show_spinner="Calculando telemetría...")
def secante(f,a,b,err):
    
    datos = Historial(['a[i]','b[i]','x[i]','f(x[i])','Dx[i]'])
    
    fa = ut.evaluar_f(f,a)
    fb = ut.evaluar_f(f,b)

    # Casos base
    if fa * fb > 0:
        return None, datos.obtener_datos()
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    x_anterior=a
    iteracion=0
    while iteracion < 100:
        
        x = b - (fb * (b - a)) / (fb - fa)
        fx = ut.evaluar_f(f, x)

        datos.agregar({
            'a[i]':a,
            'b[i]':b,
            'x[i]':x,
            'f(x[i])':fx,
            'Dx[i]':(x-a)
        })
        
        # Frena si es que la diferencia entre las derivadas es cercana al cero
        if abs(fb - fa) < 1e-12:
            st.warning("División por cero en secante. Los puntos están muy cerca.")
            return None, datos

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
            formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
            st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
            st.latex(ut.mostrar_formula(formula))
        
            c1, c2 = st.columns(2)
            with c1:
                inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
            with c2:
                sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
            
            err = st.number_input('Tolerancia de error: $ε = 10^{-n}$',value=2,min_value=1, max_value=10)
            err = 10**(-err)

            # Realizamos el cálculo aquí para saber si habilitar las opciones    
            try:
                # Asumo que tu función se llama secante() adentro de secante.py
                raiz, datos = secante(formula, inf, sup, err) 
                if raiz is not None:
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")

                    seleccion = st.pills(
                        label="Comparar con:", 
                        options=["Bisección", "Newton"], 
                        key="pills_sec", 
                        selection_mode='single'
                    )

                    if seleccion == "Newton":
                        st.info("Para comparar con Newton, necesitamos un valor inicial $x_n$:")
                        x_n_comp = st.number_input('Ingresar valor inicial $x_n$', value=sup, step=1.0)

            except Exception as e:
                raiz = None
                st.error(f'Error en la fórmula: {e}')
                st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

        # --- ZONA DE GRÁFICOS Y RESULTADOS ---
        with col_out:
            # Verifica si existe la raíz antes de mostrar opciones adicionales
            if 'raiz' in locals() and raiz is not None:

                if seleccion == "Newton":
                    comparativa.comparar_generico("Secante", "Newton", formula, err, mostrar_datos, inf=inf, sup=sup, x_n=x_n_comp)
                    
                elif seleccion == "Bisección":
                    comparativa.comparar_generico("Secante", "Bisección", formula, err, mostrar_datos, inf=inf, sup=sup)
                    
                else:
                    st.space('small')
                    st.success(f'Raíz encontrada en: $$x \\approx {round(raiz,6)}$$')
                    grafico.dibujar(formula, raiz, inf, sup, key="graf_unico_sec", iteraciones=datos.obtener_datos() if mostrar_datos else None)
                    
                    # Expander para la tabla
                    with st.expander("Ver tabla de iteraciones"):
                        st.table(datos.obtener_dataframe())       
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
    if fa * fb > 0:
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