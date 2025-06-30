import pandas as pd
from utils.cleaning import clean_html
from utils.config import unit_map, source_map, location_id_map
from utils.cleaning import nettoyer_prix, clean_images

def run_map_data():
    df = pd.read_excel("data/processed/scraping_with_dimensions.xlsx")
    df["images"] = df["images"].apply(clean_images)

    mapped = []
    for _, row in df.iterrows():
        ville = str(row.get("ville", "")).strip()
        unite = str(row.get("unite", "")).strip().lower()

        item = {
            "deposit_location_id": location_id_map.get(ville),
            "name": row.get("title", ""),
            "quantity": row.get("quantite", ""),
            "unit": unit_map.get(unite, 0),
            "availability_date": pd.to_datetime("today").strftime("%Y-%m-%d"),
            "availability_expiration": None,
            "condition": None,
            "description": clean_html(row.get("description", "")),
            "comments": row.get("ean", ""),
            "deposit_demountability": None,
            "images": row.get("images", ""),
            "deposit_source": source_map.get(str(row.get("Type", "")).strip(), None),
            "price": nettoyer_prix(row.get("prix", 0)),
            "length": float(str(row.get("longueur", "0")).replace("mm", "").replace(",", ".") or 0),
            "width": float(str(row.get("largeur", "0")).replace("mm", "").replace(",", ".") or 0),
            "height": float(str(row.get("epaisseur", "0")).replace("mm", "").replace(",", ".") or 0),
            "conversion": None,
            "id_articonnex": row.get("ref_articonnex", ""),
            "url_link": row.get("product_url", ""),
            "product_comment": None,
            "potential_reuse": True
        }
        mapped.append(item)

    df_export = pd.DataFrame(mapped)
    df_export.to_excel("data/export/mapping12.xlsx", index=False)
    df_export.to_json("data/export/mapping12.json", orient="records", force_ascii=False, indent=2)
