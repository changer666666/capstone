from flask import Flask, render_template, request, flash, redirect, url_for
import altair as alt
import pandas as pd
import calculate_data
import os
import json

myPath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'testkey'

def getChart(filename):
    onStateRes = calculate_data.calculate_data(filename)
    chart = alt.Chart(onStateRes, width=400, height=200).mark_line(point=True).encode(
        x='Time:T',
        y='ONStateRES:Q',
        tooltip=['Time', 'ONStateRES']
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart


# render index.html as home page
@app.route("/", methods=("GET", "POST"))
def index():
    loaded = 'hidden'
    #isCalculated = False
    jsonData = None
    if request.method == "POST":
        filename = request.form.get('testRunSelect')
        if filename == " ":
            error = 'You need to choose one data file!'
            flash(error)
        else:
            #imgPath = os.path.join('static', 'resultImg', filename+".png")
            relativePath = './resultImg/' + filename+".png"
            filename = filename + '.json'
            #chart = getChart(filename)
            absPath = os.path.join(myPath, 'static', 'resultJSON', filename)
            #print(relativePath)
            if os.path.exists(absPath):
                f = open(absPath)
                jsonData = json.load(f)
                #isCalculated = True
            loaded = 'visible'
            return render_template('index.html', jsonData = jsonData, path = relativePath)
            # else:
            #     error = 'File No Local Version'
            #     flash(error)

    return render_template('index.html', jsonData= jsonData, loaded = loaded)

##################################################
# Altair Data Routes
##################################################

########### supplyVotage
mosfet_Path = os.path.join(myPath, 'MOSFET.parquet')
supplyV = pd.read_parquet(mosfet_Path)

@app.route("/supplyV")
def show_supplyV():
    return render_template("supplyV.html")

@app.route("/data/supplyV")
def supplyV_demo():
    chart = alt.Chart(supplyV, width=400, height=200).mark_line(point=True).encode(
        x='date:T',
        y='supplyVoltage:Q',
        tooltip=['date', 'supplyVoltage']
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart.to_json()

if __name__ == "__main__":
    app.run(debug=True)

