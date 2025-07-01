from bs4 import BeautifulSoup
import requests
import pandas as pd

def clean_html(html):
    if pd.isna(html):
        return ""
    return BeautifulSoup(str(html), "html.parser").get_text(separator=" ", strip=True)
  

def nettoyer_prix(val):
    try:
        return float(str(val).replace("€", "").replace(" ", "").replace(",", ".").strip())
    except:
        return 0.0

def clean_images(images_cell):
    if not images_cell:
        return []
    return [url.strip().split("?")[0] for url in str(images_cell).split(",") if url.startswith("http")]

def extract_dimensions(soup):
    longueur = largeur = epaisseur = None
    bloc = soup.find("div", class_="mm-wrapper-desc-caracteristiques")
    if bloc:
        for d in bloc.find_all("div", class_="mm-cp-text-car mm-flex"):
            label = d.get_text(strip=True).lower()
            val = d.find("span").get_text(strip=True) if d.find("span") else ""
            if "longueur" in label:
                longueur = val
            elif "largeur" in label:
                largeur = val
            elif "épaisseur" in label or "epaisseur" in label:
                epaisseur = val
    return longueur, largeur, epaisseur

def extract_type_gisement(soup):
    type_div = soup.find("div", class_="mm-p-collection")
    return type_div.get_text(strip=True) if type_div else None

def extract_price_info(url):
    try:
        res = requests.get(url.replace(".js", ""), timeout=10)
        if res.status_code != 200:
            return None, None, [], None, None, None, None

        soup = BeautifulSoup(res.content, "html.parser")

        prix_tag = soup.find("span", class_="mm-price-unity")
        prix = prix_tag.get_text(strip=True) if prix_tag else ""
        unite = "unité"

        stock_bloc = soup.find("div", class_="mm-product-availability")
        villes_qt = []
        if stock_bloc:
            for ligne in stock_bloc.find_all("p", class_="mm-store-produit"):
                spans = ligne.find_all("span")
                if len(spans) >= 2:
                    villes_qt.append((
                        spans[0].get_text(strip=True),
                        spans[1].get_text(strip=True)
                    ))

        l, L, e = extract_dimensions(soup)
        type_gisement = extract_type_gisement(soup)

        return prix, unite, villes_qt, l, L, e, type_gisement

    except Exception:
        return None, None, [], None, None, None, None
