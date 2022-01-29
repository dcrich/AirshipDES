# City Class
import numpy as np
import simpy

class City:
    """"""
    def __init__(self, env, id, LatLon, AvailableGoods, AvgLoadingRate, LoadingResources):
        self.env = env
        self.LatLon = LatLon
        self.ID = id
        # fruit data
        self.AvailableGoods = AvailableGoods # tons of goods available each day
        # cost function for available fruit, most expensive fruit is prioritized 
        # people data
        # city capabilities/capacities
        self.LoadingRate = AvgLoadingRate
        self.LoadingResource = simpy.Resource(env,capacity=LoadingResources)
        # tracking variables
        self.LoadedGoods = np.zeros(365, dtype=float) # goods taken by the airship, updated daily
        self.LostGoods = AvailableGoods # goods not picked up by airship so they go bad, updated daily
        self.LoadingTime = np.zeros(365, dtype=float)


    




    
    # def _calculate_daily_goods(self):
    #     # take fruit data for each city and calculate how much fruit is available for each city
    #     availableGoods = 1
    #     return availableGoods
