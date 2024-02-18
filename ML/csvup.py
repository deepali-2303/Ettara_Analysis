import streamlit as st
import pandas as pd
import sqlite3

def csv_to_sqlite(df, database_name, table_name):

    connection = sqlite3.connect(database_name)
    print("Connected")
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        {", ".join([f"{col} TEXT" for col in df.columns])}
    )
    '''
    connection.execute(create_table_query)

    df.to_sql(table_name, connection, if_exists='replace', index=False)

    connection.close()

# Streamlit web app
def main():
    st.title("CSV to SQLite Converter")

    # Upload CSV file
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])

    if csv_file is not None:
        st.success("CSV file uploaded successfully!")

        # Display uploaded data
        df = pd.read_csv(csv_file)
        st.dataframe(df)

        # Database connection details
        database_name = st.text_input("SQLite Database Name")
        table_name = st.text_input("Table Name")

        # Convert CSV to SQLite on button click
        if st.button("Convert to SQLite"):
            csv_to_sqlite(df, database_name, table_name)
            st.success(f"Data successfully inserted into {table_name} table in SQLite database!")

if __name__ == "__main__":
    main()
