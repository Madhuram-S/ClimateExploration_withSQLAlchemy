import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from sqlalchemy.sql.functions import coalesce # library to use check if null and replace with 0 or any value

from datetime import datetime as dt, timedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station



def get_year_past(end_dt = ""):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #if end_dt is passed use Max date in the DB for Measurement table
    if(end_dt == ""):
        end_dt = dt.strptime(session.query(func.max(M.date)).scalar(),"%Y-%m-%d") 
    else:
        end_dt = dt.strptime(end_dt, "%Y-%m-%d")
    
    session.close() # close the session
    
    # One year prior to end date 
    year_past = end_dt - timedelta(days = 365)
    
    
    return (end_dt.strftime("%Y-%m-%d"), year_past.strftime("%Y-%m-%d"))


def get_temps(st_dt = "", end_dt = ""):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        st_dt (string): A date string in the format %Y-%m-%d
        end_dt (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)
    
    if(st_dt == ""):
        end_dt, st_dt = get_year_past()
    
    if(end_dt == "" or end_dt is None):
        res = session.query(coalesce(func.min(M.tobs),0), coalesce(func.avg(M.tobs),0), coalesce(func.max(M.tobs),0)).\
                    filter(M.date >= st_dt).one()
    else:
        res = session.query(coalesce(func.min(M.tobs),0), coalesce(func.avg(M.tobs),0), coalesce(func.max(M.tobs),0)).\
                    filter(M.date.between(st_dt, end_dt)).one()
    
    session.close()
    
    return res


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hello!! Welcome to Climate App!. <br><br>"
        f"Going on a vacation to Hawaii? Predict how weather in Hawaii will be during your vacation based on data from 2010<br><br>"
        f"Check out:<br/>"
        f"Precipitation by dates :- /api/v1.0/precipitation<br/>"
        f"Stations where observations are made :- /api/v1.0/stations <br>"
        f"Temperature onservered by dates :- /api/v1.0/tobs<br><br>"
        
        f"You can see the Minimum, Maximum and Average Temperatures between specified date ranges<br><br>"
        f"<b>date format has to be YYYY-mm-dd only.. (e.g., 2012-07-23)</b><br>"
        f"/api/v1.0/<--give your start date here--><br>"
        f"/api/v1.0/<--give start date-->/<--give end date here-->"
        
       
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """Return Precipitation values for all dates available in DB"""
    
    #get max and year_past date from DB
    max_dt, yr_past = get_year_past()
    
    session = Session(engine)
    # Query all Measurement Table to get precipitation date for all available dates
    results = session.query(func.strftime('%Y-%m-%d',M.date), coalesce(M.prcp,0)).\
                filter(M.date >= yr_past).order_by(M.date).all()
    
    session.close()
                                 
    # Convert list of tuples into dict with date as the key and precipitation as value
    prcp_dict = [{d:p} for d,p in results]
    
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations where data is collection from. It also give latitude, longitude, elevation"""
    
    session = Session(engine)
    # Query to bring all stations
    results = pd.DataFrame(session.query(S.id.label('ID'),S.station.label('Station'),S.name.label('Name'),\
                                         S.latitude.label('Latitude'),S.longitude.label('Longitude'), \
                                         S.elevation.label('Elevation')).all())
    
    session.close()
    
    # Create a dictionary from the row data of the dataframe and return it as a JSON
    return jsonify(results.to_dict(orient = 'records'))

@app.route("/api/v1.0/tobs")
def tobs():
    """Return Temperature Observered values for 12 months prev to the given end date as available in DB"""
    
    #get max and year_past date from DB
    max_dt, yr_past = get_year_past()
    
    session = Session(engine)
    # Query all Measurement Table to get precipitation date for all available dates
    results = session.query(M.date.label('Date'), coalesce(M.tobs.label("TempObs"),0)).\
                filter(M.date >= yr_past).order_by(M.date).all()
                                 
    # Convert list of tuples into dict with date as the key and precipitation as value
    temp_dict = [{d:p} for d,p in results]
    
    session.close()
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>", defaults = {'end' : None}) 
@app.route("/api/v1.0/<start>/<end>")
def tobs_stdt_enddt(start, end):
    """Return Minimum, Average and Maximum Temperature Observered values for all months since the given start date"""
    
    # call function get_temps to get the Min, Max and Avg Temp observered values since start date
    tmin,tavg,tmax = get_temps(start, end)
                                 
    return (
        f"Here are the Minimum, Maximum and Average observered Temperature between <b>{start}</b> and <b>{end}</b> - <br><br>"
        f"---------------------------------------------------------------------------------- <br><br>"
        f"The Miminum Observered Temperature is <b>{tmin} deg F</b> <br><br>"
        f"The Average Observered Temperature is <b>{round(tavg,1)} deg F</b> <br><br>"
        f"The Maximum Observered Temperature is <b>{tmax} deg F</b> <br><br>"
        
        f"<br><br><i>**** Note: If value is 0 then no results exists for the date range specified F</i> <br><br>"
        )

if __name__ == '__main__':
    app.run(debug=True)
