"""
Simulation
- Sundays are included
- no random numbers
"""

# python libraries
import os
import time
import simpy
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
from cityDistributionGenerator import generate_new_cities


# DOE_filename = "AirshipDesignsTest.txt"
# DOE_filename = "AirshipDesigns750fleet.txt" 
# DOE = pd.read_csv(DOE_filename) #load DOE data
# AirshipDesigns = DOE.values
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
        # hubCoordinates = [-3.205, -60.025] 
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
        
        # cityCoordinates = [ [-3.293, -60.196],  
        #                     [-3.293, -59.854], 
        #                     [-3.010, -60.025]]
        # AvgLoadingRate = 0.1 # hours/ton
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
        fuelUsed = 0.0
        totalTrips = 0
        emptyTrips = 0
        loadWaitTime = 0.0
        TotalHoursWorked = 0.0
        HoursWorked = np.zeros((1,int(FleetSize)))
        unloadTime = 0.0
        refuelTime = 0.0
        maintenanceTime = 0.0
        a=0
        for airship in airshipFleet:
            fuelUsed += np.sum(airship.DailyFuelConsumption)
            totalTrips += airship.citiesVisitedInTotal
            emptyTrips += airship.EmptyTrips
            loadWaitTime += airship.loadWaitTime
            tempvar = np.sum(Workday[1]-Workday[0] - airship.DailyOverOrUnderTime)
            TotalHoursWorked += tempvar
            HoursWorked[0,a] = tempvar
            unloadTime += airship.UnloadTime
            refuelTime += airship.RefuelTime
            maintenanceTime += airship.MaintenanceTime
            a+=1

        AirshipDesignParameterTracker[counter,:] = airshipFleet[0].return_airship_parameters()
        ImpactTracker[counter,:] = impactMetrics.return_impact_array()
        OtherOuputs[counter,0] = impactMetrics.AirshipRevenue
        OtherOuputs[counter,1] = impactMetrics.AirshipLoadTime
        OtherOuputs[counter,2] = impactMetrics.produceSoldByAllBoats #sold by boat
        OtherOuputs[counter,3] = impactMetrics.BoatTripLoss
        OtherOuputs[counter,4] = fuelUsed
        OtherOuputs[counter,5] = totalTrips
        OtherOuputs[counter,6] = emptyTrips
        OtherOuputs[counter,7] = loadWaitTime
        OtherOuputs[counter,8] = np.sum(cities[0].AvailableGoods) #Careiro
        OtherOuputs[counter,9] = np.sum(cities[1].AvailableGoods) #Iranduba
        OtherOuputs[counter,10] = np.sum(cities[2].AvailableGoods) #Jutai
        OtherOuputs[counter,11] = np.sum(cities[3].AvailableGoods) #Manaquiri
        OtherOuputs[counter,12] = impactMetrics.AirshipOperationalCostPerTon
        OtherOuputs[counter,13] = impactMetrics.BoatCostPerTonWithAirship
        OtherOuputs[counter,14] = impactMetrics.BoatCostPerTonNoAirship
        OtherOuputs[counter,15] = impactMetrics.I_CropLoss_IncludingBoat
        OtherOuputs[counter,16] = TotalHoursWorked
        OtherOuputs[counter,17] = TotalHoursWorked / (FleetSize * 365.0 * Workday[0])
        OtherOuputs[counter,18] = TotalHoursWorked / (FleetSize * 365.0 * 24.0)
        OtherOuputs[counter,19] = np.sum(unloadTime)
        OtherOuputs[counter,20] = np.sum(refuelTime)
        OtherOuputs[counter,21] = np.sum(maintenanceTime)
        OtherOuputs[counter,22] = airshipCostPerAirshipInFleet
        OtherOuputs[counter,23] = heliumRefillCost
        lastcolumn = 24
        # lastcolumn2 = lastcolumn+int(FleetSize)
        # tempvar2 = HoursWorked
        # OtherOuputs[counter,lastcolumn:lastcolumn2] = tempvar2
        if numberOfNewCities>0:
            for i in range(numberOfNewCities):
                OtherOuputs[counter,lastcolumn+i] = np.sum(cities[4+i].AvailableGoods) #new city
        counter += 1



    # Data by experiment
    outputImpacts = pd.DataFrame(
        {
            "Payload": AirshipDesignParameterTracker[:,0],
            "CruiseSpeed": AirshipDesignParameterTracker[:,1],
            "FleetSize": AirshipDesignParameterTracker[:,2],
            "LoadThreshold":AirshipDesignParameterTracker[:,15],
            "AvgLoadRate":AirshipDesignParameterTracker[:,16],
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
            "Boat Trip Loss": OtherOuputs[:,3],
            "Crop Loss": ImpactTracker[:,1],
            "Forest Loss": ImpactTracker[:,2],
            "Income": ImpactTracker[:,3],
            "Time Savings": ImpactTracker[:,4],
            "Airship Revenue": OtherOuputs[:,0],
            "Airship Load Time": OtherOuputs[:,1],
            "Transported By Boat": OtherOuputs[:,2],
            "Boat Job Loss": ImpactTracker[:,0],
            "Fuel Used": OtherOuputs[:,4],
            "Total Trips": OtherOuputs[:,5],
            "Empty Trips": OtherOuputs[:,6],
            "Load Wait Time": OtherOuputs[:,7],
            "AirshipCostPerTon":OtherOuputs[:,12],
            "Boat Cost Per Ton Airship":OtherOuputs[:,13],
            "Boat Cost Per Ton Only":OtherOuputs[:,14],
            "Crop Loss Including Boat": OtherOuputs[:,15],
            "Total Usage Hours Fleet":OtherOuputs[:,16],
            "Utilization Fraction Fleet":OtherOuputs[:,17],
            "Real Utilization Fraction Fleet":OtherOuputs[:,18],
            "Unload Time":OtherOuputs[:,19],
            "Refuel Time":OtherOuputs[:,20],
            "Maintenance Time":OtherOuputs[:,21],
            "Individual Airship Acquisition Cost":OtherOuputs[:,22],
            "Helium Refill Cost":OtherOuputs[:,23],

            "Lost Careio": OtherOuputs[:,8],
            "Lost Iranduba": OtherOuputs[:,9],
            "Lost Jutai": OtherOuputs[:,10],
            "Lost Manaquiri": OtherOuputs[:,11]
        }
    )
    if numberOfNewCities > 0:
        newcityoutputs = pd.DataFrame({})
        for i in range(numberOfNewCities):
            varname = "New City "+str(i)
            outputImpacts.insert(outputImpacts.shape[1],varname,OtherOuputs[:,lastcolumn+i])
    
    print(datetime.now())
    dtstr = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
    outputImpacts.to_csv('ExperimentImpacts'+dtstr+'.csv')
    
    os.system(f'say -v {"Fiona"} {"I am done computing."}')
    toc = time.perf_counter()
    timeToRun = (toc-tic)/60.0
    if timeToRun < 60:
        print(timeToRun)
        print('Minutes')
    else:
        print(timeToRun/60.0)
        print('Hours')




#SIMULATIONS
#Threshold cutoff is between 0.057 and 0.07 for profitability, any other changes may just be affecting the schedule
# Main
AirshipDesigns = generate_designs(
    payloadrange=[1.,31.], speedrange=[20.,88.], fleetrange=[1.,5.], 
    threshrange=[0.25,0.75], loadraterange=[0.2,0.5], setsize = [1,1,1], setlength=[2,1])
run_simulation(AirshipDesigns)

# # Threshold Sensitivity - sparse
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,91], fleetrange=[1,5], 
#     threshrange=[0.0,1], loadraterange=[0.2,0.5], setsize = [2,5,1], setlength=[10,1])
# run_simulation(AirshipDesigns)

# # Threshold Sensitivity Test - Very sparse
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,81], fleetrange=[1,5], 
#     threshrange=[0.0,1], loadraterange=[0.1,0.5], setsize = [10,10,1], setlength=[4,1])
# run_simulation(AirshipDesigns)

# # Load Rate Sensitivity - sparse
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,88], fleetrange=[3,5], 
#     threshrange=[1.0,1.0], loadraterange=[0.1,0.5], setsize = [1,1,1], setlength=[1,5])
# run_simulation(AirshipDesigns)

# # Load Rate Sensitivity Test - Very sparse
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,81], fleetrange=[1,5], 
#     threshrange=[0.0,1], loadraterange=[0.1,0.5], setsize = [10,10,1], setlength=[1,4])
# run_simulation(AirshipDesigns)

# AirshipDesigns = generate_designs(
#     payloadrange=[1,26], speedrange=[20,91], fleetrange=[1,6], 
#     threshrange=[0.0,1], loadraterange=[0.1,0.5], setsize = [1,5,1], setlength=[3,3])
# run_simulation(AirshipDesigns)

# # Main with Threshold
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,91], fleetrange=[1,5], 
#     threshrange=[0.0,1], loadraterange=[0.2,0.5], setsize = [1,5,1], setlength=[10,1])
# run_simulation(AirshipDesigns)

# # Stretch Threshold
# AirshipDesigns = generate_designs(
#     payloadrange=[1,31], speedrange=[20,91], fleetrange=[1,5], 
#     threshrange=[1.0,10.0], loadraterange=[0.2,0.5], setsize = [2,10,1], setlength=[10,1])
# run_simulation(AirshipDesigns)

## TESTS
# # Main
# AirshipDesigns = generate_designs(
#     payloadrange=[9.,31.], speedrange=[38.,88.], fleetrange=[1.,2.], 
#     threshrange=[0.5,1.0], loadraterange=[0.2,0.5], setsize = [1,1,1], setlength=[1,1])
# run_simulation(AirshipDesigns)

# AirshipDesigns = np.array([[16.0, 84., 1.0, 0.5, 0.2, 0.3, 0.05, 3]])
# run_simulation(AirshipDesigns)








###########################################
################ LEFT OFF: ################
###########################################
# Other values of interest
#   - Refuel Time, Maintenance Time, Unload Time, 
#   - Utilization (sitting around during workday, time between workdays)
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


