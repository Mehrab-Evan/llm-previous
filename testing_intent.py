import psycopg2
from psycopg2 import sql

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="vector_db_test",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)


# def Create_table_User_Messages_Leads():
#     with conn.cursor() as cursor:
#         cursor.execute("""
#             CREATE TABLE test (
#                 session_id TEXT PRIMARY KEY,
#                 org_url TEXT,
#                 msg_history BYTEA,
#                 embedded_txt BYTEA,
#                 embedded_msg_history BYTEA,
#                 user_msg TEXT,
#                 user_name TEXT,
#                 user_need TEXT,
#                 user_email TEXT,
#                 user_phone TEXT,
#                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         conn.commit()


def Create_table_User_Messages_Leads():
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE test (
                session_id TEXT PRIMARY KEY,
                knowledge BYTEA,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# def insert(session_id, embedded_txt):
#     try:
#         with conn.cursor() as cursor:
#             # Email and password combination does not exist, insert the new user
#             cursor.execute("""
#                 INSERT INTO test (session_id, knowledge)
#                 VALUES (%s, %s)
#             """, (session_id, embedded_txt))
#             conn.commit()
#             return "OK"
#     except psycopg2.Error as e:
#         # Handle any database errors here
#         print(f"Error inserting user message: {e}")
#         return "Error"

import psycopg2
import pickle  # You may need to import pickle


def insert(session_id, embedded_txt):
    try:
        with conn.cursor() as cursor:
            # Serialize the embedded_txt to bytes using pickle
            embedded_txt_bytes = pickle.dumps(embedded_txt)

            cursor.execute("""
                INSERT INTO test (session_id, knowledge)
                VALUES (%s, %s)
            """, (session_id, psycopg2.Binary(embedded_txt_bytes)))
            conn.commit()
            return "OK"
    except psycopg2.Error as e:
        # Handle any database errors here
        print(f"Error inserting user message: {e}")
        return "Error"


def get_msg_history(session_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT knowledge
            FROM test
            WHERE session_id = %s
        """, (session_id,))
        user_data = cursor.fetchone()
        if user_data:
            knowledge_bytes = user_data[0]
            knowledge = pickle.loads(knowledge_bytes)
            return {
                "knowledge": knowledge
            }
        else:
            return None


# Function to get all columns of a specific user_id
# def get_msg_history(session_id):
#     with conn.cursor() as cursor:
#         cursor.execute("""
#             SELECT knowledge
#             FROM test
#             WHERE session_id = %s
#         """, (session_id,))
#         user_data = cursor.fetchone()
#         if user_data:
#             knowledge = user_data
#             return {
#                 "knowledge": knowledge
#             }
#         else:
#             return None

# Create_table_User_Messages_Leads()
