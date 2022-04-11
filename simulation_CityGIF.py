"""
Simulation
"""

# python libraries
import simpy
import random
import numpy as np
import pandas as pd
from datetime import datetime
import time
# my files
import airshipClass
import cityClass
import hubClass
import airshipDesignCalculator as ADC
import AirshipImpactMetrics as AIM
import AirshipCostModel as ACM
import fruit as fp
import BoatModel as BM
from cityDistributionGenerator import generate_new_cities
# One airship, One city
# Initialize airship, city, simulation

def run_simulation(AirshipDesigns,numberOfNewCities = 0):
    print(datetime.now())
    AirshipDesignParameterTracker = np.zeros((np.size(AirshipDesigns,0),17),dtype=float)
    ImpactTracker = np.zeros((np.size(AirshipDesigns,0),5),dtype=float)
    OtherOuputs = np.zeros((np.size(AirshipDesigns,0),40),dtype=float)
    counter = 0 
    tic = time.perf_counter()
    for dataDOE in AirshipDesigns:
        # define environment
        np.random.seed(96)
        SimTime = 365.0 * 24.0 # hours
        Workday = [8.0,17.0] # start hour, end hour
        FruitData = fp.fruit(numberOfNewCities)

        env = simpy.Environment()

        # create hub
        # Hub Attributes #
        hubCoordinates = [-3.117, -60.025]      # Manaus, BZ
        AvgUnloadingRate = 0.05 # hours/ton
        UnloadingResource = 1
        AvgRepairTime = 0.1
        RepairResource = 1
        AvgRefuelTime = 0.5
        RefuelResource = 1
        hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, 
                        AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource)

        # create cities
        # City Attributes #
        cityCoordinates = [ [-3.196, -59.826],  # Careiro
                            [-3.276, -60.190],  # Iranduba
                            [-3.387, -60.344],  # Jutai
                            [-3.441, -60.462]]  # Manaquiri
        LoadingResources = 1
        # FarmerCount = [77., 166., 47., 97.]
        boatCount = np.array([5., 7., 7., 12.]) # [5.+5., 7.+28., 7.+4., 12.+7.] # with manaus boats divided between
        CityToHubBoatDistance =  np.array([8.8, 19.3, 39.1, 48.6]) #nautical miles
        if numberOfNewCities > 0:
            cityCoordinates,newcitydistances = generate_new_cities(numberOfNewCities, hubCoordinates, cityCoordinates)
            boatM = np.mean(boatCount)
            boatS = np.std(boatCount)
            newboats = np.round(np.abs(np.random.default_rng(96).normal(boatM,boatS,numberOfNewCities)),0)
            boatCount = np.append(boatCount,newboats)
            CityToHubBoatDistance = np.append(CityToHubBoatDistance,newcitydistances)
        cities = [cityClass.City(env, c, cityCoordinates[c], FruitData, boatCount[c], 
                                CityToHubBoatDistance[c], LoadingResources)
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
            airshipCostPerAirshipInFleet, heliumRefillCost = ACM.calculate_operational_cost(airship,FleetSize)
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
            "Airship 1 End Workday": airshipFleet[1].TimeEndedWorkday,
            "Time Savings": impactMetrics.I_TimeSavings,
            "Crop Loss": impactMetrics.I_CropLoss*np.ones(365),
            "Income": impactMetrics.I_Income*np.ones(365),
            "Boat Job Loss": impactMetrics.I_BoatJobLoss*np.ones(365),
            "Forest Loss": impactMetrics.I_ForestLoss*np.ones(365)
        }
    )

    dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
    outputByDay.to_csv(str(dataDOE[0]) + '-'+ str(dataDOE[1]) + '-'+str(dataDOE[2]) + '_outputByDay'+dtstr+'.csv')
    outputTimeSeries.to_csv(str(dataDOE[0]) + '-'+ str(dataDOE[1]) + '-'+str(dataDOE[2]) + '_outputTimeSeries'+dtstr+'.csv')


AirshipDesigns = np.array([[8,	20,	2,	0.5,	0.2,	0.3,	0.05,	3]])
run_simulation(AirshipDesigns)




###########################################
################ LEFT OFF: ################
###########################################
# - 
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
