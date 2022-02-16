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

# One airship, One city
# Initialize airship, city, simulation

# define environment
random.seed(96)
SimTime = 365.0 * 24.0 # hours
Workday = [8.0,17.0] # start hour, end hour
FruitData = fp.fruit()

# for d in range(np.size(dataDOE, 0)): # loop through DOE for airship parameters
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
# Airship Parameters: payload, payload fraction, fuel tank fraction, speed, fineness ratio, fleet
dataDOE = np.array([22.5, 0.3, 0.3, 60.0, 3.0, 1])
FleetSize = dataDOE[5]
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
outputResults = pd.DataFrame(
    {
        "Production": FruitData.DailyFruitProduction,
        "Careiro Fruit Loss": cities[0].AvailableGoods,
        "Iranduba Fruit Loss": cities[1].AvailableGoods,
        "Jutai Fruit Loss": cities[2].AvailableGoods,
        "Manaquiri Fruit Loss": cities[3].AvailableGoods,
        "Careiro Visits": cities[0].NumberOfVisits,
        "Iranduba Visits": cities[1].NumberOfVisits,
        "Jutai Visits": cities[2].NumberOfVisits,
        "Manaquiri Visits": cities[3].NumberOfVisits
    }
)

dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
# outputDFL.to_csv('SimulationLogic'+dtstr+'.csv')
# outputDF.to_excel('SimulationTracker'+dtstr+'.xls',sheet_name='Discrete Event Tracker')
# outputResults.to_excel('CityTracker'+dtstr+'.xls',sheet_name='FruitLoss')




#########################################


# One airship, All cities, Fruit schedule - Make new sim file

# Fleet of airships, All cities, Fruit schedule, social impact - make new sim file



# LEFT OFF:
# Finish airship cost function, test it
# test boat model
# test simulation
# test social impact model
# might need to add constraint for hangars space for fleet
#   - maybe add environmental impact of forest loss needed for airship storage



# Stretch Goal:
# take simulation tracker and make it into a gif of the simulation
# - airships move between temporal locations 
# - airships are an oval ouline and are filled based on payload and fuel levels
