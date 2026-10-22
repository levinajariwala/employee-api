import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "localpass"),
    )


class Employee(BaseModel):
    name: str
    dept: str
    salary: float


@app.get("/health")
def health():
    return {"status": "ok", "version": "3.1"}


@app.get("/employees")
def get_employees():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM employees ORDER BY id")
        return cur.fetchall()


@app.post("/employees")
def add_employee(emp: Employee):
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO employees (name, dept, salary) VALUES (%s, %s, %s) RETURNING *",
            (emp.name, emp.dept, emp.salary),
        )
        return cur.fetchone()