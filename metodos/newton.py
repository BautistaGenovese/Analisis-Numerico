import streamlit as st
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import newton

class Newton(MetodoNumerico):
    
    @property
    def nombre(self): return "Newton"
    
    def ejecutar(self, f, err, **params):
        return newton(
            f=f,
            x_0=params['x_0'],
            err=err
            )

    def render_teoria(self):
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
    
    def render_inputs(self,key=None):
        x_0 = st.number_input('Ingresar $(x_0)$',value=-10.0,step=2.0,key=key)
        return {'x_0':x_0}
    
    def mostrar_codigo(self):
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
    
    def get_rango_grafico(self, raiz, **params):
        return raiz-5, raiz+5

if __name__ == "__main__":
    app = Newton()
    app.mostrar_info()