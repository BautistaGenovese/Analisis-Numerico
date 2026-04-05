import streamlit as st
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import secante

class Secante(MetodoNumerico):
    
    @property
    def nombre(self): return "Secante"
    
    def ejecutar(self, f, err, **params):
        return secante(
            f=f,
            x_n1=params['x_n1'],
            x_n=params['x_n'],
            err=err
            )

    def render_teoria(self):
        with st.expander("📖 ¿Cómo funciona el método de la Secante?"):
            st.markdown("""
            **Concepto básico:** Es un **método abierto** que nace como una alternativa directa a Newton-Raphson. En lugar de exigirte calcular la derivada analítica $f'(x)$ (que a veces es imposible o muy costosa), aproxima la pendiente trazando una línea **secante** entre los dos últimos puntos evaluados. Donde esta recta cruza el eje $X$, encontramos nuestra nueva aproximación.
            
            **Fórmula de iteración:**
            """)
            
            # La fórmula exacta de diferencias finitas que usabas en tangente.py
            st.latex(r"x_{i+1} = x_i - f(x_i) \cdot \frac{x_{i-1} - x_i}{f(x_{i-1}) - f(x_i)}")
            
            st.markdown("""
            **Intervalos permitidos y Condiciones:**
            * Requiere **dos puntos iniciales** ($x_{i-1}$ y $x_i$).
            * Al ser un método abierto, **no requiere** que la raíz esté encerrada entre estos dos puntos (no hace falta que haya cambio de signo).
            * **No necesitas conocer la derivada** de la función.
            * Suele converger casi tan rápido como Newton, pero requiere que los puntos iniciales estén relativamente cerca de la raíz para no divergir.
            """)
            st.warning(r"⚠️ **Restricción:** La función evaluada en los dos puntos de la iteración actual no debe tener el mismo valor ($f(x_{i-1}) \neq f(x_i)$). Si son iguales, el denominador se vuelve cero, la línea secante queda totalmente horizontal y nunca cruza el eje $X$.")
    
    def render_inputs(self,key=None):
        c1, c2 = st.columns(2)
        with c1:
            x_n = st.number_input('Ingresar $(x_n)$',value=-10.0,step=2.0,key=f'{key}_xn')
        with c2:
            x_n1 = st.number_input('Ingresar $(x_{n+1})$',value=10.0,step=2.0,key=f'{key}_xn1')
        
        return {'x_n':x_n,'x_n1':x_n1}
    
    def mostrar_codigo(self):
        st.code('''
def secante(x_n1, x_n, f, err):
    
    # Calculo de la raíz
    iteracion = 0
    while iteracion < 100:
        
        try:
            fx_n = ec.evaluar_f(f,x_n)
            fx_n1 = ec.evaluar_f(f,x_n1)

            x = x_n - fx_n * ((x_n - x_n1)/(fx_n - fx_n1))
            fx = ec.evaluar_f(f,x)

            if abs(fx) < err:
                return x
        
            else:
                x_n, x_n1 = x, x_n

            iteracion+=1

        except ZeroDivisionError:
            print("División por 0. Probar con otros valores.")
            return None''',
            "python")
    
    def get_rango_grafico(self, raiz, **params):
        return raiz-5, raiz+5

if __name__ == "__main__":
    app = Secante()
    app.mostrar_info()