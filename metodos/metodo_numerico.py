from abc import ABC, abstractmethod
import streamlit as st
from streamlit_extras.skeleton import *
from core import grafico, utils as ut

class MetodoNumerico(ABC):
    
    @property
    @abstractmethod
    def nombre(self):
        """Nombre del método. Ej: 'Bisección'"""
        pass
    
    @property
    @abstractmethod
    def categoria(self):
        """Define si el método es cerrado, abierto, etc."""
        pass
    
    # En la clase base - por defecto el toggle de las iteraciones existe
    @property
    def tiene_toggle(self):
        return True
    
    @abstractmethod
    def ejecutar(self, f, err, **params):
        """
        Corre el algoritmo y devuelve (raiz, datos).
        El parematro **params es como una mochila.
        Los ** le dicen a Python "todo lo que me manden de más, metelo en un diccionario llamado params"
        """
        pass
    
    @abstractmethod
    def render_teoria(self):
        """Muestra un fragmento en donde se explica detalladamente en que consiste el código."""
        pass
    
    @abstractmethod
    def render_inputs(self, key=None):
        """Dibuja los inputs de Streamlit y devuelve los parámetros."""
        pass
                    
    @abstractmethod
    def mostrar_codigo(self):
        """Muestra un extracto del código en Python."""
        pass
    
    @abstractmethod
    def get_rango_grafico(self, raiz, **params):
        """Devuelve (inf, sup) para el gráfico según el método."""
        pass

    def get_formula_grafico(self, f):
        """Por defecto, f ya es un string. Regresión lo pisa."""
        return f

    def _mostrar_panel_por_defecto(self):
        """Muestra un panel si no se introdujo una función o está mal escrita."""
        st.markdown("""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; text-align: center; opacity: 0.6;">
                            <h1 style="font-size: 4rem; margin-bottom: 0;">📊</h1>
                            <h2 style="color: #1a2b4c; margin-top: 15px; font-weight: 800;">Panel de Resultados</h2>
                            <p style="color: #64748b; font-size: 1.1rem; max-width: 300px;">Ingresa una función y presiona el botón para visualizar el análisis.</p>
                            <div style="margin-top: 20px; padding: 10px 20px; background-color: #eff6ff; border-radius: 10px; color: #3b82f6; font-weight: 700; font-size: 0.8rem; border: 1px dashed #3b82f6;">
                                ROOOTY ESTÁ LISTO PARA CALCULAR
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    def render_formula(self, valor_default = ''):
        f = st.text_input(
            'Función $f(x)$:',
            value=valor_default,
            placeholder='Ejemplo: x**2 + 11*x - 6'
            )
        st.caption("Usa `( )` para agrupar elementos. Por ejemplo `e^(1-x)` para $$ e^{1-x}$$.")
        
        st.space(size='small')
        
        exponente_err = st.select_slider(
            "Presición",
            options=[1,2,3,4,5,6,7,8,9,10],
            value=2,
            format_func=lambda x: f"$10^{{{-int(x)}}}$"
            )
        # Por ejemplo: 10^(-2)
        err = 10**(-exponente_err)
        return f, err, exponente_err
    
    def mostrar_resultados(self, f, raiz, datos, grafico_f):
        
        datos_dict = datos.obtener_datos()
        iteraciones = len(datos_dict['x[i]']) if 'x[i]' in datos_dict else 0
        
        # 1. LA FÓRMULA COMO PROTAGONISTA
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem; font-weight: 700; margin-bottom: -15px; letter-spacing: 1px;'>FUNCIÓN EVALUADA</p>", unsafe_allow_html=True)
        st.latex(ut.mostrar_formula(self.get_formula_grafico(f)))
        
        # 2. TARJETA DE MÉTRICAS COMPACTA Y ELEGANTE
        html_metricas = f"""
        <div style="display: flex; justify-content: space-evenly; align-items: center; background-color: #f8fafc; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; margin-top: 15px; margin-bottom: 10px;">
            <div style="text-align: center;">
                <p style="color: #64748b; font-size: 0.80rem; font-weight: 600; margin: 0; padding-bottom: 2px;">Raíz encontrada</p>
                <p style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0;">{raiz:.6f}</p>
            </div>
            <div style="height: 35px; width: 1px; background-color: #cbd5e1;"></div>
            <div style="text-align: center;">
                <p style="color: #64748b; font-size: 0.80rem; font-weight: 600; margin: 0; padding-bottom: 2px;">Iteraciones</p>
                <p style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0;">{iteraciones}</p>
            </div>
        </div>
        """
        st.markdown(html_metricas, unsafe_allow_html=True)
                
        # 3. GRÁFICO
        with st.spinner(text='Generando grafica...'):
            grafico.dibujar(grafico_f)
        
        # 4. TABLA
        with st.expander("Ver tabla de iteraciones"):
            st.dataframe(datos.obtener_dataframe(), width='stretch', hide_index=False)


    def mostrar_info(self):
        st.title(f'Método {self.nombre}')
        self.render_teoria()
        
        # Proporción equilibrada
        col_input, col_result = st.columns([1, 1.4], gap="large")

        llave_memoria = f"memoria_{self.nombre}"
        f_guardada = ""
        if llave_memoria in st.session_state and st.session_state[llave_memoria] is not None:
            f_guardada = st.session_state[llave_memoria]['f']

        with col_input:
            with st.container(border=True):
                st.markdown(f"""
                <div style='display:flex; align-items:center; flex-wrap: wrap; margin: 8px 0;'>
                    <h4 style='margin:auto; padding: 6px 8px 8px 0'><b>Parámetros</b></h4>
                    <b style=' padding:0 4px;  background-color: #cfe5fc; border-radius:3px; margin:auto 0; color:#3b82f6;'>{self.categoria.upper()}</b>
                </div>
                """, unsafe_allow_html=True)

                f, err, exponente_err = self.render_formula(valor_default=f_guardada)
                params = self.render_inputs(key=self.nombre)
                
                calcular_btn = st.button("🚀 Calcular y Graficar", type="primary", use_container_width=True)
                
                # --- Lógica de ejecución ---
                if calcular_btn:
                    if isinstance(f, str) and f.strip() == "":
                        st.warning("⚠️ Por favor, ingresa una función.")
                    elif isinstance(f, tuple) and len(f[0]) < 2:
                        st.warning("⚠️ Por favor, ingresa al menos dos puntos en la tabla.")
                    else:
                        try:
                            raiz, datos = self.ejecutar(f, err, **params)
                            if raiz is not None:
                                st.session_state[llave_memoria] = {
                                    'f': f, 'params': params, 'raiz': raiz, 'datos': datos
                                }
                            else:
                                st.session_state[llave_memoria] = None
                                st.error('No se encontró la raíz. Prueba con otros límites.')
                        except Exception as e:
                            st.session_state[llave_memoria] = None
                            st.error(f'Error: {e}')

                # --- Controles inferiores (Toggle y PDF) ---
                if llave_memoria in st.session_state and st.session_state[llave_memoria] is not None:
                    memoria = st.session_state[llave_memoria]
                    st.divider()
                    mostrar_datos = st.toggle("Mostrar iteraciones en el gráfico") if self.tiene_toggle else True
                    
                    inf, sup = self.get_rango_grafico(raiz=memoria['raiz'], **memoria['params'])
                    formula_str = self.get_formula_grafico(memoria['f'])
                    
                    grafico_f = grafico.obtener_grafico(
                        formula_str, memoria['raiz'], inf, sup, 
                        key=f'graf_{self.nombre.lower()}', 
                        iteraciones=memoria['datos'].obtener_datos() if mostrar_datos else None
                    )
                    
                    ut.boton_descarga(
                        metodo=self.nombre,
                        formula=memoria['f'],
                        params=memoria['params'],
                        raiz=memoria['raiz'],
                        datos=memoria['datos'].obtener_datos(),
                        fig=grafico_f
                    )

        with col_result:
            with st.container(border=True):
                if llave_memoria in st.session_state and st.session_state[llave_memoria] is not None:
                    memoria = st.session_state[llave_memoria]
                    if 'grafico_f' in locals():
                        self.mostrar_resultados(f=memoria['f'], raiz=memoria['raiz'], datos=memoria['datos'], grafico_f=grafico_f)
                else:
                    self._mostrar_panel_por_defecto()
                    
        st.divider()
        st.header('Código en Python')
        self.mostrar_codigo()
