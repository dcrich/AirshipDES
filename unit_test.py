"""
Unit tests for:
- Boat Model
- Social impact metrics

Run in terminal using command:
'pytest -q unit_test.py'
OR 
For detailed output:
'pytest -v -rN --tb=no --no-header'
"""
import pytest # not used but needs to be installed
import numpy as np
import random
import simpy

import airshipClass
import cityClass
import hubClass
import airshipDesignCalculator as ADC
import AirshipImpactMetrics as aim
import AirshipCostModel as ACM
import fruit as fp
import BoatModel as BM

@pytest.fixture # make it so environment can be used in each test function
def sim_env():
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
    boatCount = [5.+5., 7.+28., 7.+4., 12.+7.]
    CityToHubBoatDistance =  [8.8, 19.3, 39.1, 48.6] #nautical miles
    cities = [cityClass.City(env, c, cityCoordinates[c], FruitData, FarmerCount[c], boatCount[c], CityToHubBoatDistance[c], AvgLoadingRate, LoadingResources)
                    for c in range(len(cityCoordinates))]

    # create airships 
    # Airship Attributes #
    # Airship Parameters: payload, payload fraction, fuel tank fraction, speed, fineness ratio, fleet
    dataDOE = np.array([5.0, 0.3, 0.02, 60.0, 3.0, 1])
    FleetSize = dataDOE[5]
    airshipAttributes = ADC.DesignAirship(dataDOE) # useful payload, fuel capacity, footprint
    airshipFleet = [airshipClass.Airship(env, a, airshipAttributes, hub, cities, Workday)
                    for a in range(int(FleetSize))]

    env.run(until=SimTime)
    return hub, cities, airshipFleet, FruitData



"""BOAT TESTS"""
def test_boat_surplus_with_surplus(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production low so there will definitely be a surplus
    cities[0].AvailableGoods = np.zeros(np.size(cities[0].AvailableGoods),dtype=float) 
    boat = BM.Boats(cities[0], 8.0, FruitData)
    # maxtripsperday = 70.79646017699113 * np.ones(np.size(cities[0].AvailableGoods),dtype=float) 
    # sundayIndex = np.arange(6,365,7)
    # np.put(maxtripsperday, sundayIndex, np.zeros(np.size(sundayIndex)))
    # FruitLossAfterBoat = -maxtripsperday
    correctBoatCount = cities[0].NumberOfBoats
    correctFruitLossAfterBoat

    assert np.isclose(boat.UpdatedNumberOfBoats, correctBoatCount)
    """How to compare arrays??"""
    assert np.isclose(boat.FruitLossAfterBoat, correctFruitLossAfterBoat) 

def test_boat_surplus_no_surplus(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctBoatCount
    correctFruitLossAfterBoat

    assert np.isclose(boat.UpdatedNumberOfBoats, correctBoatCount)
    assert np.isclose(boat.FruitLossAfterBoat, correctFruitLossAfterBoat) 


def test_boat_usage_after(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env

    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctTripsForYear
    correctDailyBoatTime
    assert np.isclose(boat.TripsForYear, correctTripsForYear) 
    assert np.isclose(boat.DailyBoatTime, correctDailyBoatTime) 

def test_boat_usage_prior(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env

    boat = BM.Boats(cities[0], 8.0, FruitData)

"""AIRSHIP COST TESTS"""


"""IMPACT TESTS"""