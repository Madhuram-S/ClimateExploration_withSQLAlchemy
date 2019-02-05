import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import create_engine, func

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

# Create our session (link) from Python to the DB
session = scoped_session(sessionmaker(engine))


#res = session.query(Passenger.name,Passenger.age, Passenger.sex).all()


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
        f"Going on a vacation? Predict how weather will be during your vacation based on data from 2010<br><br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return Precipitation values for all dates available in DB"""
    # Query all Measurement Table to get precipitation date for all available dates
    results = pd.DataFrame(session.query(M.date.label('Date'), M.prcp.label('Precipitation')).all())
    results.set_index('Date', inplace = True)
                           
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    
    #session.close()
    return pd.to_json(results, orient = 'columns')


@app.route("/api/v1.0/passengers")
def passengers():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    session = Session(engine)
    # Query all passengers
    results = session.query(Passenger).all()
    #results = res
    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for passenger in results:
      passenger_dict = {}
      passenger_dict["name"] = passenger.name
      passenger_dict["age"] = passenger.age
      passenger_dict["sex"] = passenger.sex
      all_passengers.append(passenger_dict)

    session.close()
    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
