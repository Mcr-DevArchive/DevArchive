# 🏠 Idealista Scraper

Un scraper modular en Python para Idealista, con notificación opcional por Telegram.

## 🚀 Características
- Usa Selenium + BeautifulSoup para scrapear datos de inmuebles.
- Cachea las páginas localmente para evitar sobrecargar el sitio.
- Guarda resultados en CSV.
- Envía los datos a un chat de Telegram opcionalmente.

## 🛠 Requisitos
- Python 3.8+
- Firefox instalado

## ⚙ Instalación
```bash
pip install -r requirements.txt
```

🔧 Configuración

Crea un archivo .env en el raíz con:

```
TELEGRAM_TOKEN=<tu_token_aqui>
TELEGRAM_CHAT_ID=<tu_chat_id_aqui>
CACHE_DIR=./cached_pages
```

🚀 Uso

```bash
python -m scraper.main --pages 1 2 3 4 5 --send-telegram
```

Donde:

- `--pages`: lista de páginas a scrapear.
- `--send-telegram`: si se indica, enviará los resultados por Telegram.

🚀 Estructura

- `scraper/fetch.py` → descarga HTML con Selenium
- `scraper/parse.py` → parsea los datos con BeautifulSoup
- `scraper/notify.py` → envía mensajes por Telegram
- `scraper/main.py → CLI principal

# 🚀 Cómo inicializar un repositorio

Cuando todos los archivos esten en la carpeta `idealista-scraper/`, hacer:

```bash
cd idealista-scraper
git init
git add .
git commit -m "Proyecto inicial: scraper idealista modular con Telegram"
```

## Subirlo a GitHub

```bash
gh repo create idealista-scraper --public --source=. --remote=origin
git push -u origin main
```
