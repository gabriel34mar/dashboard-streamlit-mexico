# Data App | México: consumo energético y red comercial

Aplicación académica desarrollada con Streamlit, Pandas, Plotly y NetworkX.

## Funcionalidades

- Filtro múltiple por entidad federativa.
- Filtro de fechas.
- Indicadores de consumo acumulado, promedio y máximo.
- Gráfica temporal interactiva del consumo.
- Comparación de consumo entre entidades.
- Tendencia mediante promedio móvil de siete días.
- Descarga CSV del subconjunto filtrado.
- Grafo interactivo de relaciones comerciales.
- Filtro por volumen comercial mínimo.
- Tablas con conexiones y volumen conectado.

## Datos y limitaciones importantes

**Los datos incluidos son demostrativos / ilustrativos.** El CSV energético contiene cifras de práctica para septiembre de 2026 y cubre cinco entidades. El CSV de relaciones comerciales también usa enlaces y volúmenes ficticios para fines académicos. No representan estadísticas oficiales y no deben sustentar decisiones de inversión, operación o política pública.

Para un análisis real, se deben sustituir por conjuntos verificables de DataMéxico, INEGI, SENER o CENACE, conservando la documentación de cobertura, periodo, unidad, metodología y fecha de descarga.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Sube estos archivos a la raíz del repositorio `gabriel34mar/dashboard-streamlit-mexico`.
2. Inicia sesión en https://share.streamlit.io/ usando GitHub.
3. Conecta y autoriza la cuenta de GitHub para acceder al repositorio.
4. Selecciona **Create app**.
5. Repositorio: `gabriel34mar/dashboard-streamlit-mexico`.
6. Rama: `main`.
7. Archivo principal: `app.py`.
8. Selecciona **Deploy**.

La URL pública se genera al completar el despliegue. No debe darse por publicada hasta que la aplicación cargue correctamente y sea accesible en incógnito.

## Fuentes de consulta sugeridas

- Streamlit: https://docs.streamlit.io/
- Streamlit Community Cloud: https://streamlit.io/cloud
- DataMéxico: https://www.economia.gob.mx/datamexico/
- Secretaría de Economía: https://www.gob.mx/se/acciones-y-programas/data-mexico
- INEGI, Banco de Indicadores: https://www.inegi.org.mx/servicios/api-indicadores/
- 30 Days of Streamlit en español: https://github.com/streamlit/30days-spanish/
