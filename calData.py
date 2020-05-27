from pip._vendor.distlib.compat import raw_input
from format_converter import loadmat
import matplotlib.pyplot as plt
import numpy as np
from numpy import log as ln
from numpy import exp
import pandas as pd
import time
import math

#####----- GLOBALS -----#####
# print("")
# print("Hello, this program calculates the remaining useful life (RUL) of TO-220AB Power MOSFETs over time.")
# print("In our database there are 42 different samples (MOSFET 1 - MOSFET 42). In order to calculate RUL, ")
# print("data scientists from the NASA AMES Research Center discovered that, die-attach degradation was ")
# print("determined to be the primary failure mode. The collected data from the 42 MOSFETs was initially ")
# print("analyzed and it was revealed that ON-state drain-to-source resistance increased as die-attach ")
# print("degraded under high thermal stresses. Therefore, ON-state drain-to-source resistance was used as ")
# print("the primary precursor to failure feature. For all prediction algorithms, the following thresholds ")
# print("are default: ")
# print("     --> Crisp ON-state drain-to-source resistance increase of 0.05 ohms")
# print("     --> Error margin of 20%")
# print("")
#
# answer1 = input('What MOSFET would you like to analyze? ')
# answer2 = input('What crisp failure value would you like to use? ')
# answer3 = input('What is the acceptable error margin for RUL? ')

# if (answer1 == ""): mosfet = int("1")
# else: mosfet = int(answer1)
# if (answer2 == ""): failureThreshold = 0.05
# else: failureThreshold = float(answer2)
# if (answer3 == ""): rulError = int("20")
# else: rulError = float(answer3)
# print("failure threshold is: " + str(failureThreshold))

failureThreshold = 0.05
rulError = int("20")
start = time.perf_counter()

testRun = [[1, 2], [2, 3], [3, 1], [4, 2], [5, 2], [6, 2], [7, 1], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 5],
           [14, 7], [15, 1], [16, 1], [17, 1], [18, 2], [19, 2], [20, 2], [21, 1], [22, 1], [23, 2], [24, 2], [25, 4],
           [26, 1], [27, 5], [28, 2], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 3], [35, 1], [36, 1], [37, 1],
           [38, 1], [39, 1], [40, 2], [41, 1], [42, 1]]

trDeath = [[1, 23], [2, 20], [3, 32], [4, 38], [5, 34], [6, 108], [7, 94], [8, 740], [9, 0], [10, 0], [11, 0],
           [12, 0], [13, 0], [14, 590], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0],
           [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0], [29, 0], [30, 0], [31, 0], [32, 0], [33, 0],
           [34, 1123], [35, 128], [36, 208], [37, 226], [38, 57], [39, 0], [40, 0], [41, 0], [42, 0]]

trError = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, -629], [8, 718], [9, 0], [10, 0], [11, 0],
           [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0],
           [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0], [29, 0], [30, 0], [31, 0], [32, 0], [33, 0],
           [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0], [40, 0], [41, 0], [42, 0]]

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

def getAllDF(mosfet):
    #####----- EXTRACTION VARIABLES-----#####
    arraySize = 0           # size of a row in the embedded transient arrays
    gsV = 10.0              # gate signal voltage threshold for determining ON versus OFF state
    rawCaseTemp = []        # paper references flange temp as case temp
    rawGSoV = []            # raw gate-to-source voltage measurements
    rawRES = []             # all drain-source resistance calculations, ON and OFF state
    ssTotal, tTotal = 0, 0  # total number of steadyState and transient samples
    totalTime = 0.0         # time from beginning to end of entire test
    validity = []           # keeps track of ON-state and OFF-state samples

    #####----- EXTRACTION -----#####
    for run in range(testRun[int(mosfet) - 1][1]):
        data = loadmat("Test_" + str(mosfet) + "_run_" + str(run + 1) + '.mat')
        print("Test_" + str(mosfet) + "_run_" + str(run + 1) + '.mat')

        # choose measurement
        stuff = data['measurement']

        # choose pwmTempControllerState / steadyState / transient
        steadyState = stuff['steadyState']
        transient = stuff['transient']
        pwm = stuff['pwmTempControllerState']

        runStart = toSec(steadyState[0]['date'])
        runEnd = toSec(steadyState[len(steadyState) - 1]['date'])

        if (runEnd < runStart): totalTime += ((toSec("00/00/0000 23:59:59.999") - runStart) + runEnd)
        else: totalTime += (runEnd - runStart)

        ssTotal += trSteadySize[int(mosfet) - 1][1][run]
        print("these are the total steadyState samples " + str(ssTotal))
        tTotal += trTransSize[int(mosfet) - 1][1][run]
        print("these are the total transient samples " + str(tTotal))

        arraySize = len(transient[0]['timeDomain']['drainSourceVoltage'])

        # calculate and add all ON-State drain-source resistances, even if they are invalid
        for i in range(len(transient)):
            for j in range(len(transient[0]['timeDomain']['drainSourceVoltage'])):
                vDS = transient[i]['timeDomain']['drainSourceVoltage'][j]
                cD = transient[i]['timeDomain']['drainCurrent'][j]
                rawRES.append(float(vDS) / float(cD)) # input drain-source resistance
                rawGSoV.append(transient[i]['timeDomain']['gateSourceVoltage'][j])

                if (transient[i]['timeDomain']['gateSignalVoltage'][j] > gsV): validity.append(1) # ON-State
                else: validity.append(0) # OFF-State

            # temperature data
        for i in range(len(steadyState)):
            rawCaseTemp.append(steadyState[i]['timeDomain']['flangeTemperature'])

    afterOpen = time.perf_counter()
    print("Time to open files = " + str(round((afterOpen - start) * 1000000) / 1000000) + " seconds")


    #####----- CLEANING VARIABLES -----#####
    cleaned = []                          # validated data after a cleaning function has been implemented
    cleanTime = []                      # time array to match 'cleaned' array (for testing)
    cleanTracker = 0                        # keeps track of transient index
    validated = []                      # removing OFF-state data
    validatedGSoV = []
    cleanIncr = (totalTime / (tTotal / arraySize)) / 60

    #####----- CLEANING -----#####
    for i in range(round(tTotal / arraySize)):
        onCount = 0  # number of on-state samples in set
        RESonTotal = 0.0  # all on-state d-s RES combined
        GSoVonTotal = 0.0

        for j in range(arraySize):
            if (validity[cleanTracker]):
                onCount += 1
                RESonTotal += rawRES[cleanTracker]
                GSoVonTotal += rawGSoV[cleanTracker]
            cleanTracker += 1

        if (onCount == 0):
            validated.append(0.0000001)
            validatedGSoV.append(0.0000001)
        else:
            validated.append(RESonTotal / onCount)
            validatedGSoV.append(GSoVonTotal / onCount)

    for i in range(round(tTotal / arraySize)):
        cleanTime.append(i * cleanIncr)
        cleaned.append(validated[i] * math.sqrt(1.0 / validatedGSoV[i]) * 0.1)
        #   cleaning process:
        #    - normalized to sqrt(gate-to-source voltage / 250C ratio)
        #    - damped (10%)

    #####----- SAMPLING VARIABLES -----#####
    minRate = round(len(cleaned) / (totalTime / 60)) - 1    # x samples per minute
    sampled = []                                            # cleaned data after minute sampling rate has been implemented
    sampleTime = []                                         # time array to match 'sampled' array (for testing)
    sampleTracker = 0                                       # keeps track of sample index

    #####----- SAMPLING -----#####
    for set in range(round(len(cleaned) / minRate) - 1):
        setTotal = 0.0
        for i in range(minRate):
            setTotal += cleaned[sampleTracker]
            sampleTracker += 1
        sampled.append(setTotal / minRate)
        sampleTime.append(set)

    #####----- SHIFTING VARIABLES -----#####
    shift = sampled[0]  # shift is based on sampled data
    shiftedClean = []   # shifted 'cleaned' data
    shiftedSample = []  # shifted 'sampled' data

    #####----- SHIFTING -----#####
    for i in range(len(cleaned)):
        shiftedClean.append(cleaned[i] - shift)

    for i in range(len(sampled)):
        shiftedSample.append(sampled[i] - shift)


    dataCleaning = time.perf_counter()
    print("Time to process data = " + str(round((dataCleaning - afterOpen) * 1000000) / 1000000) + " seconds")

    #####----- PLOTTING VARIABLES -----#####
    death = trDeath[int(mosfet) - 1][1]
    highError = death * ((100 + int(rulError)) / 100)
    lowError = death * ((100 - int(rulError)) / 100)
    x = np.arange(0.0, death + 1, 1.0)
    Yh = -((highError / death) * x) + highError
    Ym = -x + death
    Yl = -((lowError / death) * x) + lowError

    #####----- BASIC REGRESSION VARIABLES (br) -----#####
    brPredictions = round(death / 5)
    if ((death + 5) < (totalTime / 60)): brPredictions += 1
    elif (death > (totalTime / 60)): brPredictions -= 1
    brRegression = []
    brTime = []
    lastRUL = 100.0

    #####----- BASIC REGRESSION (br) -----#####
    for i in range(brPredictions):
        Yc = shiftedSample[(i + 1) * 5]
        Yp = shiftedSample[0]
        Xc = (i + 1) * 5
        Xp = 0
        slope = (Yc - Yp) / (Xc - Xp)
        b = (Yc / Xc) - slope
        Xo = -b * (1 / slope)
        Xeol = (failureThreshold + slope - (Yc / Xc)) / slope
        rul = Xeol - Xc
        rulPercent = 100 * ((Xeol - Xc) / (Xeol - Xo))
        if (rul >= 0.0):
            if (rul < (lastRUL + 20)):
                brTime.append((i + 1) * 5)
                brRegression.append(rul)

        lastRUL = rul

    basicRegression = time.perf_counter()
    print("Time to compute basic regression = " + str(round((basicRegression - dataCleaning) * 1000000) / 1000000) + " seconds")

    #####----- LINEAR REGRESSION VARIABLES (lin) -----#####
    sumX, sumX2, sumY, sumXY = 0, 0, shiftedSample[0], 0
    linRegression = []
    linTime = []

    #####----- LINEAR REGRESSION (lin) -----#####
    for i in  range(len(shiftedSample) - 1):
        n = i + 1
        sumX += n
        sumX2 += (n * n)
        sumY += shiftedSample[n]
        sumXY += (n * shiftedSample[n])
        if (n % 5 == 0):
            b = ((n * sumXY) - (sumX * sumY)) / ((n * sumX2) - (sumX * sumX))
            a = (sumY - (b * sumX)) / n
            Xeol = (failureThreshold - a) / b
            rul = Xeol - n
            if ((rul < highError) & (rul > 0)):
                linTime.append(n)
                linRegression.append(rul)

    linearRegression = time.perf_counter()
    print("Time to compute linear regression = " + str(round((linearRegression - basicRegression) * 1000000) / 1000000) + " seconds")

    #####----- EXPONENTIAL REGRESSION VARIABLES (exp) -----#####
    sumX, sumX2, sumY, sumXY = 0, 0, shiftedSample[0], 0
    expRegression = []
    expTime = []

    #####----- EXPONENTIAL REGRESSION (exp) -----#####
    for i in range(len(shiftedSample) - 1):
        n = i + 1
        sumX += ln(n)
        sumX2 += (ln(n) * ln(n))
        if (shiftedSample[n] > 0):
            sumY += ln(shiftedSample[n])
            sumXY += (ln(n) * ln(shiftedSample[n]))
        if (n % 5 == 0):
            b = ((n * sumXY) - (sumX * sumY)) / ((n * sumX2) - (sumX * sumX))
            a = exp((sumY - (b * sumX)) / n)
            Xeol = exp(ln(failureThreshold / a) / b)
            other = failureThreshold / a
            rul = Xeol - n
            if ((rul < highError) & (rul > 0)):
                expTime.append(n)
                expRegression.append(rul ** (1. / 2))

    slice("""
            other = failureThreshold / a
            rul = Xeol - n
            #if ((rul < highError) & (rul > 0)):
            if (rul > 0):
                expTime.append(n)
                exp1.append(other - n + death - 8)
                exp2.append(other - n)
                exp3.append(other - n + b)
                exp4.append(other - n + (100 * (other - n + b)))
                exp5.append(other - n + (100 * (other - n + a)))
                """)

    exponentRegression = time.perf_counter()
    print("Time to compute curve regression = " + str(round((exponentRegression - linearRegression) * 1000000) / 1000000) + " seconds")

    #####----- PLOTTING -----#####
    # plt.figure()
    #
    # plt.subplot(211)
    # plt.title("MOSFET " + str(mosfet) + " Data Based on Gate-to-Source Voltage")
    # plt.plot(cleanTime, validated, color='black', label="Raw Data") # this is the raw data for drain-source resistance from the original .mat file
    # plt.plot(cleanTime, shiftedClean, color='blue', label="Cleaned Data") # this is the drain-source resistance data before it is sampled
    # plt.plot(sampleTime, shiftedSample, color='red', label="Sampled Data") # this is the drain-source resistance data sampled with a 1 minute rate
    # plt.legend()
    # plt.ylabel('\N{GREEK CAPITAL LETTER DELTA}RDSon (Ohms)')
    # plt.grid(True)dui

    rawData_df = pd.DataFrame({'cleanTime': cleanTime, 'validated': validated})
    dsRes_df = pd.DataFrame({'cleanTime': cleanTime, 'shiftedClean': shiftedClean})
    dsResSampled_df = pd.DataFrame({'sampleTime': sampleTime, 'shiftedSample': shiftedSample})

    # plt.subplot(212)
    # plt.plot(cleanTime, validatedGSoV, color='black', linewidth=1, label="On-State Gate-to-Source Voltage") # this is the raw gate-source voltage data
    # plt.legend()
    # plt.ylabel('Voltage (V)')
    # plt.xlabel('Time (minutes)')
    # plt.grid(True)
    # plt.figure()
    gsVoltage = pd.DataFrame({'cleanTime': cleanTime, 'validatedGSoV': validatedGSoV})


    # plt.title("MOSFET " + str(mosfet) + " RUL Prediction")
    # plt.plot(x, Yh, color='gainsboro') # upper limit of error
    # plt.plot(x, Yl, color='gainsboro') # lower limit of error
    # plt.fill_between(x, Yl, Yh, color='gainsboro') # fill in between error limits
    # plt.plot(x, Ym, color='dimgray') # perfect error line
    # plt.plot(brTime, brRegression, color='red', marker='^', label="Basic Regression") # this is the rul predictions from the basic regression algorithm
    # plt.plot(linTime, linRegression, color='yellow', marker='o', label="Linear Regression") # this is the rul predictions from the linear regression algorithm
    # plt.plot(expTime, expRegression, color='green', marker='s', label="Exponential Regression") # this is the rul predictions from the exponential regression algorithm
    # plt.legend()
    # plt.ylabel('RUL (Minutes)')
    # plt.xlabel('Time (minutes)')
    # plt.grid(True)
    br_df = pd.DataFrame({'time': brTime, 'value': brRegression})
    lir_df = pd.DataFrame({'time': linTime, 'value': linRegression})
    expr_df = pd.DataFrame({'time': expTime, 'value': expRegression})

    #
    # plotting = time.perf_counter()
    # totTime = plotting - start
    # print("Time to plot data = " + str(round((plotting - basicRegression) * 1000000) / 1000000) + " seconds")
    # print()
    # print("Time breakdown:")
    # print("                  Opening File = " + str(round(((afterOpen - start) / totTime) * 100000) / 1000) + "%")
    # print("                 Cleaning Data = " + str(round(((dataCleaning - afterOpen) / totTime) * 100000) / 1000) + "%")
    # print("         Basic Regression Calc = " + str(round(((basicRegression - dataCleaning) / totTime) * 100000) / 1000) + "%")
    # print("        Linear Regression Calc = " + str(round(((linearRegression - basicRegression) / totTime) * 100000) / 1000) + "%")
    # print("   Exponential Regression Calc = " + str(round(((exponentRegression - linearRegression) / totTime) * 100000) / 1000) + "%")
    # print("                All Algorithms = " + str(round(((exponentRegression - dataCleaning) / totTime) * 100000) / 1000) + "%")
    # print("                 Plotting Data = " + str(round(((plotting - basicRegression) / totTime) * 100000) / 1000) + "%")
    #
    # plt.show()
    print(dsRes_df.size)
    return rawData_df, dsRes_df, dsResSampled_df, gsVoltage, br_df, lir_df, expr_df
#
# getAllDF(1)