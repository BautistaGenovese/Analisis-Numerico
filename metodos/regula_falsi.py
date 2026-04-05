import streamlit as st
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import regula_falsi

class Regula_Falsi(MetodoNumerico):
    
    @property
    def nombre(self): return "Regula Falsi"
    
    def ejecutar(self, f, err, **params):
        return regula_falsi(
            f=f,
            a=params['a'],
            b=params['b'],
            err=err
            )

    def render_teoria(self):
        with st.expander("📖 ¿Cómo funciona el método de Regula Falsi (Falsa Posición)?"):
            st.markdown("""
            **Concepto básico:** Es un método cerrado que busca la raíz combinando la seguridad de la Bisección con una aproximación más inteligente. En lugar de partir el intervalo a la mitad a ciegas, traza una línea recta (secante) entre los puntos extremos del intervalo $(a, f(a))$ y $(b, f(b))$. La intersección de esta recta con el eje $X$ nos da la nueva aproximación.
            
            **Fórmula de iteración:**
            """)
            
            # La fórmula exacta que usas en algoritmos.py
            st.latex(r"x = b - \frac{f(b) \cdot (b - a)}{f(b) - f(a)}")
            
            st.markdown("""
            **Intervalos permitidos y Condiciones:**
            * Requiere **un intervalo inicial cerrado** definido por un límite inferior $a$ y un límite superior $b$.
            * **Es estrictamente necesario** que la función cambie de signo en el intervalo, es decir: $f(a) \cdot f(b) < 0$. De esta forma, nos aseguramos de que la raíz esté "atrapada".
            * Al ser un método cerrado, siempre converge (siempre encuentra la raíz), aunque puede ser lento si la curva es muy plana en uno de los extremos.
            """)
            st.warning(r"⚠️ **Restricción:** Para evitar la división por cero, las evaluaciones en los extremos no pueden ser iguales: $f(a) \neq f(b)$ (algo que se evita naturalmente gracias a la condición del cambio de signo).")
    
    def render_inputs(self,key=None):
        c1, c2 = st.columns(2)
        with c1:
            a = st.number_input('Límite $(a)$',value=-10.0,step=2.0,key=f'{key}_a')
        with c2:
            b = st.number_input('Límite $(b)$',value=10.0,step=2.0,key=f'{key}_b')
        
        return {'a':a,'b':b}
    
    def mostrar_codigo(self):
            st.code('''
def regula_falsi(a,b,err):
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
    
    def get_rango_grafico(self, raiz, **params):
        return params['a'], params['b']

if __name__ == "__main__":
    app = Regula_Falsi()
    app.mostrar_info()