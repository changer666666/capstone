from flask import Flask, render_template, request, flash, redirect, url_for
import altair as alt
import pandas as pd
import calculate_data
import os

myPath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'testkey'

# render index.html as home page
@app.route("/", methods=("GET", "POST"))
def index():
    loaded = 'hidden'
    if request.method == "POST":
        filename = request.form.get('testRunSelect')

        if filename == " ":
            error = 'You need to choose one data file!'
            flash(error)
        else:
            onStateRes = calculate_data.calculate_data(filename)
            chart = alt.Chart(onStateRes, width=600, height=300).mark_line(point=True).encode(
                    x='Time(Min):T',
                    y='ONStateRES:Q'
                ).configure_axis(
                    labelColor='gray',
                    titleColor='gray'
                ).interactive()
            absPath = os.path.join(myPath, 'static', 'resultImg', filename+ '.png')
            relativePath = './resultImg/' + filename+ ".png"

            chart.save(absPath)
            print('Save PNG Successfully')
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
    chart = alt.Chart(supplyV, width=400, height=200).mark_line(point=True).encode(
        x='date:T',
        y='supplyVoltage:Q'
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart.to_json()

if __name__ == "__main__":
    app.run(debug=True)

