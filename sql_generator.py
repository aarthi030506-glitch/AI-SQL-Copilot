import os
from dotenv import load_dotenv
from google import genai
from sql_runner import run_query
from sql_validator import validate_sql


# Load variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Database schema
SCHEMA = """
Database: company.db

Table: departments
Columns:
- department_id INTEGER
- department_name TEXT
- location TEXT

Table: employees
Columns:
- employee_id INTEGER
- name TEXT
- department TEXT
- salary REAL
- joining_year INTEGER

Table: customers
Columns:
- customer_id INTEGER
- name TEXT
- email TEXT
- city TEXT
- country TEXT

Table: suppliers
Columns:
- supplier_id INTEGER
- company_name TEXT
- contact_person TEXT
- email TEXT
- city TEXT
- country TEXT

Table: products
Columns:
- product_id INTEGER
- product_name TEXT
- supplier_id INTEGER
- price REAL
- stock_quantity INTEGER

Table: orders
Columns:
- order_id INTEGER
- customer_id INTEGER
- order_date TEXT
- status TEXT

Table: order_items
Columns:
- order_item_id INTEGER
- order_id INTEGER
- product_id INTEGER
- quantity INTEGER
- unit_price REAL
"""


def generate_sql(question, chat_history=None):
    if chat_history:
        conversation = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in chat_history
                if message["type"] == "text"
            ]
        )
    else:
        conversation = "No previous conversation."

    prompt = f"""
You are an expert SQL developer.

Convert the user's natural language question into a SQLite SQL query.

Use ONLY the tables and columns provided in the database schema.

Return ONLY the SQL query.
Do not use markdown.
Do not use ```sql.
Do not explain the query.

DATABASE SCHEMA:
{SCHEMA}

PREVIOUS CONVERSATION:
{conversation}

CURRENT USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()

    return sql
def explain_result(question, sql, columns, results):

    prompt = f"""
You are a helpful data analyst.

Answer the user's question using the SQL query and database results below.

USER QUESTION:
{question}

SQL QUERY:
{sql}

RESULT COLUMNS:
{columns}

RESULT DATA:
{results}

Give a short, clear answer in natural language.
Include important numbers when available.
Do not mention that you are an AI.
Do not invent information that is not present in the results.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()
def fix_sql(question, sql, error):

    prompt = f"""
You are an expert SQLite developer.

The SQL query below produced an error.

USER QUESTION:
{question}

ORIGINAL SQL:
{sql}

DATABASE ERROR:
{error}

DATABASE SCHEMA:
{SCHEMA}

Fix the SQL query so that it correctly answers the user's question.

Rules:
- Use only tables and columns from the schema.
- Return ONLY the corrected SQLite SQL query.
- Do not use markdown.
- Do not explain the query.
- Only generate a SELECT query.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()
if __name__ == "__main__":

    question = "How many employees are in the database?"

    bad_sql = """
    SELECT COUNT(*) FROM employee;
    """

    error = "no such table: employee"

    print("\nOriginal SQL:")
    print(bad_sql)

    corrected_sql = fix_sql(
        question,
        bad_sql,
        error
    )

    print("\nCorrected SQL:")
    print(corrected_sql)