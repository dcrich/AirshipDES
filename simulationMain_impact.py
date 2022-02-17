"""
Simulation
"""

# python libraries
import simpy
import random
import numpy as np
import pandas as pd
from datetime import datetime
# my files
import airshipClass
import cityClass
import hubClass
import airshipDesignCalculator as ADC
import AirshipImpactMetrics as AIM
import AirshipCostModel as ACM
import fruit as fp
import BoatModel as BM


DOE_filename = "AirshipDesigns.txt" #DONE
DOE = pd.read_csv(DOE_filename) #load DOE data
AirshipDesigns = DOE.values
AirshipDesignParameterTracker = np.zeros((np.size(AirshipDesigns,0),14),dtype=float)
ImpactTracker = np.zeros((np.size(AirshipDesigns,0),5),dtype=float)
counter = 0 
for dataDOE in AirshipDesigns:
    # define environment
    random.seed(96)
    SimTime = 365.0 * 24.0 # hours
    Workday = [8.0,17.0] # start hour, end hour
    FruitData = fp.fruit()

    env = simpy.Environment()

    # create hub
    # Hub Attributes #
    hubCoordinates = [-3.039, -60.048]      # Manaus, BZ
    AvgUnloadingRate = 0.05 # hours/ton
    UnloadingResource = 1
    AvgRepairTime = 0.0
    RepairResource = 1
    AvgRefuelTime = 1.0
    RefuelResource = 1
    hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource)

    # create cities
    # City Attributes #
    cityCoordinates = [ [-3.139, -60.248],  # Careiro
                        [-3.441, -60.462],  # Iranduba
                        [-3.387, -60.344],  # Jutai
                        [-3.276, -60.190] ] # Manaquiri
    AvgLoadingRate = 0.1 # hours/ton
    LoadingResources = 1
    FarmerCount = [77., 166., 47., 97.]
    boatCount = [5., 7., 7., 12.] # [5.+5., 7.+28., 7.+4., 12.+7.] # with manaus boats divided between
    CityToHubBoatDistance =  [8.8, 19.3, 39.1, 48.6] #nautical miles
    cities = [cityClass.City(env, c, cityCoordinates[c], FruitData, FarmerCount[c], boatCount[c], CityToHubBoatDistance[c], AvgLoadingRate, LoadingResources)
                    for c in range(len(cityCoordinates))]

    # create airships 
    # Airship Attributes #
    FleetSize = dataDOE[2]
    airshipAttributes = ADC.DesignAirship(dataDOE) # useful payload, fuel capacity, footprint
    airshipFleet = [airshipClass.Airship(env, a, airshipAttributes, hub, cities, Workday)
                    for a in range(int(FleetSize))]

    env.run(until=SimTime)

    # airship cost modeling
    for airship in airshipFleet:
        ACM.calculate_operational_cost(airship,FleetSize)
    # model boat use
    boats = [BM.Boats(cities[c], Workday[0], FruitData)
                    for c in range(len(cityCoordinates))]
    # Calculate Social Impacts
    impactMetrics = AIM.AirshipImpactMetrics(airshipFleet, hub, cities, FruitData, boats)

    AirshipDesignParameterTracker[counter,:] = airshipFleet[0].return_airship_parameters()
    ImpactTracker[counter,:] = impactMetrics.return_impact_array()
    counter += 1



# Data by experiment
outputImpacts = pd.DataFrame(
    {
        "Payload": AirshipDesignParameterTracker[:,0],
        "CruiseSpeed": AirshipDesignParameterTracker[:,1],
        "FleetSize": AirshipDesignParameterTracker[:,2],
        "PayloadFraction": AirshipDesignParameterTracker[:,3],
        "FuelTankFraction": AirshipDesignParameterTracker[:,4],
        "FinenessRatio": AirshipDesignParameterTracker[:,5],
        "CylinderFraction": AirshipDesignParameterTracker[:,6],
        "UsefulPayload": AirshipDesignParameterTracker[:,7],
        "FuelCapacity": AirshipDesignParameterTracker[:,8],
        "AirshipVolume_ft": AirshipDesignParameterTracker[:,9],
        "Diameter": AirshipDesignParameterTracker[:,10],
        "Length": AirshipDesignParameterTracker[:,11],
        "Footprint": AirshipDesignParameterTracker[:,12],
        "RequiredHorsepower": AirshipDesignParameterTracker[:,13],
        "Boat Job Loss": ImpactTracker[:,0],
        "Crop Loss": ImpactTracker[:,1],
        "Income": ImpactTracker[:,2],
        "Forest Loss": ImpactTracker[:,3],
        "Time Savings": ImpactTracker[:,4]
    }
)

dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
outputImpacts.to_csv('ExperimentImpacts'+dtstr+'.csv')


import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = AirshipDesignParameterTracker[:,0]
Y = AirshipDesignParameterTracker[:,1]

Z = ImpactTracker[:,2]

# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(np.min(Z), np.max(Z))
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.0f}')

ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Time Savings')

# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

###########################################
################ LEFT OFF: ################
###########################################
# - Output all data to files, output social impacts to surface plots, check data
# - might need to add constraint for hangars space for fleet
#   - maybe add environmental impact of forest loss needed for airship storage
###########################################
###########################################
###########################################



###################################
########## Stretch Goals: ##########
###################################
# - test simulation
# - output to database, save output time series data for each experiment
# - take simulation tracker and make it into a gif of the simulation
#   - airships move between temporal locations 
#   - airships are an oval ouline and are filled based on payload and fuel levels
