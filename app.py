from cs50 import SQL
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from pprint import pprint
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from database_helpers import get_db, get_filtered_results

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db = SQL("sqlite:///data/air.db")


@app.route("/", methods=["GET"])
def explore():
    # Establish database connection
    db = get_db()

    # Populate the drop-down menus
    try:
        main_locations = db.execute("SELECT * FROM locations")
    except Exception as e:
        main_locations = []
        print(e)
    try:
        sub_locations = db.execute("SELECT * FROM sub_locations")
    except Exception as e:
        sub_locations = []
        print(e)

    try:
        pollutants = db.execute("SELECT * FROM pollutants")
    except Exception as e:
        pollutants = []
        print(e)

    # TODO: Add the drop-down selection options
    main_location = request.args.get("main_location")
    sub_location = request.args.get("sub_location")
    pollutant = request.args.get("pollutant")
    # measure_date = request.args.get("date")

    # filters = get_filtered_results(main_location, sub_location, pollutant)

    # Set a variable to contain the location that is selected - Oxford or London
    location_data = ""
    try:
        location_data = request.args.get("location-data-selection").title()
    except Exception as e:
        print(f"Exception raised for location selection - Oxford vs London: {e}")

    # Pull the data for Oxford - in full programme would include London
    data_table = []
    if location_data == "Oxford":
        try:
            data_table = db.execute("""
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
                                        ORDER BY measured_at DESC
                                        LIMIT 100
                                    ;
            """)

        except Exception as e:
            print(f"Exception {e}")  # Set empty list in the except block when there's an error

    return render_template("explore_data.html",
                           location=location_data,
                           locations=main_locations,
                           sub_locations=sub_locations,
                           pollutants=pollutants,
                           data=data_table,
                           )


@app.route("/filter", methods=["GET", "POST"])
def filter_data():
    return None
