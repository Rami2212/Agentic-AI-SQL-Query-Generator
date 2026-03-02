import streamlit as st
import requests

from src.config.config import Settings

st.title("AI-Powered SQL Query Generator")

query_input = st.text_input("Enter your query:")

if st.button("Generate SQL"):
    response = requests.post(Settings.APP_URL + "/generate-sql/", json={"query": query_input})
    sql_query = response.json().get("sql_query", "Failed to generate SQL query.")
    st.code(sql_query, language="sql")

    st.session_state["generated_sql"] = sql_query

if "generated_sql" in st.session_state:
    if st.button("Execute SQL"):
        response = requests.post(Settings.APP_URL + "/execute-sql/", json={"query": st.session_state["generated_sql"]})
        result = response.json().get("results", [])
        optimization_tips = response.json().get["optimization_tips", "No optimization tips available."]

        st.subheader("Query Results:")
        st.write(result)

        st.subheader("Optimization Tips:")
        st.write(optimization_tips)