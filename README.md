# 📊 Software de Métodos Numéricos
Aplicación interactiva desarrollada con ❤️ en **Python + Streamlit** para la resolución de problemas de **Análisis Numérico**.
- https://genovese.streamlit.app/

## 📦 Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/BautistaGenovese/Analisis-Numerico.git
   cd Analisis-Numerico
   ```
3. Crear entorno de ejecución
   
    Se recomienda ejecutar el proyecto dentro de un entorno virtual de Python para evitar conflictos entre dependencias. Crear y activar el entorno virtual:

   Crear entorno virtual:

      ```bash
      python -m venv .venv
      ```

   Activar el entorno virtual:

      - En Windows:
   
         ```bash
         .venv\Scripts\activate
         ```
      
      - En Linux o Mac:
      
         ```bash
         source .venv/bin/activate
         ```

5. Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

6. Ejecutar la aplicación
    ```bash
    streamlit run app.py
    ```


## 📂 Estructura del Proyecto

```
Analisis-Numerico/
├── 📄 app.py              # Punto de entrada principal (Configuración de Streamlit)
├── 📄 inicio.py           # Pantalla de bienvenida e información del equipo
│
├── 📂 metodos/            # Lógica de los algoritmos numéricos
│   ├── 📄 biseccion.py    # Implementación del método de Bisección
│   ├── 📄 secante.py      # Implementación del método de la Secante
│   ├── 📄 newton.py       # Implementación del método de Newton-Raphson
│   ├── 📄 punto_fijo.py   # Implementación del método de Punto Fijo
│   └── 📄 regresion.py    # Cálculo de Regresión Lineal simple
│
├── 📂 core/               # Herramientas de soporte y visualización
│   ├── 📄 comparativa.py  # Lógica para contrastar dos métodos en paralelo
│   ├── 📄 grafico.py      # Generación de trazados interactivos con Plotly
│   └── 📄 utils.py        # Evaluación de funciones y formateo LaTeX
│
├── 📂 archivos/           # Documentación PDF y consignas del TP
├── 📂 animaciones/        # Archivos JSON para Lottie (Welcome.json)
└── 📄 requirements.txt    # Librerías necesarias (NumPy, Pandas, Plotly, etc.)
```

## 🛠️ Tecnologías utilizadas
- Python
- Streamlit
- NumPy
- Plotly
- Pandas
- SymPy
