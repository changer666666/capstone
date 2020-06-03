import altair as alt
import pandas as pd
import calculate_data
import os
import calculate_data
import json
import calData

myPath = os.path.abspath(os.path.dirname(__file__))

def generateJSON(testNum):
    dsRes_df, cdsRes_df, gsVoltage, temp, packTemp, br_df, lir_df, expr_df, rnn_df, trendLine_df, inciFault, stndFault = calData.getAllDF(testNum)

################################### Raw ds Resistence data
    dsResChart = alt.Chart(dsRes_df, width=400, height=200, title='Raw ON-State Drain-to-Source Resistance').mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('Resistance:Q', axis=alt.Axis(title='Resistance(Ω)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Resistance'],
        color=alt.value("#A5FC1F")
    ).interactive()

    dsResJSON = dsResChart.configure_title(color='#DCDCDC').to_json()

################################### Cleaned ds Resistence data
    cdsResChart = alt.Chart(cdsRes_df, width=400, height=200, title='Cleaned ON-State Drain-to-Source Resistance').mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('Resistance:Q', axis=alt.Axis(title='Resistance(Ω)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Resistance'],
        color=alt.value("#F43A3A")
    ).interactive()

    cdsResJSON = cdsResChart.configure_title(color='#DCDCDC').to_json()

################################### gsVoltage
    gsVoltageChart = alt.Chart(gsVoltage, width=400, height=200, title='On-State Gate-to-Source Voltage').mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('Gate-to-Source Voltage Data:Q', axis=alt.Axis(title='On-State Gate-to-Source Voltage(V)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Gate-to-Source Voltage Data'],
        color=alt.value("#F43A3A")
    ).interactive()
    gsVoltageJson = gsVoltageChart.configure_title(color='#DCDCDC').to_json()

    ################################### Temprature

    tempChart = alt.Chart(temp, width=400, height=200, title='Temperature').mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('raw_Case_Temperature:Q', axis=alt.Axis(title='Temprature', labelColor='white', titleColor='white')),
        tooltip=['time', 'raw_Case_Temperature'],
        color=alt.value("#F43A3A")
    ).interactive()

    packTempChart = alt.Chart(packTemp, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(minutes)', labelColor='white', titleColor='white')),
        alt.Y('raw_Package_Temperature:Q'),
        tooltip=['time', 'raw_Package_Temperature'],
        color=alt.value("#ffff00")
    ).interactive()

    tempJSON = (tempChart + packTempChart).configure_title(color='#DCDCDC').to_json()

    ################################### Regression
    brChart = alt.Chart(br_df, width=400, height=200, title='RUL Analysis').mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('Basic_Regression:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Basic_Regression'],
        color=alt.value("red")
    )

    lirChart = alt.Chart(lir_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('Linear_Regression:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Linear_Regression'],
        color=alt.value("blue")
    )

    exprChart = alt.Chart(expr_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('Exponentional_Regression:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Exponentional_Regression'],
        color=alt.value("green")
    )

    rnnChart = alt.Chart(rnn_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('Rnn:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Rnn'],
        color=alt.value("yellow")
    )

    baseChart = alt.Chart(trendLine_df, width=400, height=200).mark_line(point=True).encode(
        alt.X('time:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('Base:Q', axis=alt.Axis(title='RUL(Minutes)', labelColor='white', titleColor='white')),
        tooltip=['time', 'Base'],
        color=alt.value("white")
    ).properties(width=10)

    regJson = (brChart + lirChart + exprChart + rnnChart + baseChart).configure_title(color='#DCDCDC').interactive().to_json()

    ################################### Fault Investigation

    inciFaultChart = alt.Chart(inciFault, width=400, height=200, title='Fault Investigation').mark_line(point=True).encode(
        alt.X('ifTime:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('iFault:Q', axis=alt.Axis(title='Fault State', labelColor='white', titleColor='white')),
        tooltip=['ifTime', 'iFault'],
        color=alt.value("yellow")
    ).interactive()

    stndFaultChart = alt.Chart(stndFault, width=400, height=200).mark_line(point=True).encode(
        alt.X('sfTime:Q', axis=alt.Axis(title='Time(Minutes)', labelColor='white', titleColor='white')),
        alt.Y('sFault:Q', axis=alt.Axis(title='Fault State', labelColor='white', titleColor='white')),
        tooltip=['sfTime', 'sFault'],
        color=alt.value("red")
    ).interactive()

    faultJson = (inciFaultChart + stndFaultChart).configure_title(color='#DCDCDC').to_json()

    ################################### Write Files

    path = os.path.join(myPath, 'static', 'resultJSON')

    with open(os.path.join(path,'rRes{}.json'.format(testNum)), 'w') as f:
        json.dump(dsResJSON, f)

    with open(os.path.join(path,'cRes{}.json'.format(testNum)), 'w') as f:
        json.dump(cdsResJSON, f)

    with open(os.path.join(path,'gsVoltage{}.json'.format(testNum)), 'w') as f:
        json.dump(gsVoltageJson, f)

    with open(os.path.join(path,'temp{}.json'.format(testNum)), 'w') as f:
        json.dump(tempJSON, f)

    with open(os.path.join(path,'regression{}.json'.format(testNum)), 'w') as f:
        json.dump(regJson, f)

    with open(os.path.join(path,'fault{}.json'.format(testNum)), 'w') as f:
        json.dump(faultJson, f)











