import numpy as np

class Boats:
    def __init__(self, city, WorkdayTime, fruit):
        self.GoodsSoldNoAirship = fruit.CitySoldFraction[city.ID] * fruit.DailyCityFruitProduction_TonsPerDay[city.ID,:]
        self.NumberOfBoatsCity = city.NumberOfBoats
        self.NumberOfBoats = 0.0
        self.BoatSpeed = 20.0 #knots
        self.WorkdayTime = WorkdayTime
        self.WorkdayTimeForYear = 52.0 * 6.0 * self.WorkdayTime  # weeks per year * days per week * hours per day
        self.Capacity = 1.0 #tons
        self.LoadTime = 0.125 #hours
        self.TripDistance = 2.0 * city.CityToHubBoatDistance #nautical miles
        self.FruitLoss = city.AvailableGoods.copy()
        self.FruitLossAfterBoat = 0.0
        self.BoatSurplus = 0.0
        self.UpdatedNumberOfBoats = 0.0
        self.TripsForYearAirship = 0.0
        self.DailyBoatTime = 0.0
        self.DailyBoatCostToSell = 0.0
        self.BoatTimeNoAirship = 0.0
        self.BoatCostToSellNoAirship = 0.0
        self.no_airship_calculations()
        self.simulate_usage()


    def no_airship_calculations(self):
        """
        Finds how many boats are needed to make the trips necessary to transport all fruit historically sold
        Finds time and cost to transport all goods historically sold
        """
        self.MaxDailyTripsPerBoat =  np.floor(self.BoatSpeed * self.WorkdayTime /                                                           \
                                     (self.TripDistance * (1.0 + self.BoatSpeed * 2.0 * self.LoadTime / self.TripDistance)))
        # maximum number of trips possible is what the data suggests they are already doing, assuming the boats can carry one ton of fruit
        self.TripsPerDay = np.ceil(self.GoodsSoldNoAirship / self.Capacity)
        self.TotalTrips =  np.sum(self.TripsPerDay)
        # time and cost to complete all trips without airship
        self.BoatTimeNoAirship = self.TripDistance / self.BoatSpeed * self.TotalTrips + 2.0*self.LoadTime *  self.TotalTrips
        self.BoatCostToSellNoAirship = self.BoatTimeNoAirship * 50.0 / self.WorkdayTime
        # need enough boats for the day the most fruit was transported, choose minimum between the ideal and demographic data
        self.NumberOfBoats = min(np.ceil(np.max(self.TripsPerDay) / self.MaxDailyTripsPerBoat),self.NumberOfBoatsCity) 
        self.MaxDailyTrips = self.MaxDailyTripsPerBoat * self.NumberOfBoats
        
        if self.NumberOfBoats * self.MaxDailyTripsPerBoat < np.max(self.TripsPerDay): # check if boat count from demographics is enough
            raise Exception("Not enough boats")


    def simulate_usage(self):
        """
        Possibilities:
        - needs more boats because airship transporting less than the ~80% transported historically without airship -> not possible, nothing changes ---OR more boats added?? -- no if there was a need for more boats there would be more boats
        - needs less boats on average -> less boats are used, may result in more fruit loss due to above average days
        - needs same boats -> nothing changes
        """
        self.TripsPerDayWithAirship =  np.ceil(self.FruitLoss / self.Capacity) # max number of trips needed to transport fruit lost by airship
        AverageBoatsNeededWithAirship = np.ceil(np.mean(self.TripsPerDayWithAirship) / self.MaxDailyTripsPerBoat)
        # check if the number of trips is more than the max possible based on max trips
        if np.max(self.TripsPerDayWithAirship) > self.MaxDailyTrips:
            # update trip array to cap at maxtrips
            self.TripsPerDayWithAirship[self.TripsPerDayWithAirship > self.MaxDailyTrips] = self.MaxDailyTrips
            self.FruitLossAfterBoat = self.FruitLoss - self.Capacity * self.TripsPerDayWithAirship
            self.UpdatedNumberOfBoats = self.NumberOfBoats
        # check if average number of boats needed is less than all boats
        elif AverageBoatsNeededWithAirship < self.NumberOfBoats:
            # update boat count
            self.UpdatedNumberOfBoats = np.ceil(np.mean(self.TripsPerDayWithAirship) / self.MaxDailyTripsPerBoat) 
            self.UpdatedMaxDailyTrips = self.UpdatedNumberOfBoats * self.MaxDailyTripsPerBoat
            self.TripsPerDayWithAirship[self.TripsPerDayWithAirship > self.UpdatedMaxDailyTrips] = self.UpdatedMaxDailyTrips
            self.FruitLossAfterBoat = self.FruitLoss - self.Capacity * self.TripsPerDayWithAirship
        else:
            self.UpdatedNumberOfBoats = self.NumberOfBoats
            self.FruitLossAfterBoat = self.FruitLoss - self.Capacity * self.TripsPerDayWithAirship
        
        self.BoatSurplus = self.NumberOfBoats - self.UpdatedNumberOfBoats
        self.FruitLossAfterBoat[self.FruitLossAfterBoat<0] = 0.0   # removes negative values
        self.DailyBoatTime = self.TripDistance / self.BoatSpeed * self.TripsPerDayWithAirship + 2.0*self.LoadTime * self.TripsPerDayWithAirship   # should be zero if airship gets all goods
        boatSalary = 50.0 #Brazilian Reals
        self.DailyBoatCostToSell = self.DailyBoatTime * boatSalary / self.WorkdayTime                                                             # should be zero if airship gets all goods