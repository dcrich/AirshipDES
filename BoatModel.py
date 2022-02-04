""" Need to Test """

import numpy as np
Workdays = np.size(np.arange(6,365,7))
class Boats:
    def __init__(self, city, hub, workdayAttributes, GoodsSoldNoAirship):
        self.GoodsSoldNoAirship = GoodsSoldNoAirship
        self.NumberOfBoats = city.NumberOfBoats
        self.BoatSpeed = 20.0 #knots
        self.WorkdayTime = workdayAttributes[0]
        self.WorkdayTimeForYear = 52.0 * 6.0 * self.WorkdayTime # 52 * workdayAttributes[0] * workdayAttributes[1]
        self.Capacity = 1.0 #tons
        self.LoadTime = 0.125 #hours
        self.TripDistance = self.calculate_trip_distance(city,hub)
        self.simulate_usage(city)
        self.calculate_boat_surplus()
        self.TripsForYear = self.UpdatedNumberOfBoats * self.BoatSpeed * self.WorkdayTime /                        \
                            (self.TripDistance * (1.0 + self.BoatSpeed * 2.0 * self.LoadTime / self.TripDistance)) *   \
                            np.ones(np.size(self.FruitLoss), dtype=float)                                                   # should be all zero if airship gets all goods
        self.DailyBoatTime = self.TripDistance / self.BoatSpeed * self.TripsForYear + 2.0*self.LoadTime * self.TripsForYear # should be zero if airship gets all goods
        self.DailyBoatCostToSell = self.DailyBoatTime * 50.0 / self.WorkdayTime                                             # should be zero if airship gets all goods
        self.no_airship_calculations()
    
    def simulate_usage(self, city):
        # find number of possible trips each day for the year
        self.FruitLoss = city.AvailableGoods
        self.MaxTripsForYear = self.NumberOfBoats * self.BoatSpeed * self.WorkdayTime / (self.TripDistance * (1.0 + self.BoatSpeed * 2.0 * self.LoadTime / self.TripDistance))     \
                            * np.ones(np.size(self.FruitLoss), dtype=float)
        sundayIndex = np.arange(6,365,7)
        np.put(self.MaxTripsForYear, sundayIndex, np.zeros(np.size(sundayIndex)))

        self.FruitLossAfterBoat = self.FruitLoss - self.BoatCapacity * self.MaxTripsForYear

        
    def calculate_boat_surplus(self):
        Workdays = 365 - np.size(np.arange(6,365,7))
        WorkdailyAverageFruitLoss = np.sum(self.AfterBoatFruitLoss) / Workdays 
        TripsPerWorkDay = np.sum(self.MaxTripsForYear) / Workdays

        if WorkdailyAverageFruitLoss < 0:
            TripSurplus = abs(WorkdailyAverageFruitLoss) / self.Capacity
            self.BoatSurplus = np.floor(TripSurplus / TripsPerWorkDay)
        else: 
            self.BoatSurplus = 0

        self.UpdatedNumberOfBoats = self.NumberOfBoats - self.BoatSurplus # should be zero if airship gets all goods
        
    def no_airship_calculations(self):
        TripsForYear = self.GoodsSoldNoAirship / self.Capacity
        self.BoatTimeNoAirship = self.TripDistance / self.BoatSpeed * TripsForYear + 2.0*self.LoadTime * TripsForYear
        self.BoatCostToSellNoAirship = self.BoatTimeNoAirship * 50.0 / self.WorkdayTime



