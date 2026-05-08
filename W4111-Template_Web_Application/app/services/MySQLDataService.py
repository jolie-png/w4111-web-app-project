from __future__ import annotations

import os

import mysql.connector
from mysql.connector import IntegrityError

from .AbstractBaseDataService import AbstractBaseDataService


class MySQLDataService(AbstractBaseDataService):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._host = config.get("host") or os.getenv("MYSQL_HOST", "localhost")
        self._port = int(config.get("port") or os.getenv("MYSQL_PORT", "3306"))
        self._user = config.get("user") or os.getenv("MYSQL_USER", "root")
        self._password = config.get("password") or os.getenv("MYSQL_PASSWORD", "")
        self._database = config.get("database") or os.getenv("MYSQL_DB", "classicmodels")
        self._table = config["table_name"]
        self._pk_field = config.get("primary_key_field", "id")

    def _get_connection(self):
        conn = mysql.connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        return conn

    def retrieveByPrimaryKey(self, primary_key: str) -> dict:
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM {self._table} WHERE {self._pk_field} = %s"
        cursor.execute(query, (primary_key,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return dict(row)
        return {}

    def retrieveByTemplate(self, template: dict) -> list[dict]:
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        if not template:
            query = f"SELECT * FROM {self._table}"
            cursor.execute(query)
        else:
            clauses = [f"{col} = %s" for col in template]
            query = f"SELECT * FROM {self._table} WHERE {' AND '.join(clauses)}"
            cursor.execute(query, tuple(template.values()))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]

    def create(self, payload: dict) -> str:
        conn = self._get_connection()
        cursor = conn.cursor()
        cols = list(payload.keys())
        values = [payload[c] for c in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        col_list = ", ".join(cols)
        query = f"INSERT INTO {self._table} ({col_list}) VALUES ({placeholders})"
        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            pk = str(cursor.lastrowid)
            cursor.close()
            conn.close()
            return pk
        except IntegrityError as e:
            cursor.close()
            conn.close()
            raise ValueError(f"Database constraint violation: {e.msg}") from e

    def updateByPrimaryKey(self, primary_key: str, payload: dict) -> int:
        if not payload:
            return 0
        cols = [f"{col} = %s" for col in payload if col != self._pk_field]
        values = [val for col, val in payload.items() if col != self._pk_field]
        if not cols:
            return 0
        query = f"UPDATE {self._table} SET {', '.join(cols)} WHERE {self._pk_field} = %s"
        values.append(primary_key)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return count

    def deleteByPrimaryKey(self, primary_key: str) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {self._table} WHERE {self._pk_field} = %s"
        cursor.execute(query, (primary_key,))
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return count

    def updateByTemplate(self, template: dict, payload: dict) -> int:
        if not template or not payload:
            return 0
        set_clauses = [f"{col} = %s" for col in payload]
        set_values = list(payload.values())
        where_clauses = [f"{col} = %s" for col in template]
        where_values = list(template.values())
        query = f"UPDATE {self._table} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(set_values + where_values))
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return count

    def deleteByTemplate(self, template: dict) -> int:
        if not template:
            return 0
        where_clauses = [f"{col} = %s" for col in template]
        values = list(template.values())
        query = f"DELETE FROM {self._table} WHERE {' AND '.join(where_clauses)}"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return count