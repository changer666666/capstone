from flask import Flask, render_template, request, flash, redirect, url_for
import altair as alt
import pandas as pd
import calculate_data
import os
import json
import boto3

myPath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'testkey'


def read_file_from_cloud(bucket, filename):
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAI3UJLE5E54WROCRA',
                        aws_secret_access_key='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')
    content_object = s3.Object(bucket, filename)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content

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
    basicData = None
    regData = None
    gsVoltageData = None
    # imgPath = None
    if request.method == "POST":
        testNum = request.form.get('testRunSelect')
        if testNum == " ":
            error = 'You need to choose one data file!'
            flash(error)
        else:
            # Get data path
            imgPath = './resultImg/' + 'mosfet' + str(testNum) + '.png'
            basicPath = os.path.join(myPath, 'static', 'resultJSON', 'basic{}.json'.format(testNum))
            gsVoltagePath = os.path.join(myPath, 'static', 'resultJSON', 'gsVoltage{}.json'.format(testNum))
            regPath = os.path.join(myPath, 'static', 'resultJSON', 'regression{}.json'.format(testNum))

            # Load data if exist
            if os.path.exists(basicPath) and os.path.exists(gsVoltagePath) and os.path.exists(regPath):
                f = open(basicPath)
                basicData = json.load(f)
                f = open(gsVoltagePath)
                gsVoltageData = json.load(f)
                f = open(regPath)
                regData = json.load(f)
            else:
                # load image
                loaded = 'visible'

            return render_template('index.html', loaded = loaded, basicData = basicData, gsVoltageData = gsVoltageData, regData = regData, path = imgPath)

    return render_template('index.html', loaded = loaded, basicData = basicData, gsVoltageData = gsVoltageData, regData = regData)

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

