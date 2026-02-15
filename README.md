📦 Mercado Livre Scraper

Um scraper simples e robusto para coletar informações de produtos no Mercado Livre, com interface gráfica em PyQt6, persistência em SQLite, processamento paralelo com ThreadPoolExecutor e exportação para Excel/CSV.
🚀 Objetivo

Exercitar boas práticas em Python para criar softwares pequenos, organizados e escaláveis.
Este projeto serve como base para entender arquitetura, modularização e testes em automações.

📂 Estrutura do Projeto

web-scraper/

├── main.py                # Ponto de entrada <br>
├── data/                  # Dados de entrada/saída<br>
│   ├── produtos.xlsx<br>
│   ├── resultados.xlsx<br>
│   └── produtos.db<br>
├── src/                   # Código-fonte<br>
│   ├── gui.py             # Interface PyQt6<br>
│   ├── worker_manager.py  # Coordenação de threads + retries<br>
│   ├── web_scraper.py     # Scraper Mercado Livre<br>
│   ├── db_manager.py      # Banco SQLite + lock<br>
│   └── excel_manager.py   # Entrada/saída Excel<br>
├── tests/                 # Testes automatizados<br>
│   ├── conftest.py        # Fixtures globais (db, excel fake, etc.)<br>
│   ├── test_db_manager.py<br>
│   ├── test_excel_manager.py<br>
│   ├── test_web_scraper.py<br>
│   └── test_worker_manager.py<br>
├── requirements.txt       # Dependências<br>
└── README.md              # Documentação


⚙️ Fluxo de funcionamento

    Entrada

        Usuário fornece produtos.xlsx com coluna Produto.

        Produtos são carregados no banco (DBManager).

    Processamento paralelo

        WorkerManager cria threads para scraping.

        Resultados brutos vão para fila (result_queue).

    Validação e salvamento

        Thread dedicada consome fila e salva no banco.

        Resultados inválidos vão para retry.

    Retry automático

        Até 3 tentativas para produtos inválidos.

        Produtos não resolvidos são logados.

    Saída

        ExcelManager exporta resultados válidos para resultados.xlsx ou .csv.

    Encerramento

        GUI fecha conexão do banco ao sair.

📚 Tecnologias utilizadas

    PyQt6 → interface gráfica.

    pandas → leitura/escrita de Excel/CSV.

    sqlite3 → banco local persistente.

    threading + ThreadPoolExecutor → concorrência controlada.

    queue.Queue → comunicação entre threads.

    logging → feedback em tempo real.

    requests + BeautifulSoup → scraping.

🧪 Testes (boas práticas)

    conftest.py

        Fixtures para banco em memória (sqlite3.connect(":memory:")).

        Excel fake com pandas.DataFrame.

        Uso de faker para dados falsos.

    Testes unitários

        test_db_manager.py: inserção, consulta e limpeza.

        test_excel_manager.py: leitura e exportação.

        test_web_scraper.py: parsing de HTML fake (mock de requests).

        test_worker_manager.py: retries e fluxo de salvamento.

    Cenários de erro

        Excel sem coluna Produto.

        Banco vazio.

        Scraper sem resultados.

        Timeout em requisição.

📖 Boas práticas aplicadas

    Separação de responsabilidades (entrada, persistência, processamento, saída).

    Concorrência controlada com fila producer–consumer.

    Validação e retries automáticos.

    Logging estruturado.

    Tipagem e docstrings para clareza.

    Testes cobrindo sucesso e erro.

    🛠️ Como rodar

Instale dependências:

pip install -r requirements.txt

Execute a aplicação:

python main.py

📦 Distribuição

Para gerar executável para terceiros:

pyinstaller --onefile main.py

Usuário só precisa fornecer produtos.xlsx com coluna Produto.
Saída será resultados.xlsx com colunas Produto | Título | Preço | Link.
🧭 Roadmap de evolução

    Estrutura organizada com src/, data/, tests/.

    Documentação clara em README.md.

    Testes cobrindo cenários de sucesso e erro.

    Aplicar lint/format (black, flake8).

    Empacotar executável para terceiros.

    Modularizar para reaproveitar fluxo em outras automações.
