from fastapi import FastAPI, HTTPException
import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel
import os

DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return psycopg.connect(
        host='localhost',
        port=5432,
        dbname='app_db',
        user='postgres',
        password=DB_PASSWORD,
        row_factory=dict_row
    )

class ServerCreate(BaseModel):
    hostname: str
    ip_address: str
    os: str
    status: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello DevOps"}

@app.get("/servers")
def get_servers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM servers ORDER BY id;"
        )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.get("/servers/{server_id}")
def get_servers_id(server_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM servers WHERE id = %s;",
        (server_id,)
        )
    # rows = cursor.fetchall()
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    return row
@app.post("/servers")
def create_server(server: ServerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO servers
        (hostname, ip_address, os, status)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
        (
            server.hostname,
            server.ip_address,
            server.os,
            server.status
        )
    )
    new_server = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return new_server
@app.put("/servers/{server_id}")
def update_server(server_id: int, server: ServerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE servers
        SET hostname = %s,
            ip_address = %s,
            os = %s,
            status = %s
        WHERE id = %s
        RETURNING *;
        """,
        (
            server.hostname,
            server.ip_address,
            server.os,
            server.status,
            server_id
        )
    )
    updated_server = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if updated_server is None:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )
    return updated_server

@app.delete('/servers/{server_id}')
def delete_servers(server_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM servers
        WHERE id = %s
        RETURNING *;
        """,
        (
            server_id,
        )
    )

    delete_server = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if delete_server is None:
        raise HTTPException(
            status_code=404,
            detail='Server not found'
        )

    return delete_server