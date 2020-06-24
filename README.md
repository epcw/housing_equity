# Center for Equitable Policy in a Changing World
## Housing Equity Network model

### Codebase
Graphing: Python-based [Plotly Dash](https://plotly.com/dash/) app running a [NetworkX](https://networkx.github.io/) social networking graph, using [bhargavchippada's Force Atlas 2 for Python algorithm](https://github.com/bhargavchippada/forceatlas2)
Data crunching: Python [Pandas](https://pandas.pydata.org/) with some pre-work in MySQL to parse text files pulled from the [US Census API](https://www.census.gov/data/developers.html).

### Data source
[American Community Survey 5-year survey](https://www.census.gov/data/developers/data-sets/acs-5year.html), 2010 through 2018

### Principal researchers
Richard W. Sharp
Patrick W. Zimmerman

#### Package requirements (as well as all their dependencies)
dash
geopandas
geopy
matplotlib
networkx
numpy
pandas
scipy
sklearn
