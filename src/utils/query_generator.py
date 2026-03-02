import re
import openai
import sqlparse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..connectors.database import engine, get_schema
from ..config.config import Settings


def clean_sql_output(response_text):
    """Removes markdown formatting and exracts the raw SQL query."""
    clean_sql = re.sub(r'```sql\n(.*?)\n```', r'\1', response_text, flags=re.DOTALL)

    sql_match = re.search(r"SELECT.*?;", clean_sql, re.IGNORECASE | re.DOTALL)

    return sql_match.group(0) if sql_match else clean_sql.strip()

def validate_sql_query(query):
    """Validates the SQL query syntax before execution."""
    try:
        parsed = sqlparse.parse(query)
        if not parsed:
            return False, "Invalid SQL syntax."
        return True, None
    except Exception as e:
        return False, str(e)

def generate_sql_query(nl_input):
    """Converts natural language input into an optimized SQL query."""
    schema = get_schema()

    schema_text = "\n".join([
        f"{table}: {', '.join(columns)}"
        for table, columns in schema.items()]
    )

    prompt = f"""
    You are an expert SQL generator. Convert the following natural language request into an optimized SQL query. 
    Ensure:
    - Proper use of INDEXING where applicable.
    - Use of efficient JOINs instead of nested queries.
    - Use GROUP BY when aggregations are needed.
    - Ensure SQL is valid and optimized for execution.

    Database Schema:
    {schema_text}

    User Request:
    {nl_input}

    SQL Query:
    """

    try:
        response = openai.chat.completions.create(
            model=Settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert SQL generator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.2,
        )
        raw_sql_query = response.choices[0].message.content.strip()

        sql_query = clean_sql_output(raw_sql_query)
        return sql_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def suggest_indexes(sql_query):
    """Suggests indexes for the executed SQL query."""
    try:
        with engine.connect() as connection:
            explain_query = f"EXPLAIN {sql_query}"
            result = connection.execute(text(explain_query))
            explain_output = result.fetchall()

            print("\nQuery Execution Plan:")
            for row in explain_output:
                print(row)

            return "Consider adding an index on frequent used WHERE condition."

    except Exception as e:
        return f"Error generating execution plan: {e}"

def execute_query(sql_query):
    """Executes the SQL query"""
    is_valid, error_msg = validate_sql_query(sql_query)
    if not is_valid:
        print(f"SQL validation error: {error_msg}")
        return None

    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            fetched_results = result.fetchall()

        index_suggestions = suggest_indexes(sql_query)

        return {
            "results": fetched_results,
            "optimization_tips": index_suggestions
        }

    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        return None

if __name__ == "__main__":
    user_input = input("Enter your SQL query: ")
    sql_query = generate_sql_query(user_input)

    if sql_query:
        print(f"\nGenerated SQL Query:\n{sql_query}")

        execution_result = execute_query(sql_query)
        if execution_result:
            print("\nQuery Results:")
            for row in execution_result["results"]:
                print(row)
            print("\nOptimization Tips:")
            print(execution_result["optimization_tips"])
        else:
            print("No results returned or error during execution.")
    else:
        print("Failed to execute the query.")
