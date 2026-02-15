import threading
import queue
import logging
from concurrent.futures import ThreadPoolExecutor
from .web_scraper import WebScraper


class WorkerManager:
    def __init__(self, db, max_workers=4):
        self.db = db
        self.max_workers = max_workers
        self.result_queue = queue.Queue()
        self.retry_queue = queue.Queue()

    def _process(self, produto, limit=5):
        scraper = WebScraper()
        resultados = scraper.search_product(produto, limit=limit)
        self.result_queue.put((produto, resultados))

    def _saver(self):
        while True:
            try:
                produto, resultados = self.result_queue.get(timeout=2)
            except queue.Empty:
                break

            # Validação antes de salvar
            valid = [r for r in resultados if r["title"] and r["price"] != "N/A" and r["link"]]
            if not valid:
                logging.warning(f"{produto} inválido, reprocessando...")
                self.retry_queue.put(produto)
            else:
                ok = self.db.insert_resultados(produto, valid)
                if ok:
                    logging.info(f"{produto} → {len(valid)} resultados salvos")
                else:
                    logging.warning(f"{produto} não pôde ser salvo, reprocessando...")
                    self.retry_queue.put(produto)

            self.result_queue.task_done()

    def run(self, limit=5):
        produtos = self.db.get_produtos()

        # Primeira rodada
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for p in produtos:
                executor.submit(self._process, p, limit)

        saver_thread = threading.Thread(target=self._saver)
        saver_thread.start()
        saver_thread.join()

        # Retry loop com até 3 tentativas
        retries = 0
        while not self.retry_queue.empty() and retries < 3:
            produtos_retry = []
            while not self.retry_queue.empty():
                produtos_retry.append(self.retry_queue.get())

            logging.info(f"Retry {retries+1} para {len(produtos_retry)} produtos...")

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for p in produtos_retry:
                    executor.submit(self._process, p, limit)

            saver_thread = threading.Thread(target=self._saver)
            saver_thread.start()
            saver_thread.join()

            retries += 1

        if not self.retry_queue.empty():
            logging.error(f"Produtos não resolvidos após {retries} tentativas: {list(self.retry_queue.queue)}")
