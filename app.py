import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Consumo Energético",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard interactivo de consumo energético")
st.write(
    "Aplicación desarrollada con Streamlit, Pandas y Plotly. "
    "Los controles de la barra lateral actualizan el gráfico dinámicamente."
)

@st.cache_data
def cargar_datos():
    return pd.read_csv(
        "/Users/e/Library/CloudStorage/Dropbox/UMx/Carreras/Big Data/CUARTO CUATRI/VISUALIZACION DE DATOS/datos_consumo_energia.csv"
    )

df = cargar_datos()
df["Fecha"] = pd.to_datetime(df["Fecha"])

# -----------------------------
# Barra lateral
# -----------------------------
st.sidebar.header("Controles")

entidad = st.sidebar.selectbox(
    "Selecciona una entidad:",
    options=["Todas"] + sorted(df["Entidad"].unique().tolist())
)

min_mwh = float(df["Consumo_MWh"].min())
max_mwh = float(df["Consumo_MWh"].max())

rango = st.sidebar.slider(
    "Rango de consumo (MWh):",
    min_value=min_mwh,
    max_value=max_mwh,
    value=(min_mwh, max_mwh),
    step=10.0
)

# -----------------------------
# Filtrado dinámico
# -----------------------------
filtrado = df[
    df["Consumo_MWh"].between(rango[0], rango[1])
].copy()

if entidad != "Todas":
    filtrado = filtrado[filtrado["Entidad"] == entidad]

# -----------------------------
# Gráfico Plotly
# -----------------------------
fig = px.line(
    filtrado.sort_values("Fecha"),
    x="Fecha",
    y="Consumo_MWh",
    color="Entidad" if entidad == "Todas" else None,
    markers=True,
    title="Consumo energético diario"
)

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Consumo (MWh)",
    hovermode="x unified"
)

st.plotly_chart(fig, width="stretch")

st.subheader("Datos filtrados")
st.dataframe(filtrado.sort_values(["Fecha", "Entidad"]), width="stretch")

st.caption(
    "Fuente: dataset de práctica elaborado para la actividad. "
    "Los valores son de demostración."
)
