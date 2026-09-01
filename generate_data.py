import sqlite3
from faker import Faker
import random

fake = Faker()

# Connect to database
connection = sqlite3.connect("company.db")
cursor = connection.cursor()


# ==========================================
# 1. CREATE TABLES
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT,
        location TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL,
        joining_year INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        city TEXT,
        country TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY,
        company_name TEXT,
        contact_person TEXT,
        email TEXT,
        city TEXT,
        country TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        supplier_id INTEGER,
        price REAL,
        stock_quantity INTEGER,
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
    )
""")


# ==========================================
# 2. DEPARTMENTS
# ==========================================

departments = [
    (1, "IT", "Chennai"),
    (2, "HR", "Bangalore"),
    (3, "Finance", "Mumbai"),
    (4, "Sales", "Hyderabad"),
    (5, "Marketing", "Delhi"),
    (6, "Operations", "Pune"),
    (7, "Research", "Bangalore"),
    (8, "Engineering", "Chennai"),
    (9, "Customer Support", "Kolkata"),
    (10, "Procurement", "Mumbai")
]

cursor.executemany("""
    INSERT OR IGNORE INTO departments
    (department_id, department_name, location)
    VALUES (?, ?, ?)
""", departments)


# ==========================================
# 3. EMPLOYEES
# ==========================================

department_names = [
    "IT",
    "HR",
    "Finance",
    "Sales",
    "Marketing",
    "Operations",
    "Research",
    "Engineering",
    "Customer Support",
    "Procurement"
]

employees = []

for employee_id in range(1, 501):

    employees.append((
        employee_id,
        fake.name(),
        random.choice(department_names),
        random.randint(30000, 120000),
        random.randint(2018, 2025)
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO employees
    (employee_id, name, department, salary, joining_year)
    VALUES (?, ?, ?, ?, ?)
""", employees)


# ==========================================
# 4. CUSTOMERS
# ==========================================

customers = []

for customer_id in range(1, 501):

    customers.append((
        customer_id,
        fake.name(),
        fake.email(),
        fake.city(),
        fake.country()
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO customers
    (customer_id, name, email, city, country)
    VALUES (?, ?, ?, ?, ?)
""", customers)


# ==========================================
# 5. SUPPLIERS
# ==========================================

suppliers = []

for supplier_id in range(1, 101):

    suppliers.append((
        supplier_id,
        fake.company(),
        fake.name(),
        fake.email(),
        fake.city(),
        fake.country()
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO suppliers
    (supplier_id, company_name, contact_person, email, city, country)
    VALUES (?, ?, ?, ?, ?, ?)
""", suppliers)


# ==========================================
# 6. PRODUCTS
# ==========================================

product_names = [
    "Laptop",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Printer",
    "Office Chair",
    "Desk",
    "Headphones",
    "Webcam",
    "Router",
    "External Hard Drive",
    "USB Cable",
    "Smartphone",
    "Tablet",
    "Projector"
]

products = []

for product_id in range(1, 501):

    products.append((
        product_id,
        random.choice(product_names),
        random.randint(1, 100),
        round(random.uniform(500, 100000), 2),
        random.randint(0, 500)
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO products
    (product_id, product_name, supplier_id, price, stock_quantity)
    VALUES (?, ?, ?, ?, ?)
""", products)


# ==========================================
# 7. ORDERS
# ==========================================

orders = []

order_statuses = [
    "Completed",
    "Pending",
    "Cancelled",
    "Shipped"
]

for order_id in range(1, 2001):

    orders.append((
        order_id,
        random.randint(1, 500),
        fake.date_between(
            start_date="-2y",
            end_date="today"
        ).isoformat(),
        random.choice(order_statuses)
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO orders
    (order_id, customer_id, order_date, status)
    VALUES (?, ?, ?, ?)
""", orders)


# ==========================================
# 8. ORDER ITEMS
# ==========================================

order_items = []

order_item_id = 1

for order_id in range(1, 2001):

    number_of_products = random.randint(1, 5)

    selected_products = random.sample(
        range(1, 501),
        number_of_products
    )

    for product_id in selected_products:

        quantity = random.randint(1, 10)

        cursor.execute("""
            SELECT price
            FROM products
            WHERE product_id = ?
        """, (product_id,))

        result = cursor.fetchone()

        unit_price = result[0]

        order_items.append((
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        order_item_id += 1


cursor.executemany("""
    INSERT OR IGNORE INTO order_items
    (order_item_id, order_id, product_id, quantity, unit_price)
    VALUES (?, ?, ?, ?, ?)
""", order_items)


# ==========================================
# 9. SAVE DATABASE
# ==========================================

connection.commit()
connection.close()


print("===================================")
print("DATABASE GENERATED SUCCESSFULLY!")
print("===================================")
print("Departments : 10")
print("Employees   : 500")
print("Customers   : 500")
print("Suppliers   : 100")
print("Products    : 500")
print("Orders      : 2000")
print("Order Items :", len(order_items))
print("===================================")