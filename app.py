from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from database_helpers import get_db, get_filtered_results
from graphing import display_color

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db = SQL("sqlite:///data/air.db")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/explore", methods=["GET"])
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

    filtered_results = []
    selected_main_location = None
    selected_sub_location = None
    selected_pollutant = None
    location_data = None

    if request.method == "GET":
        # TODO: Add the drop-down selection options
        selected_main_location = request.args.get("main_location")
        selected_sub_location = request.args.get("sub_location")
        selected_pollutant = request.args.get("pollutant")
        # selected_measure_date = request.args.getlist("date")

        filtered_results = get_filtered_results(db,
                                                main_location=selected_main_location,
                                                sub_location=selected_sub_location,
                                                pollutant=selected_pollutant
                                                )

        # Set a variable to contain the location that is selected - Oxford or London
        location_data = ""
        try:
            location_data = request.args.get("location-data-selection").title()
        except Exception as e:
            print(f"Exception raised for location selection - Oxford vs London: {e}")

    return render_template("explore_data.html",
                           data=filtered_results,
                           location=location_data,
                           locations=main_locations,
                           sub_locations=sub_locations,
                           pollutants=pollutants,
                           selected_main_location=selected_main_location,
                           selected_sub_location=selected_sub_location,
                           selected_pollutant=selected_pollutant,
                           )


@app.route("/graphs", methods=["GET"])
def graphs():
    fig = display_color("Gold")
    return render_template("graphs.html", fig=fig)
