from flask import Flask, render_template, request
import altair as alt
import pandas as pd
from vega_datasets import data
import scipy.io as spio
import numpy as np
from pandas.io.json import json_normalize
import pyarrow
import calculate_data

# imported data from calculate_data.py
calculated_data = calculate_data.data_df
rul_calculated_data = calculate_data.rul

##########################
# raw data extraction
##########################
supplyV = pd.read_parquet('MOSFET.parquet')


app = Flask(__name__)

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def index():
    return render_template('index.html')


# render cars.html page
@app.route("/cars")
def show_cars():
    return render_template("cars.html")


# render iowa electricity.html
@app.route("/electricity")
def show_electricity():
    return render_template("electricity.html")


# render supplyVoltage.html
@app.route("/supplyV")
def show_supplyV():
    return render_template("supplyV.html")

# render onState.html
@app.route("/onState")
def show_onState():
    return render_template("onState.html")

# render rul.html
@app.route("/rul")
def show_rul():
    return render_template("rul.html")


#########################
### Altair Data Routes
#########################

WIDTH = 600
HEIGHT = 300

@app.route("/data/onState")
def onState_demo():
    chart = alt.Chart(calculated_data).mark_line(point=True, height=700, width=700).encode(
                x='Time(Min)',
                y='ONStateRES'
            ).interactive()
    return chart.to_json()

@app.route("/data/rul")
def rul_demo():
    chart = alt.Chart(rul_calculated_data).mark_line(point=True, height=700, width=700).encode(
                x='Time(Min)',
                y='ONStateRES'
            ).interactive()
    return chart.to_json()

if __name__ == "__main__":
    app.run(debug=True)

