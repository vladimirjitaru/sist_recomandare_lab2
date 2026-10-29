import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

LAB02_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab02')

def citeste_token():
    token = os.environ.get('RECOMBEE_PRIVATE_TOKEN')
    if not token:
        with open(os.path.join(LAB02_DIR, '.env'), encoding='utf-8') as f:
            token = dict(linie.strip().split('=', 1) for linie in f if '=' in linie)['RECOMBEE_PRIVATE_TOKEN']
    return token

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = 'vladimirjitaru-prod'
PRIVATE_TOKEN = citeste_token()
REGION = 'eu-west'

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region[REGION.upper().replace('-', '_')])

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = os.path.join(LAB02_DIR, 'imdb_top_1000.csv')

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []
    erori = 0

    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        item_id = f"movie_{index + 1:04d}"

        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        properties = {
            "title": str(row['Series_Title']),
            "released_year": 1995 if row['Released_Year'] == 'PG' else int(row['Released_Year']),
            "certificate": str(row['Certificate']) if pd.notna(row['Certificate']) else None,
            "runtime_min": int(row['Runtime'].replace(' min', '')),
            "genres": [gen.strip() for gen in row['Genre'].split(',')],
            "imdb_rating": float(row['IMDB_Rating']),
            "meta_score": float(row['Meta_score']) if pd.notna(row['Meta_score']) else None,
            "overview": str(row['Overview']),
            "director": str(row['Director']),
            "stars": [row['Star1'], row['Star2'], row['Star3'], row['Star4']],
            "num_votes": int(row['No_of_Votes']),
            "gross": float(row['Gross'].replace(',', '')) if pd.notna(row['Gross']) else None,
            "poster_url": str(row['Poster_Link']),
        }
        properties = {nume: valoare for nume, valoare in properties.items() if valoare is not None}

        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            raspunsuri = client.send(Batch(requests))
            erori += sum(1 for raspuns in raspunsuri if raspuns['code'] >= 300)
            requests = []
            print("S-a trimis un lot de 100 item-uri...")

    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        raspunsuri = client.send(Batch(requests))
        erori += sum(1 for raspuns in raspunsuri if raspuns['code'] >= 300)
        print("S-a trimis ultimul lot de item-uri.")

    if erori == 0:
        print("Toate item-urile au fost trimise cu succes!")
    else:
        print(f"ATENTIE: {erori} item-uri au fost respinse de Recombee.")

if __name__ == "__main__":
    send_items()
