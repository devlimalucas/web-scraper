import requests
from bs4 import BeautifulSoup
import logging


class WebScraper:
    def search_product(self, product_name, limit=5):
        query = product_name.replace(" ", "-")
        url = f"https://lista.mercadolivre.com.br/{query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Erro ao buscar {product_name}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("ol.ui-search-layout li.ui-search-layout__item")
        results = []

        for item in items[:limit]:
            # Fallback de seletores para título/link
            link_elem = (
                item.select_one("h3 a")
                or item.select_one("h2.ui-search-item__title a")
                or item.select_one("a.ui-search-link")
            )
            price_elem = item.select_one("span.andes-money-amount__fraction")

            if link_elem:
                title = link_elem.get_text(strip=True)
                link = link_elem.get("href", "")
                price = price_elem.get_text(strip=True) if price_elem else "N/A"

                # Validação básica: descarta se título ou link estiverem vazios
                if title and link:
                    results.append({
                        "title": title,
                        "price": price,
                        "link": link
                    })

        logging.info(f"{product_name} → {len(results)} resultados capturados")
        return results
