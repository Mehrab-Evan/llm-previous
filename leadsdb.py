import psycopg2
from psycopg2 import sql

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="chirpent_dashboard",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)


def Create_table_User_Messages_Leads():
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE chirpent_user_messages_leads (
                session_id TEXT PRIMARY KEY,
                org_url TEXT,
                msg_history BYTEA,
                user_msg TEXT,
                user_email TEXT,
                user_phone TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def insert_user_message(session_id, msg_history, org_url):
    try:
        with conn.cursor() as cursor:
            # Email and password combination does not exist, insert the new user
            cursor.execute("""
                INSERT INTO chirpent_user_messages_leads (session_id, msg_history, org_url)
                VALUES (%s, %s, %s)
            """, (session_id, msg_history, org_url))
            conn.commit()
            return "OK"
    except psycopg2.Error as e:
        # Handle any database errors here
        print(f"Error inserting user message: {e}")
        return "Error"


# Function to update the msg_history
def update_msg_history(session_id, new_msg_history, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET msg_history = %s
            WHERE session_id = %s AND org_url = %s
        """, (new_msg_history, session_id, org_url))
        conn.commit()


def update_email(session_id, email, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_email = %s
            WHERE session_id = %s AND org_url = %s
        """, (email, session_id, org_url))
        conn.commit()

def update_phone_no(session_id, phone, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_phone = %s
            WHERE session_id = %s AND org_url = %s
        """, (phone, session_id, org_url))
        conn.commit()

def update_user_msg(session_id, user_msg, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_msg = %s
            WHERE session_id = %s AND org_url = %s
        """, (user_msg, session_id, org_url))
        conn.commit()


# Function to get all columns of a specific user_id
def get_msg_history(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT session_id, msg_history
            FROM chirpent_user_messages_leads
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        user_data = cursor.fetchone()
        if user_data:
            session_id, msg_history = user_data
            return {
                "user_id": session_id,
                "msg_history": msg_history
            }
        else:
            return None

# Function to delete a row for a specific user_id
def delete_user_data(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM chirpent_user_messages_leads
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        conn.commit()

# Example usage
if __name__ == "__main__":
    Create_table_User_Messages_Leads()
