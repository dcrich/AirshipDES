# take deisgn parameters and design airship
import numpy as np


def DesignAirship(airshipParameters):
        Payload = round(airshipParameters[0])
        CruiseSpeed = round(airshipParameters[1])
        FleetSize = airshipParameters[2]
        LoadThreshold = airshipParameters[3]
        AvgLoadRate = airshipParameters[4]
        PayloadFraction = airshipParameters[5]
        FuelTankFraction = airshipParameters[6]
        FinenessRatio = airshipParameters[7]
       
        airshipAttributes = np.zeros(50)
        airshipAttributes[0],airshipAttributes[1]  = calculate_useful_payload(Payload, FuelTankFraction)
        airshipAttributes[2], airshipAttributes[3], airshipAttributes[5], airshipAttributes[6] = calculate_size(Payload, PayloadFraction, FinenessRatio)
        airshipAttributes[4] = CruiseSpeed
        airshipAttributes[7] = Payload
        airshipAttributes[8] = PayloadFraction
        airshipAttributes[9] = FuelTankFraction
        airshipAttributes[10] = FinenessRatio
        airshipAttributes[11] = FleetSize
        airshipAttributes[12] = LoadThreshold
        airshipAttributes[13] = AvgLoadRate

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
        specificDensity = 0.95 # at ~1500 ft
        
        airshipVolume_ft3 = (totalLift_lb / liftLbPerCubicFoot) / specificDensity
        
        diameter_ft = 0.3048 * (4*airshipVolume_ft3 / (0.6 * np.pi * FinenessRatio))**(1/3) # m # not using percent cylinder
        length_ft = diameter_ft * FinenessRatio # m
        
        footprint_ft2 = length_ft * diameter_ft
        
        return footprint_ft2, airshipVolume_ft3, diameter_ft, length_ft

