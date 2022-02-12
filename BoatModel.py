""" Need to Test """

import numpy as np


class Boats:
    def __init__(self, city, WorkdayTime, fruit):
        self.GoodsSoldNoAirship = fruit.TotalGoodsSoldFraction * fruit.TotalFruitProduction
        self.NumberOfBoats = city.NumberOfBoats
        self.BoatSpeed = 20.0 #knots
        self.WorkdayTime = WorkdayTime
        self.WorkdayTimeForYear = 52.0 * 6.0 * self.WorkdayTime  # weeks per year * days per week * hours per day
        self.Capacity = 1.0 #tons
        self.LoadTime = 0.125 #hours
        self.TripDistance = 2.0 * city.CityToHubBoatDistance #nautical miles
        self.FruitLoss = city.AvailableGoods
        self.FruitLossAfterBoat = 0.0
        self.BoatSurplus = 0.0
        self.UpdatedNumberOfBoats = 0.0
        self.TripsForYear = 0.0
        self.DailyBoatTime = 0.0
        self.DailyBoatCostToSell = 0.0
        self.simulate_usage()

        self.BoatTimeNoAirship = 0.0
        self.BoatCostToSellNoAirship = 0.0
        self.no_airship_calculations()

    def simulate_usage(self):
        # find number of possible trips each day for the year
        self.MaxTripsForYear = self.NumberOfBoats * self.BoatSpeed * self.WorkdayTime /                                    \
                                (self.TripDistance * (1.0 + self.BoatSpeed * 2.0 * self.LoadTime / self.TripDistance))     \
                                * np.ones(np.size(self.FruitLoss), dtype=float)
        sundayIndex = np.arange(6,365,7)
        np.put(self.MaxTripsForYear, sundayIndex, np.zeros(np.size(sundayIndex)))

        # may include negative values, these will get zeroed after boat surplus calculated
        self.FruitLossAfterBoat = self.FruitLoss - self.Capacity * self.MaxTripsForYear 

        self.calculate_boat_surplus()

        self.TripsForYear = self.UpdatedNumberOfBoats * self.BoatSpeed * self.WorkdayTime /                                 \
                            (self.TripDistance * (1.0 + self.BoatSpeed * 2.0 * self.LoadTime / self.TripDistance)) *        \
                            np.ones(np.size(self.FruitLoss), dtype=float)                                                   # should be all zero if airship gets all goods
        self.DailyBoatTime = self.TripDistance / self.BoatSpeed * self.TripsForYear + 2.0*self.LoadTime * self.TripsForYear # should be zero if airship gets all goods
        self.DailyBoatCostToSell = self.DailyBoatTime * 50.0 / self.WorkdayTime                                             # should be zero if airship gets all goods
        
        
    def calculate_boat_surplus(self):
        """On the average workday, finds how many boats go unused"""

        Workdays = 365 - np.size(np.arange(6,365,7))
        WorkdailyAverageFruitLoss = np.sum(self.FruitLossAfterBoat) / Workdays 
        TripsPerWorkDay = np.sum(self.MaxTripsForYear) / Workdays

        if WorkdailyAverageFruitLoss < 0: 
            TripSurplus = abs(WorkdailyAverageFruitLoss) / self.Capacity
            self.BoatSurplus = np.floor(TripSurplus / TripsPerWorkDay)
        else: 
            self.BoatSurplus = 0

        self.UpdatedNumberOfBoats = self.NumberOfBoats - self.BoatSurplus                                                   # should be zero if airship gets all goods
        self.FruitLossAfterBoat[self.FruitLossAfterBoat<0] = 0.0   # remove negative values

    def no_airship_calculations(self):
        TripsForYear = self.GoodsSoldNoAirship / self.Capacity
        self.BoatTimeNoAirship = self.TripDistance / self.BoatSpeed * TripsForYear + 2.0*self.LoadTime * TripsForYear
        self.BoatCostToSellNoAirship = self.BoatTimeNoAirship * 50.0 / self.WorkdayTime


