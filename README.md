# Center for Equitable Policy in a Changing World
## Housing Equity in Seattle

### Codebase
Graphing: Python-based [Plotly Dash](https://plotly.com/dash/) app.  Network model runs a [NetworkX](https://networkx.github.io/) social networking graph, using [bhargavchippada's Force Atlas 2 for Python algorithm](https://github.com/bhargavchippada/forceatlas2)\
Data crunching: Python [Pandas](https://pandas.pydata.org/) with some pre-work in MySQL to parse text files pulled from the [US Census API](https://www.census.gov/data/developers.html).

### Data source
[American Community Survey 5-year survey](https://www.census.gov/data/developers/data-sets/acs-5year.html), 2010 through 2018

### Principal researchers
Richard W. Sharp\
Patrick W. Zimmerman

### Use guide (first time, run in this order)
##### Build dataframes from new data (WILL NEED TO SUPPLY NEW RAW DATA in CSV format - OUTPUT IS CSVs)
/sandbox-singlepage/data_build.sh
##### Build network graph from above dataframes
/sandbox-singlepage/build_graphs.py
##### Build maps and other graphs
/sandbox-singlepage/build_network.py
##### Launch dashboard server
/sandbox-singlepage/application.py


#### Package requirements (as well as all their dependencies)
dash\
Flask-Caching\
geopandas\
geopy\
matplotlib\
networkx\
numpy\
pandas\
scipy\
sklearn\
fa2\
rtree (usually this needs to be installed with 'sudo apt-get install python3-rtree')

### Repository Structure
.\
|-- main root folder. License and readme.\
|-- interactive-map - Interactive map app\
|   |-- assets - Has CSS and javascript files along with favicon\
|   |-- cache - Cache used by Flask for the dataframe to create temp files (so reloads don't have to completely re-run the pandas script)\
|   |-- data - Your datafiles go here (REMOVED FOR SPACE CONSIDERATIONS - the app expects to find .csv files and a geojson for maps)\
|-- jupyter-utilities - Has some example jupyter scripts\
|-- sandbox-singlepage - Network model pilot app
|   |-- assets - Has CSS and javascript files along with favicon\
|   |-- data - Your datafiles go here (REMOVED FOR SPACE CONSIDERATIONS - the app expects to find .csv files and a geojson for maps)\
|   |   |-- shapefiles - Exactly what it says on the tin.  These are also used by interactive-maps, but removed to save space\
|   |   |-- maps - json files for scatterplot and choropleth maps\
|   |   |-- json - json files that are an intermediate step in the network build\
|   |   |-- network - network options for server to swap between