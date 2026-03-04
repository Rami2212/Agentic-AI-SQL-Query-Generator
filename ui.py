import streamlit as st
import requests
import pandas as pd

from core.config import get_settings

settings = get_settings()

st.title("AI-Powered SQL Query Generator")

query_input = st.text_input("Enter your query:")

if st.button("Generate SQL"):
    response = requests.post(settings.APP_URL + "/generate-sql/", json={"query": query_input})
    sql_query = response.json().get("sql_query", "Failed to generate SQL query.")
    st.code(sql_query, language="sql")

    st.session_state["generated_sql"] = sql_query

if "generated_sql" in st.session_state:
    if st.button("Execute SQL"):
        response = requests.post(settings.APP_URL + "/execute-sql/", json={"query": st.session_state["generated_sql"]})
        result = response.json().get("results", [])
        optimization_tips = response.json().get("optimization_tips", "No optimization tips available.")

        st.subheader("Query Results:")

        if result:
            # Convert list of dicts to DataFrame
            df = pd.DataFrame(result)
            st.dataframe(df)  # or use st.table(df) for static table
        else:
            st.write("No results returned.")

        st.subheader("Optimization Tips:")
        st.write(optimization_tips)