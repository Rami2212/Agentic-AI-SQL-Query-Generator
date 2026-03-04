# AI-Powered SQL Query Generator

A full-stack application that converts natural language into optimized SQL queries using an AI model, executes them against a MySQL database, and surfaces results through a Streamlit UI backed by a FastAPI service.

---

## Features

- **Natural Language to SQL** — Describe what you want in plain English; the AI generates a valid, optimized SQL query.
- **Schema-Aware Generation** — Automatically introspects your MySQL database schema and feeds it to the model as context.
- **Query Validation** — SQL syntax is validated via `sqlparse` before any execution attempt.
- **Query Execution** — Runs the generated (or user-provided) query and returns results as structured data.
- **Optimization Tips** — Runs `EXPLAIN` on executed queries and suggests indexing improvements.
- **Interactive UI** — Streamlit frontend for generating, reviewing, and executing queries with tabular result display.
- **REST API** — FastAPI backend exposes `/generate-sql/` and `/execute-sql/` endpoints.

---

## Project Structure

```
.
├── app.py                  # FastAPI application and route definitions
├── ui.py                   # Streamlit frontend
├── core/
│   ├── config.py           # Settings loaded from environment variables
│   ├── database.py         # SQLAlchemy engine, connection, and schema introspection
│   └── sql_generator.py    # AI query generation, validation, execution, and optimization
└── .env                    # Environment variables (not committed)
```

---

## Prerequisites

- Python 3.9+
- A running MySQL instance
- An OpenAI-compatible API key and base URL (e.g. OpenAI, Azure OpenAI, or a compatible local model)

---

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-directory>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn streamlit sqlalchemy mysql-connector-python sqlparse openai python-dotenv pandas requests
```

---

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Application
APP_URL=http://127.0.0.1:8000

# MySQL Database
MYSQL_HOST=localhost
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_PORT=3306            

# AI Model
AICC_API_KEY=your_api_key
AICC_BASE_URL=base_url
AI_MODEL=model_name                         
```

---

## Running the Application

### 1. Start the FastAPI backend

```bash
python app.py
# or
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

### 2. Start the Streamlit UI

```bash
streamlit run ui.py
```

The UI will open in your browser at `http://localhost:8501`.

---

## API Reference

### `POST /generate-sql/`

Converts a natural language query into a SQL statement.

**Request body:**
```json
{ "query": "Show me the top 10 customers by total order value" }
```

**Response:**
```json
{
  "success": true,
  "sql_query": "SELECT customer_id, SUM(order_value) AS total FROM orders GROUP BY customer_id ORDER BY total DESC LIMIT 10;"
}
```

---

### `POST /execute-sql/`

Executes a SQL query and returns results with optimization suggestions.

**Request body:**
```json
{ "query": "SELECT * FROM customers LIMIT 5;" }
```

**Response:**
```json
{
  "success": true,
  "results": [{ "id": 1, "name": "Alice", "email": "alice@example.com" }],
  "optimization_tips": "Consider adding an index on frequent used WHERE condition."
}
```

---

## Usage (CLI)

The `sql_generator.py` module can also be run directly:

```bash
python core/sql_generator.py
# Enter your SQL query: List all products with fewer than 10 units in stock
```