# Laborator 2 - Dataset: IMDB Top 1000 Movies and TV Shows

## Domeniul ales

**Filme.** Sistemul de recomandare va sugera filme utilizatorilor pe baza genului, regizorului, actorilor, rating-ului și a descrierii acțiunii.

## Sursa

- **Dataset:** [IMDB Movies Dataset - Top 1000 Movies and TV Shows](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows) (Kaggle)
- **Fișier:** [`imdb_top_1000.csv`](imdb_top_1000.csv)
- **Volum:** 1000 de filme (cele mai bine cotate filme pe IMDB), 16 coloane

## Proprietăți înregistrate în Recombee

| Proprietate Recombee | Coloana din CSV | Tip | Descriere |
| --- | --- | --- | --- |
| `title` | `Series_Title` | `string` | Titlul filmului |
| `released_year` | `Released_Year` | `int` | Anul lansării |
| `certificate` | `Certificate` | `string` | Clasificarea de vârstă (ex.: `PG-13`, `R`, `U`) |
| `runtime_min` | `Runtime` | `int` | Durata în minute (`"142 min"` → `142`) |
| `genres` | `Genre` | `set` | Genurile filmului (`"Crime, Drama"` → `["Crime", "Drama"]`) |
| `imdb_rating` | `IMDB_Rating` | `double` | Rating-ul IMDB (0-10) |
| `meta_score` | `Meta_score` | `double` | Scorul criticilor pe Metacritic (0-100) |
| `overview` | `Overview` | `string` | Scurtă descriere a acțiunii |
| `director` | `Director` | `string` | Regizorul |
| `stars` | `Star1`-`Star4` | `set` | Primii 4 actori din distribuție |
| `num_votes` | `No_of_Votes` | `int` | Numărul de voturi pe IMDB |
| `gross` | `Gross` | `double` | Încasările în USD (`"28,341,469"` → `28341469.0`) |
| `poster_url` | `Poster_Link` | `image` | URL-ul posterului |

**Identificatorul produsului:** dataset-ul nu are o coloană de ID. Acesta nu se înregistrează ca proprietate; la încărcarea produselor (laboratorul 3) fiecare film va primi un `itemId` generat (ex.: `movie_0001`).

## Observații despre date

- `Certificate` lipsește la 101 filme, `Meta_score` la 157, iar `Gross` la 169; acestea vor fi trimise ca `null`.
- `Released_Year` are o valoare greșită: filmul *Apollo 13* are `PG` în loc de `1995`.

## Rulare script

1. Activați mediul virtual și instalați dependențele:
   ```
   pip install recombee-api-client pandas
   ```
2. Setați tokenul privat Recombee (Settings → API Logins) fie ca variabilă de mediu `RECOMBEE_PRIVATE_TOKEN`, fie într-un fișier `lab02/.env` (ignorat de git):
   ```
   RECOMBEE_PRIVATE_TOKEN=tokenul_vostru_privat
   ```
3. Rulați:
   ```
   python lab02/recombee_properties.py
   ```
