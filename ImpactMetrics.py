
from signal import ItimerError
import AirshipCostModel as acm # or pass in data to functions

# Time Savings
def time_savings_impact():
    initialTime = SIMULATION # not sure how to calculate this in the sim yet
    airshipTime = SIMULATION
    boatTime = SIMULATION

    I_TimeSavings = initialTime - (airshipTime + boatTime)

    return I_TimeSavings

# Crop Loss
def crop_loss_impact():
    # I_CropLoss = percentOfLossRecoupedByAirship * ProduceLoss - ProduceLossWithoutAirship # FROM PAPER
    sumProduceLossWithAirship = SIMULATION
    CropLossFromData = DATA

    I_CropLoss = sumProduceLossWithAirship - CropLossFromData # simplified to what i think it means

    return I_CropLoss

# Income
def income_impact():
    TotalHarvest = DATA
    sumProduceLossWithAirship = SIMULATION
    MarketPriceForCrop = DATA
    CosttoSellCropWithAirship = SIMULATION # via cost model  --- # what did phil do for this?
    CropLossFromData = DATA
    CosttoSellCropWithoutAirship = DATA # via intermediate calcs


    I_Income = ((TotalHarvest - sumProduceLossWithAirship) * MarketPriceForCrop - CosttoSellCropWithAirship) - \
               ((TotalHarvest - CropLossFromData) * MarketPriceForCrop - CosttoSellCropWithoutAirship)

    return I_Income

# Displaced boat people

def impact_boat_job_loss():
    # base boat people on average amount of fruit loss and demographic data
    BoatPeopleAfterAirship = SIMULATION
    BoatPeopleBeforeAirship = DATA
    I_BoatJobLoss = BoatPeopleAfterAirship - BoatPeopleBeforeAirship

    return I_BoatJobLoss

