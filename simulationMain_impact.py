"""
Simulation
"""

# python libraries
import os
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

# DOE_filename = "AirshipDesignsTest.txt"
DOE_filename = "AirshipDesignsTestFleet.txt" 
DOE = pd.read_csv(DOE_filename) #load DOE data
AirshipDesigns = DOE.values
AirshipDesignParameterTracker = np.zeros((np.size(AirshipDesigns,0),15),dtype=float)
ImpactTracker = np.zeros((np.size(AirshipDesigns,0),5),dtype=float)
RevenueLoadTime = np.zeros((np.size(AirshipDesigns,0),2),dtype=float)
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
    hubCoordinates = [-3.117, -60.025]      # Manaus, BZ
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

    AirshipDesignParameterTracker[counter,:] = airshipFleet[0].return_airship_parameters()
    ImpactTracker[counter,:] = impactMetrics.return_impact_array()
    RevenueLoadTime[counter,0] = impactMetrics.AirshipRevenue
    RevenueLoadTime[counter,1] = impactMetrics.AirshipLoadTime
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
        "Airship Revenue": RevenueLoadTime[:,0],
        "Airship Load Time": RevenueLoadTime[:,1]
    }
)

dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
outputImpacts.to_csv('ExperimentImpacts'+dtstr+'.csv')

os.system(f'say -v {"Fiona"} {"I am done computing."}')

###########################################
################ LEFT OFF: ################
###########################################
# rethink crop loss logic. rn ranges from prior loss to ?
# test fleets
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


