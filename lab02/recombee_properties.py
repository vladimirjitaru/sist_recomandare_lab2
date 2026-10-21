import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItemProperty, ListItemProperties
from recombee_api_client.exceptions import APIException

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def citeste_token():
    """Citeste tokenul privat din variabila de mediu sau din fisierul .env (ignorat de git)"""
    token = os.environ.get('RECOMBEE_PRIVATE_TOKEN')
    if token:
        return token
    try:
        with open(os.path.join(SCRIPT_DIR, '.env'), encoding='utf-8') as f:
            for linie in f:
                cheie, _, valoare = linie.strip().partition('=')
                if cheie == 'RECOMBEE_PRIVATE_TOKEN':
                    return valoare.strip()
    except FileNotFoundError:
        pass
    raise SystemExit("Eroare: setati RECOMBEE_PRIVATE_TOKEN ca variabila de mediu sau in lab02/.env")

# TODO 1: Configurare credentiale Recombee
# Introduceti datele din contul vostru (Settings -> API Logins in Recombee Admin UI)
DB_NAME = 'vladimirjitaru-prod'
PRIVATE_TOKEN = citeste_token()  # Tokenul NU se scrie in cod, ca sa nu ajunga pe GitHub
REGION = 'eu-west'  # Schimbati cu 'us-west' sau regiunea potrivita daca este cazul

# Initializarea clientului Recombee
# SDK-ul asteapta regiunea ca enum (ex.: 'eu-west' -> Region.EU_WEST), nu ca string
client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region[REGION.upper().replace('-', '_')])

# TODO 2: Configurare dataset propriu
# Descarcati un dataset (CSV) de pe Kaggle/data.world (100-10K de intrari)
# Urcati fisierul in acelasi folder cu acest script si setati numele in variabila de mai jos
PATH_DATASET = os.path.join(SCRIPT_DIR, 'imdb_top_1000.csv')

# TODO 3: Definirea schemei de date (minim 3 proprietati)
# Adaptati aceasta lista in functie de coloanele din dataset-ul ales
# Tipurile de date suportate de Recombee includ: 'string', 'int', 'double', 'boolean', 'timestamp'
# (plus 'set' pentru liste de valori si 'image' pentru URL-uri de imagini)
# Dataset: IMDB Top 1000 Movies and TV Shows (Kaggle) - coloana CSV in comentariu
PROPRIETATI_CATALOG = [
    {"name": "title", "type": "string"},          # Series_Title
    {"name": "released_year", "type": "int"},     # Released_Year
    {"name": "certificate", "type": "string"},    # Certificate (ex.: PG-13, R, U)
    {"name": "runtime_min", "type": "int"},       # Runtime ("142 min" -> 142)
    {"name": "genres", "type": "set"},            # Genre ("Crime, Drama" -> ["Crime", "Drama"])
    {"name": "imdb_rating", "type": "double"},    # IMDB_Rating
    {"name": "meta_score", "type": "double"},     # Meta_score
    {"name": "overview", "type": "string"},       # Overview
    {"name": "director", "type": "string"},       # Director
    {"name": "stars", "type": "set"},             # Star1..Star4
    {"name": "num_votes", "type": "int"},         # No_of_Votes
    {"name": "gross", "type": "double"},          # Gross ("28,341,469" -> 28341469.0)
    {"name": "poster_url", "type": "image"},      # Poster_Link
]

def load_dataset():
    """Functie helper care citeste si verifica dataset-ul"""
    try:
        df = pd.read_csv(PATH_DATASET)
        total_randuri = len(df)
        print(f"Dataset incarcat cu succes! Total randuri: {total_randuri}")
        
        # Verificare numar de randuri (100 - 10K)
        if total_randuri < 100:
            print("ATENTIE: Dataset-ul are sub 100 de produse!")
        elif total_randuri > 10 * 1000:
            print("ATENTIE: Dataset-ul este prea mare! Limitati-l la primele 10K randuri.")
            
        print("\nPreview primele 3 randuri:")
        print(df.head(3))
        print("-" * 50)
        return df
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{PATH_DATASET}' nu a fost gasit!")
        return None

def set_properties():
    """Functie care trimite structura coloanelor catre Recombee"""
    print(f"\nIncepe definirea proprietatilor pentru baza de date: '{DB_NAME}'...")
    
    for prop in PROPRIETATI_CATALOG:
        # Validare nume proprietati valide
        if "nume_proprietate" in prop["name"]:
            print("Eroare: Trebuie sa schimbati 'nume_proprietate_x' cu denumirile reale din coloanele fisierul vostru!")
            continue
            
        try:
            # Request API Recombee pentru adaugarea proprietatii (echivalentul adaugarii unei coloane intr-un tabel)
            client.send(AddItemProperty(prop["name"], prop["type"]))
            print(f"Proprietatea '{prop['name']}' ({prop['type']}) a fost adaugata cu succes.")
        except APIException as e:
            # Recombee returnează eroare daca proprietatea a fost deja definita la o rulare anterioara
            if "already exists" in str(e).lower():
                print(f"Proprietatea '{prop['name']}' exista deja in Recombee.")
            else:
                print(f"Eroare API la proprietatea '{prop['name']}': {e}")

def verify():
    """Interogheaza API-ul pentru a lista toate proprietatile active dsin cont"""
    print("Se verifica structura finala din Recombee Admin UI...")
    try:
        atribute_active = client.send(ListItemProperties())
        print("Proprietatile configurate in acest moment in baza ta de date:")
        for atribute in atribute_active:
            print(f"- {atribute['name']} => tip de date: {atribute['type']}")
    except APIException as e:
        print(f"Nu s-a putut efectua verificarea. Detalii eroare: {e}")

if __name__ == "__main__":
    # Verificam daca fisierul CSV local se citeste corect
    dataset_ok = load_dataset()
    
    if dataset_ok is not None:
        # Trimitem proprietatile catre Recombee prin API
        set_properties()
        
        # Listam ce s-a salvat in baza de date pentru confirmare
        verify()
