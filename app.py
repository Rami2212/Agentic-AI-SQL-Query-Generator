from fastapi import FastAPI
from pydantic import BaseModel
from core.query_generator import generate_sql_query, execute_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/generate-sql/")
async def generate_sql(request: QueryRequest):
    """Generate SQL query from natural language model."""
    sql_query = generate_sql_query(request.query)
    if not sql_query:
        return {"success": False, "sql_query": None, "error": "Failed to generate SQL query."}
    return {"success": True, "sql_query": sql_query}

@app.post("/execute-sql/")
async def execute_sql(request: QueryRequest):
    """Execute the provided SQL query and return results."""
    sql_query = request.query
    execution_result = execute_query(sql_query)
    if execution_result is None:
        return {"success": False, "results": [], "optimization_tips": "Failed to execute SQL query."}

    results = execution_result.get("results", [])
    optimization_tips = execution_result.get("optimization_tips", "No optimization tips available.")

    return {"success": True, "results": results, "optimization_tips": optimization_tips}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)