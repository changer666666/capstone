from flask import Flask, render_template, request
import altair as alt
import pandas as pd
from vega_datasets import data
import numpy as np
import pyarrow


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

# render supplyVoltage.html
@app.route("/supplyV")
def show_supplyV():
    return render_template("supplyV.html")

#########################
### Altair Data Routes
#########################

@app.route("/data/supplyV")
def supplyV_demo():
    chart = alt.Chart(supplyV, width=600, height=300).mark_line(point=True).encode(
                x='date:T',
                y='supplyVoltage:Q'
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart.to_json()

if __name__ == "__main__":
    app.run(debug=True)

