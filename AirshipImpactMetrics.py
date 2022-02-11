""" CHANGE SO AIRSHIP TIME IS JUST LOADING TIME NOT FLIGHT TIME"""
import numpy as np
import AirshipCostModel as acm # or pass in data to functions

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
        
        self.time_savings_impact()
        self.crop_loss_impact()
        self.income_impact()
        self.impact_boat_job_loss()


    def time_savings_impact(self): # done, need to test
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

        self.I_TimeSavings = boatTimeInitial - (airshipTime + boatTimeAirship)

    # Crop Loss
    def crop_loss_impact(self): # done, need to test
        """
        Crops lost using boat and airship during simulation - Lost crops from data
        """
        CropLossFromData = self.Fruit.TotalLossFraction * self.Fruit.TotalFruitProuction
        sumProduceLossWithAirship = 0.0
        for boat in self.Boats:
            sumProduceLossWithAirship += np.sum(boat.FruitLossAfterBoat) 

        self.I_CropLoss = sumProduceLossWithAirship - CropLossFromData # simplified to what i think it means

    # Income
    def income_impact(self):# done, need to test
        ValueProduceSoldBeforeAirship = self.Fruit.TotalGoodsSoldFraction * self.Fruit.TotalProductionValue 
        ValueProduceSoldWithAirshipAndBoat = 0.0
        boatCostToSell = 0.0
        boatCostToSellNoAirship = 0.0
        for i in range(len(self.Cities)):
            produceSold = np.sum(self.Fruit.DailyCityFruitProduction_TonsPerDay[i]) - np.sum(self.Boats[i].FruitLossAfterBoat)
            ValueProduceSoldWithAirshipAndBoat += produceSold * self.Fruit.AverageCityFruitValue_RealsPerTon[self.Cities[i].ID]
            boatCostToSell += np.sum(self.Boats[i].DailyBoatCostToSell)
            boatCostToSellNoAirship += self.Boats[i].BoatCostToSellNoAirship
        AirshipCostToSell = 0.0
        for airship in self.Airships:
            AirshipCostToSell += airship.CostToOperate
        
        CosttoSellCropWithAirship = AirshipCostToSell + boatCostToSell 
        CosttoSellCropWithoutAirship = boatCostToSellNoAirship

        self.I_Income = (ValueProduceSoldWithAirshipAndBoat - CosttoSellCropWithAirship) - (ValueProduceSoldBeforeAirship - CosttoSellCropWithoutAirship)

    # Displaced boat people
    def impact_boat_job_loss(self): #done, need to test
        self.I_BoatJobLoss = 0.0
        for boat in self.Boats:
            self.I_BoatJobLoss -= boat.BoatSurplus

    def impact_to_forest(self):
        landmargin = 1.1
        self.I_ForestLoss = landmargin * np.size(self.Airships) * self.Airships.Footprint

# LEFT OFF:
# need boat demographics