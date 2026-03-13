import streamlit as st
import utils as ec
import pandas as pd
import grafico, comparativa
import base64
import streamlit.components.v1 as components

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

# Función para convertir imagen a formato web (base64)
def img_to_base64(path):
    import pathlib
    img_bytes = pathlib.Path(path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def mostrar_info():


    # 1. Plantamos una bandera invisible bien arriba
    st.markdown("<span id='banderita-tope'></span>", unsafe_allow_html=True)

    # Ruta exacta de tu imagen (revisá que esté bien)
    ruta_imagen = "animaciones/fondoCalculadoras1.jpg" 
    
    # Definimos la altura del banner a tu gusto (ej: 220 píxeles)
    altura_banner = "220px" 

    try:
        img_base64 = img_to_base64(ruta_imagen)
        
        st.markdown(f"""
            <style>
                    
            /* MAGIA CSS: Ocultamos el encabezado de Streamlit (Deploy y puntitos) */
            [data-testid="stHeader"] {{
                display: none !important;
            }}

            /* Le sacamos el espacio blanco de arriba a la página */
            .block-container {{
                padding-top: 0rem !important;
            }}
            
            /* ... (acá sigue tu código de .notion-banner que ya tenés) ... */

            /* Le sacamos el espacio blanco de arriba a la página */
            .block-container {{
                padding-top: 0rem !important;
            }}

            /* MAGIA CSS: Obligamos solo al banner a romper los márgenes del centro */
            .notion-banner {{
                width: 100vw; /* 100% del ancho de la pantalla (Viewport Width) */
                position: relative;
                left: 50%;
                right: 50%;
                margin-left: -50vw;
                margin-right: -50vw;
                height: 150px; /* La achicamos un poco para que no se vea tan borrosa */
                background-image: url("data:image/png;base64,{img_base64}");
                background-size: cover; 
                background-position: center; /* Mantiene enfocada la parte del medio */
                margin-bottom: 25px;
            }}
            </style>
            
            <div class="notion-banner"></div>

        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"No se encontró la imagen en {ruta_imagen}")
        # Si no hay imagen, resetear márgenes básicos igualmente
        st.markdown("""<style>.block-container {padding-top: 2rem !important;}</style>""", unsafe_allow_html=True)

    # Esto inyecta un código invisible que fuerza a la página a scrollear arriba de todo
    components.html("""
            <script>
                // Esperamos un cachito a que aparezca la bandera
                setTimeout(function() {
                    // Buscamos nuestra bandera exacta por el ID
                    var bandera = window.parent.document.getElementById('banderita-tope');
                    if (bandera) {
                        // Le decimos al navegador que la ponga en la pantalla a la fuerza
                        bandera.scrollIntoView({behavior: 'instant', block: 'start'});
                    }
                }, 200); 
            </script>
        """, height=0)

    # Botón para volver al menú principal
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.pagina_actual = "Inicio"
        st.rerun() # Esto fuerza a la página a recargarse instantáneamente


    st.header('Metodo Bisección')
    
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
    
    st.latex(ec.mostrar_formula(formula))

    col1, col2, col3 = st.columns(3)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
    with col2:
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
    with col3:
        err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        raiz, datos = biseccion(formula,inf,sup,err)

        if raiz is not None:
            opcion = ["Comparar con Secante", "Mostrar datos de iteraciones"]
            seleccion = st.pills(
                label="Selecciona una opción:", 
                options=opcion, 
                key="pills_bis", 
                selection_mode='multi'
                )
            if "Comparar con Secante" in seleccion:
                comparativa.comparar_sec_bis(formula,inf,sup,err, "Mostrar datos de iteraciones" in seleccion)
            else:
                st.success(f'Raíz encontrada en: $$x ≈ {round(raiz,6)}$$')
                    
                grafico.dibujar(formula, raiz, inf, sup,key="grafico_unico", iteraciones=datos if ("Mostrar datos de iteraciones" in seleccion) else None)
                
                if "Mostrar datos de iteraciones" in seleccion:
                    st.dataframe(pd.DataFrame(datos),use_container_width=True)          
        else:
            st.error('No se ha encontrado la raíz.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

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