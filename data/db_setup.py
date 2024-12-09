import sqlite3


def db_setup():
    """Create a new db with defined schema"""

    # connect to db
    conn = sqlite3.connect("air.db")
    db = conn.cursor()

    # Read in the sql file so it can be used
    with open("db_schema.sql", mode="r") as sql_schema_file:
        schema = sql_schema_file.read()

    # Execute the schema from the read in sql file
    db.executescript(schema)

    # Commit the changes to the db and close
    conn.commit()
    conn.close()
    print("Database setup Complete")


if __name__ == "__main__":
    db_setup()
