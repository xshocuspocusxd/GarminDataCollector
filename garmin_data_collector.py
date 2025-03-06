from garminconnect import Garmin
from datetime import datetime, timedelta
import sqlite3
import pandas as pd

# Dane logowania do Garmin
email = 'your_email_login_to_garmin_connect'
password = 'your_password_to_garmin_connect'

# Połączenie z Garmin Connect
client = Garmin(email, password)
client.login()

# Określenie zakresu dat (ostatnie 30 dni)
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

# Połączenie z bazą danych SQLite
conn = sqlite3.connect('garmin_data.db')
cursor = conn.cursor()

# Tworzenie tabeli na dane RAW (jeśli nie istnieje)
cursor.execute('''
CREATE TABLE IF NOT EXISTS garmin_data_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    start_time TEXT,
    end_time TEXT,
    value REAL
)
''')
conn.commit()

# Funkcja zapisu danych kroków
def save_steps_data(date_str):
    try:
        steps_data = client.get_steps_data(date_str)
        for record in steps_data:
            cursor.execute('''
            INSERT INTO garmin_data_raw (date, type, start_time, end_time, value)
            VALUES (?, ?, ?, ?, ?)
            ''', (date_str, 'steps', record['startGMT'], record['endGMT'], record['steps']))
        conn.commit()
        print(f"Zapisano dane kroków dla {date_str}")
    except Exception as e:
        print(f"Błąd podczas pobierania danych kroków dla {date_str}: {e}")

# Funkcja zapisu danych stresu
def save_stress_data(date_str):
    try:
        stress_data = client.get_stress_data(date_str)
        stress_array = stress_data['stressValuesArray']
        for timestamp, stress_level in stress_array:
            if stress_level >= 0:  # Pomijamy wartości -1 i -2 jako nieprawidłowe
                timestamp_gmt = datetime.utcfromtimestamp(timestamp / 1000)  # Konwersja z ms do datetime
                cursor.execute('''
                INSERT INTO garmin_data_raw (date, type, start_time, end_time, value)
                VALUES (?, ?, ?, ?, ?)
                ''', (date_str, 'stress', timestamp_gmt, timestamp_gmt, stress_level))
        conn.commit()
        print(f"Zapisano dane stresu dla {date_str}")
    except Exception as e:
        print(f"Błąd podczas pobierania danych stresu dla {date_str}: {e}")

# Funkcja zapisu głównych danych snu
def save_sleep_data(date_str):
    try:
        sleep_data = client.get_sleep_data(date_str)
        
        # Główne podsumowanie snu
        sleep_summary = sleep_data.get('dailySleepDTO')
        if sleep_summary:
            sleep_start = datetime.utcfromtimestamp(sleep_summary['sleepStartTimestampGMT'] / 1000)
            sleep_end = datetime.utcfromtimestamp(sleep_summary['sleepEndTimestampGMT'] / 1000)
            cursor.execute('''
            INSERT INTO garmin_data_raw (date, type, start_time, end_time, value)
            VALUES (?, ?, ?, ?, ?)
            ''', (date_str, 'sleep_summary', sleep_start, sleep_end, sleep_summary['sleepTimeSeconds']))
        
        # Dane ruchu podczas snu
        sleep_movements = sleep_data.get('sleepMovement', [])
        for movement in sleep_movements:
            cursor.execute('''
            INSERT INTO garmin_data_raw (date, type, start_time, end_time, value)
            VALUES (?, ?, ?, ?, ?)
            ''', (date_str, 'sleep_movement', movement['startGMT'], movement['endGMT'], movement['activityLevel']))
        
        conn.commit()
        print(f"Zapisano dane snu dla {date_str}")
    except Exception as e:
        print(f"Błąd podczas pobierania danych snu dla {date_str}: {e}")

# Pobieranie danych dla każdego dnia w zakresie 30 dni
current_date = datetime.strptime(start_date, '%Y-%m-%d')
end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

print(f"Rozpoczynam pobieranie danych od {start_date} do {end_date}")

while current_date <= end_datetime:
    current_date_str = current_date.strftime('%Y-%m-%d')
    print(f"\nPobieranie danych dla {current_date_str}")
    
    # Pobieranie różnych typów danych dla bieżącego dnia
    save_steps_data(current_date_str)
    save_stress_data(current_date_str)
    save_sleep_data(current_date_str)
    
    # Przejście do następnego dnia
    current_date += timedelta(days=1)

print("\nZakończono pobieranie danych za ostatnie 30 dni")

# Funkcja pobierania danych z bazy dla zakresu dat
def fetch_data_range(data_type, start_date, end_date):
    cursor.execute('''
    SELECT date, start_time, end_time, value 
    FROM garmin_data_raw 
    WHERE type = ? AND date BETWEEN ? AND ?
    ''', (data_type, start_date, end_date))
    
    raw_data = cursor.fetchall()
    df = pd.DataFrame(raw_data, columns=['date', 'start_time', 'end_time', 'value'])
    df['date'] = pd.to_datetime(df['date'])
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    return df

# Funkcja generująca dzienne podsumowania
def generate_daily_summary(data_type, agg_func='sum'):
    df = fetch_data_range(data_type, start_date, end_date)
    
    if df.empty:
        print(f"Brak danych typu {data_type} w wybranym okresie")
        return pd.DataFrame()
    
    if agg_func == 'sum':
        daily = df.groupby('date')['value'].sum().reset_index()
    elif agg_func == 'mean':
        daily = df.groupby('date')['value'].mean().reset_index()
    elif agg_func == 'max':
        daily = df.groupby('date')['value'].max().reset_index()
    elif agg_func == 'min':
        daily = df.groupby('date')['value'].min().reset_index()
    
    return daily

# Generowanie podsumowań
print("\n--- PODSUMOWANIE DANYCH ZA OSTATNIE 30 DNI ---")

# Podsumowanie kroków
steps_summary = generate_daily_summary('steps', 'sum')
if not steps_summary.empty:
    print("\nDzienne podsumowanie kroków:")
    avg_steps = steps_summary['value'].mean()
    max_steps = steps_summary['value'].max()
    max_steps_date = steps_summary.loc[steps_summary['value'].idxmax(), 'date'].strftime('%Y-%m-%d')
    
    print(f"Średnia dzienna liczba kroków: {avg_steps:.0f}")
    print(f"Największa dzienna liczba kroków: {max_steps:.0f} ({max_steps_date})")
    
    # Wyświetlenie danych dla każdego dnia
    for _, row in steps_summary.iterrows():
        print(f"{row['date'].strftime('%Y-%m-%d')}: {row['value']:.0f} kroków")

# Podsumowanie stresu
stress_summary = generate_daily_summary('stress', 'mean')
if not stress_summary.empty:
    print("\nDzienne podsumowanie poziomu stresu (średnia):")
    avg_stress = stress_summary['value'].mean()
    
    print(f"Średni poziom stresu w okresie 30 dni: {avg_stress:.2f}")
    
    # Wyświetlenie danych dla każdego dnia
    for _, row in stress_summary.iterrows():
        stress_level = row['value']
        if stress_level <= 20:
            stress_desc = "niski"
        elif stress_level <= 40:
            stress_desc = "średni"
        elif stress_level <= 60:
            stress_desc = "wysoki"
        else:
            stress_desc = "bardzo wysoki"
        print(f"{row['date'].strftime('%Y-%m-%d')}: {stress_level:.2f} ({stress_desc})")

# Podsumowanie snu
sleep_summary = fetch_data_range('sleep_summary', start_date, end_date)
if not sleep_summary.empty:
    print("\nPodsumowanie snu:")
    avg_sleep_time = sleep_summary['value'].mean() / 3600  # Konwersja sekund na godziny
    
    print(f"Średni czas snu w okresie 30 dni: {avg_sleep_time:.2f} godz.")
    
    # Wyświetlenie danych dla każdego dnia
    for _, row in sleep_summary.iterrows():
        sleep_hours = row['value'] / 3600
        print(f"{row['date'].strftime('%Y-%m-%d')}: {sleep_hours:.2f} godz.")

# Zamknięcie połączenia z bazą danych
conn.close()
print("\nZakończono przetwarzanie danych.")
