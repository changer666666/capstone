from flask import Flask, render_template, request
import altair as alt
import pandas as pd
import calculate_data
import json
import os

#
# from selenium import webdriver
# driver = webdriver.Chrome('C:\capstone\chromedriver.exe')


myPath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


# render index.html as home page
@app.route("/", methods=("GET", "POST"))
def index():
    loaded = 'hidden'
    if request.method == "POST":
        filename = request.form.get('testRunSelect')
        onStateRes = calculate_data.calculate_data(filename)
        chart = alt.Chart(onStateRes, width=600, height=300).mark_line(point=True).encode(
                x='Time(Min):T',
                y='ONStateRES:Q'
            ).configure_axis(
                labelColor='gray',
                titleColor='gray'
            ).interactive()
        #print(type(chart))
        imgPath = os.path.join(myPath, 'static', 'img', filename+".png")
        relativePath = './img/' + filename+".png"
        chart.save(imgPath)
        print('Save PNG Successfully', relativePath)
        loaded = 'visible'
        return render_template('index.html', path = relativePath, jsonData = chart.to_json())

    return render_template('index.html', loaded = loaded)

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
    chart = alt.Chart(supplyV, width=600, height=300).mark_line(point=True).encode(
        x='date:T',
        y='supplyVoltage:Q'
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart.to_json()

########### onStateRes
@app.route("/onStateRes")
def show_onStateRes():
    return render_template("onStateRes.html")
'''
@app.route("/data/onStateRes")
def onStateRes_demo():

    chart = alt.Chart(onStateRes, width=600, height=300).mark_line(point=True).encode(
        x='Time(Min):T',
        y='ONStateRES:Q'
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart.to_json()
'''

if __name__ == "__main__":
    app.run(debug=True)

