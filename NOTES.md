### Sunday 8th Dec
- changed index page to 'explore data page'
- updated HTML style to add margins so elements not cramped
- Added buttons (dead) to the explore data page for 'Oxford Data' and 'London Data'
- Created new index page for the 'Home page'

### Monday 9th Dec
- Created SQL query that presents the whole dataset in table format, ready for ingestion into the the web page
- Updated the HTML buttons to pass back to the server side whether oxford or london data selected
  - 20mins of debugging
- Added if statement to pull the oxford data when oxford is pressed. Pulls all sql data (10 rows) from above query
- Added the above sql query into the python per above in try block
- Added data to the main page in table format, using bootstrap styling
  - Caption
  - Hover-over rows
  - Header row colour - grey
- Updated html to use flexbox and bootstrap styling
  - added better spacing between elements
  - Ensured that the table sits in the middle of the page
  - Responsive design

### Tuesday 10th Dec
- Started the README.md file with core inputs
- Connected the filter buttons to the table so the table updates - filters don't update depending on which one is selected - BUG
  - Took and absolute age
- Increased number of results in the table to 100 - need to look at flexing the number

### Wednesday
- Created index / home page
- added links to table data and graph data to the layout file
- Tidy up the database connection function and the get data app

### Thursday 
- Add a graph to the garphs page using plotly
- Add a graph that is connected to the dataset
- Do it properly with Dash
- Tidy up the explore function to remove unwanted code
- Add a date option to the drop-downs list for filtering by date - maybe just month
- Add download funtionality to the datatable page