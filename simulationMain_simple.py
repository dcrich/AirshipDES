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
import AirshipImpactMetrics
import AirshipCostModel as ACM
import fruit
import BoatModel as BM

# One airship, One city
# Initialize airship, city, simulation

# define environment
random.seed(96)
SimTime = 365.0 * 24.0 # hours
WorkdayLength = 8.0
FruitData = fruit()
hubCoordinates = [-3.039, -60.048]      # Manaus, BZ
cityCoordinates = [ [-3.139, -60.248],  # city
                    [-3.441, -60.462],  # city
                    [-3.387, -60.344],  # city
                    [-3.276, -60.190] ] # city
# Hub Attributes #
AvgUnloadingRate = 50.0 # tons/hour
UnloadingResource = 1
AvgRepairTime = 0.0
RepairResource = 1
AvgRefuelTime = 1.0
RefuelResource = 1

# City Attributes #
AvailableGoods = np.ones(365)*100.0
AvgLoadingRate = 50.0 # tons/hour
LoadingResources = 1

# Airship Attributes #
# Airship Parameters: payload, payload fraction, fuel tank fraction, speed, fineness ratio, fleet
dataDOE = np.array([100.0, 0.3, 0.003, 60.0, 3.0, 1])

# for d in range(np.size(dataDOE, 0)): # loop through DOE for airship parameters
env = simpy.Environment()

# create hub
hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource)

# create cities
cities = [cityClass.City(env, 'City_%d'%c, cityCoordinates[c], AvailableGoods, AvgLoadingRate, LoadingResources)
                for c in range(len(cityCoordinates))]

# create airships 
airshipAttributes = ADC.DesignAirship(dataDOE) # useful payload, fuel capacity, footprint
airshipFleet = [airshipClass.Airship(env, 'RED_%d'%a, airshipAttributes, hub, cities)
                for a in range(int(dataDOE[5]))]

env.run(until=SimTime)

# airship cost modeling
for airship in airshipFleet:
    ACM.calculate_operational_cost(airship)
# model boat use
boats = [BM.Boats(cities[c], WorkdayLength, FruitData)
                for c in range(len(cityCoordinates))]
# Calculate Social Impacts
impactMetrics = AirshipImpactMetrics(airshipFleet, hub, cities, FruitData, boats)



logicDifferences = np.array(airshipFleet[0].SimulationLogic[1:])-np.array(airshipFleet[0].SimulationLogic[0:-1])
logicDifferences = np.insert(logicDifferences,0,0)
outputDFL = pd.DataFrame(
    {
        "SimulationLogic": airshipFleet[0].SimulationLogic,
        "Differences": logicDifferences
    }
)
outputDF = pd.DataFrame(
    {
        "SimulationTime": hub.SimulationTracker[:,0],
        "Airship": hub.SimulationTracker[:,1],
        "Activity": hub.SimulationTracker[:,2],
        "PayloadLevel": hub.SimulationTracker[:,3],
        "FuelLevel": hub.SimulationTracker[:,4]
    }
)

dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
# outputDFL.to_csv('SimulationLogic'+dtstr+'.csv')
outputDF.to_excel('SimulationTracker'+dtstr+'.xls',sheet_name='Discrete Event Tracker')
#########################################


# One airship, All cities, Fruit schedule - Make new sim file

# Fleet of airships, All cities, Fruit schedule, social impact - make new sim file



# LEFT OFF:
# Finish airship cost function, test it
# test boat model
# test simulation
# test social impact model





# Stretch Goal:
# take simulation tracker and make it into a gif of the simulation
# - airships move between temporal locations 
# - airships are an oval ouline and are filled based on payload and fuel levels
