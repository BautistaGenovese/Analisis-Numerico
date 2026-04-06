import streamlit as st
from metodos.metodo_numerico import MetodoNumerico
from core.algoritmos import biseccion

class Biseccion(MetodoNumerico):
    
    @property
    def nombre(self): return "Bisección"
    
    @property
    def categoria(self): return "Método Cerrado"
    
    def ejecutar(self, f, err, **params):
        
        # return raiz, datos
        return biseccion(
            f=f,
            a=params['a'],
            b=params['b'],
            err=err
            )

    def render_teoria(self):
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
    
    def render_inputs(self,key=None):
        c1, c2 = st.columns(2)
        with c1:
            a = st.number_input('Límite $(a)$',value=-10.0,step=2.0,key=f'{key}_a')
        with c2:
            b = st.number_input('Límite $(b)$',value=10.0,step=2.0,key=f'{key}_b')
        
        return {'a':a,'b':b}
    
    def mostrar_codigo(self):
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
    
    def get_rango_grafico(self, raiz, **params):
        return params['a'], params['b']

if __name__ == "__main__":
    app = Biseccion()
    app.mostrar_info()