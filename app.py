from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from pprint import pprint
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/air.db")


@app.route("/", methods=["GET"])
def explore():
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

    location_data = request.args.get("location-data-selection").title()
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
                                        LIMIT 10
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
