# CLI + orquestación.
import argparse
import csv
import json
import logging
import time
from random import randint
from . import fetch, parse, notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def random_sleep(min_s=2, max_s=10):
    s = randint(min_s, max_s)
    logging.info(f"Dormimos {s}s para no ser detectados.")
    time.sleep(s)

def get_url_for_page(page):
    return (
        "https://www.idealista.com/venta-viviendas/madrid/zona-norte/"
        "con-precio-hasta_220000,metros-cuadrados-mas-de_60,"
        "solo-pisos,publicado_ultima-semana,ultimas-plantas,"
        "plantas-intermedias,para-reformar,buen-estado,sin-inquilinos/"
        f"pagina-{page}.htm"
    )

def save_to_csv(data, path):
    if not data:
        logging.warning("No hay datos para guardar.")
        return
    campos = data[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    logging.info(f"CSV guardado: {path}")

import json

def save_to_json(data, json_path: str):
    """
    Saves the list of dictionaries as a JSON file.
    """
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"JSON file created successfully: {json_path}")

def send_csv_to_telegram(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            texto = (
                f"Precio: {fila.get('price','–')}\n"
                f"Localidad: {fila.get('location','–')}\n"
                f"Tamaño (m²): {fila.get('size_m2','–')}\n"
                f"Habitaciones: {fila.get('rooms','–')}\n"
                f"Descripción: {fila.get('description','–')}\n"
                f"Link: {fila.get('link','–')}"
            )
            notify.send_message(texto)
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Scraper Idealista con Telegram")
    parser.add_argument("--pages", nargs="+", type=int, default=[1,2,3,4,5],
                        help="Páginas a scrapear")
    parser.add_argument("--send-telegram", action="store_true",
                        help="Enviar resultados por Telegram")
    args = parser.parse_args()

    properties = []
    for num in args.pages:
        url = get_url_for_page(num)
        html = fetch.load_or_fetch_page(url)
        if not html:
            continue
        divs = parse.parse_html(html)
        datos = parse.extract_data(divs)
        properties.extend(datos)
        random_sleep()

    save_to_csv(properties, "properties.csv")

    save_to_json(properties, "properties.json")

    if args.send_telegram:
        send_csv_to_telegram("properties.csv")

if __name__ == "__main__":
    main()
