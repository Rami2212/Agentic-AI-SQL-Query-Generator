import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")

connection_string = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(connection_string, echo=True)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            print(f"Connected to database: {result.fetchone()[0]}")
    except Exception as e:
        print(f"Error connecting to database: {e}")

def get_schema():
    query = """
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = :database;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"database": MYSQL_DB})
        schema_info = result.fetchall()

        schema_dict = {}
        for table_name, column_name, data_type in schema_info:
            if table_name not in schema_dict:
                schema_dict[table_name] = []
            schema_dict[table_name].append((column_name, data_type))

        return schema_dict

if __name__ == "__main__":
    test_connection()