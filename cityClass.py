"""
City Class
Add: 
- Number of boats per city, assume 60% of boat demogrpahics go to fruit transport
- City to Hub River Distance in naut miles, maybe change to Time and update boat equations
"""
import numpy as np
import simpy

class City:
    """"""
    def __init__(self, env, id, LatLon, fruit, boatCount, AvgLoadingRate, LoadingResources):
        self.env = env
        self.LatLon = LatLon
        self.ID = id
        # fruit data
        self.ProducedGoods = fruit.DailyCityFruitProduction_TonsPerDay[id]
        self.AvailableGoods = fruit.DailyCityFruitProduction_TonsPerDay[id] # tons of goods available each day, constant throughout

        # people data
        self.MongerDailySalary = 50

        # city capabilities/capacities
        self.LoadingRate = AvgLoadingRate
        self.LoadingResource = simpy.Resource(env,capacity=LoadingResources)
        self.NumberOfBoats = boatCount

        # tracking variables
        self.LoadedGoods = np.zeros(365, dtype=float) # goods taken by the airship, updated daily
        self.LostGoods = fruit.DailyCityFruitProduction_TonsPerDay[id] # goods not picked up by airship so they go bad, updated daily
        self.LoadingTime = np.zeros(365, dtype=float)
        self.NumberOfVisits = 0
        self.DaysMissed = 0

        # boat related

