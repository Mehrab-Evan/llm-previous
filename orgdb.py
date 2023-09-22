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

def get_msg_limit(org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT msg_limit, msg_count
            FROM org
            WHERE org_url = %s
        """, (org_url,))
        org_data = cursor.fetchone()
        if org_data:
            msg_limit, msg_count = org_data
            return {
                "org_url": org_url,
                "msg_limit": msg_limit,
                "msg_count": msg_count
            }
        else:
            return None

