""" CHANGE SO AIRSHIP TIME IS JUST LOADING TIME NOT FLIGHT TIME"""
import numpy as np
import AirshipCostModel as acm # or pass in data to functions

# Time Savings

class AirshipImpactMetrics:
    def __init__(self, airshipFleet, hub, cities, fruit, boats, data):
        self.Airships = airshipFleet
        self.Cities = cities
        self.Hub = hub
        self.Fruit = fruit
        self.Boats = boats
        self.time_savings_impact()
        self.crop_loss_impact()
        self.income_impact()
        self.impact_boat_job_loss()


    def time_savings_impact(self):
        initialTime = SIMULATION # not sure how to calculate this in the sim yet
        
        boatTime = SIMULATION

        airshipTime = 0.0
        for city in self.Cities:
            airshipTime += np.sum(city.LoadingTime) 

        self.I_TimeSavings = initialTime - (airshipTime + boatTime)

    # Crop Loss
    def crop_loss_impact(self):
        # I_CropLoss = percentOfLossRecoupedByAirship * ProduceLoss - ProduceLossWithoutAirship # FROM PAPER
        sumProduceLossWithAirship = 0.0
        for city in self.Cities:
            sumProduceLossWithAirship += np.sum(city.LostGoods) #-np.sum(city.BoatTransportedGoods)
        CropLossFromData = self.Fruit.TotalLossFraction * np.sum(self.Fruit.DailyFruitProduction) 

        self.I_CropLoss = sumProduceLossWithAirship - CropLossFromData # simplified to what i think it means

    # Income
    def income_impact(self):
        ProduceSoldBeforeAirship = self.Fruit.TotalGoodsSoldFraction * self.Fruit.TotalProductionValue 
        ProduceSoldWithAirship = 0.0
        for city in self.Cities:
            ProduceSoldWithAirship += self.Fruit.AverageCityFruitValue_RealsPerTon[city.ID] * np.sum(city.LoadedGoods)
        
        CosttoSellCropWithAirship = airshipcosttosell + boatcosttosell#SIMULATION # via cost model  --- # what did phil do for this?
        CosttoSellCropWithoutAirship = boatcosttosellnoairship # via intermediate calcs


        self.I_Income = (ProduceSoldWithAirship - CosttoSellCropWithAirship) - (ProduceSoldBeforeAirship - CosttoSellCropWithoutAirship)

    # Displaced boat people
    def impact_boat_job_loss(self):
        # base boat people on average amount of fruit loss and demographic data
        # time not loading the airship can be put towards filling the boat?
        self.I_BoatJobLoss = 0
        for boat in self.Boats:
            self.I_BoatJobLoss -= boat.BoatSurplus

# LEFT OFF:
# and boat calculations to impact calculations