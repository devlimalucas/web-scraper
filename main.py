import sys
import logging
from PyQt6.QtWidgets import QApplication
from src.gui import ScraperApp


def main():
    # Configuração global de logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        force=True  # garante que não haja duplicação de handlers
    )

    try:
        app = QApplication(sys.argv)
        window = ScraperApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.critical(f"Erro crítico na aplicação: {e}", exc_info=True)


if __name__ == "__main__":
    main()
