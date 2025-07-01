
Scraping 2/
├── data/
│   ├── raw/           # Données brutes extraites scraping
│   ├── processed/     # Données nettoyées/enrichies
│   └── export/        # Résultats finaux exportés
├── scripts/           # Scripts principaux du pipeline
│   ├── scrape_products.py
│   ├── extract_site_data.py
│   └── map_data.py
├── utils/             # Fonctions utilitaires (nettoyage, config...)
│   ├── cleaning.py
│   ├── config.py
│   └── map_data.py
├── requirements.txt   # Liste des dépendances Python
├── README.md          # Documentation du projet
└── main.py            # Script principal pour exécuter le pipeline


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
