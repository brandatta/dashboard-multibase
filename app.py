import streamlit as st
import pandas as pd
import mysql.connector

# Configuración de conexión (puedes usar st.secrets en Streamlit Cloud)
def get_conn(db_name):
    return mysql.connector.connect(
        host=st.secrets[db_name]["host"],
        user=st.secrets[db_name]["user"],
        password=st.secrets[db_name]["password"],
        database=st.secrets[db_name]["database"]
    )

def fetch_data(conn, view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, conn)

st.set_page_config(page_title="Dashboard Multi-BD", layout="wide")
st.title("📊 Dashboard Multiempresa")

schemas = {
    "Brandatta": {"db": "bd", "view": "inv_esp"},
    "Georgalos": {"db": "georgalos", "view": "control_apps"},
    "Georgalos2": {"db": "georgalos", "view": "control_efi"}
}

cols = st.columns(len(schemas))

for idx, (label, config) in enumerate(schemas.items()):
    with cols[idx]:
        try:
            conn = get_conn(config["db"])
            df = fetch_data(conn, config["view"])
            conn.close()
            st.metric(label, f"{len(df):,} registros")
            st.dataframe(df.head(5))
        except Exception as e:
            st.error(f"Error en {label}: {e}")
