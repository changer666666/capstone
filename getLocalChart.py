import altair as alt
import pandas as pd
import calculate_data
import os
import calculate_data
import json

myPath = os.path.abspath(os.path.dirname(__file__))

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
    return chart.to_json()

# Get test file
for i in range(8,11):
    filename = 'Test_' + str(i) + '_Run_1'
    chartJSON = getChart(filename)
    #print(chartJSON)
    path = os.path.join(myPath, 'static', 'resultJSON', filename+ '.json')
    with open(path, 'w') as f:
        json.dump(chartJSON, f)

