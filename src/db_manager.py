import sqlite3
import threading
import logging


class DBManager:
    def __init__(self, db_name="data/produtos.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.lock = threading.Lock()
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            titulo TEXT,
            preco TEXT,
            link TEXT)""")
        self.conn.commit()

    def insert_produtos(self, produtos):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.executemany("INSERT INTO produtos (nome) VALUES (?)", [(p,) for p in produtos])
            self.conn.commit()
        logging.info(f"{len(produtos)} produtos inseridos no banco.")

    def insert_resultados(self, produto, resultados):
        valid = [(produto, r["title"], r["price"], r["link"]) 
                 for r in resultados if r["title"] and r["price"] != "N/A" and r["link"]]
        if not valid:
            return False
        with self.lock:
            cursor = self.conn.cursor()
            cursor.executemany(
                "INSERT INTO resultados (produto, titulo, preco, link) VALUES (?, ?, ?, ?)", valid
            )
            self.conn.commit()
        return True

    def get_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nome FROM produtos")
        return [row[0] for row in cursor.fetchall()]

    def get_resultados(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT produto, titulo, preco, link FROM resultados")
        return cursor.fetchall()

    def clear_produtos(self):
        with self.lock:
            self.conn.execute("DELETE FROM produtos")
            self.conn.commit()
        logging.info("Tabela de produtos limpa.")

    def clear_resultados(self):
        with self.lock:
            self.conn.execute("DELETE FROM resultados")
            self.conn.commit()
        logging.info("Tabela de resultados limpa.")

    def close(self):
        self.conn.close()
        logging.info("Conexão com o banco encerrada.")
