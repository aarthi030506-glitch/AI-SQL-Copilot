import sqlite3


connection = sqlite3.connect("company.db")
cursor = connection.cursor()


tables = [
    "departments",
    "employees",
    "customers",
    "suppliers",
    "products",
    "orders",
    "order_items"
]


print("=" * 40)
print("       DATABASE VERIFICATION")
print("=" * 40)


total_records = 0


for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")

    count = cursor.fetchone()[0]

    total_records += count

    print(f"{table:<15} : {count}")


print("=" * 40)
print(f"TOTAL RECORDS    : {total_records}")
print("=" * 40)


connection.close()