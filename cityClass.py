"""
City Class
"""
import numpy as np
import simpy

class City:
    """"""
    def __init__(self, env, id, LatLon, fruit, boatCount, CityToHubBoatDistance, LoadingResources):
        self.env = env
        self.LatLon = LatLon
        self.ID = id
        self.CityToHubBoatDistance = CityToHubBoatDistance
        # fruit data
        # self.ProducedGoods = fruit.DailyCityFruitProduction_TonsPerDay[id,:].copy()
        self.AvailableGoods = fruit.DailyCityFruitProduction_TonsPerDay[id].copy() # tons of goods available each day, constant throughout
        self.EstimatedAvailableGoods = fruit.DailyCityFruitProduction_TonsPerDay[id].copy()
        # people data
        self.MongerDailySalary = 50

        # city capabilities/capacities
        # self.LoadingRate = AvgLoadingRate # hours/ton
        self.LoadingResource = simpy.Resource(env,capacity=LoadingResources)
        self.NumberOfBoats = boatCount

        # tracking variables
        self.LoadedGoods = np.zeros(365, dtype=float) # goods taken by the airship, updated daily
        self.LostGoods = fruit.DailyCityFruitProduction_TonsPerDay[id].copy() # goods not picked up by airship so they go bad, updated daily
        self.LoadingTime = np.zeros(365, dtype=float)
        self.NumberOfVisits = np.zeros(365, dtype=float)
        self.CurrentlyOccupied = 0
        self.CurrentlyOverOccupied = 0
        
