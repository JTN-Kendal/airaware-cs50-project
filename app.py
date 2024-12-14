from flask import Flask, flash, redirect, render_template, request, session, send_file, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from database_helpers import get_filtered_results, close_db, get_db, generate_csv
from graphing import build_graph, create_interactive_graph
from table_helpers import basic_table
from datetime import datetime

# Configure the flask application
app = Flask(__name__)
app.teardown_appcontext(close_db)  # Closes db connections - clean-up

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    """Render the application's home page.

    This Flask route handler serves the main landing page of the application.
    It is bound to the root URL ("/").

    Returns:
        flask.Response: Rendered index.html template.
    """
    return render_template("index.html")


@app.route("/explore", methods=["GET"])
def explore():
    """Handle requests to the explore data page, managing filters and data display.

    This Flask route handler manages the data exploration page, handling both initial page loads
    and filtered data requests. It retrieves data from the database based on user-selected
    filters and renders the exploration interface.

    Request Parameters:
        main_location (str, optional): Name of the main location to filter by
        sub_location (str, optional): Name of the sub-location to filter by
        pollutant (str, optional): Name of the pollutant to filter by
        num_records (str, optional): Number of records to display (default: "14")
        location-data-selection (str, optional): Dataset selection ("oxford" or "london")

    Returns:
        flask.Response: Rendered explore_data.html template with the following context:
            data (list): Filtered measurement results
            location (str): Currently selected dataset location ("Oxford" or "London")
            locations (list): Available main locations for filtering
            sub_locations (list): Available sub-locations for filtering
            pollutants (list): Available pollutants for filtering
            selected_main_location (str|None): Currently selected main location
            selected_sub_location (str|None): Currently selected sub-location
            selected_pollutant (str|None): Currently selected pollutant

    Notes:
        - Only handles GET requests
        - Defaults to Oxford dataset if location selection fails
        - Validates num_records to be between 1 and 10000, defaulting to 14 if invalid
        - Database exceptions are caught and result in empty lists for the relevant dropdowns
    """

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
    location_data = "Oxford"
    selected_num_records = None

    if request.method == "GET":
        # drop-down selection options
        selected_main_location = request.args.get("main_location")
        selected_sub_location = request.args.get("sub_location")
        selected_pollutant = request.args.get("pollutant")
        selected_num_records = request.args.get("num_records", "14")

        # Manage the default behaviour of the number of records selected to not mess with other filters
        try:
            selected_num_records = int(selected_num_records)
            if selected_num_records < 1 or selected_num_records > 10000:
                selected_num_records = 14
        except (ValueError, TypeError):
            selected_num_records = 14

        print("\n")
        print(f"SELECTED RECORDS: {request.args.getlist('num_records')}")
        print(f"SELECTED RECORDS: {type(selected_num_records)}")
        print("\n")

        filtered_results = get_filtered_results(db,
                                                main_location=selected_main_location,
                                                sub_location=selected_sub_location,
                                                pollutant=selected_pollutant,
                                                limit=selected_num_records,
                                                )

        # Set a variable to contain the location that is selected - Oxford or London
        location_data = ""
        try:
            location_data = request.args.get("location-data-selection").title()
        except Exception as e:
            print(f"Exception raised for location selection - Oxford vs London: {e}")
            location_data = "Oxford"

    return render_template("explore_data.html",
                           data=filtered_results,
                           location=location_data,
                           locations=main_locations,
                           sub_locations=sub_locations,
                           pollutants=pollutants,
                           selected_main_location=selected_main_location,
                           selected_sub_location=selected_sub_location,
                           selected_pollutant=selected_pollutant,
                           # selected_num_records=selected_num_records,
                           )


@app.route("/graphs", methods=["GET"])
def graphs():
    """Render the data visualization page with interactive Plotly graphs.

    This Flask route handler generates interactive visualizations of air quality data.
    It retrieves data from the database and creates a Plotly graph figure, which
    is then passed to the template for rendering.

    Returns:
        flask.Response: Rendered graphs.html template with the following context:
            fig (str): JSON-encoded Plotly figure data for the interactive graph

    Notes:
        - Only accepts GET requests
        - Requires a working database connection
        - Depends on create_interactive_graph() for visualization generation
    """
    db = get_db()
    fig_data = create_interactive_graph(db)
    return render_template("graphs.html", fig=fig_data)


@app.route("/plotly_table", methods=["GET"])
def table():
    """Render a Plotly-enhanced data table page.

    This Flask route handler generates an interactive table view of air quality data.
    It retrieves filtered data from the database, converts it to a Plotly table,
    and renders it as HTML in the template.

    Returns:
        flask.Response: Rendered plotly_table.html template with the following context:
            table (str): HTML string of the Plotly-formatted data table

    Notes:
        - Only accepts GET requests
        - Retrieves up to 10,000 records from the database
        - Uses basic_table() for Plotly table formatting
        - Returns a partial HTML string that doesn't include the full HTML document
    """
    # DB connection
    db = get_db()
    # get data for the table
    data = get_filtered_results(db, limit=10000)

    # Create the table
    table_data = basic_table(data=data)

    # Convert table to HTML
    table_html = table_data.to_html(
        full_html=False,
        include_plotlyjs=True,
    )

    return render_template("plotly_table.html", table=table_html)


@app.route("/download", methods=["GET"])
def download(file_name: str = "Oxford"):
    """Generate and serve a CSV download of filtered air quality data.

    This Flask route handler retrieves filtered data based on URL parameters,
    converts it to CSV format, and serves it as a downloadable file. The file
    name includes the location and current date.

    Args:
        file_name (str, optional): Base name for the downloaded file. Defaults to "Oxford".

    Request Parameters:
        main_location (str, optional): Main location to filter by
        sub_location (str, optional): Sub-location to filter by
        pollutant (str, optional): Pollutant type to filter by

    Returns:
        flask.Response: CSV file download response with the filtered data, or
        flask.Response: Redirect to explore page if download fails

    Notes:
        - Only accepts GET requests
        - Filename format: "Air Quality Data for: {file_name}_{YYYY-MM-DD}"
        - Returns all matching records without pagination
        - Redirects to explore page on any error
        - Requires database connection and working CSV generation
    """

    timestamp = datetime.today().strftime("%Y-%m-%d")
    try:
        # Open the db connection
        db = get_db()

        # Create filters group for passing to the db query
        filters = {
            "main_location": request.args.get("main_location"),
            "sub_location": request.args.get("sub_location"),
            "pollutant": request.args.get("pollutant"),
        }

        # send the query to the db & then generate the csv for downloading
        query_data = get_filtered_results(db=db, **filters)
        download_data = generate_csv(query_data=query_data)

        # return the download with filename
        return send_file(download_data,
                         mimetype="text/csv",
                         as_attachment=True,
                         download_name=f"Air Quality Data for: {file_name}_{timestamp}",
                         )

    except Exception as e:
        print(f"Data Download Failed with code: {e}")
        return redirect(url_for("explore"))
