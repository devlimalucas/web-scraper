import pandas as pd
import logging
from src.db_manager import DBManager


class ExcelManager:
    def __init__(self):
        self.db = DBManager()

    def carregar_produtos(self, excel_path):
        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            logging.error(f"Erro ao ler Excel {excel_path}: {e}")
            return

        if "Produto" not in df.columns:
            logging.error("O Excel deve ter uma coluna chamada 'Produto'")
            return

        produtos = df["Produto"].dropna().tolist()
        if not produtos:
            logging.warning("Nenhum produto encontrado no Excel")
            return

        self.db.clear_produtos()
        self.db.insert_produtos(produtos)
        logging.info(f"{len(produtos)} produtos carregados no banco.")

    def exportar_resultados(self, excel_path="data/resultados.xlsx", formato="excel"):
        resultados = self.db.get_resultados()
        if not resultados:
            logging.warning("Nenhum resultado para exportar.")
            return

        df = pd.DataFrame(resultados, columns=["Produto", "Título", "Preço", "Link"])

        try:
            if formato == "excel":
                df.to_excel(excel_path, index=False)
                logging.info(f"Resultados exportados para {excel_path}")
            elif formato == "csv":
                csv_path = excel_path.replace(".xlsx", ".csv")
                df.to_csv(csv_path, index=False)
                logging.info(f"Resultados exportados para {csv_path}")
            else:
                logging.error("Formato inválido. Use 'excel' ou 'csv'.")
        except Exception as e:
            logging.error(f"Erro ao exportar resultados: {e}")
