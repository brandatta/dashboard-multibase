import streamlit as st
import pandas as pd
import mysql.connector

# Configuración de la página
st.set_page_config(page_title="Dashboard Multi-BD", layout="wide")

# 🔠 CSS para achicar fuente
st.markdown("""
    <style>
    .stMetricValue {
        font-size: 16px !important;
    }
    .stMetricLabel {
        font-size: 10px !important;
    }
    div[data-testid="stDataFrame"] * {
        font-size: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Multiempresa")

# Función de conexión
def get_conn(db_name):
    return mysql.connector.connect(
        host=st.secrets[db_name]["host"],
        user=st.secrets[db_name]["user"],
        password=st.secrets[db_name]["password"],
        database=st.secrets[db_name]["database"]
    )

# Traer datos
def fetch_data(conn, view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, conn)

# Diccionario de vistas
schemas = {
    "Brandatta": {"db": "app_marco_new", "view": "inv_esp"},
    "Georgalos": {"db": "georgalos", "view": "control_apps"},
    "Victoria": {"db": "victoria", "view": "control_efi"}
}

# Columnas horizontales
cols = st.columns(len(schemas))

for idx, (label, config) in enumerate(schemas.items()):
    with cols[idx]:
        st.subheader(label)
        try:
            conn = get_conn(config["db"])
            df = fetch_data(conn, config["view"])
            conn.close()

            # Slider visible arriba
            max_rows = min(len(df), 1000)
            num_rows = st.slider(
                "Filas", min_value=5, max_value=max_rows,
                value=min(10, max_rows), key=label
            )

            st.metric("Registros", f"{len(df):,}")
            st.dataframe(df.head(num_rows), use_container_width=True)

        except Exception as e:
            st.error(f"Error en {label}: {e}")
