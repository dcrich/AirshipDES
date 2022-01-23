# Hub Class
import numpy as np
import simpy

class Hub:
    """"""
    def __init__(self, env, LatLon, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource):
        self.env = env
        self.LatLon = LatLon
        # hub capabilities/capacities
        self.UnloadingRate = AvgUnloadingRate
        self.UnloadingResource = simpy.Resource(env,capacity=UnloadingResource)
        self.RepairResource = simpy.Resource(env,capacity=RepairResource)
        self.AvgRepairTime = AvgRepairTime
        # tracking variables
        self.RecievedGoods = np.zeros(360, dtype=float)
        