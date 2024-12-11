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


def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None):
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
    '''

    # For CS50 SQL, we need to pass parameters directly in execute()
    if main_location and main_location.strip():
        query += " AND locations.name = ?"

    if sub_location and sub_location.strip():
        query += " AND sub_locations.name = ?"

    if pollutant and pollutant.strip():
        query += " AND pollutants.name = ?"

    query += " ORDER BY measured_at DESC LIMIT 10"

    print("\nFinal SQL:")
    print("Query:", query)

    # Build args list in order of parameters
    args = []
    if main_location and main_location.strip():
        args.append(main_location)
    if sub_location and sub_location.strip():
        args.append(sub_location)
    if pollutant and pollutant.strip():
        args.append(pollutant)

    print("Args:", args)

    # Execute with or without parameters
    if not args:
        return db.execute(query)
    return db.execute(query, *args)  # Unpack args list