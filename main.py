from scripts.scrape_products import run_scrape_products
from scripts.extract_site_data import run_extract_site_data
from scripts.map_data import run_map_data

def main():
    print(" Étape 1 ")
    run_scrape_products()
    print(" Étape 2 ")
    run_extract_site_data()
    print(" Étape 3 : Mapping ")
    run_map_data()
    print("Fin ")

if __name__ == "__main__":
    main()
