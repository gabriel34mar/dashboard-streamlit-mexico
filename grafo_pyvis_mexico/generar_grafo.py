"""Generador del grafo con PyVis. Los volúmenes son ilustrativos."""
import pandas as pd
import networkx as nx
from pyvis.network import Network

CSV = "relaciones_comerciales_mexico.csv"
HTML = "grafo_comercial_mexico.html"

df = pd.read_csv(CSV)
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["Origen"], row["Destino"], weight=row["Volumen_Comercial_MDP"])

weighted_degree = dict(G.degree(weight="weight"))
degree = dict(G.degree())
max_weighted = max(weighted_degree.values())
max_edge = df["Volumen_Comercial_MDP"].max()

net = Network(
    height="780px", width="100%", bgcolor="#0f172a", font_color="#f8fafc",
    heading="Red interactiva de relaciones comerciales entre entidades de México",
    directed=False, neighborhood_highlight=True, select_menu=True,
    filter_menu=True, cdn_resources="in_line"
)
net.barnes_hut(gravity=-22000, central_gravity=0.25, spring_length=150,
               spring_strength=0.035, damping=0.85)

for node in sorted(G.nodes()):
    influence = weighted_degree[node]
    size = 18 + 32 * influence / max_weighted
    color = "#f59e0b" if influence >= .75 * max_weighted else ("#38bdf8" if influence >= .50 * max_weighted else "#94a3b8")
    title = (f"<b>{node}</b><br>Relaciones: {degree[node]}<br>"
             f"Volumen comercial acumulado: {influence:,.0f} MDP<br>"
             "<i>El tamaño representa la influencia ponderada.</i>")
    net.add_node(node, label=node, title=title, size=size, color=color,
                 borderWidth=2, font={"size":16, "face":"Arial", "color":"#f8fafc"})

for _, row in df.iterrows():
    width = 1.5 + 7.5 * row["Volumen_Comercial_MDP"] / max_edge
    net.add_edge(row["Origen"], row["Destino"], value=float(row["Volumen_Comercial_MDP"]),
                 width=width,
                 title=f"{row['Origen']} ↔ {row['Destino']}<br>Volumen: {row['Volumen_Comercial_MDP']:,.0f} MDP",
                 color={"color":"#64748b", "highlight":"#f8fafc", "hover":"#cbd5e1"},
                 smooth={"enabled":True, "type":"dynamic"})

net.show_buttons(filter_=["physics", "interaction"])
net.write_html(HTML, notebook=False, open_browser=False)

print("Grafo generado:", HTML)
print("\nTop 5 por volumen comercial acumulado:")
for node, value in sorted(weighted_degree.items(), key=lambda x:x[1], reverse=True)[:5]:
    print(f"- {node}: {value:,.0f} MDP")
