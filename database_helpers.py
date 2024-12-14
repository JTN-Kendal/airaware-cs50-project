import csv
from io import BytesIO, StringIO
from flask import g
import sqlite3
import logging

logger = logging.getLogger(__name__)


def get_db():
    """Get or create a database connection for the current request.

        Creates a new SQLite connection if one doesn't exist for the current request
        context, storing it in Flask's g object. Subsequent calls within the same
        request context will return the existing connection.

        Returns:
            sqlite3.Connection: Database connection object with Row factory enabled

        Notes:
            - Uses Flask's g object for request-scoped connection management
            - Connects to 'data/air.db' SQLite database
            - Sets sqlite3.Row as row_factory for dictionary-like row access
            - Should be used in conjunction with close_db() for proper cleanup
        """
    if 'db' not in g:
        g.db = sqlite3.connect("data/air.db")
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the database connection at the end of a request.

    Safely removes and closes the database connection stored in Flask's g object.
    Designed to be used as a teardown function for Flask's application context.

    Args:
        e (Exception, optional): Error that occurred during the request, if any.
            Defaults to None.

    Notes:
        - Should be registered with @app.teardown_appcontext decorator
        - Safely handles cases where no database connection exists
        - Companion function to get_db()
        - Will close connection even if an error occurred during the request
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None, limit: int = 14):
    """Retrieve filtered air quality measurements from the database.

    Executes a SQL query to fetch air quality measurements with optional filtering
    by location and pollutant type. Results are ordered by date (descending) and
    limited to a specified number of records.

    Args:
        db (sqlite3.Connection): Database connection object
        main_location (str, optional): Main location name to filter by. Defaults to None.
        sub_location (str, optional): Sub-location name to filter by. Defaults to None.
        pollutant (str, optional): Pollutant name to filter by. Defaults to None.
        limit (int, optional): Maximum number of records to return. Defaults to 14.

    Returns:
        list[sqlite3.Row]: List of measurement records with the following fields:
            - loc_name (str): Main location name
            - sub_name (str): Sub-location name
            - pollutant_name (str): Pollutant name
            - value (float): Measurement value
            - status (str): Measurement status
            - measured_at (str): Measurement date

    Raises:
        sqlite3.Error: If there's an error executing the database query

    Notes:
        - Empty or whitespace-only filter values are ignored
        - Results are ordered by measurement date (newest first)
        - All string matching is exact (case-sensitive)
        - Uses parameterized queries for SQL injection prevention
    """

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
    """Convert database query results to a CSV file in memory.

    Takes query results containing air quality measurements and generates a CSV file
    in a binary buffer. The CSV includes headers and formatted data rows.

    Args:
        query_data (list[sqlite3.Row]): Database query results containing measurement data
            with the following expected fields:
            - loc_name: Location name
            - sub_name: Sub-location name
            - pollutant_name: Pollutant name
            - value: Measurement value
            - status: Measurement status
            - measured_at: Measurement date

    Returns:
        BytesIO: Binary buffer containing the CSV data, with cursor positioned at
        the start of the buffer. The CSV includes the following columns:
        Location, Sub-location, Pollutant, Value, Status, Date

    Notes:
        - Returns an empty buffer if query_data is empty
        - Uses UTF-8 encoding for the CSV data
        - Handles file-like operations in memory without disk I/O
        - CSV is created with standard formatting (comma-separated, quoted as needed)
    """

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
