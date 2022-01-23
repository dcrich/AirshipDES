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
SimTime = 360.0 * 24.0 # hours
hubCoordinates = [-3.039, -60.048]      # Manaus, BZ
cityCoordinates = [ [-3.139, -60.248],  # city
                    [-3.441, -60.462],  # city
                    [-3.387, -60.344],  # city
                    [-3.276, -60.190] ] # city
# Hub Attributes #
AvgUnloadingRate = 10 # tons/hour
UnloadingResource = 1
AvgRepairTime = 5
RepairResource = 1

# City Attributes #
AvailableGoods = np.ones(360)*100.0
AvgLoadingRate = 10 # tons/hour
LoadingResources = 1

# Airship Attributes #
# Airship Parameters: payload, payload fraction, fuel tank fraction, speed, fleet size
dataDOE = np.array([100.0, 0.3, 0.5, 40.0, 1.0])

for d in np.size(dataDOE, 0): # loop through DOE for airship parameters
    env = simpy.Environment()
    
    # create hub
    hub = hubClass.Hub(env, hubCoordinates, AvgUnloadingRate, UnloadingResource, AvgRepairTime, RepairResource)
    
    # create cities
    cities = [cityClass.City(env, 'City_%d'%c, cityCoordinates[c], AvailableGoods, AvgLoadingRate, LoadingResources)
                    for c in range(np.size(cityCoordinates),0)]

    # create airships
    airshipAttributes = [50,50,1000] # ADC.DesignAirship(dataDOE[d,:]) # useful payload, fuel capacity, footprint
    airshipFleet = [airshipClass.Airship(env, 'RED_%d'%a, airshipAttributes, hub, cities)
                    for a in range(dataDOE[0,4])]

    env.run(until=SimTime)

#########################################
# One airship, Two cities

# One airship, Two cities, Fruit schedule

# One airship, All cities, Fruit schedule