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


def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None):
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

    query += " ORDER BY measured_at DESC LIMIT 10"

    print("\nFinal SQL:")
    print("Query:", query)
    print("Params:", params)

    try:
        # CHANGED: Use standard sqlite3 execute with fetchall()
        # Instead of just db.execute(query), we now need cursor.execute() and fetchall()
        cursor = db.execute(query, params)  # Note: No need to unpack params
        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Database error in get_filtered_results: {e}")
        raise

# TO DELETE IF ALL WORKS
# from flask import g
# import sqlite3
# from cs50 import SQL
#
#
# # Function to create the database connection, using
# def get_db():
#     if 'db' not in g:
#         # g.db = sqlite3.connect("data/air.db")
#         g.db = SQL("sqlite:///data/air.db")
#     return g.db
#
#
# def get_filtered_results(db, main_location=None, sub_location=None, pollutant=None):
#     query = '''
#             SELECT
#                 locations.name as loc_name,
#                 sub_locations.name as sub_name,
#                 pollutants.name as pollutant_name,
#                 value,
#                 status,
#                 measured_at
#             FROM measurements
#             JOIN sub_locations ON sub_locations.sub_location_id = measurements.sub_location_id
#             JOIN locations ON locations.location_id = sub_locations.location_id
#             JOIN pollutants ON pollutants.pollutant_id = measurements.pollutant_id
#             WHERE 1=1
#     '''
#
#     # For CS50 SQL, we need to pass parameters directly in execute()
#     if main_location and main_location.strip():
#         query += " AND locations.name = ?"
#
#     if sub_location and sub_location.strip():
#         query += " AND sub_locations.name = ?"
#
#     if pollutant and pollutant.strip():
#         query += " AND pollutants.name = ?"
#
#     query += " ORDER BY measured_at DESC LIMIT 10"
#
#     print("\nFinal SQL:")
#     print("Query:", query)
#
#     # Build args list in order of parameters
#     args = []
#     if main_location and main_location.strip():
#         args.append(main_location)
#     if sub_location and sub_location.strip():
#         args.append(sub_location)
#     if pollutant and pollutant.strip():
#         args.append(pollutant)
#
#     print("Args:", args)
#
#     # Execute with or without parameters
#     if not args:
#         return db.execute(query)
#     return db.execute(query, *args)  # Unpack args list