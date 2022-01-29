# take deisgn parameters and design airship
from matplotlib import use
import numpy as np

def DesignAirship(airshipParameters):
        Payload = airshipParameters[0]
        PayloadFraction = airshipParameters[1]
        FuelTankFraction = airshipParameters[2]
        CruiseSpeed = airshipParameters[3]
        FinenessRatio = airshipParameters[4]

        airshipAttributes = np.zeros(50)
        airshipAttributes[0],airshipAttributes[1]  = calculate_useful_payload(Payload, FuelTankFraction)
        airshipAttributes[2], airshipAttributes[3] = calculate_size(Payload, PayloadFraction, FinenessRatio)
        airshipAttributes[4] = CruiseSpeed

        return airshipAttributes

def calculate_useful_payload(Payload, FuelTankFraction):
        fuel_tons = calculate_fuel_capacity(Payload, FuelTankFraction)
        usefulPayload = Payload - fuel_tons
        return usefulPayload, fuel_tons

def calculate_fuel_capacity(Payload, FuelTankFraction):
        fuel_tons = Payload * FuelTankFraction
        return fuel_tons

def calculate_size(MaxPayload, PayloadFraction, FinenessRatio):
        totalLift_lb = 2000 * MaxPayload / PayloadFraction
        liftLbPerCubicFoot = 0.06 # helium
        specificDensity = 0.81 # at 7000ft
        
        airshipVolume_ft3 = (totalLift_lb / liftLbPerCubicFoot) / specificDensity
        
        diameter_ft = 0.3048 * (4*airshipVolume_ft3 / (0.6 * np.pi * FinenessRatio))**(1/3) # m # not using percent cylinder
        length_ft = diameter_ft * FinenessRatio # m
        
        footprint_ft2 = length_ft * diameter_ft
        
        return footprint_ft2, airshipVolume_ft3

