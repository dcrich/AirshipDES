""" CHANGE SO AIRSHIP TIME IS JUST LOADING TIME NOT FLIGHT TIME"""
import numpy as np

# Time Savings

class AirshipImpactMetrics:
    def __init__(self, airshipFleet, hub, cities, fruit, boats):
        self.Airships = airshipFleet
        self.Cities = cities
        self.Hub = hub
        self.Fruit = fruit
        self.Boats = boats
        self.I_TimeSavings = 0.0
        self.I_CropLoss = 0.0
        self.I_Income = 0.0
        self.I_BoatJobLoss = 0.0
        self.I_ForestLoss = 0.0
        
        self.time_savings_impact()
        self.crop_loss_impact()
        self.income_impact()
        self.impact_boat_job_loss()
        self.impact_to_forest()


    def time_savings_impact(self):
        """
        Boat Times: time for farmer to load and unload fruit, go to city and back with one ton of fruit 
            - Initial Boat Time: Boat time for all fruit sold in the year
            - Airship Boat Time: Boat time for fruit not taken by airship
        Airship Time: Just the loading time
        """
        boatTimeInitial = 0.0
        boatTimeAirship = 0.0
        for boat in self.Boats:
            boatTimeInitial += boat.BoatTimeNoAirship
            boatTimeAirship += np.sum(boat.DailyBoatTime)

        airshipTime = 0.0
        for city in self.Cities:
            airshipTime += np.sum(city.LoadingTime) 
        self.AirshipLoadTime = airshipTime
        
        self.I_TimeSavings = boatTimeInitial - (airshipTime + boatTimeAirship) # hours

    # Crop Loss
    def crop_loss_impact(self): 
        """
        Crops lost using boat and airship during simulation - Lost crops from data
        """
        CropLossFromData = self.Fruit.TotalLossFraction * self.Fruit.TotalFruitProduction
        sumProduceLossWithAirship = 0.0
        # for boat in self.Boats:
        #     sumProduceLossWithAirship += np.sum(boat.FruitLossAfterBoat) 
        for city in self.Cities:
            sumProduceLossWithAirship += np.sum(city.AvailableGoods)
        goodsAfter = self.Fruit.TotalFruitProduction - sumProduceLossWithAirship
        goodsBefore = self.Fruit.TotalFruitProduction - CropLossFromData
        self.I_CropLoss = goodsAfter - goodsBefore # imperial tons of fruit
        

    # Income
    def income_impact(self):
        ValueProduceSoldBeforeAirship = 0.0
        ValueProduceSoldWithAirship = 0.0
        ValueProduceSoldWithBoat = 0.0
        boatCostToSell = 0.0
        boatCostToSellNoAirship = 0.0
        self.produceSoldByAllBoats = 0.0
        for i in range(len(self.Cities)):
            producedByCity = np.sum(self.Fruit.DailyCityFruitProduction_TonsPerDay[i])
            lossedByCity = np.sum(self.Cities[i].AvailableGoods)
            produceSoldByAirship = producedByCity - lossedByCity
            produceSoldByBoat = np.sum(self.Cities[i].AvailableGoods) - np.sum(self.Boats[i].FruitLossAfterBoat)
            self.produceSoldByAllBoats += produceSoldByBoat
            ValueProduceSoldWithAirship += produceSoldByAirship * self.Fruit.AverageFruitValueCity_RealsPerTon[i]
            ValueProduceSoldWithBoat += produceSoldByBoat * self.Fruit.AverageFruitValueCity_RealsPerTon[i]
            boatCostToSell += np.sum(self.Boats[i].DailyBoatCostToSell)
            boatCostToSellNoAirship += self.Boats[i].BoatCostToSellNoAirship
            ValueProduceSoldBeforeAirship += self.Fruit.CitySoldFraction[i] * producedByCity * self.Fruit.AverageFruitValueCity_RealsPerTon[i]
        AirshipCostToSell = 0.0
        for airship in self.Airships:
            AirshipCostToSell += airship.CostToOperate
        
        ValueProduceSoldWithAirshipAndBoat = ValueProduceSoldWithAirship + ValueProduceSoldWithBoat
        CosttoSellCropWithAirship = AirshipCostToSell + boatCostToSell 
        CosttoSellCropWithoutAirship = boatCostToSellNoAirship
       
        incomeBefore = ValueProduceSoldBeforeAirship - CosttoSellCropWithoutAirship
        incomeAfter = ValueProduceSoldWithAirshipAndBoat - CosttoSellCropWithAirship
        self.AirshipRevenue = ValueProduceSoldWithAirship
        self.I_Income = incomeAfter - incomeBefore # Brazilian Reals
        if airship.Payload > 15:
            stophere = 1

    # Displaced boat people
    def impact_boat_job_loss(self):
        self.BoatTripLoss = 0.0
        self.I_BoatJobLoss = 0.0
        for boat in self.Boats:
            self.BoatTripLoss -= boat.ChangeInTrips
            self.I_BoatJobLoss -= boat.BoatSurplus # people

    # area need to store airships
    def impact_to_forest(self):
        landmargin = 1.1
        cumulativeAirshipFootprint = 0.0
        for airship in self.Airships:
            cumulativeAirshipFootprint += airship.Footprint
        self.I_ForestLoss = landmargin * cumulativeAirshipFootprint # ft^2

    def return_impact_array(self):
        return np.array([self.I_BoatJobLoss, self.I_CropLoss, self.I_ForestLoss, self.I_Income, self.I_TimeSavings])