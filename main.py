import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path
import lasio
import welly
import matplotlib.pyplot as plt

def calcular_parametros(las_df):
    # Saturación de agua irreducible
    las_df["SWIRR"] = las_df["SW"] * las_df["BVW"]

    # Porosidad efectiva
    las_df["PHIE"] = las_df["PHIF"] * (1 - las_df["SWIRR"])
    return las_df


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
        # Sección para cálculos petrofísicos
        st.write("## Cálculos Petrofísicos")
        las_df = calcular_parametros(las_df)
        st.write("### Resultados de Cálculos Petrofísicos")
        st.dataframe(las_df[["PHIE", "SWIRR"]].head(10))

        # Agregar sección para graficar registros petrofísicos
        st.write("## Gráficos de registros petrofísicos")
        disponibles = list(las.keys())
        tracks = st.multiselect("Selecciona los tracks que deseas graficar", disponibles,
                                default=["KLOGH", "PHIF", "SAND_FLAG", "SW", "VSH"])

        if tracks:
            fig, axes = plt.subplots(1, len(tracks), figsize=(20, 40))

            for ind, track in enumerate(tracks):
                try:
                    datos = las[track]
                    profundidad = las.index  # Profundidad como índice

                    # Graficar el track seleccionado
                    axes[ind].plot(datos, profundidad)
                    axes[ind].invert_yaxis()  # Eje Y invertido
                    axes[ind].set_title(track)

                except KeyError:
                    st.error(f"No se encontró el track: {track}")

            axes[0].set_ylabel("Profundidad (m)", fontsize=14)
            fig.suptitle("Registros Petrofísicos", fontsize=16)
            fig.tight_layout()

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)
        else:
            st.warning("Por favor, selecciona al menos un track para graficar.")

    except Exception as e:
        st.error(f"No se pudo procesar el archivo LAS: {e}")
else:
    st.info("Por favor, carga un archivo LAS para continuar.")


# Generar archivo requirements.txt
with open('requirements.txt', 'w') as f:
    f.write("streamlit\n")
    f.write("pandas\n")
    f.write("plotly\n")
    f.write("Pillow\n")
    f.write("lasio\n")
    f.write("welly\n")
    f.write("numpy\n")
    f.write("matplotlib\n")