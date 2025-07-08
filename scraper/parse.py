import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
URL_IDEALISTA = "https://www.idealista.com"

def parse_html(html, div_class="item-info-container"):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("div", class_=div_class)

def extract_data(divs):
    results = []
    for div in divs:
        try:
            chars = div.find("div", class_="item-detail-char").find_all("span", class_="item-detail")
            rooms = chars[0].get_text().split()[0]
            size_m2 = chars[1].get_text().split()[0]
            description = chars[2].get_text().strip()
            price = div.find("span", class_="item-price h2-simulated").get_text().split("€")[0].strip()
            location = div.find("a", class_="item-link").get_text().replace("\n", "").split(",")[:2]
            location = ", ".join([s.strip() for s in location])
            link = URL_IDEALISTA + div.find("a", class_="item-link")["href"]
            results.append({
                "price": price,
                "location": location,
                "size_m2": size_m2,
                "rooms": rooms,
                "description": description,
                "link": link
            })
        except Exception as e:
            logger.warning(f"Error al parsear div: {e}")
    return results
