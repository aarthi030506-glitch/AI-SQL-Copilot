import sqlite3


def run_query(sql):

    connection = sqlite3.connect("company.db")

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    column_names = [
        description[0]
        for description in cursor.description
    ]

    connection.close()

    return column_names, results


if __name__ == "__main__":

    sql = """
    SELECT department, AVG(salary) AS average_salary
    FROM employees
    GROUP BY department
    ORDER BY average_salary DESC;
    """

    columns, results = run_query(sql)

    print(columns)

    for row in results:
        print(row)
def get_table_count(table_name):
    query = f"SELECT COUNT(*) FROM {table_name};"

    columns, results = run_query(query)

    return results[0][0]