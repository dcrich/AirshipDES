"""
Simulation
- Sundays are included
- no random numbers
"""

# python libraries
from itertools import count
import os
import time
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
from generatorDOE import generate_designs

# DOE_filename = "AirshipDesignsTest.txt"
# DOE_filename = "AirshipDesigns750fleet.txt" 
# DOE = pd.read_csv(DOE_filename) #load DOE data
# AirshipDesigns = DOE.values
AirshipDesigns, payloadG, speedG, fleetG, payloadfraction, fueltankfraction, finenessratio = generate_designs(payloadrange=[1,16], speedrange=[20,101], fleetrange=[1,3], setsize = 100)

AirshipDesignParameterTracker = np.zeros((np.size(AirshipDesigns,0),15),dtype=float)
ImpactTracker = np.zeros((np.size(AirshipDesigns,0),5),dtype=float)
OtherOuputs = np.zeros((np.size(AirshipDesigns,0),11),dtype=float)
counter = 0 
tic = time.perf_counter()
for dataDOE in AirshipDesigns:
    # define environment
    random.seed(96)
    SimTime = 365.0 * 24.0 # hours
    Workday = [8.0,17.0] # start hour, end hour
    FruitData = fp.fruit()

    env = simpy.Environment()

    # create hub
    # Hub Attributes #
    hubCoordinates = [-3.117, -60.025]      # Manaus, BZ
    # hubCoordinates = [-3.0, -60.0] 
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
                        [-3.276, -60.190]]#,  # Iranduba
                        # [-3.387, -60.344],  # Jutai
                        # [-3.441, -60.462]]  # Manaquiri
    # cityCoordinates = [ [-2.9, -59.9],  
    #                     [-2.9, -60.1],  
    #                     [-3.1, -59.9],  
    #                     [-3.1, -60.1]]  
    AvgLoadingRate = 0.1 # hours/ton
    LoadingResources = 1
    FarmerCount = [77., 166., 47., 97.]
    boatCount = [5., 7., 7., 12.] # [5.+5., 7.+28., 7.+4., 12.+7.] # with manaus boats divided between
    CityToHubBoatDistance =  [8.8, 19.3, 39.1, 48.6] #nautical miles
    cities = [cityClass.City(env, c, cityCoordinates[c], FruitData, FarmerCount[c], boatCount[c], CityToHubBoatDistance[c], AvgLoadingRate, LoadingResources)
                    for c in range(len(cityCoordinates))]

    # create airships 
    # Airship Attributes #
    dataDOE[2] = round(dataDOE[2])
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
    fuelUsed = 0.0
    totalTrips = 0
    emptyTrips = 0
    for airship in airshipFleet:
        fuelUsed += np.sum(airship.DailyFuelConsumption)
        totalTrips += airship.citiesVisitedInTotal
        emptyTrips += airship.EmptyTrips
    AirshipDesignParameterTracker[counter,:] = airshipFleet[0].return_airship_parameters()
    ImpactTracker[counter,:] = impactMetrics.return_impact_array()
    OtherOuputs[counter,0] = impactMetrics.AirshipRevenue
    OtherOuputs[counter,1] = impactMetrics.AirshipLoadTime
    OtherOuputs[counter,2] = impactMetrics.produceSoldByAllBoats #sold by boat
    OtherOuputs[counter,3] = impactMetrics.BoatTripLoss
    OtherOuputs[counter,4] = fuelUsed
    OtherOuputs[counter,5] = totalTrips
    OtherOuputs[counter,6] = emptyTrips
    OtherOuputs[counter,7] = np.sum(cities[0].AvailableGoods) #Careiro
    OtherOuputs[counter,8] = np.sum(cities[1].AvailableGoods) #Iranduba
    # OtherOuputs[counter,9] = np.sum(cities[2].AvailableGoods) #Jutai
    # OtherOuputs[counter,10] = np.sum(cities[3].AvailableGoods) #Manaquiri

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
        "Range": AirshipDesignParameterTracker[:,14],
        "Boat Job Loss": ImpactTracker[:,0],
        "Crop Loss": ImpactTracker[:,1],
        "Forest Loss": ImpactTracker[:,2],
        "Income": ImpactTracker[:,3],
        "Time Savings": ImpactTracker[:,4],
        "Airship Revenue": OtherOuputs[:,0],
        "Airship Load Time": OtherOuputs[:,1],
        "Transported By Boat": OtherOuputs[:,2],
        "Boat Trip Loss": OtherOuputs[:,3],
        "Fuel Used": OtherOuputs[:,4],
        "Total Trips": OtherOuputs[:,5],
        "Lost Careio": OtherOuputs[:,6],
        "Lost Iranduba": OtherOuputs[:,7],
        "Lost Jutai": OtherOuputs[:,8],
        "Lost Manaquiri": OtherOuputs[:,9]
    }
)

dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
outputImpacts.to_csv('ExperimentImpacts'+dtstr+'.csv')
toc = time.perf_counter()

os.system(f'say -v {"Fiona"} {"I am done computing."}')
timeToRun = (toc-tic)/60.0
if timeToRun < 60:
    print(timeToRun)
    print('Minutes')
else:
    print(timeToRun/60.0)
    print('Hours')

###########################################
################ LEFT OFF: ################
###########################################
# Bugs when visiting multiple cities
#   - How can the airships know if another airship is already enroute and will pick up the cargo?
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


