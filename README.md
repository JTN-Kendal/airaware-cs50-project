## ReadMe: AirWare - CS50 Final Project 
### By Nathan Wiles
###

#### Overview
AirAware is a web-based application for visualizing and analyzing air quality data in Oxford, with potential extension to London data. The application provides multiple ways to view, filter, and export air quality measurements across different locations and pollutant types.

Data based on sample pulled from https://www.oxonair.uk/data/data-selector/9096d84b-fae1-4857-a5b0-98ed4f049588

Aim was to connect to regular updates but didn't have time
Extention plan to connect to data for London via API from https://www.londonair.org.uk/Londonair/API/

#### Running the site / Setup
- Open app.py
- In terminal type: 'flask run' 
- Launch browser if needed from flask URL in terminal
- Navigation / key features
  - From home screen select table data
  - Select a location to look at - choose Oxford (no london data yet)
  - Use drop-downs on the left to filter the data - note change in table data via database queries
    - change pollutant type, location, number of records
  - Option to download data (num records possibly defaulting to 14 - needs fix)
  - Navigate to graph data:
    - use legend to select one or more location to view
    - More than one provides overlay view
    - Graph built using Plotly library & with customisation by me
  - Navigate to  'table data (plotly)'
    - table view using plotly
    - I had expected this to be better than HTML version but limited
    - I could add drop-downs, but no time
  - NOTE:
    - links to register and log-in pages do not work. PLEASE DON'T press

#### Core features
##### Data Exploration
- Interactive data table with multiple filtering options:
  - Main location filtering
  - Sub-location filtering
  - Pollutant type filtering
  - Custom record limit selection
- Support for both Oxford and London datasets
- Pagination and sorting capabilities

##### Data Visualization
- Interactive Plotly graphs showing air quality trends
- Customized table views with styled headers and cells
- Visual indicators for data status and measurements

##### Data Export
- CSV download functionality
- Customized file naming with location and timestamp
- Filtered data export based on user selections

##### Location Management

Hierarchical location structure:
- Main locations (e.g., Oxford, SODC Henley)
- Sub-locations (e.g., High Street, St Aldates)

Support for multiple pollutant types at each location

##### Not built
- no log-in / register feature which I'd originally planned. Ran out of time and purpose didn't seem critical


#### Future Development
- Connect to data source to get database refresh whenever the app run
- Connect to London data API
- Add additional data visualisations
- Build the log-in feature
####Primary Learning Outcomes / Observations  
- Everything takes longer than you think
- Setting up the database schema, and making sure it is correct is critical
- LLMs are an incredible learning tool and development partner - I used for debugging, explaining topics or code I didn't understand - but prone to errors for more niche topics eg smaller libraries.
- There are compromises from the very start - trade-offs on what is possible vs time available
- Using other peoples data isn't always easy - need to shape into usable format before importing into db or using
- Starting without a plan creates extra work
- There is so much to read when learning a new library

