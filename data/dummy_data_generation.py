import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def insert_initial_data(conn):
    """Insert the base data for locations, sub-locations, and pollutants if they don't exist"""
    # Insert locations if they don't exist
    locations = [
        ('Oxford',),
        ('SODC',),  # South Oxfordshire District Council
        ('VOWH',),  # Vale of White Horse
    ]
    for location in locations:
        conn.execute('INSERT OR IGNORE INTO locations (name) VALUES (?)', location)

    # Insert sub-locations if they don't exist
    sub_locations = [
        (1, 'High Street'),
        (1, 'St Aldates'),
        (1, 'St Ebbes'),
        (2, 'Henley Duke St'),
        (2, 'Wallingford High St'),
        (2, 'Watlington High St'),
        (3, 'Abingdon Stert St'),
    ]
    for sub_location in sub_locations:
        conn.execute('INSERT OR IGNORE INTO sub_locations (location_id, name) VALUES (?, ?)', sub_location)

    # Insert pollutants if they don't exist
    pollutants = [
        ('Nitric Oxide',),
        ('Nitrogen dioxide',),
        ('Oxides of Nitrogen',),
        ('PM10 Particulate matter',),
        ('PM2.5 Particulate matter',),
        ('Ozone',),
    ]
    for pollutant in pollutants:
        conn.execute('INSERT OR IGNORE INTO pollutants (name) VALUES (?)', pollutant)

def generate_measurement(base_value, date_factor):
    """Generate a realistic measurement with some variation"""
    # Add seasonal variation (higher in winter)
    seasonal = np.sin(date_factor * 2 * np.pi + np.pi) * 10
    # Add random noise
    noise = np.random.normal(0, base_value * 0.2)
    return max(1, base_value + seasonal + noise)

def generate_measurements(conn, start_date, end_date):
    """Generate measurements for all locations and pollutants"""
    # Get all sub_locations and pollutants
    sub_locations = conn.execute('SELECT sub_location_id FROM sub_locations').fetchall()
    pollutants = conn.execute('SELECT pollutant_id FROM pollutants').fetchall()

    # Check existing dates to avoid duplicates
    existing_dates = set(row[0] for row in conn.execute(
        'SELECT DISTINCT measured_at FROM measurements'
    ).fetchall())

    measurements = []
    dates = pd.date_range(start_date, end_date, freq='D')

    # Base values for different pollutants (based on sample data)
    base_values = {
        1: 15,  # Nitric Oxide
        2: 25,  # Nitrogen dioxide
        3: 40,  # Oxides of Nitrogen
        4: 10,  # PM10
        5: 5,   # PM2.5
        6: 50,  # Ozone
    }

    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        if date_str in existing_dates:
            continue

        # Date factor for seasonal variation (0 to 1)
        date_factor = (date.dayofyear - 1) / 365.0

        for sub_loc in sub_locations:
            for poll in pollutants:
                # Skip Ozone for locations that don't measure it
                if poll[0] == 6 and sub_loc[0] != 3:  # St Ebbes only
                    continue

                value = generate_measurement(base_values[poll[0]], date_factor)
                status = 'P' if np.random.random() > 0.3 else 'V'  # 70% P, 30% V

                measurements.append((
                    sub_loc[0],
                    poll[0],
                    round(value, 1),
                    f"{status} µg/m³",
                    date_str
                ))

    # Insert in batches
    batch_size = 100
    for i in range(0, len(measurements), batch_size):
        batch = measurements[i:i + batch_size]
        conn.executemany('''
            INSERT INTO measurements 
            (sub_location_id, pollutant_id, value, status, measured_at)
            VALUES (?, ?, ?, ?, ?)
        ''', batch)

def main():
    # Connect to existing database
    conn = sqlite3.connect('air.db')

    try:
        # Make sure reference data exists
        insert_initial_data(conn)

        # Generate measurements for the past year
        end_date = datetime.now()
        start_date = datetime(2023, 1, 1)  # Starting from January 1, 2023

        generate_measurements(conn, start_date, end_date)

        # Commit all changes
        conn.commit()
        print(f"Successfully generated data from {start_date.date()} to {end_date.date()}")

        # Print some stats
        cursor = conn.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM measurements').fetchone()[0]
        print(f"Total number of measurements in database: {count}")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
