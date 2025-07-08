# Encapsula Slenium + caching
import os
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from .config import CACHE_DIR

logger = logging.getLogger(__name__)

def fetch_page(url):
    """
    Usa Selenium para descargar el HTML.
    """
    options = Options()
    options.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)
        html = driver.page_source
        return html
    except Exception as e:
        logger.error(f"Error al obtener {url}: {e}")
        return None
    finally:
        driver.quit()

def load_or_fetch_page(url):
    """
    Devuelve HTML desde cache o lo descarga.
    """
    fname = os.path.join(
        CACHE_DIR,
        url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
    )
    if os.path.isfile(fname):
        logger.info(f"Cargando desde cache: {fname}")
        with open(fname, "r", encoding="utf-8") as f:
            return f.read()
    html = fetch_page(url)
    if html:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"Guardado en cache: {fname}")
    return html
