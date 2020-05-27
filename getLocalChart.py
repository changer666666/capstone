import altair as alt
import pandas as pd
import calculate_data
import os
import calculate_data
import json
import calData

myPath = os.path.abspath(os.path.dirname(__file__))

def generateJSON(testNum):
    rawData_df, dsRes_df, dsResSampled_df, gsVoltage, br_df, lir_df, expr_df = calData.getAllDF(testNum)

################################### Basic Information
    rawDataChart = alt.Chart(rawData_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('cleanTime:T', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('validated:Q', axis=alt.Axis(title='validated', labelColor='white', titleColor='white')),
        tooltip=['cleanTime', 'validated'],
        color=alt.value("#A5FC1F")
    ).interactive()

    dsResChart = alt.Chart(dsRes_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('cleanTime:T', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('shiftedClean:Q', axis=alt.Axis(title='shiftedClean', labelColor='white', titleColor='white')),
        tooltip=['cleanTime', 'shiftedClean'],
        color=alt.value("#EECACA")
    ).interactive()

    dsResSampledChart = alt.Chart(dsResSampled_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('sampleTime:T', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('shiftedSample:Q', axis=alt.Axis(title='shiftedSample', labelColor='white', titleColor='white')),
        tooltip=['sampleTime', 'shiftedSample'],
        color=alt.value("#F43A3A")
    ).interactive()

    basicDataJSON = (rawDataChart + dsResChart + dsResSampledChart).to_json()

################################### gsVoltage

    gsVoltageChart = alt.Chart(gsVoltage, width=400, height=200).mark_line(point=True).encode(
        alt.X('cleanTime:T', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('validatedGSoV:Q', axis=alt.Axis(title='validatedGSoV', labelColor='white', titleColor='white')),
        tooltip=['cleanTime', 'validatedGSoV'],
        color=alt.value("#F43A3A")
    ).interactive()
    gsVoltageJson = gsVoltageChart.to_json()

################################### Regression
    brChart = alt.Chart(br_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:T', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('value:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'value'],
        color=alt.value("red")
    ).interactive()

    lirChart = alt.Chart(lir_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:T', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('value:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'value'],
        color=alt.value("blue")
    ).interactive()

    exprChart = alt.Chart(expr_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:T', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('value:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'value'],
        color=alt.value("white")
    ).interactive()
    regJson = (brChart + lirChart + exprChart).to_json()

    path = os.path.join(myPath, 'static', 'resultJSON')
    with open(os.path.join(path,'basic{}.json'.format(testNum)), 'w') as f:
        json.dump(basicDataJSON, f)

    with open(os.path.join(path,'gsVoltage{}.json'.format(testNum)), 'w') as f:
        json.dump(gsVoltageJson, f)

    with open(os.path.join(path,'regression{}.json'.format(testNum)), 'w') as f:
        json.dump(regJson, f)
    # Get test file
    # for i in [36]:

for i in range(1,4):
    try:
        generateJSON(i)
    except:
        continue



