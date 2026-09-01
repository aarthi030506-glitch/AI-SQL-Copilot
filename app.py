import streamlit as st
import pandas as pd

from sql_generator import generate_sql, explain_result, fix_sql
from sql_runner import run_query, get_table_count
from sql_validator import validate_sql


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI SQL Copilot",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_columns" not in st.session_state:
    st.session_state.last_columns = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "last_sql" not in st.session_state:
    st.session_state.last_sql = None

if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("🤖 AI SQL Copilot")

    st.write(
        "Your intelligent assistant for querying "
        "business data using natural language."
    )

    st.divider()

    # ======================================
    # DATABASE INFORMATION
    # ======================================

    st.subheader("🗄️ Database")

    st.write("SQLite — company.db")

    st.write("📊 7 Tables")
    st.write("👥 500 Employees")
    st.write("🧑‍💼 500 Customers")
    st.write("🏭 100 Suppliers")
    st.write("📦 500 Products")
    st.write("🛒 2,000 Orders")
    st.write("📋 5,938 Order Items")

    st.divider()

    # ======================================
    # DATABASE SCHEMA
    # ======================================

    st.subheader("🗂️ Database Schema")

    with st.expander("View Tables"):

        st.write("**departments**")
        st.caption(
            "department_id, department_name, location"
        )

        st.write("**employees**")
        st.caption(
            "employee_id, name, department, salary, joining_year"
        )

        st.write("**customers**")
        st.caption(
            "customer_id, name, email, city, country"
        )

        st.write("**suppliers**")
        st.caption(
            "supplier_id, company_name, contact_person, "
            "email, city, country"
        )

        st.write("**products**")
        st.caption(
            "product_id, product_name, supplier_id, "
            "price, stock_quantity"
        )

        st.write("**orders**")
        st.caption(
            "order_id, customer_id, order_date, status"
        )

        st.write("**order_items**")
        st.caption(
            "order_item_id, order_id, product_id, "
            "quantity, unit_price"
        )

    st.divider()

    # ======================================
    # EXAMPLE QUESTIONS
    # ======================================

    st.subheader("💡 Example Questions")

    st.write("• How many employees are there?")

    st.write(
        "• Which department has the highest average salary?"
    )

    st.write(
        "• Show the 10 most expensive products."
    )

    st.write(
        "• How many customers are in the database?"
    )

    st.write(
        "• Show suppliers and their products."
    )

    st.divider()

    # ======================================
    # CLEAR CHAT
    # ======================================

    st.subheader("🧹 Chat")

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.query_history = []

        st.session_state.last_result = None
        st.session_state.last_columns = None
        st.session_state.last_question = None
        st.session_state.last_sql = None
        st.session_state.last_explanation = None

        st.rerun()

    st.divider()

    # ======================================
    # QUERY HISTORY
    # ======================================

    st.subheader("🧾 Query History")

    if st.session_state.query_history:

        for i, item in enumerate(
            reversed(st.session_state.query_history),
            start=1
        ):

            with st.expander(
                f"Query {i}: {item['question'][:35]}"
            ):

                st.write("**Question:**")

                st.write(
                    item["question"]
                )

                st.write("**SQL:**")

                st.code(
                    item["sql"],
                    language="sql"
                )

    else:

        st.caption("No queries yet.")

    st.divider()

    st.caption(
        "🛡️ Read-only SQL protection enabled"
    )


# ==========================================
# DATABASE STATUS
# ==========================================

try:

    get_table_count("employees")

    st.success(
        "🟢 Database connected successfully"
    )

except Exception:

    st.error(
        "🔴 Database connection failed"
    )


# ==========================================
# MAIN TITLE
# ==========================================

st.title("🤖 AI SQL Copilot")

st.write(
    "Ask questions about your database in natural language."
)


# ==========================================
# DASHBOARD METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

employee_count = get_table_count("employees")
customer_count = get_table_count("customers")
product_count = get_table_count("products")
order_count = get_table_count("orders")


with col1:

    st.metric(
        "👥 Employees",
        employee_count
    )


with col2:

    st.metric(
        "🧑‍💼 Customers",
        customer_count
    )


with col3:

    st.metric(
        "📦 Products",
        product_count
    )


with col4:

    st.metric(
        "🛒 Orders",
        order_count
    )


st.divider()


# ==========================================
# DISPLAY PREVIOUS CHAT
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        if message["type"] == "text":

            st.write(
                message["content"]
            )

        elif message["type"] == "sql":

            st.markdown(
                "**📝 Generated SQL**"
            )

            st.code(
                message["content"],
                language="sql"
            )

        elif message["type"] == "result":

            st.markdown(
                "**📊 Query Results**"
            )

            st.dataframe(
                message["content"],
                use_container_width=True
            )

        elif message["type"] == "error":

            st.error(
                message["content"]
            )


# ==========================================
# DISPLAY LAST RESULT
# ==========================================

if (
    st.session_state.last_result is not None
    and st.session_state.last_columns is not None
):

    st.divider()

    st.markdown(
        "### 📊 Latest Query Result"
    )

    latest_dataframe = pd.DataFrame(
        st.session_state.last_result,
        columns=st.session_state.last_columns
    )

    st.dataframe(
        latest_dataframe,
        use_container_width=True
    )


    # ======================================
    # CSV DOWNLOAD
    # ======================================

    csv_data = latest_dataframe.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name="sql_query_results.csv",
        mime="text/csv",
        key="download_latest_results"
    )


    # ======================================
    # VISUALIZATION
    # ======================================

    if len(latest_dataframe.columns) >= 2:

        numeric_columns = (
            latest_dataframe
            .select_dtypes(
                include="number"
            )
            .columns
        )

        if len(numeric_columns) > 0:

            chart_column = numeric_columns[0]

            st.markdown(
                "### 📈 Visualization"
            )

            st.bar_chart(
                latest_dataframe,
                x=latest_dataframe.columns[0],
                y=chart_column
            )


    # ======================================
    # OPTIONAL AI INSIGHT
    # ======================================

    if st.button(
        "💡 Explain Insight",
        use_container_width=True,
        key="explain_latest"
    ):

        with st.spinner(
            "Analyzing results..."
        ):

            st.session_state.last_explanation = (
                explain_result(
                    st.session_state.last_question,
                    st.session_state.last_sql,
                    st.session_state.last_columns,
                    st.session_state.last_result
                )
            )

        st.rerun()


    # ======================================
    # SHOW SAVED AI INSIGHT
    # ======================================

    if st.session_state.last_explanation:

        st.markdown(
            "### 💡 AI Insight"
        )

        st.write(
            st.session_state.last_explanation
        )


# ==========================================
# CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask a question about your database..."
)


# ==========================================
# PROCESS QUESTION
# ==========================================

if question:

    # Clear previous explanation
    st.session_state.last_explanation = None


    # ======================================
    # DISPLAY USER QUESTION
    # ======================================

    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": question
    })


    try:

        # ==================================
        # GENERATE SQL
        # ==================================

        with st.chat_message("assistant"):

            with st.spinner(
                "Generating SQL..."
            ):

                sql = generate_sql(
                    question,
                    st.session_state.messages
                )


            st.markdown(
                "### 📝 Generated SQL"
            )

            st.code(
                sql,
                language="sql"
            )


            # ==================================
            # SAVE GENERATED SQL
            # ==================================

            st.session_state.messages.append({
                "role": "assistant",
                "type": "sql",
                "content": sql
            })

            st.session_state.query_history.append({
                "question": question,
                "sql": sql
            })


            # ==================================
            # SECURITY CHECK
            # ==================================

            safe, message = validate_sql(
                sql
            )

            st.markdown(
                "### 🛡️ Security Check"
            )

            if not safe:

                st.error(message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "error",
                    "content": message
                })

                st.stop()


            st.success(message)


            # ==================================
            # RUN SQL
            # ==================================

            with st.spinner(
                "Running query..."
            ):

                try:

                    columns, results = run_query(
                        sql
                    )

                except Exception as query_error:

                    # ==========================
                    # AUTOMATIC SQL CORRECTION
                    # ==========================

                    st.warning(
                        "⚠️ The generated SQL failed. "
                        "Trying to correct it automatically..."
                    )

                    corrected_sql = fix_sql(
                        question,
                        sql,
                        str(query_error)
                    )

                    st.markdown(
                        "### 🔧 Corrected SQL"
                    )

                    st.code(
                        corrected_sql,
                        language="sql"
                    )


                    # ==========================
                    # VALIDATE CORRECTED SQL
                    # ==========================

                    corrected_safe, corrected_message = (
                        validate_sql(
                            corrected_sql
                        )
                    )


                    if not corrected_safe:

                        st.error(
                            "Corrected SQL was rejected "
                            "by the security check."
                        )

                        st.stop()


                    st.success(
                        "Corrected SQL passed the "
                        "security check."
                    )


                    # ==========================
                    # RUN CORRECTED SQL
                    # ==========================

                    with st.spinner(
                        "Running corrected SQL..."
                    ):

                        columns, results = run_query(
                            corrected_sql
                        )


                    sql = corrected_sql


            # ==================================
            # SAVE LATEST RESULT
            # ==================================

            st.session_state.last_question = question
            st.session_state.last_sql = sql
            st.session_state.last_columns = columns
            st.session_state.last_result = results
            st.session_state.last_explanation = None


            # ==================================
            # DISPLAY RESULTS
            # ==================================

            st.markdown(
                "### 📊 Query Results"
            )


            if results:

                dataframe = pd.DataFrame(
                    results,
                    columns=columns
                )


                st.dataframe(
                    dataframe,
                    use_container_width=True
                )


                # ==================================
                # CSV DOWNLOAD
                # ==================================

                csv_data = dataframe.to_csv(
                    index=False
                )

                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name="sql_query_results.csv",
                    mime="text/csv",
                    key="download_current_results"
                )


                # ==================================
                # SAVE RESULT TO CHAT
                # ==================================

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "result",
                    "content": dataframe
                })


                # ==================================
                # AUTOMATIC CHART
                # ==================================

                if len(dataframe.columns) >= 2:

                    numeric_columns = (
                        dataframe
                        .select_dtypes(
                            include="number"
                        )
                        .columns
                    )


                    if len(numeric_columns) > 0:

                        chart_column = (
                            numeric_columns[0]
                        )


                        st.markdown(
                            "### 📈 Visualization"
                        )


                        st.bar_chart(
                            dataframe,
                            x=dataframe.columns[0],
                            y=chart_column
                        )


                # ==================================
                # OPTIONAL AI INSIGHT
                # ==================================

                if st.button(
                    "💡 Explain Insight",
                    use_container_width=True,
                    key="explain_current"
                ):

                    with st.spinner(
                        "Analyzing results..."
                    ):

                        st.session_state.last_explanation = (
                            explain_result(
                                question,
                                sql,
                                columns,
                                results
                            )
                        )

                    st.rerun()


                if st.session_state.last_explanation:

                    st.markdown(
                        "### 💡 AI Insight"
                    )

                    st.write(
                        st.session_state.last_explanation
                    )


            else:

                st.info(
                    "The query returned no results."
                )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )