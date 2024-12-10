from flask import g
import sqlite3
from cs50 import SQL


# Function to create the database connection, using
def get_db():
    """
    Gets or creates a database connection for the current request.

    Uses Flask's application context `g` object to store the database connection,
    ensuring only one connection per request context. If a connection doesn't
    exist, creates a new one using CS50's SQL library.

    Returns:
        SQL: A CS50 SQL database connection object pointing to the AirAware SQLite database.
            The same connection is returned for multiple calls within the same request.

    Note:
        This function requires Flask's application context to be active, as it uses
        the `g` object for connection storage. The connection is automatically
        managed by CS50's SQL library, which handles connection pooling and cleanup.
    """
    if 'db' not in g:
        # g.db = sqlite3.connect("data/air.db")
        g.db = SQL("sqlite:///data/air.db")
    return g.db


def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None, date=None):
    query = '''
            SELECT
                locations.name as loc_name,
                sub_locations.name as sub_name,
                pollutants.name as pollutant_name,
                value,
                status,
                measured_at
            FROM measurements
            JOIN sub_locations ON sub_locations.sub_location_id = measurements.sub_location_id
            JOIN locations ON locations.location_id = sub_locations.location_id
            JOIN pollutants ON pollutants.pollutant_id = measurements.pollutant_id
            WHERE 1=1
            ;
    '''
    params = []

    if main_location:
        query += " AND locations.name = ?"
        params.append(main_location)

    if sub_location:
        query += " AND sub_locations.name = ?"
        params.append(sub_location)

    if pollutant:
        query += " AND pollutants.name = ?"
        params.append(pollutant)

    query += " ORDER BY measured_at LIMIT 10"

    return db.execute(query, params).fetchall()
