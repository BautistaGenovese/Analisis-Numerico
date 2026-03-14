import streamlit as st
import utils as ec
import pandas as pd
import grafico, comparativa

@st.cache_data(show_spinner="Calculando telemetría...")
def biseccion(f,a,b,err):
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
    x_anterior = a
    i=0
    while i < 100:
        x = round((a+b)/2,6)
        fx = ec.evaluar_f(f,x)

        cuadro['a[i]'].append(f'{a:.6f}')
        cuadro['b[i]'].append(f'{b:.6f}')
        cuadro['x[i]'].append(f'{x:.6f}')
        cuadro['f(x[i])'].append(f'{fx:.6f}')
        cuadro['Dx[i]'].append(f'{x-a:.6f}')

        if abs(fx) < err: 
            return x, cuadro
        if round(x,6) == round(x_anterior,6):
            break
        
        x_anterior = x
        
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
        i+=1

    return x, cuadro

def mostrar_info():
    st.header('Metodo Bisección')
    # Dividimos la pantalla: 1 parte para inputs, 2 partes para gráficos
    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        
        formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
        st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $e^{1-x}$.")
        st.latex(ec.mostrar_formula(formula))

        c1, c2 = st.columns(2)
        with c1:
            inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
        with c2:
            sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
        
        err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
        
        # Realizamos el cálculo aquí para saber si habilitar las opciones
        try:
            raiz, datos = biseccion(formula, inf, sup, err)
            if raiz is not None:
                # Usamos un Toggle (interruptor) para prender/apagar los puntos
                mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico")
                seleccion = st.pills(
                    label="Comparar con:", 
                    options=["Newton", "Secante"], 
                    key="pills_bis", 
                    selection_mode='single'
                )
                
                if seleccion == "Newton":
                    st.info("Para comparar con Newton, necesitamos un valor inicial $x_n$:")
                    x_n_comp = st.number_input('Ingresar valor inicial $x_n$', value=(inf+sup)/2, step=1.0)
                    
        except Exception as e:
            raiz = None
            st.error(f'Error en la fórmula: {e}')
            st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

    # --- ZONA DE GRÁFICOS Y RESULTADOS ---
    with col_out:
        # Verifica si existe la raíz antes de mostrar opciones adicionales
        if 'raiz' in locals() and raiz is not None:
            
            if seleccion == "Newton":
                comparativa.comparar_generico("Bisección", "Newton", formula, err, mostrar_datos, inf=inf, sup=sup, x_n=x_n_comp)
            elif seleccion == "Secante":
                comparativa.comparar_generico("Bisección", "Secante", formula, err, mostrar_datos, inf=inf, sup=sup)
            else:
                st.space('small')
                st.success(f'Raíz encontrada en: $x \\approx {round(raiz,6)}$')
                
                # Gráfico
                grafico.dibujar(formula, raiz, inf, sup, key="graf_unico_bis", iteraciones=datos if mostrar_datos else None)
                
                # Expander para la tabla
                with st.expander("Ver tabla de iteraciones"):
                    st.dataframe(pd.DataFrame(datos), use_container_width=True)
        else:
            if 'raiz' in locals():
                st.error('No se ha encontrado la raíz o no hay cambio de signo en el intervalo.')

    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def biseccion(f,a,b,err,max_i):
    fa = f(a)
    fb = f(b)
    # Casos base
    if f(a) * f(b) > 0:
        return None
    if a  > b:
        a, b = b, a
    # Calculo de la raíz
    for i in range(1, max_i+1):
        x = (a+b)/2
        fx = f(x)
        if abs(fx) < err or max_i<=0: 
            return x
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return x''',
            "python")