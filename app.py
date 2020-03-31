from flask import Flask, render_template, request
import altair as alt
import pandas as pd
import calculate_data
import json
import os


app = Flask(__name__)


# render index.html as home page
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        filename = request.form.get('testRunSelect')
        onStateRes = calculate_data.calculate_data(filename)
        print(type(onStateRes))

        # onStateRes_demo(onStateRes)
        chart = alt.Chart(onStateRes, width=600, height=300).mark_line(point=True).encode(
                x='Time(Min):T',
                y='ONStateRES:Q'
            ).configure_axis(
                labelColor='gray',
                titleColor='gray'
            ).interactive().to_dict()
        print(type(chart))

        my_path = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(my_path, 'data.json')
        with open(filename, 'w') as f:
            json.dump(chart, f)
            print('Successfully write json file!')

    return render_template('index.html')

##################################################
# Altair Data Routes
##################################################

########### supplyVotage
supplyV = pd.read_parquet('/home/cybao/capstone/MOSFET.parquet', engine='pyarrow')

# @app.route("/supplyV")
# def show_supplyV():
#     return render_template("supplyV.html")
#
# @app.route("/data/supplyV")
# def supplyV_demo():
#     chart = alt.Chart(supplyV, width=600, height=300).mark_line(point=True).encode(
#         x='date:T',
#         y='supplyVoltage:Q'
#     ).configure_axis(
#         labelColor='gray',
#         titleColor='gray'
#     ).interactive()
#     return chart.to_json()

########### onStateRes
@app.route("/onStateRes")
def show_onStateRes():
    return render_template("onStateRes.html")

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


if __name__ == "__main__":
    app.run(debug=True)

