# Garmin Data Collector

# EN

## Description
This script fetches data from a Garmin watch using the `garminconnect` library and stores it in an SQLite database. It analyzes step count, stress levels, and sleep data for the last 30 days and generates daily summaries.

## Requirements

### Python Libraries
Before running the script, install the required dependencies:
```bash
pip install garminconnect pandas sqlite3
```

### Garmin Account
A Garmin account is required to use this script. You need to enter your login credentials in the `email` and `password` variables.

## Installation and Configuration
1. Copy the script to a Python file (`garmin_data.py`).
2. Fill in your Garmin Connect login details:
   ```python
   email = 'your_email'
   password = 'your_password'
   ```
3. Run the script:
   ```bash
   python garmin_data.py
   ```

## How It Works
1. Logs into Garmin Connect and retrieves data from the last 30 days.
2. Creates a local SQLite database `garmin_data.db` and a table `garmin_data_raw`.
3. Fetches and stores:
   - **Steps**
   - **Stress levels**
   - **Sleep** (total sleep time and movement during sleep)
4. Generates daily summaries for the 30-day period.

## Database Structure
The `garmin_data_raw` table contains:
- `id` - unique record identifier
- `date` - date of entry
- `type` - data type (`steps`, `stress`, `sleep_summary`, `sleep_movement`)
- `start_time` - start time of the activity
- `end_time` - end time of the activity
- `value` - recorded value

## Data Analysis
The script calculates:
- Average daily step count
- Maximum steps on a given day
- Average stress level
- Average sleep duration
- Daily activity reports

## Example Output
```
--- SUMMARY OF DATA FOR THE LAST 30 DAYS ---

Daily Step Summary:
Average daily steps: 7500
Highest step count on a single day: 12000 (2024-03-01)

Daily Stress Level Summary (average):
Average stress level: 35.4

Sleep Summary:
Average sleep duration: 7.2 hours
```

## Troubleshooting
- **Login error to Garmin Connect** – check your login credentials.
- **No data in the database** – ensure your Garmin account has recorded data.
- **Incorrect values** – verify that the stored data does not contain anomalies.

## Extensions
You can enhance the script by:
- Fetching additional data (e.g., heart rate, workout activities)
- Exporting data to CSV files
- Visualizing results using `matplotlib` or `seaborn`

## Author
This script was created as part of an analysis of Garmin watch data.

# PL

# Garmin Data Collector

## Opis
Ten skrypt pobiera dane z zegarka Garmin przy użyciu biblioteki `garminconnect` i zapisuje je w bazie danych SQLite. Analizuje dane dotyczące kroków, stresu i snu dla ostatnich 30 dni i generuje dzienne podsumowania.

## Wymagania

### Biblioteki Python
Przed uruchomieniem skryptu należy zainstalować wymagane biblioteki:
```bash
pip install garminconnect pandas sqlite3
```

### Konto Garmin
Do działania skryptu wymagane jest konto Garmin, którego dane logowania należy podać w zmiennych `email` i `password`.

## Instalacja i konfiguracja
1. Skopiuj skrypt do pliku Python (`garmin_data.py`).
2. Uzupełnij swoje dane logowania do Garmin Connect:
   ```python
   email = 'twoj_email'
   password = 'twoje_haslo'
   ```
3. Uruchom skrypt:
   ```bash
   python garmin_data.py
   ```

## Działanie skryptu
1. Loguje się do Garmin Connect i pobiera dane z ostatnich 30 dni.
2. Tworzy lokalną bazę danych `garmin_data.db` i tabelę `garmin_data_raw`.
3. Pobiera i zapisuje:
   - **Kroki**
   - **Poziom stresu**
   - **Sen** (czas snu i ruchy podczas snu)
4. Generuje podsumowanie dla każdego dnia w zakresie 30 dni.

## Struktura bazy danych
Tabela `garmin_data_raw` zawiera:
- `id` - unikalny identyfikator rekordu
- `date` - data zapisu
- `type` - typ danych (`steps`, `stress`, `sleep_summary`, `sleep_movement`)
- `start_time` - czas rozpoczęcia aktywności
- `end_time` - czas zakończenia aktywności
- `value` - wartość pomiaru

## Analiza danych
Skrypt oblicza:
- Średnią dzienną liczbę kroków
- Największą liczbę kroków w danym dniu
- Średni poziom stresu
- Średni czas snu
- Dzienne raporty aktywności

## Przykładowe wyniki
```
--- PODSUMOWANIE DANYCH ZA OSTATNIE 30 DNI ---

Dzienne podsumowanie kroków:
Średnia dzienna liczba kroków: 7500
Największa dzienna liczba kroków: 12000 (2024-03-01)

Dzienne podsumowanie poziomu stresu (średnia):
Średni poziom stresu: 35.4

Podsumowanie snu:
Średni czas snu: 7.2 godz.
```

## Rozwiązywanie problemów
- **Błąd logowania do Garmin Connect** – sprawdź poprawność danych logowania.
- **Brak danych w bazie** – upewnij się, że Twoje konto Garmin ma zapisane dane.
- **Nieprawidłowe wartości** – sprawdź, czy wartości w bazie danych nie zawierają anomalii.

## Rozszerzenia
Możesz rozszerzyć skrypt o:
- Pobieranie dodatkowych danych (np. tętno, aktywności sportowe)
- Eksport danych do pliku CSV
- Wizualizację wyników za pomocą `matplotlib` lub `seaborn`

## Autor
Skrypt został przygotowany jako część analizy danych z zegarków Garmin.



