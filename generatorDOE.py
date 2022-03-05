import numpy as np
import matplotlib.pyplot as plt

def generate_designs(payloadrange=[1,31], speedrange=[20,101], fleetrange=[1,6], setsize = 100):
    if setsize == 100:
        payload = np.arange(payloadrange[0],payloadrange[1], 2)
        speed = np.arange(speedrange[0], speedrange[1], 2)
        fleet = np.arange(fleetrange[0],fleetrange[1], 1)
    else:
        payload = np.arange(payloadrange[0],payloadrange[1], 1)
        speed = np.arange(speedrange[0], speedrange[1], 1)
        fleet = np.arange(fleetrange[0],fleetrange[1], 1)
    payloadG, speedG, fleetG = np.meshgrid(payload, speed, fleet)
    payloadfraction = 0.3 * np.ones(np.shape(payloadG))
    fueltankfraction = 0.05 * np.ones(np.shape(payloadG))
    finenessratio = 3 * np.ones(np.shape(payloadG))
    designset = np.array([payloadG.flatten(), speedG.flatten(), fleetG.flatten(), payloadfraction.flatten(), fueltankfraction.flatten(), finenessratio.flatten()]).transpose()
    return designset, payloadG, speedG, fleetG, payloadfraction, fueltankfraction, finenessratio

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(payloadG, speedG, fleetG)
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()
# designset, payloadG, speedG, fleetG, payloadfraction, fueltankfraction, finenessratio = generate_designs()