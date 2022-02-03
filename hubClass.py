# Hub Class
import numpy as np
import simpy

class Hub:
    """"""
    def __init__(self, env, LatLon, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource):
        self.env = env
        self.LatLon = LatLon
        # hub capabilities/capacities
        self.UnloadingRate = AvgUnloadingRate
        self.UnloadingResource = simpy.Resource(env,capacity=UnloadingResource)
        self.RepairResource = simpy.Resource(env,capacity=RepairResource)
        self.RefuelResource = simpy.Resource(env,capacity=RefuelResource)
        self.AvgRepairTime = AvgRepairTime
        self.AvgRefuelTime = AvgRefuelTime
        # tracking variables
        self.RecievedGoods = np.zeros(365, dtype=float)
        self.SimulationTracker = np.zeros((1,5))