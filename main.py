import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from pathlib import Path
import lasio
import welly


# Insert an icon
icon = Image.open("resources/logo.jpeg")

# State the design of the app
st.set_page_config(page_title="Petro APP", page_icon=icon)

# Insert css codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
footer {
  display: none;
}
</style>""",
    unsafe_allow_html=True,
)

# Insert title for app
st.title("Petrophysics App")

st.write("---")

# Add information of the app
st.markdown(
    """
  La aplicación Petrophysics es una solución innovadora creada para el manejo y análisis de registros de pozos en 
  la industria petrolera. Proporciona herramientas especializadas para evaluar datos provenientes de 
  registros eléctricos, sónicos, de densidad y porosidad, mejorando la comprensión de los yacimientos y facilitando 
  la detección de zonas con potencial productivo"""


)

# Add additional information
expander = st.expander("Information")
expander.write(
    "This open-source web application, fully developed in Python, is designed for analyzing and optimizing well log data."
    " It facilitates the interpretation of petrophysical parameters such as porosity, fluid saturation, and permeability, "
    "supporting real-time decision-making and reservoir characterization"
)

# Insert subheader
st.subheader("*Qué es un registro de pozo?*")
# Insert Image
image = Image.open("resources/concepto.png")
st.image(image, width=100, use_container_width=True)

# Importar archivo LAS
uploaded_file = st.file_uploader("Sube un archivo LAS", type=["las"])

if uploaded_file is not None:
    try:
        las = lasio.read(uploaded_file.read().decode("utf-8"))

        st.write("### Información del archivo LAS")
        st.write("Campo: Volve (Noruega)")
        st.text(f"Versión LAS: {las.version[0].value}")
        st.text(f"Nombre del pozo: {las.well.WELL.value}")

        # Mostrar lista de curvas disponibles
        st.write("### Curvas contenidas")
        st.text(", ".join(las.keys()))

        # Convertir las curvas a un DataFrame
        las_df = las.df()

        # Mostrar una vista previa del DataFrame
        st.write("### Datos del archivo LAS")
        st.dataframe(las_df.head(10))

        # Botón para descargar el DataFrame como CSV
        csv = las_df.to_csv().encode('utf-8')
        st.download_button(
            label="Descargar datos como archivo CSV",
            data=csv,
            file_name="datos_volve.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"No se pudo procesar el archivo LAS: {e}")
else:
    st.info("Por favor, carga un archivo LAS para continuar.")