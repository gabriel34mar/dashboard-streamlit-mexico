from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent
ENERGY_FILE = BASE / "datos_consumo_energia.csv"
TRADE_FILE = BASE / "grafo_pyvis_mexico" / "relaciones_comerciales_mexico.csv"

st.set_page_config(
    page_title="México | Energía y red comercial",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 1.35rem; padding-bottom: 2rem;}
      [data-testid="stMetric"] {background:#f2f6fb;padding:13px 15px;border-radius:12px;}
      .notice {background:#fff4dc;border-left:5px solid #d99a00;padding:12px 15px;
               border-radius:6px;color:#574100;margin:8px 0 18px 0;}
      .small-note {font-size:.88rem;color:#657386;}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_energy():
    if not ENERGY_FILE.exists():
        raise FileNotFoundError(f"No se encontró {ENERGY_FILE.name}")
    df = pd.read_csv(ENERGY_FILE, encoding="utf-8-sig")
    needed = {"Fecha", "Entidad", "Consumo_MWh"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(missing))}")
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Consumo_MWh"] = pd.to_numeric(df["Consumo_MWh"], errors="coerce")
    return df.dropna(subset=["Fecha", "Entidad", "Consumo_MWh"]).sort_values("Fecha")

@st.cache_data
def load_trade():
    if not TRADE_FILE.exists():
        raise FileNotFoundError(f"No se encontró {TRADE_FILE.name}")
    df = pd.read_csv(TRADE_FILE, encoding="utf-8-sig")
    needed = {"Origen", "Destino", "Volumen_Comercial_MDP"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(missing))}")
    df["Volumen_Comercial_MDP"] = pd.to_numeric(df["Volumen_Comercial_MDP"], errors="coerce")
    return df.dropna(subset=["Origen", "Destino", "Volumen_Comercial_MDP"])

st.title("México: consumo energético y conexiones comerciales")
st.write(
    "Aplicación académica para explorar patrones de consumo energético y "
    "relaciones comerciales entre entidades federativas."
)
st.markdown(
    '<div class="notice"><b>Importante:</b> los CSV incluidos son datos ilustrativos '
    "para demostrar el funcionamiento de la Data App. No son estadísticas oficiales "
    "ni deben utilizarse para decisiones operativas, financieras o de inversión. "
    "Consulta fuentes oficiales como DataMéxico, INEGI, SENER y CENACE para análisis reales.</div>",
    unsafe_allow_html=True,
)

try:
    energy = load_energy()
    trade = load_trade()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"No se pudieron cargar los datos: {exc}")
    st.stop()

st.sidebar.header("Filtros")
available_entities = sorted(energy["Entidad"].unique().tolist())
selected_entities = st.sidebar.multiselect(
    "Entidades federativas",
    options=available_entities,
    default=available_entities,
)
min_date = energy["Fecha"].min().date()
max_date = energy["Fecha"].max().date()
date_range = st.sidebar.date_input(
    "Periodo",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

min_trade = int(trade["Volumen_Comercial_MDP"].min())
max_trade = int(trade["Volumen_Comercial_MDP"].max())
trade_minimum = st.sidebar.slider(
    "Volumen comercial mínimo (MDP)",
    min_value=min_trade,
    max_value=max_trade,
    value=min_trade,
    step=10,
)
st.sidebar.caption("Los filtros modifican las visualizaciones y tablas.")

filtered = energy[
    energy["Entidad"].isin(selected_entities)
    & energy["Fecha"].dt.date.between(start_date, end_date)
].copy()

tab_energy, tab_network, tab_method = st.tabs(
    ["⚡ Consumo energético", "🔗 Red comercial", "📋 Datos y metodología"]
)

with tab_energy:
    st.subheader("Exploración del consumo energético")
    if filtered.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    else:
        total = filtered["Consumo_MWh"].sum()
        mean = filtered["Consumo_MWh"].mean()
        maximum = filtered["Consumo_MWh"].max()
        count = filtered["Entidad"].nunique()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Consumo acumulado", f"{total:,.1f} MWh")
        c2.metric("Promedio por registro", f"{mean:,.1f} MWh")
        c3.metric("Máximo diario", f"{maximum:,.1f} MWh")
        c4.metric("Entidades", f"{count}")

        daily = (
            filtered.groupby(["Fecha", "Entidad"], as_index=False)["Consumo_MWh"]
            .sum()
            .sort_values("Fecha")
        )
        fig = px.line(
            daily,
            x="Fecha",
            y="Consumo_MWh",
            color="Entidad",
            markers=True,
            title="Evolución diaria del consumo",
            labels={"Fecha": "Fecha", "Consumo_MWh": "Consumo (MWh)", "Entidad": "Entidad"},
        )
        fig.update_layout(hovermode="x unified", legend_title_text="Entidad")
        st.plotly_chart(fig, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            ranking = (
                filtered.groupby("Entidad", as_index=False)["Consumo_MWh"]
                .sum()
                .sort_values("Consumo_MWh", ascending=False)
            )
            bar = px.bar(
                ranking,
                x="Entidad",
                y="Consumo_MWh",
                title="Consumo acumulado por entidad",
                labels={"Entidad": "Entidad", "Consumo_MWh": "Consumo (MWh)"},
                text_auto=".1f",
            )
            st.plotly_chart(bar, use_container_width=True)
        with col_b:
            daily_total = filtered.groupby("Fecha", as_index=False)["Consumo_MWh"].sum()
            daily_total["Promedio móvil (7 días)"] = (
                daily_total["Consumo_MWh"].rolling(7, min_periods=1).mean()
            )
            area = px.area(
                daily_total,
                x="Fecha",
                y="Promedio móvil (7 días)",
                title="Tendencia suavizada (promedio móvil de 7 días)",
                labels={"Fecha": "Fecha", "Promedio móvil (7 días)": "MWh"},
            )
            st.plotly_chart(area, use_container_width=True)

        st.subheader("Registros filtrados")
        st.dataframe(
            filtered.sort_values(["Fecha", "Entidad"]),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Descargar datos filtrados (CSV)",
            data=filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="consumo_energetico_filtrado.csv",
            mime="text/csv",
        )

with tab_network:
    st.subheader("Red de relaciones comerciales entre entidades")
    st.caption("Conjunto de práctica: los enlaces y volúmenes son ilustrativos.")
    edges = trade[trade["Volumen_Comercial_MDP"] >= trade_minimum].copy()
    if edges.empty:
        st.info("No hay conexiones con ese umbral. Reduce el volumen mínimo.")
    else:
        graph = nx.Graph()
        for row in edges.itertuples(index=False):
            graph.add_edge(row.Origen, row.Destino, weight=float(row.Volumen_Comercial_MDP))
        weighted_degree = dict(graph.degree(weight="weight"))
        degree = dict(graph.degree())
        position = nx.spring_layout(graph, seed=42, weight="weight", k=0.9)

        edge_x, edge_y = [], []
        for source, target in graph.edges():
            x0, y0 = position[source]
            x1, y1 = position[target]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y, mode="lines",
            line=dict(width=1.4, color="#98A2B3"),
            hoverinfo="none", name="Conexiones",
        )
        nodes = list(graph.nodes())
        node_trace = go.Scatter(
            x=[position[node][0] for node in nodes],
            y=[position[node][1] for node in nodes],
            mode="markers+text",
            text=nodes,
            textposition="top center",
            marker=dict(
                size=[16 + 28 * weighted_degree[node] / max(weighted_degree.values()) for node in nodes],
                color=[weighted_degree[node] for node in nodes],
                colorscale="Blues",
                showscale=True,
                colorbar=dict(title="Volumen conectado<br>(MDP)"),
                line=dict(width=1, color="#ffffff"),
            ),
            customdata=[[degree[node], weighted_degree[node]] for node in nodes],
            hovertemplate=(
                "<b>%{text}</b><br>Conexiones: %{customdata[0]}"
                "<br>Volumen conectado: %{customdata[1]:,.0f} MDP<extra></extra>"
            ),
            name="Entidades",
        )
        network_fig = go.Figure(data=[edge_trace, node_trace])
        network_fig.update_layout(
            title="Mapa interactivo de conexiones comerciales",
            showlegend=False,
            height=630,
            margin=dict(l=10, r=10, t=55, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="#F8FAFC",
        )
        st.plotly_chart(network_fig, use_container_width=True)

        strength_table = pd.DataFrame(
            {
                "Entidad": list(weighted_degree.keys()),
                "Volumen conectado (MDP)": list(weighted_degree.values()),
                "Número de conexiones": [degree[node] for node in weighted_degree],
            }
        ).sort_values("Volumen conectado (MDP)", ascending=False)
        k1, k2 = st.columns(2)
        k1.metric("Conexiones visibles", f"{len(edges)}")
        k2.metric("Entidades visibles", f"{len(nodes)}")
        st.subheader("Entidades con mayor volumen conectado")
        st.dataframe(strength_table, use_container_width=True, hide_index=True)
        st.subheader("Detalle de conexiones")
        st.dataframe(
            edges.sort_values("Volumen_Comercial_MDP", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

with tab_method:
    st.subheader("Datos, alcance y limitaciones")
    st.markdown(
        """
        **Consumo energético**
        - Archivo: `datos_consumo_energia.csv`.
        - Variables: fecha, entidad y consumo (MWh).
        - Periodo del conjunto incluido: septiembre de 2026.
        - Cobertura: Querétaro, Guanajuato, Jalisco, Nuevo León y Ciudad de México.
        - Valores de demostración para fines académicos.

        **Red comercial**
        - Archivo: `grafo_pyvis_mexico/relaciones_comerciales_mexico.csv`.
        - Variables: origen, destino y volumen comercial (MDP).
        - Los enlaces y volúmenes son ilustrativos; no son registros oficiales.
        - La influencia ponderada de cada nodo es la suma de los pesos de sus conexiones.

        **Fuentes para sustituir datos de práctica**
        - [DataMéxico — Secretaría de Economía](https://www.economia.gob.mx/datamexico/)
        - [INEGI — Banco de Indicadores](https://www.inegi.org.mx/servicios/api-indicadores/)
        - [SENER](https://www.gob.mx/sener)
        """
    )

st.divider()
st.caption(
    "Proyecto académico de visualización de datos · Streamlit, Pandas, Plotly y NetworkX"
)
