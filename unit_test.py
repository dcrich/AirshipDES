"""
Unit tests for:
- Boat Model
- Social impact metrics

Run in terminal using command:
'cd /Users/danada/Coding/AirshipDES'
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
    SimTime = 0.1 # 365.0 * 24.0 # hours
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
def test_boat_surplus_less_boats(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production low so there will definitely be a surplus
    cities[1].AvailableGoods = 0.01 * np.ones(np.size(cities[1].AvailableGoods),dtype=float) 
    sundayIndex = np.arange(6,365,7)
    np.put(cities[1].AvailableGoods, sundayIndex, np.zeros(np.size(sundayIndex)))

    boat = BM.Boats(cities[1], 8.0, FruitData)
    correctBoatCount = 1.0
    correctFruitLossAfterBoat = np.zeros(np.size(cities[1].AvailableGoods),dtype=float)

    assert np.isclose(boat.UpdatedNumberOfBoats, correctBoatCount)
    assert np.allclose(boat.FruitLossAfterBoat, correctFruitLossAfterBoat) 


def test_boat_surplus_more_boats(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production twice as much as can be transported by the available boats
    cities[0].NumberOfBoats = 1.0
    cities[0].AvailableGoods = 2.0*cities[0].NumberOfBoats * 7.0 * 1.0 * np.ones(np.size(cities[0].AvailableGoods),dtype=float) 
    sundayIndex = np.arange(6,365,7)
    np.put(cities[0].AvailableGoods, sundayIndex, np.zeros(np.size(sundayIndex)))

    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctBoatCount = cities[0].NumberOfBoats
    correctFruitLossAfterBoat = cities[0].NumberOfBoats * 7.0 * 1.0 * np.ones(np.size(cities[0].AvailableGoods),dtype=float)
    sundayIndex = np.arange(6,365,7)
    np.put(correctFruitLossAfterBoat, sundayIndex, np.zeros(np.size(sundayIndex)))

    assert np.isclose(boat.UpdatedNumberOfBoats, correctBoatCount)
    assert np.allclose(boat.FruitLossAfterBoat, correctFruitLossAfterBoat) 


def test_boat_surplus_same_boats(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production equal to goods sold without airship
    cities[0].NumberOfBoats = 1.0
    cities[0].AvailableGoods = FruitData.CitySoldFraction[0] * FruitData.DailyCityFruitProduction_TonsPerDay[0,:]
    sundayIndex = np.arange(6,365,7)
    np.put(cities[0].AvailableGoods, sundayIndex, np.zeros(np.size(sundayIndex)))

    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctBoatCount = cities[0].NumberOfBoats
    correctFruitLossAfterBoat = np.zeros(np.size(cities[0].AvailableGoods),dtype=float)
    sundayIndex = np.arange(6,365,7)
    np.put(cities[0].AvailableGoods, sundayIndex, np.zeros(np.size(sundayIndex)))
    
    assert np.isclose(boat.UpdatedNumberOfBoats, correctBoatCount)
    assert np.allclose(boat.FruitLossAfterBoat, correctFruitLossAfterBoat) 


def test_boat_usage_boat_used(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production equal to goods sold without airship
    cities[0].NumberOfBoats = 1.0
    cities[0].AvailableGoods = cities[0].NumberOfBoats * 7.0 * 1.0 * np.ones(np.size(cities[0].AvailableGoods),dtype=float)
    sundayIndex = np.arange(6,365,7)
    np.put(cities[0].AvailableGoods, sundayIndex, np.zeros(np.size(sundayIndex)))

    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctDailyBoatTime = boat.TripDistance / boat.BoatSpeed * 7.0 + 2.0 *boat.LoadTime * 7.0

    assert np.isclose(boat.DailyBoatTime[0], correctDailyBoatTime)


def test_boat_usage_boat_unused(sim_env):
    hub, cities, airshipFleet, FruitData = sim_env
    # change city and fruit data to be checkable
    # set fruit production equal to goods sold without airship
    cities[0].NumberOfBoats = 1.0
    cities[0].AvailableGoods = np.zeros(np.size(cities[0].AvailableGoods),dtype=float)

    boat = BM.Boats(cities[0], 8.0, FruitData)
    correctDailyBoatTime = np.zeros(np.size(cities[0].AvailableGoods),dtype=float)

    assert np.allclose(boat.DailyBoatTime, correctDailyBoatTime)

"""Airship Class TESTS"""
# Test Candidates:
# - choose_city
#     - CitySelected
#     - NextCity
# - load_cargo
#     - yesterdaysGoods
#     - goodsLoaded
#     - AvailableGoods
# - check if citiesVisitedInTrip is getting filled and emptied as expected

def test_choose_city_NotWorkday(sim_env):
    idk


def test_choose_city_NoGoodsAtCity(sim_env):
    idk

def test_choose_city_PayloadUsed(sim_env):
    idk

def test_choose_city_AlreadyVisitedAllCities(sim_env):
    idk

def test_choose_city_SameCity(sim_env):
    idk

def test_choose_city_NotInRange(sim_env):
    idk

def test_choose_city_InRange(sim_env):
    idk


def test_in_range_NotInTimeRange(sim_env):
    idk

def test_in_range_NotInFuelRange(sim_env):
    idk

def test_in_range_InTimeRange(sim_env):
    idk

def test_in_range_InFuelRange(sim_env):
    idk


# For using debugger on this file, comment @fixture line, uncomment code below, change to desired function
# test_boat_surplus_more_boats(sim_env())