## ReadMe: AirWare - CS50 Final Project 
### By Nathan Wiles
###

#### Overview
AirAware is a Flask web application that provides interactive visualization and analysis of air quality data for Oxford and surrounding areas. The platform offers various ways to explore air quality measurements, including interactive tables, graphs, and downloadable data exports.

Data based on sample pulled from https://www.oxonair.uk/data/data-selector/9096d84b-fae1-4857-a5b0-98ed4f049588

Aim was to connect to regular updates but didn't have time.

Next step plan is to connect data for London via API from https://www.londonair.org.uk/Londonair/API/

#### Required packages that need to be installed to run the project
- python 3
- Flask
- Pandas
- SQLite3
- Plotly

#### Running the site / Setup
- Open app.py from IDE (developed with PyCharm CE - preferred)
- From the terminal navigate to project directory and type: 'flask run' 
- Launch browser if needed from flask URL in terminal
  - Navigate to http://localhost:5000 in your web browser
- Navigation / key features
  - From home screen select table data
  - Select a location to look at - choose Oxford (no london data yet)
  - Use drop-downs on the left to filter the data - note change in table data via dynamic database queries
    - change pollutant type, location, number of records
  - Option to download data (num records possibly defaulting to 14 - needs fix)
  - Navigate to graph data (from home page or top menu):
    - use legend to select one or more location to view
    - More than one provides overlay view
    - Graph built using Plotly library & with customisation by me
  - Navigate to  'table data (plotly)'
    - table view using plotly
    - I had expected this to be better than HTML version but limited, and I wasted **a lot** of time going through documentation
    - I could add drop-downs, but run out of time
  - NOTE:
    - links to register and log-in pages do not work. PLEASE DON'T press
    - If selected use back button to return to previous page, or access url in browser and delete '/register' from the end of the url


#### Main Pages
**Home Page (/)**

- Landing page with overview of available features
- Navigation to data exploration and visualization tools

**Explore Data Page (/explore)**
Features:

- Main location dropdown
- Sub-location dropdown
- Pollutant type filter
- Number of records selector
- Download data option

Filter Usage:

- Select main location (e.g., "Oxford High Street")
- Choose sub-location if desired
- Select specific pollutant type
- Enter number of days to display (default: 14)
- Click "Submit" to update results

**Graphs Page (/graphs)**

- Interactive Plotly visualizations
- Faceted charts by pollutant type
- Legend-based filtering
- Multiple location comparison

Data Download

- Click "Download Data (CSV)" button on explore page
- Files named with location and timestamp
- Includes all filtered data in CSV format

#### Key Files
**app.py**

Main application file containing:

- Route handlers
- Session configuration
- Core application logic

**database_helpers.py**

Database utilities including:

- Connection management
- Query execution
- CSV generation
- Error handling (limited)

**graphing.py**

Visualization logic including:

- Plotly graph generation
- Data formatting
- Graph layout customization

**table_helpers.py**

Table display utilities:

- Interactive table creation
- Data formatting
- Style configuration

##### Not built
- no log-in / register feature which I'd originally planned. Ran out of time and purpose didn't seem critical

#### Future Development
- Connect to data source to get database refresh whenever the app run
- Connect to London data API
- Add additional data visualisations
- Build the log-in feature
- 
####Primary Learning Outcomes / Observations  
- Everything takes longer than you think
- Setting up the database schema, and making sure it is correct is critical
- LLMs are an incredible learning tool and development partner - I used for debugging, explaining topics or code I didn't understand - but prone to errors for more niche topics eg smaller libraries.
- There are compromises from the very start - trade-offs on what is possible vs time available
- Using other peoples data isn't always easy - need to shape into usable format before importing into db or using
- Starting without a plan creates extra work
- There is so much to read when learning a new library

