import sys
import logging
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QSpinBox, QLabel
from src.excel_manager import ExcelManager
from src.worker_manager import WorkerManager


class QTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)


class ScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mercado Livre Scraper")
        self.layout = QVBoxLayout()

        # Área de logs
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.layout.addWidget(self.log_area)

        # Logger integrado
        log_handler = QTextEditLogger(self.log_area)
        log_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)

        # Botões
        self.btn_excel = QPushButton("Selecionar Excel")
        self.btn_excel.clicked.connect(self.selecionar_excel)
        self.layout.addWidget(self.btn_excel)

        self.btn_carregar = QPushButton("Carregar Produtos no Banco")
        self.btn_carregar.clicked.connect(self.carregar_produtos)
        self.layout.addWidget(self.btn_carregar)

        # Configuração de threads
        self.layout.addWidget(QLabel("Número de threads:"))
        self.spin_threads = QSpinBox()
        self.spin_threads.setValue(4)
        self.layout.addWidget(self.spin_threads)

        # Configuração de limite de resultados
        self.layout.addWidget(QLabel("Resultados por produto:"))
        self.spin_limit = QSpinBox()
        self.spin_limit.setValue(5)
        self.layout.addWidget(self.spin_limit)

        self.btn_pesquisar = QPushButton("Pesquisar")
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        self.layout.addWidget(self.btn_pesquisar)

        self.btn_exportar = QPushButton("Exportar Resultados para Excel")
        self.btn_exportar.clicked.connect(self.exportar)
        self.layout.addWidget(self.btn_exportar)

        self.setLayout(self.layout)
        self.excel_manager = ExcelManager()
        self.worker_manager = None
        self.excel_path = None

    def selecionar_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Excel", "data/", "Excel Files (*.xlsx)")
        if path:
            self.excel_path = path
            logging.info(f"Excel selecionado: {path}")
        else:
            logging.warning("Nenhum arquivo Excel selecionado.")

    def carregar_produtos(self):
        if self.excel_path:
            self.excel_manager.carregar_produtos(self.excel_path)
            logging.info("Produtos carregados no banco.")
        else:
            logging.error("Selecione um arquivo Excel antes de carregar produtos.")

    def pesquisar(self):
        threads = self.spin_threads.value()
        limit = self.spin_limit.value()
        self.worker_manager = WorkerManager(self.excel_manager.db, max_workers=threads)
        self.worker_manager.run(limit=limit)
        logging.info("Pesquisa concluída.")

    def exportar(self):
        self.excel_manager.exportar_resultados()
        logging.info("Resultados exportados para data/resultados.xlsx")

    def closeEvent(self, event):
        # Fecha conexão do banco ao encerrar o app
        self.excel_manager.db.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec())
