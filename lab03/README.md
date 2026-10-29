# Laborator 3 - Încărcarea filmelor în Recombee

Dataset-ul și proprietățile definite în Recombee sunt descrise în [Laboratorul 2](../lab02/README.md).

## Rezultat

✅ **Datele au fost încărcate cu succes în Recombee:** toate cele **1000 de filme** din `imdb_top_1000.csv` se află în catalogul bazei de date `vladimirjitaru-prod`, cu cele 13 proprietăți completate.

Verificare:
- **Recombee Admin UI** → *Items*: apar 1000 de item-uri (`movie_0001` … `movie_1000`) cu atributele completate.
- **API** (`ListItems`): 1000 de item-uri; ex.: `movie_0001` → *The Shawshank Redemption*, 1994, `["Drama"]`.

## Identificatorul unic (`itemId`)

Dataset-ul nu are o coloană de ID, așa că `itemId` este generat din poziția rândului în CSV:

| Rând CSV | `itemId` | Film |
| --- | --- | --- |
| 1 | `movie_0001` | The Shawshank Redemption |
| 2 | `movie_0002` | The Godfather |
| … | … | … |
| 1000 | `movie_1000` | The 39 Steps |

## Maparea coloanelor CSV → proprietăți Recombee

| Coloana CSV | Proprietate | Tip | Prelucrare |
| --- | --- | --- | --- |
| `Series_Title` | `title` | `string` | - |
| `Released_Year` | `released_year` | `int` | *Apollo 13* are `PG` în CSV → corectat la `1995` |
| `Certificate` | `certificate` | `string` | lipsește la 101 filme → netrimis |
| `Runtime` | `runtime_min` | `int` | `"142 min"` → `142` |
| `Genre` | `genres` | `set` | `"Crime, Drama"` → `["Crime", "Drama"]` |
| `IMDB_Rating` | `imdb_rating` | `double` | - |
| `Meta_score` | `meta_score` | `double` | lipsește la 157 de filme → netrimis |
| `Overview` | `overview` | `string` | - |
| `Director` | `director` | `string` | - |
| `Star1`-`Star4` | `stars` | `set` | cele 4 coloane → o listă |
| `No_of_Votes` | `num_votes` | `int` | - |
| `Gross` | `gross` | `double` | `"28,341,469"` → `28341469.0`; lipsește la 169 de filme → netrimis |
| `Poster_Link` | `poster_url` | `image` | - |

Valorile lipsă nu sunt trimise, iar în Recombee proprietățile respective rămân goale.

## Trimiterea în Recombee

Script: [`recombee_items.py`](recombee_items.py)

- Fiecare film devine o cerere `SetItemValues` cu `cascade_create=True`, care creează item-ul dacă nu există încă în catalog.
- Cererile sunt grupate în loturi de câte **100** și trimise cu `Batch`: **10 cereri HTTP** în loc de 1000.
- Pentru fiecare lot se verifică codul de răspuns al fiecărui item, deoarece `Batch` răspunde cu `200` chiar dacă unele cereri individuale eșuează.

## Rulare

1. Activați mediul virtual și instalați dependențele:
   ```
   pip install recombee-api-client pandas
   ```
2. Tokenul privat Recombee se citește din variabila de mediu `RECOMBEE_PRIVATE_TOKEN` sau din fișierul `lab02/.env` (ignorat de git):
   ```
   RECOMBEE_PRIVATE_TOKEN=tokenul_vostru_privat
   ```
3. Rulați:
   ```
   python lab03/recombee_items.py
   ```

Rularea repetată nu creează duplicate: același film primește mereu același `itemId`, iar valorile lui sunt doar actualizate.
