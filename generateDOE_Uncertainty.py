import numpy as np
import matplotlib.pyplot as plt

def generate_designs_uncertainty(payloadrange=10, speedrange=[30,88], threshrange=1, loadraterange=0.2,fleetrange=1,setNumber=1000):
    speedArray = np.arange(speedrange[0],speedrange[1], 1)
    speedDOE = speedArray.copy()
    for i in range(setNumber):
        speedDOE = np.append(speedDOE,speedArray)
    fleetDOE = fleetrange* np.ones(np.shape(speedDOE))
    payloadDOE = payloadrange * np.ones(np.shape(speedDOE))
    thresholdDOE = threshrange * np.ones(np.shape(speedDOE))
    rateDOE = loadraterange * np.ones(np.shape(speedDOE))
    payloadfraction = 0.3 * np.ones(np.shape(speedDOE))
    fueltankfraction = 0.05 * np.ones(np.shape(speedDOE))
    finenessratio = 3 * np.ones(np.shape(speedDOE))

    designset = np.array([payloadDOE, speedDOE, fleetDOE, 
                          thresholdDOE,rateDOE,
                          payloadfraction, fueltankfraction,finenessratio]).transpose()
    numberOfRuns = np.size(designset,0)
    print(numberOfRuns)
    estimatedTimeToComplete = 0.028 * numberOfRuns
    if estimatedTimeToComplete < 60:
        print("Estimated Time To Complete: " + str(estimatedTimeToComplete) + " minutes")
    else:
        print("Estimated Time To Complete: " + str(estimatedTimeToComplete/60.0) + " hours")
    return designset

# generate_designs_uncertainty()