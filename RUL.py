from pip._vendor.distlib.compat import raw_input
from format_converter import loadmat
import matplotlib.pyplot as plt
import pandas as pd

#file = raw_input('What is file would you like to use? ')
file = "Test_1_run_1"
data = loadmat(file + '.mat')

# choose measurement
mosfet = data['measurement']

# choose pwmTempControllerState / steadyState / transient
pwmState = mosfet['pwmTempControllerState']
steadyState = mosfet['steadyState']
transient = mosfet['transient']


def toSec(time):
    '''
    converts string-time to float-time in seconds
    ex: '02/17/2010 17:45:29.301' --> 63929.301
    '''
    hr = slice(11, 13, 1)
    fHr = float(time[hr])
    min = slice(14, 16, 1)
    fMin = float(time[min])
    sec = slice(17, 19, 1)
    fSec = float(time[sec])
    m_sec = slice(20, 23, 1)
    fM_sec = float(time[m_sec])
    return (fHr * 3600) + (fMin * 60) + fSec + (fM_sec / 1000)

#####----- Index Out of Bounds Error Fixer Upper -----#####
tableSize = 0
for i in transient[0]['timeDomain']['drainSourceVoltage']:
    tableSize += 1

#####----- TRANSIENT -----#####
transONstateRES = []
tKeyIndex = 0
for tKey in transient:
    tSampleIndex = 0
    for sample in range(tableSize):
        tDSV = transient[tKeyIndex]['timeDomain']['drainSourceVoltage'][tSampleIndex]
        tDC = transient[tKeyIndex]['timeDomain']['drainCurrent'][tSampleIndex]
        transONstateRES.append(float(tDSV) / float(tDC))
        tSampleIndex += 1
    tKeyIndex += 1
tKeyIndex -= 1

trans_total_len = len(transONstateRES)
deltaT = [0]
for d in range(trans_total_len - 1):
    deltaT.append(transONstateRES[d + 1] - transONstateRES[d])

trans_tot_dt = toSec(transient[tKeyIndex]['date']) - toSec(transient[0]['date'])
trans_avg_dt = trans_tot_dt / float(tKeyIndex * 1000.0) / 60.0
trans_time = [0]
for i in range(1, trans_total_len):
    trans_time.append(trans_time[i - 1] + trans_avg_dt)

#####----- POST CELAYA EMAIL -----#####
cONstateRES = []
rul = []
cKeyIndex = 0
for cKey in transient:
    cSampleIndex = 0
    cAveRES = 0
    for sampleC in range(tableSize):
        cDSV = transient[cKeyIndex]['timeDomain']['drainSourceVoltage'][cSampleIndex]
        cDC = transient[cKeyIndex]['timeDomain']['drainCurrent'][cSampleIndex]
        cAveRES += float(cDSV) / float(cDC)
        cSampleIndex += 1
    cONstateRES.append(float(cAveRES) / float(cSampleIndex) / 100.0)
    if (cKeyIndex == 0):
        rul.append(100.0)
    else:
        rul.append(rul[cKeyIndex - 1] - (float(cAveRES) / float(cSampleIndex) / 1000.0))
    cKeyIndex += 1
cKeyIndex -= 1

c_total_len = len(cONstateRES)
c_tot_dt = toSec(transient[cKeyIndex]['date']) - toSec(transient[0]['date'])
c_avg_dt = c_tot_dt / float(cKeyIndex) / 60.0
c_time = [0]
for i in range(1, c_total_len):
    c_time.append(c_time[i - 1] + c_avg_dt)
import random

#####----- PLOTTING -----#####
plt.figure()

#transient
#plt.subplot(211)
#plt.plot(trans_time, deltaT)
#plt.xlabel('Time(min)')
#plt.ylabel('Change in ON-State Resistance')
#plt.title(file + ' Transient Data')
#plt.grid(True)

#celaya
plt.subplot(211)
plt.plot(c_time, cONstateRES)
plt.xlabel('Time(min)')
plt.ylabel('Average ON-State Resistance')
plt.title(file + ' Data')
plt.grid(True)

#rul
plt.subplot(212)
plt.plot(c_time, rul)
plt.xlabel('Time(min)')
plt.ylabel('Remaining Useful Life (%)')
plt.title(str(rul[cKeyIndex - 3]) + '% RUL')
plt.grid(True)

plt.show()

#Build a nonlinear regression model of supposed 'good' tests in data, which include devices 8, 9, 11, 12, 14, and 36 (Ben)

