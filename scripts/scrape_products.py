import requests
import json
from bs4 import BeautifulSoup
import re 


def extract_ean_from_handle(handle):
    match = re.search(r'ean-(\d+)', handle)
    return match.group(1) if match else "EAN indisponible"  

def run_scrape_products():
    url = "https://articonnex.com/collections"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    handles = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/collections/") and href.count("/") == 2:
            handle = href.split("/")[-1]
            handles.add(handle)

    handles = sorted(handles)
    with open("data/raw/collection_handles.json", "w", encoding="utf-8") as f:
        json.dump(handles, f, ensure_ascii=False, indent=2)

    all_products = []
    for handle in handles:
        print(f"🔍 Collection : {handle}")
        url = f"https://articonnex.com/collections/{handle}/products.json?limit=250"
        while url:
            res = requests.get(url)
            if res.status_code != 200:
                break
            data = res.json()
            for p in data.get("products", []):
                variant = p.get("variants", [{}])[0]
                all_products.append({
                    "collection": handle,
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "vendor": p.get("vendor"),
                    "product_type": p.get("product_type"),
                    "handle": p.get("handle"),
                    "created_at": p.get("created_at"),
                    "price": variant.get("price"),
                    "available": "VRAI" if variant.get("available") else "FAUX",
                    "product_url": f"https://articonnex.com/products/{p.get('handle')}.js",
                    "description": p.get("body_html", ""),
                    "ean": str(variant.get("barcode")).strip() if variant.get("barcode") else extract_ean_from_handle(p.get("handle", "")),
                    "ref_articonnex": variant.get("sku"),
                    "tags": ", ".join(p.get("tags", [])),
                    "stock_quantity": variant.get("inventory_quantity"),
                    "images": ", ".join(img.get("src", "") for img in p.get("images", []))
                })
            link = res.headers.get("Link", "")
            if 'rel="next"' in link:
                next_url = [part.split(";")[0].strip()[1:-1] for part in link.split(",") if 'rel="next"' in part][0]
                url = next_url
            else:
                break

    import pandas as pd
    df = pd.DataFrame(all_products).drop_duplicates(subset="id")
    df.to_excel("data/raw/all_products2.xlsx", index=False)
