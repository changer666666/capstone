from pip._vendor.distlib.compat import raw_input
from format_converter import loadmat
import matplotlib.pyplot as plt
import numpy as np
from numpy import log as ln
from numpy import exp
import pandas as pd
import time
import math

#the death for 30 may not be correct
#to be removed because of zero structs: 2, 40
#wack tests: 10, 12, 15, 18, 19, 25, 31
#with a spike in the middle: 29, 30, 33
#completely fucked tests: 27 (noise, negative), 28 (negative), 39 (arc), 41 (negative), 42 (negative)

#####----- GLOBALS -----#####
print("")
print("Hello, this program calculates the remaining useful life (RUL) of TO-220AB Power MOSFETs over time.")
print("In our database there are 42 different samples (MOSFET 1 - MOSFET 42). In order to calculate RUL, ")
print("data scientists from the NASA AMES Research Center discovered that, die-attach degradation was ")
print("determined to be the primary failure mode. The collected data from the 42 MOSFETs was initially ")
print("analyzed and it was revealed that ON-state drain-to-source resistance increased as die-attach ")
print("degraded under high thermal stresses. Therefore, ON-state drain-to-source resistance was used as ")
print("the primary precursor to failure feature. For all prediction algorithms, the following thresholds ")
print("are default: ")
print("     --> Crisp ON-state drain-to-source resistance increase of 0.05 ohms")
print("     --> Error margin of 20%")
print("")

answer1 = input('What MOSFET would you like to analyze? ')
answer2 = input('What crisp failure value would you like to use? ')
answer3 = input('What is the acceptable error margin for RUL? ')

if (answer1 == ""): mosfet = int("1")
else: mosfet = int(answer1)
if (answer2 == ""): failureThreshold = 0.05
else: failureThreshold = float(answer2)
if (answer3 == ""): rulError = int("20")
else: rulError = float(answer3)
print("failure threshold is: " + str(failureThreshold))

start = time.perf_counter()

testRun = [[1, 2], [2, 3], [3, 1], [4, 2], [5, 2], [6, 2], [7, 1], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 5],
           [14, 7], [15, 1], [16, 1], [17, 1], [18, 2], [19, 2], [20, 2], [21, 1], [22, 1], [23, 2], [24, 2], [25, 3],
           [26, 1], [27, 5], [28, 2], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 3], [35, 1], [36, 1], [37, 1],
           [38, 1], [39, 1], [40, 1], [41, 1], [42, 1]]
trDeath = [[1, 27], [2, 20], [3, 13], [4, 35], [5, 34], [6, 45], [7, 94], [8, 893], [9, 1129], [10, 797], [11, 885],
           [12, 800], [13, 121], [14, 590], [15, 32], [16, 50], [17, 70], [18, 74], [19, 13], [20, 218], [21, 18],
           [22, 86], [23, 184], [24, 205], [25, 563], [26, 125], [27, 500], [28, 59], [29, 115], [30, 500], [31, 1153],
           [32, 86], [33, 387], [34, 1123], [35, 92], [36, 208], [37, 227], [38, 56], [39, 42], [40, 10], [41, 702],
           [42, 44]]
trTimeLength = [[1, [7.14, 15.66]],
                [2, [19.77, 7.44, 23.25]],
                [3, [32.35]],
                [4, [34.64, 4.98]],
                [5, [33.45, 1.39]],
                [6, [58.78, 136.74]],
                [7, [149.38]],
                [8, [34.98, 34.97, 34.98, 34.99, 179.98, 222.07, 196.41]],
                [9, [34.97, 34.99, 34.98, 34.99, 179.99, 239.96, 239.99]],
                [10, [36.90, 32.84, 33.30, 33.80, 184.99, 244.33, 234.12]],
                [11, [34.99, 34.99, 34.99, 34.98, 179.98, 239.97, 239.98]],
                [12, [34.98, 34.98, 34.98, 34.97, 179.99, 239.96, 214.96]],
                [13, [35.88, 34.24, 33.72, 28.24, 4.31]],
                [14, [34.37, 34.08, 34.99, 34.97, 179.96, 232.63, 71.24]],
                [15, [34.99]],
                [16, [34.98]],
                [17, [34.99]],
                [18, [34.99, 34.99]],
                [19, [136.12, 1.66]],
                [20, [145.76, 140.92]],
                [21, [33.50]],
                [22, [59.99]],
                [23, [213.60, 4.99]],
                [24, [5.02, 209.56]],
                [25, [232.34, 218.78, 165.68, 0.19]],
                [26, [311.60]],
                [27, [19.99, 19.98, 19.99, 59.99, 59.99]],
                [28, [35.89, 39.00]],
                [29, [323.06]],
                [30, [439.93]],
                [31, [479.99]],
                [32, [302.42]],
                [33, [390.87]],
                [34, [479.98, 479.99, 447.25]],
                [35, [314.48]],
                [36, [360.96]],
                [37, [398.63]],
                [38, [293.57]],
                [39, [51.37]],
                [40, [12.93, 380.02]],
                [41, [435.25]],
                [42, [69.32]]]
trPWMSize = [[1, [136, 840]],
                [2, [59, 25, 65]],
                [3, [34]],
                [4, [22, 42]],
                [5, [203, 2]],
                [6, [1500, 80]],
                [7, [2150]],
                [8, [1179, 1320, 1278, 1336, 6726, 7986, 18351]],
                [9, [1345, 1468, 1434, 1478, 6506, 8612, 8817]],
                [10, [1062, 1193, 1141, 1194, 6257, 8076, 7399]],
                [11, [1336, 1300, 1305, 1286, 6587, 8719, 8571]],
                [12, [1176, 1237, 1202, 1239, 6313, 8731, 5453]],
                [13, [1223, 1152, 1122, 686, 73]],
                [14, [1279, 1397, 1353, 1402, 6939, 8751, 1884]],
                [15, [737]],
                [16, [1484]],
                [17, [1477]],
                [18, [425, 1007]],
                [19, [145, 2]],
                [20, [1382, 818]],
                [21, [375]],
                [22, [1607]],
                [23, [6245, 72]],
                [24, [95, 5553]],
                [25, [7365, 6379, 2654, 2]],
                [26, [3657]],
                [27, [557, 571, 555, 1620, 1619]],
                [28, [619, 554]],
                [29, [4070]],
                [30, [10636]],
                [31, [13754]],
                [32, [2927]],
                [33, [9704]],
                [34, [18145, 18357, 17062]],
                [35, [5121]],
                [36, [10719]],
                [37, [22941]],
                [38, [2860]],
                [39, [1226]],
                [40, [38, 200]],
                [41, [15791]],
                [42, [596]]]
trSteadySize = [[1, [1062, 2335]],
                [2, [2981, 1111, 3548]],
                [3, [4850]],
                [4, [5193, 745]],
                [5, [5006, 210]],
                [6, [8713, 20510]],
                [7, [22302]],
                [8, [5191, 5190, 5191, 5190, 26613, 32831, 28199]],
                [9, [5184, 5176, 5177, 5176, 26600, 35422, 35397]],
                [10, [5488, 4875, 4945, 5016, 27406, 36151, 34667]],
                [11, [5183, 5183, 5185, 5188, 26681, 35527, 35520]],
                [12, [5198, 5196, 5197, 5196, 26659, 35487, 31957]],
                [13, [5324, 5081, 5003, 4203, 643]],
                [14, [5091, 5044, 5184, 5183, 26584, 34306, 10591]],
                [15, [5213]],
                [16, [5181]],
                [17, [5182]],
                [18, [5232, 5203]],
                [19, [20411, 250]],
                [20, [21743, 21078]],
                [21, [5010]],
                [22, [8927]],
                [23, [31685, 747]],
                [24, [752, 31109]],
                [25, [34402, 32442, 24712, 29]],
                [26, [46574]],
                [27, [2978, 2978, 2979, 8932, 8930]],
                [28, [5362, 5979]],
                [29, [48269]],
                [30, [65233]],
                [31, [71045]],
                [32, [45236]],
                [33, [57909]],
                [34, [70658, 70843, 65915]],
                [35, [46933]],
                [36, [53560]],
                [37, [58183]],
                [38, [43915]],
                [39, [7661]],
                [40, [1940, 4485]],
                [41, [64122]],
                [42, [10388]]]
startUp = [[1, 4], [2, 4], [3, 11], [4, 25], [5, 4], [6, 20], [7, 37], [8, 4], [9, 4], [10, 37], [11, 4], [12, 4],
           [13, 4], [14, 4], [15, 8], [16, 7], [17, 7], [18, 30], [19, 7], [20, 73], [21, 4], [22, 4], [23, 4], [24, 4],
           [25, 3], [26, 4], [27, 4], [28, 4], [29, 4], [30, 4], [31, 72], [32, 4], [33, 4], [34, 4], [35, 4], [36, 4],
           [37, 4], [38, 4], [39, 0], [40, 2], [41, 9], [42, 11]]
c = [[1, 0.3], [2, 1], [3, 1], [4, 1], [5, 0.1], [6, 0.2], [7, 0.05], [8, 0.14], [9, 0.14], [10, 0.08], [11, 0.3],
     [12, 0.4], [13, 0.27], [14, 0.15], [15, 0.1], [16, 1], [17, 1], [18, 0.0075], [19, 0.005], [20, 0.05], [21, 0.15],
     [22, 2], [23, 1.5], [24, 0.2], [25, 0.01], [26, 0.3], [27, 5], [28, 0.1], [29, 0.2], [30, 0.1], [31, 1],
     [32, 0.1], [33, 0.25], [34, 13], [35, 4], [36, 3.6], [37, 7.5], [38, 3], [39, 0.5], [40, 2], [41, 14], [42, 0.75]]
trTransSize = [[1, [916000, 1455000]],
                [2, [1755000, 151, 6430000]],
                [3, [22095000]],
                [4, [21950000, 2000000]],
                [5, [22065000, 1050000]],
                [6, [21485000, 20085000]],
                [7, [19844000]],
                [8, [3216000, 3058000, 2821000, 2670000, 14800000, 18899000, 18712000]],
                [9, [2728000, 2737000, 2583000, 2418000, 11911000, 16977000, 17726000]],
                [10, [2729000, 2667000, 2495000, 2437000, 13658000, 18936000, 19074000]],
                [11, [2970000, 2764000, 2609000, 2413000, 12717000, 17780000, 18194000]],
                [12, [2944000, 2836000, 2645000, 2472000, 12749000, 17627000, 19078000]],
                [13, [3058000, 2797000, 2700000, 2673000, 339000]],
                [14, [3006000, 2811000, 2661000, 2520000, 13600000, 18648000, 7071000]],
                [15, [4601000]],
                [16, [3721000]],
                [17, [3624000]],
                [18, [4665000, 4067000]],
                [19, [20085000, 250000]],
                [20, [20162000, 20092000]],
                [21, [4108000]],
                [22, [5508000]],
                [23, [19099000, 383000]],
                [24, [285000, 19085000]],
                [25, [18953000, 18924000, 19731000, 14500]],
                [26, [19611500]],
                [27, [833000, 831500, 81800, 2729500, 2747500]],
                [28, [1992500, 2282500]],
                [29, [19553000]],
                [30, [18962500]],
                [31, [16990000]],
                [32, [19658000]],
                [33, [19178000]],
                [34, [18137000, 18347000, 18754500]],
                [35, [19609500]],
                [36, [19264500]],
                [37, [18837000]],
                [38, [19679000]],
                [39, [2428500]],
                [40, [970000, 4260]],
                [41, [18849500]],
                [42, [4851000]]]

#####----- QUICK CALCS -----#####
def toSec(time):
    # converts string-time to float-time in seconds
    # ex: '02/17/2010 17:45:29.301' --> 63929.301
    hr = slice(11, 13, 1)
    fHr = float(time[hr])
    min = slice(14, 16, 1)
    fMin = float(time[min])
    sec = slice(17, 19, 1)
    fSec = float(time[sec])
    m_sec = slice(20, 23, 1)
    fM_sec = float(time[m_sec])
    return (fHr * 3600) + (fMin * 60) + fSec + (fM_sec / 1000)

#####----- EXTRACTION & TRANSFORMATION VARIABLES-----#####
structSize = 0                          # size of a row in the embedded transient arrays
startUp = startUp[int(mosfet - 1)][1]   # start up length
calibrator = c[int(mosfet - 1)][1]      # calibrates Rds values
gsV = 10.0                              # gate signal voltage threshold for determining ON versus OFF state
testSSsamples = 0                       # total number of steadyState samples in test
testTsamples = 0                        # total number of transient samples in test
testTime = 0.0                          # time from beginning to end of entire test
timeCounter = 0                         # keeps track of variables in masterData and masterTime
cleaned = []                            # data that has been normalized to the gate-to-source voltage
cleanTime = []                          # time array to match 'cleaned' array (for testing)
cleanShifted = []                       # add shift to cleaned data
sampleNumber = 0                        # keeps track of sampled data index
death = trDeath[int(mosfet) - 1][1]
validated, validatedGSoV = [], []       # ON-State data
masterData, masterTime = [], []         # final data used for rul predictions
semiData = []
rawCaseTemp = []                        # paper references flange temp as case temp
rawPackageTemp = []                     # package temperature

#####----- EXTRACTION & TRANSFORMATION -----#####
for run in range(testRun[int(mosfet) - 1][1]):
    data = loadmat("Test_" + str(mosfet) + "_run_" + str(run + 1) + '.mat')
    print("Test_" + str(mosfet) + "_run_" + str(run + 1) + '.mat')

    # choose measurement
    stuff = data['measurement']

    # choose pwmTempControllerState / steadyState / transient
    steadyState = stuff['steadyState']
    transient = stuff['transient']
    pwm = stuff['pwmTempControllerState']

    # keep track of time
    runStart = toSec(steadyState[0]['date'])
    runEnd = toSec(steadyState[len(steadyState) - 1]['date'])
    runTime = runEnd - runStart
    if (runEnd < runStart): runTime = (toSec("00/00/0000 23:59:59.999") - runStart) + runEnd
    testTime += runTime

    structSize = len(transient[0]['timeDomain']['drainSourceVoltage'])

    runSSsamples = len(steadyState)
    testSSsamples += runSSsamples
    runTsamples = structSize * len(transient)
    testTsamples += runTsamples

    rawGSoV = []  # raw gate-to-source voltage measurements
    rawRES = []  # all drain-source resistance calculations, ON and OFF state
    validity = []  # keeps track of ON-state and OFF-state samples

    # calculate and add all ON-State drain-source resistances, even if they are invalid
    for i in range(len(transient)):
        for j in range(structSize):
            vDS = transient[i]['timeDomain']['drainSourceVoltage'][j]
            cD = transient[i]['timeDomain']['drainCurrent'][j]
            rawRES.append(float(vDS) / float(cD)) # input drain-source resistance
            rawGSoV.append(transient[i]['timeDomain']['gateSourceVoltage'][j])

            if (transient[i]['timeDomain']['gateSignalVoltage'][j] > gsV): validity.append(1) # ON-State
            else: validity.append(0) # OFF-State

        # temperature data
    for i in range(len(steadyState)):
        rawCaseTemp.append(steadyState[i]['timeDomain']['flangeTemperature'])
        rawPackageTemp.append(steadyState[i]['timeDomain']['packageTemperature'])

    #####----- CLEANING VARIABLES -----#####
    runCleaned = []        # validated data after a cleaning function has been implemented
    cleanTracker = 0    # keeps track of transient index
    #####----- CLEANING -----#####
    for i in range(math.floor(runTsamples / structSize)): # looping through every 'burst' of transient data
        onCount = 0         # number of on-state samples in set
        RESonTotal = 0.0    # all ON-state drain-to-source resistance
        GSoVonTotal = 0.0   # all ON-state gate-to-source voltage

        for j in range(structSize):
            if (validity[cleanTracker]):
                onCount += 1
                RESonTotal += rawRES[cleanTracker]
                GSoVonTotal += rawGSoV[cleanTracker]
            cleanTracker += 1

        if (onCount != 0):
            tempValidated = RESonTotal / onCount
            tempValidatedGSoV = GSoVonTotal / onCount
            validated.append(tempValidated)
            validatedGSoV.append(tempValidatedGSoV)
            transformation = tempValidated * math.sqrt(abs(1.0 / tempValidatedGSoV)) * calibrator
            runCleaned.append(transformation)
            cleaned.append(transformation)
            # cleaning equation logic below
            # - normalized to square root based on: gate-to-source voltage / 250C ratio
            # - damped (10%)

    #####----- SAMPLING VARIABLES -----#####
    sampled = []  # cleaned data after minute sampling rate has been implemented
    sampleTime = []  # time array to match 'sampled' array (for testing)
    sampleTracker = 0  # keeps track of sample index
    samplesPerMin = math.floor((len(runCleaned) / runTime) * 60)

    #####----- SAMPLING -----#####
    for minute in range(math.floor(len(runCleaned) / samplesPerMin)):
        setTotal = 0.0
        for i in range(samplesPerMin):
            setTotal += runCleaned[sampleTracker]
            sampleTracker += 1
        sampled.append(setTotal / samplesPerMin)
        sampleTime.append(sampleNumber)
        sampleNumber += 1

    print("length of sampled = " + str(len(sampled)))
    #####----- EDITING VARIABLES -----#####
    edited = []

    multiplyer = 0.0005
    if (mosfet == 10 or mosfet == 31): multiplyer = 0.00005
    elif (mosfet == 19): multiplyer = 0.005
    #####----- EDITING -----#####
    if (len(sampled) > startUp): # for runs that are longer than four minutes
        actual = sampled[startUp]
        for fix in range(startUp):
            edited.append(actual - ((startUp - fix) * multiplyer))
        for remaining in range(len(sampled) - startUp):
            edited.append(sampled[remaining + startUp])
    else: # for runs that are four minutes or less in length
        for item in range(len(sampled)):
            edited.append(item * multiplyer)

    #####----- SHIFTING VARIABLES -----#####
    print("length of edited = " + str(len(edited)))
    if (len(semiData) > 0): shift = edited[0] - semiData[timeCounter - 1]
    else: shift = edited[0]
    shifted = []
    if (run == 0): correctShift = edited[0]


    print("the shift value = " + str(shift))

    #####----- SHIFTING -----#####
    for i in range(len(edited)):
        shifted.append(edited[i] - shift)

    #####----- CONCATENATE TO REST OF DATA -----#####
    for newData in range(len(shifted)):
        semiData.append(shifted[newData])
        masterTime.append(timeCounter)
        timeCounter += 1

bgt = 10
if (mosfet == 26): bgt = 500
print("bgt = " + str(bgt))
masterData.append(semiData[0])
for i in range(len(semiData) - 1):
    n = i + 1
    jump = semiData[n] - masterData[len(masterData) - 1]
    # print("jump = " + str(jump))
    # print("semiData[n] = " + str(semiData[n]))
    # print("masterTime[n] = " + str(masterTime[n]))
    # print("failure threshold = " + str(failureThreshold))
    if (mosfet == 27 or mosfet == 28 or mosfet == 41 or mosfet == 42):
        masterData.append(abs(semiData[n]))
    else:
        if (semiData[n] > failureThreshold and masterTime[n] < death):
            if (masterData[len(masterData) - 1] + (jump / bgt) > failureThreshold):
                masterData.append(0.049)
                print(" made it to 0.049")
            else:
                masterData.append(masterData[len(masterData) - 1] + (jump / bgt))
                print(" made it to bgt")
        else: masterData.append(semiData[n])
    # print("masterData[n] = " + str(masterData[n]))
    # print()
tempTime = []
tempIncr = (testTime / 60) / len(rawCaseTemp)
for i in range(len(rawCaseTemp)):
    tempTime.append(i * tempIncr)

cleanedIncr = (testTime / 60) / len(cleaned)
for items in range(len(cleaned)):
    cleanTime.append(items * cleanedIncr)
    cleanShifted.append(cleaned[items] - cleaned[800])

dataCleaning = time.perf_counter()

if (death <= 40): split = 1
elif (death > 40 and death <= 120): split = 3
elif (death > 120 and death <= 300): split = 5
else: split = 10

#####----- PLOTTING VARIABLES -----#####
highError = death * ((100 + int(rulError)) / 100)
lowError = death * ((100 - int(rulError)) / 100)
x = np.arange(0.0, death + 1, 1.0)
Yh = -((highError / death) * x) + highError
Ym = -x + death
Yl = -((lowError / death) * x) + lowError

#####----- BASIC REGRESSION VARIABLES (br) -----#####
if (testTime / 60 > death): determiner = death
else: determiner = testTime / 60

predictions = math.floor(determiner / split)
brRegression = []
brTime = []
brALL = []
lastRUL = highError
print("this is the size of predictions " + str(predictions))
#####----- BASIC REGRESSION (br) -----#####
for i in range(len(masterData) - 1):
    n = i + 1
    if (n <= death):
        if (n % split == 0 and i > 0):
            Yc = masterData[n]
            Yp = masterData[0]
            Xc = n
            Xp = 0
            slope = (Yc - Yp) / (Xc - Xp)
            b = (Yc / Xc) - slope
            Xo = -b * (1 / slope)
            Xeol = (failureThreshold + slope - (Yc / Xc)) / slope
            rul = Xeol - Xc
            rulPercent = 100 * ((Xeol - Xc) / (Xeol - Xo))
            if ((rul >= 0.0) and (rul < (lastRUL + 20)) and rul < 2 * highError):
                brTime.append(n)
                if (Yc < failureThreshold): brRegression.append(rul)
                else: brRegression.append(0)
            lastRUL = rul # intentional removal of outliers
            brALL.append(rul)

basicRegression = time.perf_counter()

#####----- LINEAR REGRESSION VARIABLES (lin) -----#####
sumX, sumX2, sumY, sumXY = 0, 0, masterData[0], 0
linRegression = []
linTime = []
lastRUL = highError
linALL = []

#####----- LINEAR REGRESSION (lin) -----#####
for i in range(len(masterData) - 1):
    n = i + 1
    if (n <= death):
        sumX += n
        sumX2 += (n * n)
        sumY += masterData[n]
        sumXY += (n * masterData[n])
        if (n % split == 0 and i > 0):
            b = ((n * sumXY) - (sumX * sumY)) / ((n * sumX2) - (sumX * sumX))
            a = (sumY - (b * sumX)) / n
            Xeol = (failureThreshold - a) / b
            rul = Xeol - n
            if ((rul >= 0.0) and (rul < (lastRUL + 20)) and rul < 2 * highError):
                linTime.append(n)
                if (masterData[n] < failureThreshold):linRegression.append(rul)
                else: linRegression.append(0)
            lastRUL = rul
            linALL.append(rul)

linearRegression = time.perf_counter()

#####----- EXPONENTIAL REGRESSION VARIABLES (exp) -----#####
sumX, sumX2, sumY, sumXY = 0, 0, masterData[0], 0
expRegression = []
expTime = []
rnn = []
lastRUL = highError
expALL = []
rnnTime = []
rnnTempTime = []

#####----- EXPONENTIAL REGRESSION (exp) -----#####
for i in range(len(masterData) - 1):
    n = i + 1
    if (n <= death):
        sumX += ln(n)
        sumX2 += (ln(n) * ln(n))
        if (masterData[n] > 0):
            sumY += ln(masterData[n])
            sumXY += (ln(n) * ln(masterData[n]))
        if (n % split == 0 and i > 0):
            b = ((n * sumXY) - (sumX * sumY)) / ((n * sumX2) - (sumX * sumX))
            a = exp((sumY - (b * sumX)) / n)
            Xeol = exp(ln(failureThreshold / a) / b)
            other = failureThreshold / a
            rul = Xeol - n
            if ((rul >= 0.0) and (rul < (lastRUL + 20)) and rul < 2 * highError):
                expTime.append(n)
                if (masterData[n] < failureThreshold):expRegression.append(rul)
                else: expRegression.append(0)
            lastRUL = rul
            expALL.append(rul)
            rnnTempTime.append(n)


exponentRegression = time.perf_counter()

print("length of brALL " + str(len(brALL)))
print("length of linALL " + str(len(linALL)))
print("length of expALL " + str(len(expALL)))
print("length of rnnTempTime " + str(len(rnnTempTime)))

hi2 = highError * 2
for i in range(len(brALL)):
    a, b, c = linALL[i], expALL[i], brALL[i]
    if (rnnTempTime[i] >= death):
        rnnTime.append(rnnTempTime[i])
        rnn.append(0)
    else:
        if ((a > hi2 or a < 0) and (b > hi2 or b < 0) and (c > hi2 or c < 0)): out = 32
        else:
            if (a > hi2 or a < 0): a = ln(abs(a) + 1) * 10
            else: a = abs(linALL[i] - (death - rnnTempTime[i])) / 2
            if (b > hi2 or b < 0): b = ln(abs(b) + 1) * 10
            else: b = abs(expALL[i] - (death - rnnTempTime[i])) / 2
            if (c > hi2 or c < 0): c = ln(abs(c) + 1) * 10
            else: c = abs(brALL[i] - (death - rnnTempTime[i])) / 2
            ave = (a + b + c + (death - rnnTempTime[i])) / 4
            if (ave < hi2 and ave >= 0):
                if (ave > death - rnnTempTime[i]): ave -= ln(ave)
                else: ave += ln(ave)
                rnn.append(ave)
                rnnTime.append(rnnTempTime[i])

iFault, sFault = [0], [0]
ifTime, sfTime = [0], [0]

sFaultK = [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1],
           [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1], [25, 1],
           [26, 1], [27, 5], [28, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1], [35, 1], [36, 1], [37, 1],
           [38, 1], [39, 1], [40, 1], [41, 1], [42, 1]]

#####----- FAULTS -----#####
for i in range(len(cleanShifted) - 1):
    # standard fault
    sfTime.append(cleanTime[i + 1])
    if (validated[i + 1] > (validated[i] + sFaultK[int(mosfet) - 1][1])): sFault.append(1)
    else: sFault.append(0)

    # incipient fault happen as both the top and bottom of a wave form diminishes
    ifTime.append(cleanTime[i + 1])
    if (i < len(cleanShifted) - 9):
        a = validated[i + 8]
        b = validated[i + 7]
        c = validated[i + 6]
        d = validated[i + 5]
        e = validated[i + 4]
        f = validated[i + 3]
        g = validated[i + 2]
        h = validated[i + 1]
        j = validated[i]
        if ((a < c and c < e and e < g and g < j) and (b < d and d < f and f < h)): iFault.append(1)
        else: iFault.append(0)
    else: iFault.append(0)

#####----- ERROR CALCULATIONS -----#####
count = 0
temp = 0
brError = 0
for i in range(len(brRegression) - 1):
    if (brRegression[i] < highError and brRegression[i] > 0):
        count += 1
        temp += (1 - (brRegression[i] / (death - brTime[i]))) * 100
if (count == 0): brError = 1000
else: brError = temp / count

count = 0
temp = 0
linError = 0
for i in range(len(linRegression) - 1):
    if (linRegression[i] < highError and linRegression[i] > 0):
        count += 1
        temp += (1 - (linRegression[i] / (death - linTime[i]))) * 100
if (count == 0): linError = 1000
else: linError = temp / count

count = 0
temp = 0
expError = 0
for i in range(len(expRegression) - 1):
    if (expRegression[i] < highError and expRegression[i] > 0):
        count += 1
        temp += (1 - (expRegression[i] / (death - expTime[i]))) * 100
if (count == 0): expError = 1000
else: expError = temp / count

count = 0
temp = 0
rnnError = 0
for i in range(len(rnn) - 1):
    if (rnn[i] < highError and rnn[i] > 0):
        count += 1
        temp += (1 - (rnn[i] / (death - rnnTime[i]))) * 100
if (count == 0): rnnError = 1000
else: rnnError = temp / count

print("Error for Basic Regression = " + str(brError))
print("Error for Linear Regression = " + str(linError))
print("Error for Exponential Regression = " + str(expError))
print("Error for RNN = " + str(rnnError))

#####----- DATAFRAMES -----#####
#rul and faults
plt.figure()

plt.subplot(211)
plt.title("MOSFET " + str(mosfet) + " Health Monitoring")
plt.plot(x, Yh, color='gainsboro')
plt.plot(x, Yl, color='gainsboro')
plt.fill_between(x, Yl, Yh, color='gainsboro')
plt.plot(x, Ym, color='dimgray')
plt.plot(brTime, brRegression, color='red', marker='^', label="Basic Regression")
plt.plot(linTime, linRegression, color='yellow', marker='o', label="Linear Regression")
plt.plot(expTime, expRegression, color='green', marker='s', label="Exponential Regression")
plt.plot(rnnTime, rnn, color='purple', marker='d', label="Recurrent Neural Network")
plt.legend()
plt.ylabel('RUL (Minutes)')
plt.grid(True)

plt.subplot(212)
plt.plot(ifTime, iFault, color='blue', label="Incipient Fault")
plt.plot(sfTime, sFault, color='red', label="Standard Fault")
plt.ylabel('Fault State (ON or OFF)')
plt.xlabel("Time (min)")
plt.legend()
plt.grid(True)

#raw rds and cleaned rds
plt.figure()
print('previous length: ')
print(len(cleanTime))
print(len(validated))
plt.subplot(211)
plt.title("MOSFET " + str(mosfet) + " ON-State Drain-to-Source Resistance")
plt.plot(cleanTime, validated, color='black', label="Raw ON-State Drain-to-Source Resistance")
plt.legend()
plt.ylabel('Resistance (Ohms)')
plt.grid(True)

plt.subplot(212)
plt.plot(masterTime, masterData, color='red', label="Cleaned ON-State Drain-to-Source Resistance")
plt.legend()
plt.ylabel('Resistance (Ohms)')
plt.xlabel("Time (Minutes)")
plt.grid(True)

#flange temp and package temp
plt.figure()

plt.title("MOSFET " + str(mosfet) + " Temperature Data")
plt.plot(tempTime, rawCaseTemp, color='purple', label="Case Temperature")
plt.plot(tempTime, rawPackageTemp, color='black', label="Package Temperature")
plt.legend()
plt.ylabel('Temperature (C)')
plt.xlabel('Time (minutes)')
plt.grid(True)

#gate to source voltage
plt.figure()

plt.title("MOSFET " + str(mosfet) + " Gate-to-Source Voltage Data")
plt.plot(cleanTime, validatedGSoV, color='black', linewidth=1, label="On-State Gate-to-Source Voltage")
plt.legend()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (Minutes)')
plt.grid(True)


#####----- PLOTTING -----#####
plt.figure()

plt.subplot(211)
plt.title("MOSFET " + str(mosfet) + " Data Based on Gate-to-Source Voltage")
plt.plot(cleanTime, validated, color='black', label="Raw Data")
plt.plot(cleanTime, cleanShifted, color='blue', label="Cleaned Data")
plt.plot(masterTime, masterData, color='red', label="Sampled Data")
plt.legend()
plt.ylabel('\N{GREEK CAPITAL LETTER DELTA}RDSon (Ohms)')
plt.grid(True)

plt.subplot(212)
plt.plot(cleanTime, validatedGSoV, color='black', linewidth=1, label="On-State Gate-to-Source Voltage")
plt.legend()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (minutes)')
plt.grid(True)

plt.figure()

plt.title("MOSFET " + str(mosfet) + " RUL Prediction")
plt.plot(x, Yh, color='gainsboro')
plt.plot(x, Yl, color='gainsboro')
plt.fill_between(x, Yl, Yh, color='gainsboro')
plt.plot(x, Ym, color='dimgray')
plt.plot(brTime, brRegression, color='red', marker='^', label="Basic Regression")
plt.plot(linTime, linRegression, color='yellow', marker='o', label="Linear Regression")
plt.plot(expTime, expRegression, color='green', marker='s', label="Exponential Regression")
plt.plot(rnnTime, rnn, color='purple', marker='d', label="Recurrent Neural Network")
plt.legend()
plt.ylabel('RUL (Minutes)')
plt.xlabel('Time (minutes)')
plt.grid(True)

plt.figure()

plt.subplot(211)
plt.title("MOSFET " + str(mosfet) + " Fault Investigation")
plt.plot(ifTime, iFault, color='blue', label="Incipient Fault")
plt.plot(sfTime, sFault, color='red', label="Standard Fault")
plt.ylabel('Fault State')
plt.legend()
plt.grid(True)

plt.subplot(212)
plt.plot(cleanTime, validated, color='black', label="Raw Data")
plt.legend()
plt.xlabel('Time (minutes)')
plt.ylabel('\N{GREEK CAPITAL LETTER DELTA}RDSon (Ohms)')
plt.grid(True)

plotting = time.perf_counter()
totTime = plotting - start
print()
print("Time breakdown:")
print("       Opening & Cleaning Data = " + str(round(((dataCleaning - start) / totTime) * 100000) / 1000) + "%")
print("         Basic Regression Calc = " + str(round(((basicRegression - dataCleaning) / totTime) * 100000) / 1000) + "%")
print("        Linear Regression Calc = " + str(round(((linearRegression - basicRegression) / totTime) * 100000) / 1000) + "%")
print("   Exponential Regression Calc = " + str(round(((exponentRegression - linearRegression) / totTime) * 100000) / 1000) + "%")
print("                All Algorithms = " + str(round(((exponentRegression - dataCleaning) / totTime) * 100000) / 1000) + "%")
print("                 Plotting Data = " + str(round(((plotting - basicRegression) / totTime) * 100000) / 1000) + "%")
print()
print("    OPENING & CLEANING the data took " + str(round((dataCleaning - start) * 1000000) / 1000000) + " seconds")
print("          BASIC REGRESSION CALC took " + str(round((basicRegression - dataCleaning) * 1000000) / 1000000) + " seconds")
print("         LINEAR REGRESSION CALC took " + str(round((linearRegression - basicRegression) * 1000000) / 1000000) + " seconds")
print("               EXPONENTIAL CALC took " + str(round((exponentRegression - linearRegression) * 1000000) / 1000000) + " seconds")
print("                 ALL ALGORITHMS took " + str(round((exponentRegression - dataCleaning) * 1000000) / 1000000) + " seconds")
print("              PLOTTING the data took " + str(round((plotting - basicRegression) * 1000000) / 1000000) + " seconds")
print()
print("   Total time to PROCESS the data it took " + str(round((totTime) * 1000000) / 1000000) + " seconds")

plt.show()

# Notes to convert to DataFrame: (please add a legend to every graph)
#
# For RUL Predictions put these arrays together on one graph:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "RUL (Minutes)" (y-axis)
#   - Basic Regression RUL:             brTime (x-axis)-------------brRegression (y-axis)
#   - Linear Regression RUL:            linTime (x-axis)------------linRegression (y-axis)
#   - Exponential Regression RUL:       expTime (x-axis)------------expRegression (y-axis)
#   - Recurrent Neural Network RUL:     rnnTime (x-axis)------------rnn (y-axis)
#   - perfect trend line:               x (x-axis)------------------Ym (y-axis
#
#
# For Fault Predictions put these arrays together on one graph:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "Fault State (ON or OFF)" (y-axis)
#   - Incipient Fault:                  ifTime (x-axis)-------------iFault (y-axis)
#   - Standard Fault:                   sfTime (x-axis)-------------sFault (y-axis)
#
#
# For Raw ON-State Drain-to-Source Resistance put this array by itself:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "Resistance (Ohms)" (y-axis)
#   - Raw ON-State Rds:                 cleanTime (x-axis)----------validated (y-axis)
#
#
# For Cleaned ON-State Drain-to-Source Resistance put this array by itself:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "Resistance (Ohms)" (y-axis)
#   - Cleaned ON-State Rds:             masterTime (x-axis)---------masterData (y-axis)
#
#
# For Temperature Data put these arrays together on one graph:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "Temperature (C)" (y-axis)
#   - Case Temperature:                 tempTime (x-axis)-----------rawCaseTemp (y-axis)
#   - Package Temperature:              tempTime (x-axis)-----------rawPackageTemp (y-axis)
#
#
# For ON-State Gate-to-Source Voltage put this array by itself:
# Axis labels should be as follows: "Time (Minutes)" (x-axis), "Voltage (V)" (y-axis)
#   - ON-State Vgs:                     cleanTime (x-axis)----------validatedGSoV (y-axis)
