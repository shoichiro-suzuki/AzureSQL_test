import streamlit as st
import pyodbc
import logging
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTIONSTRING_SQL = os.getenv("CONNECTIONSTRING_SQL")
CONNECTIONSTRING_ENTRA = os.getenv("CONNECTIONSTRING_ENTRA")

logging.basicConfig(level=logging.DEBUG)


def get_conn():
    try:
        conn = pyodbc.connect(st.session_state.connection_string)
        logging.info("Connection successful")
        return conn
    except pyodbc.Error as e:
        logging.error(f"Error connecting to database: {e}")
        st.error(f"Error connecting to database: {e}")
        raise


def create_table():
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Persons' AND xtype='U')
            CREATE TABLE Persons (
                ID int NOT NULL PRIMARY KEY IDENTITY,
                FirstName varchar(255),
                LastName varchar(255)
            );
        """
        )
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        return False
    finally:
        if conn:
            conn.close()


def insert_sample_data(first_name, last_name):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO Persons (FirstName, LastName) VALUES ({first_name}, {last_name})"
        )
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        return False
    finally:
        if conn:
            conn.close()


def fetch_data():
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Persons")
        data = cursor.fetchall()
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()


def main():
    if "connection_string" not in st.session_state:
        st.session_state.connection_string = ""
    if "res_data" not in st.session_state:
        st.session_state.res_data = ""

    st.title("Azure SQL Database 接続テスト")
    if st.button("SQL認証で接続"):
        st.session_state.connection_string = CONNECTIONSTRING_SQL

    if st.button("Entra認証で接続"):
        st.session_state.connection_string = CONNECTIONSTRING_ENTRA

    if st.button("テーブル作成"):
        con_res = create_table()
        st.write(f"テーブル作成結果: {con_res}")

    st.subheader("データ挿入")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    if st.button("データ挿入"):
        insert_res = insert_sample_data(first_name, last_name)
        st.write(f"データ挿入結果: {insert_res}")

    if st.button("データ取得"):
        res_data = fetch_data()
        st.session_state.res_data = res_data
        st.write(st.session_state.res_data)


if __name__ == "__main__":
    main()
