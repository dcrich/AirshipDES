"""
Simulation
"""

# python libraries
import simpy
import random
import numpy as np
# my files
import airshipClass
import cityClass
import hubClass
import airshipDesignCalculator as ADC

# One airship, One city
# Initialize airship, city, simulation

# define environment
random.seed(96)
SimTime = 365.0 * 24.0 # hours
hubCoordinates = [-3.039, -60.048]      # Manaus, BZ
cityCoordinates = [ [-3.139, -60.248],  # city
                    [-3.441, -60.462],  # city
                    [-3.387, -60.344],  # city
                    [-3.276, -60.190] ] # city
# Hub Attributes #
AvgUnloadingRate = 10.0 # tons/hour
UnloadingResource = 1
AvgRepairTime = 0.0
RepairResource = 1
AvgRefuelTime = 1.0
RefuelResource = 1

# City Attributes #
AvailableGoods = np.ones(365)*100.0
AvgLoadingRate = 10.0 # tons/hour
LoadingResources = 1

# Airship Attributes #
# Airship Parameters: payload, payload fraction, fuel tank fraction, speed, fineness ratio, fleet
dataDOE = np.array([100.0, 0.3, 0.5, 40.0, 3.0, 1])

# for d in range(np.size(dataDOE, 0)): # loop through DOE for airship parameters
env = simpy.Environment()

# create hub
hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource, AvgRefuelTime, RefuelResource)

# create cities
cities = [cityClass.City(env, 'City_%d'%c, cityCoordinates[c], AvailableGoods, AvgLoadingRate, LoadingResources)
                for c in range(len(cityCoordinates))]

# create airships 
airshipAttributes = ADC.DesignAirship(dataDOE) # useful payload, fuel capacity, footprint
airshipFleet = [airshipClass.Airship(env, 'RED_%d'%a, airshipAttributes, hub, cities)
                for a in range(int(dataDOE[5]))]

env.run(until=SimTime)

#########################################
# One airship, Two cities

# One airship, Two cities, Fruit schedule

# One airship, All cities, Fruit schedule



# LEFT OFF:
# No glaring bugs, Validate simulation logic
# - for each location have a number that gets saved to an array.
#   After sim, subtract each value in the array from the one before it
#   and if there is anything wrong in the processes, the numbers will 
#   be something other than 1