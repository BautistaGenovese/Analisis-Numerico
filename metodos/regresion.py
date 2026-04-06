import streamlit as st
import pandas as pd
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import regresion
from core import grafico

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

    # ✅ Pisa render_formula: en vez de text_input, muestra la tabla
    def render_formula(self, valor_default=None):
        st.info("💡 Edita la tabla directamente. Toca la fila vacía al final para agregar más puntos.")
        
        df_base = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [2.1, 4.0, 6.2]})
        df_usuario = st.data_editor(df_base, num_rows="dynamic", width='stretch')
        
        x_vals = df_usuario["x"].dropna().tolist()
        y_vals = df_usuario["y"].dropna().tolist()
        
        # Devuelve la misma estructura (f, err, exponente_err)
        # f en este caso son los datos crudos empaquetados como string
        # err y exponente no aplican, devolvemos None
        
        return (x_vals, y_vals), None, None

    def render_inputs(self,key=None):
        return {}  # Mochila vacía, no necesita nada más

    def ejecutar(self, f, err, **params):
        x_vals, y_vals = f
        m, b, raiz, r2, datos = regresion(x_vals, y_vals)

        # Guardamos los extras como atributos
        self._m = m
        self._b = b
        self._r2 = r2
        self._x_vals = x_vals

        return raiz, datos  # ← Misma firma que todos ✅
    
    def get_formula_grafico(self, f):
        # String válido para el gráfico
        return f"{self._m}*x + {self._b}"

    def get_rango_grafico(self, raiz, **params):
        return min(raiz, min(self._x_vals)) - 1, max(raiz, max(self._x_vals)) + 1

    def mostrar_resultados(self, raiz, datos, grafico_f):
        st.metric(label="✅ Raíz encontrada $(x)$", value=f"${raiz:.6f}$")
        grafico.dibujar(grafico_f)
        with st.expander("📊 Ver métricas del modelo"):
            st.write(f"- **Pendiente ($m$):** `{self._m:.4f}`")
            st.write(f"- **Ordenada al origen ($b$):** `{self._b:.4f}`")
            st.write(f"- **Coeficiente de determinación ($R^2$):** `{self._r2:.4f}`")
            
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