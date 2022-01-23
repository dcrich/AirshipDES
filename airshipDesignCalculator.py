# take deisgn parameters and design airship
from matplotlib import use
import numpy as np

def DesignAirship(airshipParameters):
        airshipAttributes = np.zeros(50)
        airshipAttributes[0] = calculate_useful_payload()
        airshipAttributes[6] = calculate_fuel_capacity()
        airshipAttributes[5] = calculate_size()
        

        return airshipAttributes

def calculate_useful_payload():
        usefulPayload = 1
        return usefulPayload

def calculate_fuel_capacity():
        fuel_tons = 1
        return fuel_tons

def calculate_size(self):
        totalLift_N = 9.81 * 1000 * self.MaxPayload / self.PayloadFraction
        totalLift_lb = 0.2248 * totalLift_N
        liftLbPerCubicFoot = 0.06 # helium
        specificDensity = 0.81 # at 7000ft
        self.airshipVolume_ft = (totalLift_lb / liftLbPerCubicFoot) / specificDensity
        self.AirshipVolume = 0.0283168 * self.airshipVolume_ft  # m^3
        
        diameter_ft = 0.3048 * (4*self.airshipVolume_ft / (0.6 * np.pi * self.FinenessRatio))**(1/3) # m # not using percent cylinder
        length_ft = self.Diameter * self.FinenessRatio # m
        footprint_ft2 = length_ft * diameter_ft
        return length_ft, diameter_ft, footprint_ft2

