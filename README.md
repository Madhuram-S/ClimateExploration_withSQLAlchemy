# Climate Analysis and Exploration
## Step 1 - Analyse using SQLAlchemy

In this assignment, we are exploring Hawaii climate (Percipitation and Temperature) based on sqlite database provided.

We will use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All plots will be plotted using Matplotlib

Following exploration and analysis are done

- Understand the tables
    - Using sqlchemy.inspect(), we will understand 
        * Tables in the sqlite database
        * columns of each table along with their data types
    - Using func.min() and func.max() functions with sqlalchemy, we will derive
        * Start date of the climate data and end date of the climate data
        * date that is exactly a year previous to the end date within the climate data

- Precipitation Analysis using a query to retrieve the last 12 months of precipitation data

- Station Analysis
    * Total number of stations
    * Most active stations
    * Explore last 12 months of temperature observation data (tobs) for the most active station
    * Plot a histogram with bins = 12

- Temperature Analysis 
    * Find the minimum, average and maximum temperature for dates same as trip planned dates but a previous year
    * Plot the min, avg, and max temperature from your previous query as a bar chart.
         * with average temperature as the bar height.
         * and peak-to-peak (tmax-tmin) value as the y error bar (yerr)
         
- Calculate the rainfall per weather station using the previous year's matching dates.

- Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures
    * Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.
    * Use Pandas to plot an area plot (`stacked=False`) for the daily normals
    
## Step 2 - Climate App using Flask (refer to file climate_explore_api.py)

Design a Flask API based on the queries and to create routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of the results dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

