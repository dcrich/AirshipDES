import numpy as np
import matplotlib.pyplot as plt

def generate_designs(payloadrange=[1,31], speedrange=[20,101], fleetrange=[1,6], threshrange=[0.0,1], loadraterange=[0.1,0.5], setsize = [1,1,1], setlength=[1,1]):
    payload = np.arange(payloadrange[0],payloadrange[1], setsize[0])
    speed = np.arange(speedrange[0], speedrange[1], setsize[1])
    fleet = np.arange(fleetrange[0],fleetrange[1], setsize[2])
    payloadG, speedG, fleetG = np.meshgrid(payload, speed, fleet)
    payloadG=payloadG.flatten()
    speedG=speedG.flatten()
    fleetG=fleetG.flatten()

    loadThreshold = np.linspace(threshrange[0],threshrange[1], setlength[0])
    loadRate = np.linspace(loadraterange[0],loadraterange[1], setlength[1])
    payloadDOE1 = np.array([])
    speedDOE1 = np.array([])
    fleetDOE1 = np.array([])
    thresholdDOE1 = np.array([])
    for thresh in loadThreshold:
        payloadDOE1 = np.append(payloadDOE1,payloadG)
        speedDOE1 = np.append(speedDOE1,speedG)
        fleetDOE1 = np.append(fleetDOE1,fleetG)
        thresholdDOE1 = np.append(thresholdDOE1,thresh*np.ones(np.size(payloadG),dtype=float))
    payloadDOE = np.array([])
    speedDOE = np.array([])
    fleetDOE = np.array([])
    thresholdDOE = np.array([])
    rateDOE = np.array([])
    for rate in loadRate:
        payloadDOE = np.append(payloadDOE,payloadDOE1)
        speedDOE = np.append(speedDOE,speedDOE1)
        fleetDOE = np.append(fleetDOE,fleetDOE1)
        thresholdDOE = np.append(thresholdDOE,thresholdDOE1)
        rateDOE = np.append(rateDOE,rate*np.ones(np.size(payloadDOE1),dtype=float))
    payloadfraction = 0.3 * np.ones(np.shape(payloadDOE))
    fueltankfraction = 0.05 * np.ones(np.shape(payloadDOE))
    finenessratio = 3 * np.ones(np.shape(payloadDOE))
    
    designset = np.array([payloadDOE, speedDOE, fleetDOE, 
                          thresholdDOE,rateDOE,
                          payloadfraction, fueltankfraction,finenessratio, 
                          ]).transpose()
    numberOfRuns = np.size(designset,0)
    print(numberOfRuns)
    estimatedTimeToComplete = 0.028 * numberOfRuns
    if estimatedTimeToComplete < 60:
        print("Estimated Time To Complete: " + str(estimatedTimeToComplete) + " minutes")
    else:
        print("Estimated Time To Complete: " + str(estimatedTimeToComplete/60.0) + " hours")
    return designset

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(payloadG, speedG, fleetG)
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# plt.show()

# designset, payloadG, speedG, fleetG, payloadfraction, fueltankfraction, finenessratio = generate_designs()

# mu = 0.1
# sigma = 0.75
# l = np.abs(np.random.default_rng().normal(mu,sigma,10000))
# count, bins, ignored = plt.hist(l, 30, density=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                 np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#                 linewidth=2, color='r')
# plt.show()