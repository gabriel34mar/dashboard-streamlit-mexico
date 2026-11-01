# Grafo interactivo de relaciones comerciales entre entidades de México

## Recursos consultados
- Principios de Gestalt aplicados a visualización: proximidad, similitud, continuidad, conexión y figura-fondo.
- Documentación oficial de PyVis para construir redes interactivas mediante Python.
- Conceptos de grafos: nodos, enlaces, pesos e influencia.

## Elementos solicitados
1. **Conjunto de datos:** `relaciones_comerciales_mexico.csv`.
2. **Nodos:** representan entidades federativas de México.
3. **Enlaces:** representan relaciones comerciales y su peso corresponde al volumen comercial.
4. **Propiedades visuales de los nodos:** tamaño proporcional al volumen comercial acumulado y color según nivel de influencia.
5. **Propiedades visuales de los enlaces:** grosor proporcional al volumen comercial y ventana emergente con el detalle de cada relación.
6. **Archivo HTML interactivo:** `grafo_comercial_mexico.html`.
7. **Nodos con mayor influencia:** se considera como medida principal la suma de los volúmenes comerciales de las conexiones de cada entidad.

## Influencia en la red de práctica
- **Ciudad de México:** 6,070 MDP
- **Nuevo León:** 5,880 MDP
- **Jalisco:** 5,090 MDP
- **Estado de México:** 5,060 MDP
- **Querétaro:** 5,040 MDP

> Los volúmenes son datos ilustrativos creados para fines académicos; no representan estadísticas oficiales.

## Aplicación de Gestalt
- **Proximidad:** la distribución espacial facilita identificar grupos de entidades conectadas.
- **Similitud:** los nodos comparten una codificación visual coherente y el color distingue niveles de influencia.
- **Conexión:** las líneas permiten identificar directamente las relaciones.
- **Continuidad:** los enlaces curvos y suaves facilitan seguir las conexiones.
- **Figura-fondo:** el contraste entre la red y el fondo ayuda a distinguir nodos y enlaces.

## Ejecución con PyVis
```bash
python3 -m pip install --break-system-packages -r requirements.txt
python3 generar_grafo.py
```
Luego abre `grafo_comercial_mexico.html`.
