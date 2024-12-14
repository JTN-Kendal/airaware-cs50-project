import csv
from io import BytesIO, StringIO
from flask import g
import sqlite3
import logging

logger = logging.getLogger(__name__)


def get_db():
    """Get database connection for current request."""
    if 'db' not in g:
        # CHANGED: Use standard sqlite3 connection instead of CS50 SQL
        g.db = sqlite3.connect("data/air.db")
        # ADDED: Enable dictionary-like row access (similar to CS50 SQL)
        g.db.row_factory = sqlite3.Row
    return g.db


# ADDED: New function to properly close database connection
def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None, limit: int = 14):
    """Get filtered measurement results from database."""
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

    # Build parameters list - No changes needed to query building
    params = []
    if main_location and main_location.strip():
        query += " AND locations.name = ?"
        params.append(main_location)

    if sub_location and sub_location.strip():
        query += " AND sub_locations.name = ?"
        params.append(sub_location)

    if pollutant and pollutant.strip():
        query += " AND pollutants.name = ?"
        params.append(pollutant)

    query += f" ORDER BY measured_at DESC LIMIT {limit}"

    try:
        # CHANGED: Use standard sqlite3 execute with fetchall()
        # Instead of just db.execute(query), we now need cursor.execute() and fetchall()
        cursor = db.execute(query, params)  # Note: No need to unpack params
        return cursor.fetchall()

    except sqlite3.Error as e:
        logger.error(f"Database error in get_filtered_results: {e}")
        raise


def generate_csv(query_data):
    # Set up the buffer and writer to write the data to
    binary_buffer = BytesIO()

    with StringIO(newline="") as string_buffer:
        writer = csv.writer(string_buffer)

        # Get the header rows from the input
        if query_data:
            headers = ['Location', 'Sub-location', 'Pollutant', 'Value', 'Status', 'Date']
            writer.writerow(headers)  # Write the headers to the buffer - first row

            # For each row in the dataset pull out the data for each column and write to the buffer
            for row in query_data:
                writer.writerow([
                    row['loc_name'],
                    row['sub_name'],
                    row['pollutant_name'],
                    row['value'],
                    row['status'],
                    row['measured_at']
                ])

    # Returns the buffer cursor to the beginning of the buffer so that when we write the contents to an output file/
    # it's in the correct position ie at the begining of the content to be compied
        binary_buffer.write(string_buffer.getvalue().encode("utf-8"))

    binary_buffer.seek(0)

    return binary_buffer
