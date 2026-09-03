\# 🤖 AI SQL Copilot



An AI-powered conversational SQL assistant that converts natural language questions into secure SQL queries and provides database insights through an interactive Streamlit dashboard.



\## 🚀 Features



\* 🗣️ Natural Language → SQL using Google Gemini

\* 🔐 Secure SQL validation — SELECT queries only

\* 🔧 Automatic SQL correction

\* 📊 Query results and visualizations

\* 📥 CSV export

\* 💡 AI-generated insights

\* 💬 Conversation history

\* 🟢 Database connection monitoring



\## 🏗️ Architecture



```text

User Question

&#x20;     ↓

Streamlit UI

&#x20;     ↓

Gemini LLM

&#x20;     ↓

SQL Generation

&#x20;     ↓

SQL Validation

&#x20;     ↓

SQLite Database

&#x20;     ↓

Results + Charts + AI Insights

```



\## 🛠️ Tech Stack



\*\*Python | Streamlit | Google Gemini | SQLite | Pandas | SQL | Faker\*\*



\## 🔐 Security



Only safe `SELECT` queries are allowed. The application blocks operations such as:



`DELETE` • `UPDATE` • `INSERT` • `DROP` • `ALTER` • `CREATE` • `PRAGMA`



It also prevents multiple SQL statements and dangerous SQLite functions.



\## 📊 Database



The application uses a business database containing \*\*9,500+ records\*\* across employees, customers, suppliers, products, orders, and departments.



\## 💡 Example Questions



```text

Which department has the highest average salary?



Show the top 10 most expensive products.



Show the number of orders by status.



Which suppliers provide the most products?

```



\## 🎯 Objective



Demonstrate the integration of \*\*Generative AI, Python, SQL, data analytics, and application security\*\* to make database analysis accessible through natural language.



\## ▶️ Run



```bash

git clone https://github.com/aarthi030506-glitch/AI-SQL-Copilot.git

cd AI-SQL-Copilot

pip install -r requirements.txt

streamlit run app.py

```



Create a `.env` file with your Gemini API key before running the application.



\## 👩‍💻 Author



\*\*Aarthi\*\* — AI \& Data Analytics Portfolio



