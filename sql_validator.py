import re


def validate_sql(sql):

    # ------------------------------------------
    # Basic validation
    # ------------------------------------------

    if not isinstance(sql, str):
        return False, "Invalid SQL input."

    sql = sql.strip()

    if not sql:
        return False, "SQL query is empty."


    # ------------------------------------------
    # Remove trailing semicolon
    # ------------------------------------------

    sql = sql.rstrip(";").strip()


    # ------------------------------------------
    # Only allow SELECT statements
    # ------------------------------------------

    if not re.match(r"^\s*select\b", sql, re.IGNORECASE):

        return False, "Only SELECT queries are allowed."


    # ------------------------------------------
    # Prevent multiple SQL statements
    # ------------------------------------------

    if ";" in sql:

        return False, "Multiple SQL statements are not allowed."


    # ------------------------------------------
    # Dangerous SQL keywords
    # ------------------------------------------

    dangerous_keywords = [
        "drop",
        "delete",
        "update",
        "insert",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "vacuum",
        "reindex",
        "pragma",
        "grant",
        "revoke"
    ]


    for keyword in dangerous_keywords:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            sql,
            re.IGNORECASE
        ):

            return (
                False,
                f"Unsafe SQL detected: {keyword.upper()}"
            )


    # ------------------------------------------
    # Prevent SQLite dangerous functions
    # ------------------------------------------

    dangerous_functions = [
        "load_extension",
        "writefile",
        "readfile"
    ]


    for function in dangerous_functions:

        pattern = rf"\b{function}\s*\("

        if re.search(
            pattern,
            sql,
            re.IGNORECASE
        ):

            return (
                False,
                f"Unsafe SQL function detected: {function.upper()}"
            )


    # ------------------------------------------
    # Block comments
    # ------------------------------------------

    if "/*" in sql or "*/" in sql:

        return (
            False,
            "SQL comments are not allowed."
        )


    # ------------------------------------------
    # Block SQL comment injection
    # ------------------------------------------

    if "--" in sql:

        return (
            False,
            "SQL comments are not allowed."
        )


    # ------------------------------------------
    # Security check passed
    # ------------------------------------------

    return True, "SQL is safe."


# ==========================================
# TEST SECURITY
# ==========================================

if __name__ == "__main__":

    test_queries = [

        "SELECT * FROM employees;",

        "SELECT COUNT(*) FROM customers;",

        "DROP TABLE employees;",

        "DELETE FROM employees;",

        "UPDATE employees SET salary = 0;",

        "INSERT INTO employees VALUES (1, 'Test');",

        "ALTER TABLE employees ADD COLUMN test TEXT;",

        "CREATE TABLE test (id INTEGER);",

        "SELECT * FROM employees; DROP TABLE employees;",

        "SELECT * FROM employees -- dangerous comment",

        "SELECT load_extension('test');",

        "PRAGMA database_list;"
    ]


    print("=" * 60)
    print("SQL SECURITY TEST")
    print("=" * 60)


    for query in test_queries:

        safe, message = validate_sql(query)

        print("\nQuery:")
        print(query)

        print("Safe:", safe)

        print("Message:", message)


    print("\n" + "=" * 60)