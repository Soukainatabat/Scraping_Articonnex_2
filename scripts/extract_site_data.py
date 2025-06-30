import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from utils.cleaning import clean_html, extract_dimensions, extract_type_gisement, extract_price_info

def run_extract_site_data():
    df = pd.read_excel("data/raw/all_products2.xlsx").drop_duplicates(subset="id")
    enriched = []

    for _, row in df.iterrows():

        prix, unite, villes_qt, longueur, largeur, epaisseur, type_gisement = extract_price_info(row["product_url"])
        time.sleep(0.5)

        base = row.to_dict()
        base.update({
            "prix": prix,
            "unite": unite,
            "longueur": longueur,
            "largeur": largeur,
            "epaisseur": epaisseur,
            "Type": type_gisement
        })

        if villes_qt:
            for ville, qte in villes_qt:
                ligne = base.copy()
                ligne.update({"ville": ville, "quantite": qte})
                enriched.append(ligne)
        else:
            base.update({"ville": None, "quantite": None})
            enriched.append(base)

    pd.DataFrame(enriched).to_excel("data/processed/scraping_with_dimensions.xlsx", index=False)
