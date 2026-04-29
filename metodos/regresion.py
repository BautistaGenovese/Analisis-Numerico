import streamlit as st
import pandas as pd
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import regresion
from core import grafico
from core import utils as ut

class Regresion(MetodoNumerico):
    """
    El orden de ejecución en `mostrar_info` garantiza que esto funcione:
        1. ejecutar()            → guarda self._m, self._b, self._r2
        2. get_formula_grafico() → los usa para armar el string
        3. get_rango_grafico()   → usa self._x_vals
        4. mostrar_resultados()  → muestra self._m, self._b
    """

    @property
    def nombre(self): return "Regresion"
    
    @property
    def categoria(self): return "Método de Mínimos Cuadrados"

    @property
    def tiene_toggle(self): return False

    def render_formula(self, valor_default=None):
        st.info("💡 Edita la tabla directamente. Toca la fila vacía al final para agregar más puntos.")
        
        # Si venimos de la memoria, valor_default es una tupla: (x_vals, y_vals)
        if isinstance(valor_default, tuple) and len(valor_default) == 2:
            df_base = pd.DataFrame({"x": valor_default[0], "y": valor_default[1]})
        else:
            df_base = pd.DataFrame({"x": [], "y": []})
            
        df_usuario = st.data_editor(df_base, num_rows="dynamic", width='stretch')
        
        x_vals = df_usuario["x"].dropna().tolist()
        y_vals = df_usuario["y"].dropna().tolist()
        
        return (x_vals, y_vals), None, None

    def render_inputs(self, key=None):
        return {} 

    def _asegurar_estado(self, f):
        """Si la página se recarga, los atributos _m, _b, etc., no existen en esta instancia. 
        Esto los reconstruye instantáneamente usando los datos de la memoria."""
        if not hasattr(self, '_m'):
            x_vals, y_vals = f
            m, b, _, r2, _ = regresion(x_vals, y_vals)
            self._m = m
            self._b = b
            self._r2 = r2
            self._x_vals = x_vals

    def ejecutar(self, f, err, **params):
        x_vals, y_vals = f
        m, b, raiz, r2, datos = regresion(x_vals, y_vals)

        self._m = m
        self._b = b
        self._r2 = r2
        self._x_vals = x_vals

        return raiz, datos 
    
    def get_formula_grafico(self, f):
        self._asegurar_estado(f) # Reconstruye si es necesario
        return f"{self._m:.4f}*x + {self._b:.4f}"

    def get_rango_grafico(self, raiz, **params):
        # Como aquí no recibimos 'f' en los parámetros directos, la buscamos en la caja fuerte
        memoria = st.session_state.get(f"memoria_{self.nombre}")
        if memoria and 'f' in memoria:
            self._asegurar_estado(memoria['f'])
            
        # Fallback de seguridad extrema
        if not hasattr(self, '_x_vals'):
            return raiz - 5, raiz + 5
            
        return min(raiz, min(self._x_vals)) - 1, max(raiz, max(self._x_vals)) + 1

    # ✅ 3. ACTUALIZACIÓN DE FIRMA (agregamos 'f' para que coincida con la base)
    def mostrar_resultados(self, f, raiz, datos, grafico_f):
        self._asegurar_estado(f) # Reconstruye si es necesario
        
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem; font-weight: 700; margin-bottom: -15px; letter-spacing: 1px;'>FUNCIÓN APROXIMADA</p>", unsafe_allow_html=True)
        st.latex(ut.mostrar_formula(self.get_formula_grafico(f)))

        html_metricas = f"""
        <div style="display: flex; justify-content: space-evenly; align-items: center; background-color: #f8fafc; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; margin-top: 15px; margin-bottom: 10px;">
            <div style="text-align: center;">
                <p style="color: #64748b; font-size: 0.80rem; font-weight: 600; margin: 0; padding-bottom: 2px;">Raíz encontrada</p>
                <p style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0;">{raiz:.12f}</p>
            </div>
        </div>
        """
        st.markdown(html_metricas, unsafe_allow_html=True)

        with st.spinner(text='Generando grafica...'):
            grafico.dibujar(grafico_f)
            
        with st.expander("📊 Ver métricas del modelo"):
            st.write(f"- **Raíz ($x$):** `{raiz}`")
            st.write(f"- **Pendiente ($m$):** `{self._m}`")
            st.write(f"- **Ordenada al origen ($b$):** `{self._b}`")
            st.write(f"- **Coeficiente de determinación ($R^2$):** `{self._r2}`")
            
    def render_teoria(self):
        with st.expander("📖 ¿Cómo funciona la Regresión Lineal?"):
            st.markdown("""
            **Concepto básico:** A diferencia de los métodos anteriores, aquí no buscamos la raíz de una ecuación no lineal, sino que modelamos la relación entre un conjunto de datos (puntos sueltos). La regresión lineal simple busca la **recta de mejor ajuste** que minimice la distancia vertical (error cuadrático) entre los puntos reales y la recta trazada.
            
            **Ecuación de la recta resultante:**
            """)
            st.latex(r"f(x) = mx + b")
            
            st.markdown("""
            Donde:
            * **$m$**: Pendiente de la recta.
            * **$b$**: Ordenada al origen (intersección con el eje Y).
            
            **Intervalos permitidos y Condiciones:**
            * Se requiere ingresar como mínimo **dos pares de coordenadas** $(x, y)$.
            * El cálculo de la raíz (donde la recta cruza el eje X) se realiza despejando la ecuación resultante, siempre y cuando la pendiente $m$ no sea exactamente cero.
            """)

    def mostrar_codigo(self):
        st.code('''
def calcular_regresion(datos):
    m, int = statistics.linear_regression(
        datos['x'],
        datos['y']
    )
    if m != 0:
        raiz = int / m * (-1)
        return m, int, raiz
        
    else:
        st.error('La recta no tiene raices.')
        return None
            ''',
            "python")

if __name__ == "__main__":
    app = Regresion()
    app.mostrar_info()
