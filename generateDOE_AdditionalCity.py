import numpy as np
import matplotlib.pyplot as plt

def generate_designs_and_cities(payloadrange=10, speedrange=40, threshrange=1, loadraterange=0.2,fleetrange=[1,2], latRange=[-3.117, -3.6], lonRange=[-60.72,-59.6], setLatSteps = 100, setLonSteps=100):
    fleet = np.linspace(fleetrange[0],fleetrange[1], 2)
    lat = np.linspace(latRange[0],latRange[1], setLatSteps)
    lon = np.linspace(lonRange[0],lonRange[1], setLonSteps)
    latG, lonG, fleetG = np.meshgrid(lat, lon, fleet)
    latDOE=latG.flatten()
    lonDOE=lonG.flatten()
    fleetDOE=fleetG.flatten()
    payloadDOE = payloadrange * np.ones(np.shape(fleetDOE))
    speedDOE = speedrange * np.ones(np.shape(fleetDOE))
    thresholdDOE = threshrange * np.ones(np.shape(fleetDOE))
    rateDOE = loadraterange * np.ones(np.shape(fleetDOE))
    payloadfraction = 0.3 * np.ones(np.shape(fleetDOE))
    fueltankfraction = 0.05 * np.ones(np.shape(fleetDOE))
    finenessratio = 3 * np.ones(np.shape(fleetDOE))

    designset = np.array([payloadDOE, speedDOE, fleetDOE, 
                          thresholdDOE,rateDOE,
                          payloadfraction, fueltankfraction,finenessratio, 
                          latDOE, lonDOE ]).transpose()
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

# designset = generate_designs_and_cities()

# mu = 0.1
# sigma = 0.75
# l = np.abs(np.random.default_rng().normal(mu,sigma,10000))
# count, bins, ignored = plt.hist(l, 30, density=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                 np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#                 linewidth=2, color='r')
# plt.show()