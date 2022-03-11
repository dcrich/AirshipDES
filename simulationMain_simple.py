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
# hubCoordinates = [-3.117, -60.025]     # Manaus, BZ
hubCoordinates = [-3.205, -60.025] 
AvgUnloadingRate = 0.05 # hours/ton
UnloadingResource = 1
AvgRepairTime = 0.0
RepairResource = 1
AvgRefuelTime = 0.5
RefuelResource = 1
hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource)

# create cities
# City Attributes #
cityCoordinates = [ [-3.196, -59.826],  # Careiro
                    [-3.276, -60.190],  # Iranduba
                    [-3.387, -60.344],  # Jutai
                    [-3.441, -60.462]]  # Manaquiri
cityCoordinates = [ [-3.293, -60.196],  # Careiro
                    [-3.293, -59.854],  # Iranduba
                    [-3.010, -60.025]]
AvgLoadingRate = 0.1 # hours/ton
LoadingResources = 1
FarmerCount = [77., 166., 47., 97.]
boatCount = [5., 7., 7., 12.] # [5.+5., 7.+28., 7.+4., 12.+7.] # with manaus boats divided between
CityToHubBoatDistance =  [8.8, 19.3, 39.1, 48.6] #nautical miles
cities = [cityClass.City(env, c, cityCoordinates[c], FruitData, FarmerCount[c], boatCount[c], CityToHubBoatDistance[c], AvgLoadingRate, LoadingResources)
                for c in range(len(cityCoordinates))]

# create airships 
# Airship Attributes #
# Airship Parameters: Payload,Speed,FleetSize,PayloadFraction,FuelTankFraction,FinenessRatio
dataDOE = np.array([1.,44-3.,1.0,0.3,0.05,3])
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


# Data by time step, ?by experiment?
outputTimeSeries = pd.DataFrame(
    {
        "SimulationTime": hub.SimulationTracker[:,0],
        "Airship": hub.SimulationTracker[:,1],
        "Activity": hub.SimulationTracker[:,2],
        "PayloadLevel": hub.SimulationTracker[:,3],
        "FuelLevel": hub.SimulationTracker[:,4]
    }
)

# Data by day, ?by experiment?
outputByDay = pd.DataFrame(
    {
        "Simulation Day": np.arange(0,365,1),
        "Production": FruitData.DailyFruitProduction,
        "Careiro Fruit Loss": cities[0].AvailableGoods,
        "Iranduba Fruit Loss": cities[1].AvailableGoods,
        "Jutai Fruit Loss": cities[2].AvailableGoods,
        "Manaquiri Fruit Loss": cities[3].AvailableGoods,
        "Careiro Visits": cities[0].NumberOfVisits,
        "Iranduba Visits": cities[1].NumberOfVisits,
        "Jutai Visits": cities[2].NumberOfVisits,
        "Manaquiri Visits": cities[3].NumberOfVisits,
        "Careiro Load Time": cities[0].LoadingTime,
        "Iranduba Load Time": cities[1].LoadingTime,
        "Jutai Load Time": cities[2].LoadingTime,
        "Manaquiri Load Time": cities[3].LoadingTime,
        "Careiro Loaded Goods": cities[0].LoadedGoods,
        "Iranduba Loaded Goods": cities[1].LoadedGoods,
        "Jutai Loaded Goods": cities[2].LoadedGoods,
        "Manaquiri Loaded Goods": cities[3].LoadedGoods,
        "Airship 0 End Workday": airshipFleet[0].TimeEndedWorkday,
        # "Airship 1 End Workday": airshipFleet[1].TimeEndedWorkday,
        "Time Savings": impactMetrics.I_TimeSavings,
        "Crop Loss": impactMetrics.I_CropLoss*np.ones(365),
        "Income": impactMetrics.I_Income*np.ones(365),
        "Boat Job Loss": impactMetrics.I_BoatJobLoss*np.ones(365),
        "Forest Loss": impactMetrics.I_ForestLoss*np.ones(365)
    }
)

# outputByDay = pd.DataFrame(
#     {
#         "Simulation Day": np.arange(0,365,1),
#         "Production": FruitData.DailyFruitProduction,
#         "Careiro Fruit Loss": cities[0].AvailableGoods,
#         "Iranduba Fruit Loss": cities[1].AvailableGoods,
#         "Careiro Visits": cities[0].NumberOfVisits,
#         "Iranduba Visits": cities[1].NumberOfVisits,
#         "Careiro Load Time": cities[0].LoadingTime,
#         "Iranduba Load Time": cities[1].LoadingTime,
#         "Careiro Loaded Goods": cities[0].LoadedGoods,
#         "Iranduba Loaded Goods": cities[1].LoadedGoods,
#         "Airship 0 End Workday": airshipFleet[0].TimeEndedWorkday,
#         "Airship 1 End Workday": airshipFleet[1].TimeEndedWorkday,
#         "Time Savings": impactMetrics.I_TimeSavings,
#         "Crop Loss": impactMetrics.I_CropLoss*np.ones(365),
#         "Income": impactMetrics.I_Income*np.ones(365),
#         "Boat Job Loss": impactMetrics.I_BoatJobLoss*np.ones(365),
#         "Forest Loss": impactMetrics.I_ForestLoss*np.ones(365)
#     }
# )


# Data by experiment
# outputImpacts = pd.DataFrame(
#     {
#         "Time Savings": impactMetrics.I_TimeSavings,
#         "Crop Loss": impactMetrics.I_CropLoss,
#         "Income": impactMetrics.I_Income,
#         "Boat Job Loss": impactMetrics.I_BoatJobLoss,
#         "Forest Loss": impactMetrics.I_ForestLoss
#     }
# )


dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
outputByDay.to_csv(str(dataDOE[0]) + '-'+ str(dataDOE[1]) + '-'+str(dataDOE[2]) + '_outputByDay'+dtstr+'.csv')
outputTimeSeries.to_csv(str(dataDOE[0]) + '-'+ str(dataDOE[1]) + '-'+str(dataDOE[2]) + '_outputTimeSeries'+dtstr+'.csv')


# outputDF.to_excel('SimulationTracker'+dtstr+'.xls',sheet_name='Discrete Event Tracker')
# outputResults.to_excel('CityTracker'+dtstr+'.xls',sheet_name='FruitLoss')




###########################################
# One airship, All cities, Fruit schedule - Make new sim file
# Fleet of airships, All cities, Fruit schedule, social impact - make new sim file




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
