import simpy
import random
import numpy as np
import pandas as pd
import statistics as stat
import math
import os 

"""I AM USING METRIC SYSTEM"""

""" 
ASSUMPTIONS:
The airship is filled with goods equal in $/m^3
Elevation is negligible
Constant 10 knot headwind
Fuel burn based solely on distance traveled, constant cruisee speed
Fuel used waiting based of 10 kmh, or a hover that uses an equivalent amount of fuel
If airship runs out of fuel waiting at city, it is refueled by a hypothetical refuel ship
    that uses fuel used to fill the airship and a there-and-back trip for itself, it is the same
    type of airship as all others
Airships only go between Hub and Cities, no inter-City travel
Only looking at One Scenario
"""

class City:
    """"""
    def __init__(self, env, ID, LatLon, cityAttributes):
        self.GoodsLoaded = simpy.Container(env)
        self.LoadingAreaResource = simpy.Resource(env, capacity=cityAttributes['numLoadingAreas'])
        
        self.env = env
        self.CityID = ID
        self.Coordinates = LatLon
        self.distance_from_hub(cityAttributes['hubCoordinates']) # calculate great circle distance
        self.AvgLoadRate = cityAttributes['avgLoadRate']
        self.IsOccupied = 0
        self.VisitCount = 0
        self.NumLoadingAreas = cityAttributes['numLoadingAreas']

    def distance_from_hub(self, hubCoordinates):
        lat1 = hubCoordinates[0] * math.pi / 180
        lon1 = hubCoordinates[1] * math.pi / 180
        lat2 = self.Coordinates[0] * math.pi / 180
        lon2 = self.Coordinates[1]  * math.pi / 180
        self.DistanceFromHub = 6371 * 2 * math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 + 
                                math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))
    def distance_to_city(self, newCoordinates):
        lat1 = newCoordinates[0] * math.pi / 180
        lon1 = newCoordinates[1] * math.pi / 180
        lat2 = self.Coordinates[0] * math.pi / 180
        lon2 = self.Coordinates[1]  * math.pi / 180
        distanceToCity = 6371 * 2 * math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 + 
                                math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))
        return distanceToCity


class Hub:
    """"""
    def __init__(self, env, hubAttributes): 
        self.GoodsReceived = simpy.Container(env)
        self.FuelProvided = simpy.Container(env)
        self.FuelProvidedWhileWaitingLoad = simpy.Container(env)
        self.FuelProvidedWhileWaitingUnload = simpy.Container(env)
        self.UnloadingAreaResource = simpy.Resource(env, capacity=hubAttributes['numUnloadingAreas'])
        self.ParkingSpaces = simpy.Resource(env, capacity=hubAttributes['parkSpaces'])
        self.TakeoffResource = simpy.Resource(env,capacity = hubAttributes['takeoffReseource'])
        
        self.env = env
        self.NumUnloadingAreas = hubAttributes['numUnloadingAreas']
        self.Runways = hubAttributes['takeoffReseource']
        self.MaintenanceResource = hubAttributes['maintenanceResource']
        self.Coordinates = hubAttributes ['coordinates']
        self.AvgUnloadRate = hubAttributes['avgUnloadRate']

    def calc_unload_area(self, unloadSpace, airshipDiameter, airshipLength):
        safetyFactor = 2
        self.UnloadingAreaResource.capacity = math.floor(unloadSpace / 
                                              (safetyFactor * airshipDiameter * airshipLength))
    
    def unload(self): #unloading process
        with self.UnloadingAreaResource.request() as unloadReq:
            yield unloadReq


class Airship:
    """"""
    def __init__(self, env, airshipID, airshipAttributes, hub,cities):
        self.FuelTankSize = airshipAttributes['fuelTankFraction'] * airshipAttributes['payload_metrictons']
        self.FuelTank = self.FuelTankSize#simpy.Container(env, capacity=self.FuelTankSize, init=self.FuelTankSize)
        
        self.IdAirship = airshipID
        self.env = env
        self.TakeoffWaitTime = 0.0
        self.LoadWaitTime = 0.0
        self.UnloadWaitTime = 0.0
        self.MaxPayload = airshipAttributes['payload_metrictons']
        self.Payload = airshipAttributes['payload_metrictons'] * (1-airshipAttributes['fuelTankFraction'])
        self.FinenessRatio = airshipAttributes['finenessRatio']
        self.CruiseSpeed = airshipAttributes['speed_kmh']
        self.MaxAltitude = airshipAttributes['maximumFlightAltitude']
        self.PayloadFraction = airshipAttributes['payloadFraction']
        self.AtHub = 1
        self.CurrentCity = NUM_CITIES
        self.NextCity = 1
        self.OverTimeWorked = 0.0
        self.UnderTimeWorked = 0.0
        self.NoTimeSoReturningToHub = 0
        self.CargoLoad = simpy.Container(env, capacity=self.Payload, init=0)
        self.MaintenanceFrequency = airshipAttributes['maintenanceFrequency']
        self.DaysWorked = 0
        self.endOfWorkday = WORK_DAY_HOURS + STARTING_HOUR
        self.NumTrips = 0
        self.NoTimeSoReturningToHub = 0
        self.NotEnoughFuel = 0
        self.FailedMission = 0
        self.FailedMissionCount = 0
        self.ConsecutiveFailures = 0
        self.CitiesAvailable = 0
        self.HubVisits = 0
        
        
        self.calculate_size()
        self.calculate_range()
        placeholder=1 # print(airshipID + ' standing by')
        env.process(self.begin_workday(hub,cities))

    def calculate_size(self):
        totalLift_N = 9.81 * 1000 * self.MaxPayload / self.PayloadFraction
        totalLift_lb = 0.2248 * totalLift_N
        liftLbPerCubicFoot = 0.06 # helium
        specificDensity = 0.81 # at 7000ft
        self.airshipVolume_ft = (totalLift_lb / liftLbPerCubicFoot) / specificDensity
        self.AirshipVolume = 0.0283168 * self.airshipVolume_ft  # m^3
        self.Diameter = 0.3048 * (4*self.airshipVolume_ft / (0.6 * math.pi * self.FinenessRatio))**(1/3) # m # not using percent cylinder
        self.Length = self.Diameter * self.FinenessRatio # m
        self.Footprint = self.Length * self.Diameter

    def calculate_range(self):
        # in imperial units
        fuelTankSize_imperial = 1.1 * self.FuelTankSize #convert to imperial
        propEfficiency = 0.7  #prop efficiency
        dragCoeff = 0.025   # Drag Coefficient
        SFC = 0.41    #lb/hp/hr
        headwindSpeed_knots = 10    # knots headwind
        speedKnots = self.CruiseSpeed * 0.539957    # knots cruise speed
        totalAirshipVolume = self.airshipVolume_ft * 10 ** -6    #M ft**3

         #Constants and Conversion Factors
        knots2fps = 1.68780986 
        lbsPerSlug = 32.1740486 
        hpPerFtLbPerSec = 550 
        rhoAir = 0.06 #densityAltitude at 7000 ft

        # Calculate fuel per mile based on cruise speed, altitude, and wind
        v = speedKnots * knots2fps    # ft/s cruise speed
        HpFuelCalc = dragCoeff * (totalAirshipVolume * 10 ** 6) ** (2 / 3) * rhoAir *        \
                        v ** 3 / (2 * propEfficiency * hpPerFtLbPerSec * lbsPerSlug)    #propulsion horsepower
        tonsPerHour = HpFuelCalc * SFC / 2000    # tons of fuel per hour
        
        tonsPerMile = tonsPerHour / (speedKnots - headwindSpeed_knots)    #tons of fuel per mile        
        
        safetyFactor = 1.1
        self.Range_km = fuelTankSize_imperial / (safetyFactor * tonsPerMile)

    def calculate_cities_within_range(self,hub,cities):
        atLeastOneCitySelected = 0
        self.CitiesInRange = []
        for i in range(NUM_CITIES):
            distanceHubCity = cities[i].DistanceFromHub
            fractionFuelTankNeeded = (2 * distanceHubCity / self.Range_km)
            if fractionFuelTankNeeded < 1:
                self.CitiesInRange.append(i)
                atLeastOneCitySelected = 1
        if atLeastOneCitySelected == 1:
            self.CitiesAvailable = 1
    
    def check_time_range(self, temp_CitiesInRange, cities):
        # check if cities within time range
        lengthCities = len(temp_CitiesInRange)
        j=0
        for i in range(lengthCities):
            distanceToCity = cities[temp_CitiesInRange[j]].DistanceFromHub
            travelTime = distanceToCity / self.CruiseSpeed
            estimatedTimeToComplete = 2 * travelTime + self.Payload / cities[temp_CitiesInRange[j]].AvgLoadRate
            noTime = self.env.now + estimatedTimeToComplete > self.endOfWorkday
            if noTime:
                temp_CitiesInRange.remove(temp_CitiesInRange[j])
                i = i+1
            else:
                j = j+1
        return temp_CitiesInRange

    def begin_workday(self,hub,cities):
        yield self.env.timeout(STARTING_HOUR) # start working at 8am
        
        while True: # run until sim is over
            self.calculate_cities_within_range(hub,cities)
            while self.env.now < self.endOfWorkday: # run until workday over
                yield self.env.process(self.choose_city(hub,cities))
                if self.NoTimeSoReturningToHub == 1:
                    break
                # yield self.env.process(self.choose_next_destination(hub,cities))
                
            # calculate days and how much time was spent overtime or wasted undertime
            self.DaysWorked = self.DaysWorked + 1
            if self.env.now > self.endOfWorkday:
                self.OverTimeWorked = self.OverTimeWorked + (self.env.now - self.endOfWorkday)
            else:
                self.UnderTimeWorked = self.UnderTimeWorked + (self.endOfWorkday - self.env.now)
            
            self.endOfWorkday = self.endOfWorkday + 24 # set new workday target
            timeUntilNewWorkday = (self.endOfWorkday - WORK_DAY_HOURS) - env.now 
            if timeUntilNewWorkday < 0:
                placeholder=1 # print('negative time')
                break
            placeholder=1 # print('')
            placeholder=1 # print(self.IdAirship + ' ending workday at %.4f'%env.now)
            placeholder=1 # print('')
            yield self.env.timeout(timeUntilNewWorkday)

    def leave_hub(self,hub):
        """ 
        Taxi and Takeoff from Hub
        """
        with hub.TakeoffResource.request() as takeoffReq:
            startwait = self.env.now
            placeholder=1 # print(self.IdAirship + ' requesting takeoff at %.2f' % startwait)
            yield takeoffReq
            self.TakeoffWaitTime += (self.env.now - startwait)
            placeholder=1 # print(self.IdAirship + ' leaving hub at %.2f' % self.env.now)
            yield self.env.timeout(TAKEOFF_TIME)

    def choose_city(self,hub,cities):
        """ 
        Choose which city to go to.
        If valid city found, Go through process at city.
        Else remain at hub
        """
        if self.CitiesAvailable == 1 and len(self.CitiesInRange) > 0 :
            # check if city occupied, if needed choose new city
            self.city_checker(hub,cities)
            if self.cityValid:
                # fly to city
                cities[self.NextCity].IsOccupied = 1
                yield self.env.process(self.travel_city(hub, cities))
            else:
                placeholder=1 # print(self.IdAirship + ' Remaining Parked at %.2f'%self.env.now)
                self.NoTimeSoReturningToHub = 1
        else:
            placeholder=1 # print(self.IdAirship + ' - Not enough Fuel For any City, done for the day')
            self.FailedMissionCount +=1
            self.NoTimeSoReturningToHub = 1
        
    def city_checker(self,hub,cities):
        # create a list of possible cities unique to this work day
        temp_CitiesInRange = self.CitiesInRange
        # remove cities airship can't reach within remaining workday
        temp_CitiesInRange = self.check_time_range(temp_CitiesInRange, cities)
        self.cityValid = False # no valid cities to visit until proven otherwise
        
        lengthAvailableCities = len(temp_CitiesInRange)
        if lengthAvailableCities > 0: # check if there are cities to visit
            self.NextCity = temp_CitiesInRange[random.randrange(0,len(temp_CitiesInRange))] # set initial random city
            while not self.cityValid: # prove if city is valid
                if cities[self.NextCity].IsOccupied == 1: #check if city is occupied
                    for i in range(lengthAvailableCities): # reset city, increment up until a non-occupied city is chosen
                        self.NextCity = temp_CitiesInRange[i] 
                        if cities[self.NextCity].IsOccupied == 0: # if city available, continue while loop to find if within range
                            self.cityValid = True
                            break
                        # if all cities occupied, go to random city
                        elif cities[self.NextCity].IsOccupied == 1 and i == lengthAvailableCities - 1: 
                            self.NextCity = temp_CitiesInRange[random.randrange(0,len(temp_CitiesInRange))] 
                            self.cityValid = True
                else:
                    self.cityValid = True
            # Once a city has been found, make distance and time calculations
            self.distanceToCity = cities[self.NextCity].DistanceFromHub
            self.travelTime = self.distanceToCity / self.CruiseSpeed
            self.estimatedTimeToComplete = 2 * self.travelTime + self.Payload/cities[self.NextCity].AvgLoadRate
            self.NoTimeSoReturningToHub = 0
            
    def travel_city(self, hub, cities):
        """ Travel to city and load airship"""
        self.NoTimeSoReturningToHub = 0
        self.FailedMission = 0
        self.ConsecutiveFailures = 0
        yield self.env.process(self.leave_hub(hub))
        # travel time
        yield self.env.timeout(self.travelTime)
        self.CurrentCity = self.NextCity
        self.AtHub = 0 
        placeholder=1 # print(self.IdAirship + ' Arrived at ' + cities[self.CurrentCity].CityID + ' %.2f'%self.env.now)
        cities[self.CurrentCity].VisitCount += 1
        # wait/load at city
        yield self.env.process(self.load(cities[self.CurrentCity])) #load airship
        self.FuelTank = self.FuelTank - (self.distanceToCity/self.Range_km * self.FuelTankSize)#.get(self.distanceToCity/self.Range_km * self.FuelTankSize) #remove fraction of fuel
        self.NumTrips += 1
        yield self.env.process(self.travel_hub(hub,cities))
    
    def load(self,city): #loading process
        """ load airship"""
        with city.LoadingAreaResource.request() as loadReq:
            startwait = self.env.now
            placeholder=1 # print(self.IdAirship + ' waiting for load %.2f' % startwait)
            yield loadReq
            timeWaited = (self.env.now - startwait)
            self.LoadWaitTime += timeWaited
            self.wait(hub, cities, timeWaited)
            placeholder=1 # print(self.IdAirship + ' begin loading at %.2f' % self.env.now)
            loadTime = random.uniform(0.75*self.Payload/city.AvgLoadRate, 1.25*self.Payload/city.AvgLoadRate)
            yield self.env.timeout(loadTime)
            placeholder=1 # print(self.IdAirship + ' finished loading at %.2f' % self.env.now)
            self.CargoLoad.put(self.CargoLoad.capacity) # load airship
            city.GoodsLoaded.put(self.CargoLoad.capacity) # document goods provided by city
            city.IsOccupied = 0
        
    
            
    def travel_hub(self,hub,cities): 
        """ Return to Hub """
        distanceToHub = cities[self.CurrentCity].DistanceFromHub
        travelTime = distanceToHub / self.CruiseSpeed
        yield self.env.timeout(travelTime)
        placeholder=1 # print(self.IdAirship + ' Arrived at Hub at %.2f' % self.env.now)
        self.FuelTank = self.FuelTank - (distanceToHub/self.Range_km * self.FuelTankSize) #.get(distanceToHub/self.Range_km * self.FuelTankSize) #remove fuel used on return trip
        self.AtHub = 1
        self.CurrentCity = NUM_CITIES
        yield self.env.process(self.hub_events(hub,cities))
    
    def hub_events(self,hub,cities):
        """ """
        yield self.env.process(self.unload(hub,cities))
        yield self.env.process(self.choose_next_hub_event(hub,cities))

    def unload(self,hub,cities):
        """ """
        with hub.UnloadingAreaResource.request() as unloadReq:
            startwait = self.env.now
            placeholder=1 # print(self.IdAirship + ' waiting for unload %.2f' % startwait)
            yield unloadReq
            timeWaited = self.env.now - startwait
            self.UnloadWaitTime += timeWaited
            self.wait(hub, cities, timeWaited)
            placeholder=1 # print(self.IdAirship + ' begin unloading at %.2f' % self.env.now)
            unloadTime = random.uniform(0.75* self.Payload/hub.AvgUnloadRate , 1.25* self.Payload/hub.AvgUnloadRate)
            yield self.env.timeout(unloadTime)
            placeholder=1 # print(self.IdAirship + ' finished unloading at %.2f' % self.env.now)
            # document fuel and cargo
            self.HubVisits +=1
            hub.FuelProvided.put(self.FuelTankSize - self.FuelTank)
            hub.GoodsReceived.put(self.CargoLoad.level)
            self.FuelTank = self.FuelTankSize #.put(self.FuelTankSize)
            self.CargoLoad.get(self.CargoLoad.level)
            self.NoTimeSoReturningToHub = 0     

    def choose_next_hub_event(self,hub,cities):
        """ """
        # Needs Maintenance?
        # IF Next city?
        # ELSE Park
        with hub.ParkingSpaces.request() as parkingReq:
            yield parkingReq
            placeholder=1 # print(self.IdAirship + ' parking at %.2f' % self.env.now)
            # yield self.env.process(self.choose_city(hub,cities))
        
    def wait(self, hub, cities, timeWaited):
        """
        takes the time the airship waited
        finds the amount of fuel used by it and the refuel ship  
        """
        waitingSpeed_kmh = 20
        fuelUsedWaiting = ((timeWaited * waitingSpeed_kmh) / self.Range_km) * self.FuelTankSize
        if fuelUsedWaiting > 0:
            if self.AtHub == 0:
                fuelUsedWaiting += (self.distanceToCity/self.Range_km * self.FuelTankSize)
                hub.FuelProvidedWhileWaitingLoad.put(fuelUsedWaiting)
            else:
                hub.FuelProvidedWhileWaitingUnload.put(fuelUsedWaiting)

def Operational_Cost_PerDay(airships, cities, hub):
    """
    Operational Cost Per Day:
     - Takes hours in workday, load & unload rates, and fuel per day
    """
    FuelCostPerLiter = 0.264172 * 1.50
    FuelInLiters = (hub.FuelProvidedWhileWaitingLoad.level + hub.FuelProvidedWhileWaitingUnload.level + hub.FuelProvided.level)*(1000000/840)
    FuelInLitersDirect = ((hub.FuelProvidedWhileWaitingLoad.level + hub.FuelProvidedWhileWaitingUnload.level + hub.FuelProvided.level)*1000) /.804
    CostFuelConsumedPerDay = FuelCostPerLiter * FuelInLiters / DAYS
    
    WorkerHoursPerTon = 1.0/15.0
    CostPerHour = 1000
    TotalWorkerCostPerHour = CostPerHour * (WorkerHoursPerTon * cities[0].AvgLoadRate + WorkerHoursPerTon * hub.AvgUnloadRate)
    TotalWorkerCostPerDay = WORK_DAY_HOURS * TotalWorkerCostPerHour
    
    DailyOperationalCost = TotalWorkerCostPerDay + CostFuelConsumedPerDay
    return DailyOperationalCost
    
def Investment_Cost(airships, cities, hub): # should provide an estimate on a reasonable order of magnitude
    """
    Investment Cost:
     - All in reelative terms based on an airship of 90 T
     - One time cost USD
     - Takes Fleet Size, Airship Size, Payload fraction (lower means the airship is more expensive)
        Number of Cities, Loading Areas, Unloading Areas, and Runways
     - Returns the intial cost of the airship fleet and needed infrastructure
    """
    AirshipCost = 180000000 #180 million for 90T airhsip
    AirshipRelativeSize = airship.MaxPayload / 90 # ratio for pricing airship linearly
    AirshipPFMultiplier = 1/ (0.4 / airships[0].PayloadFraction) # ratio for making more weight efficient airships more expensive
    CostForFleet = FLEET_SIZE * AirshipCost * AirshipRelativeSize * AirshipPFMultiplier
    
    HangarCost = 1000000 # one million
    CostPerUnloadingArea = 5000000 # five million, #cheaper because more controllable variable for airship company
    RunwayCost = 500000 # half million
    TotalHangarCost = HangarCost * FLEET_SIZE * AirshipRelativeSize
    TotalRunwayCost = RunwayCost * hub.Runways * AirshipRelativeSize
    TotalUnloadingAreaCost = CostPerUnloadingArea * hub.NumUnloadingAreas * AirshipRelativeSize
    TotalAirportCost = TotalHangarCost + TotalRunwayCost + TotalUnloadingAreaCost

    CostPerLoadingArea = 10000000 # ten million
    TotalCostPerCity = CostPerLoadingArea * cities[0].NumLoadingAreas
    TotalPartnerInfrastructureCost = NUM_CITIES * TotalCostPerCity

    totalInvestmentCost = CostForFleet + TotalAirportCost + TotalPartnerInfrastructureCost
    return totalInvestmentCost

def setup_and_go(env):
    """"""
    # create hub
    myHub = Hub(env,hubAttributes)
    # create cities
    cities = [City(env, 'City_%d'%i, ALL_COORDINATES[i+1], cityAttributes)
                    for i in range(NUM_CITIES)]
    # create airship fleet
    airshipFleet = [Airship(env, 'RED_%d'%i, AIRSHIP_ATTRIBUTES, myHub, cities)
                    for i in range(FLEET_SIZE)]
    return myHub, cities, airshipFleet
    

########## no loop ##########
# random.seed(96)
# env = simpy.Environment()
# hub, cities, airshipFleet = setup_and_go(env)
# # Execute
# env.run(until=TIME_SIM)

########## loop for doe ##########
DOE_filename = "data/LHC_5000.txt" #DONE
DOEdat = pd.read_csv(DOE_filename) #load DOE data
outputDataColumns = ["AirshipUsefulPayload","AirshipRange",
                        "AvgDailyGoodsPerAirship", "DailyTripsAVG_pApD",
                        "TakeoffWaitTime", "LoadWaitTime", "UnloadWaitTime", 
                        "OvertimeWorked", "UndertimeWorked",
                        "TotalGoodsTransported", "TotalFuelConsumed", "TotalTrips",
                        "DaysWorked", "DailyOperationalCost", 
                        "InvestmentCost","FuelConsumedFlying","FuelConsumedWaitingLoad",
                        "FuelConsumedWaitingUnload","FailedTripsTotal"]
zeroArray = np.zeros((DOEdat.shape[0],len(outputDataColumns)))
outputData = pd.DataFrame(zeroArray,columns=outputDataColumns)
DOEdat[list(outputData.columns)] = outputData # add empty data frame for output variables

for i in range(1000):
    # setup and run sim for each DOE row
    WORK_DAY_HOURS = DOEdat.at[i,'Workday_hrs']
    STARTING_HOUR = 8
    DAYS = 365*10
    TIME_SIM = DAYS*24
    NUM_CITIES = 3
    FLEET_SIZE = math.floor(DOEdat.at[i,'FleetSize'])
    TAKEOFF_TIME = DOEdat.at[i,'TakeoffTime_hrs']
    ALL_COORDINATES = [[-3.039, -60.048],
                    [-3.441, -60.462],
                    [-3.387, -60.344],
                    [-3.276, -60.190]]

    AIRSHIP_ATTRIBUTES = dict(payload_metrictons=DOEdat.at[i,'Payload_tonnes'], finenessRatio=DOEdat.at[i,'FinenessRatio'], 
                            speed_kmh=DOEdat.at[i,'Speed_kmh'], maximumFlightAltitude=DOEdat.at[i,'MaxFlightAltitude_m'],
                            fuelTankFraction=DOEdat.at[i,'FuelTankFraction'], payloadFraction=DOEdat.at[i,'PayloadFraction'],
                            maintenanceFrequency=DOEdat.at[i,'MaintenanceFreq_hrs'])
    
    cityAttributes = dict(hubCoordinates=ALL_COORDINATES[0], capacity_Tons=10000, available_Tons=100, 
                        numLoadingAreas=math.floor(DOEdat.at[i,'LoadingAreas']), avgLoadRate=DOEdat.at[i,'AvgLoadRate'])
    
    hubAttributes = dict(coordinates=ALL_COORDINATES[0], numUnloadingAreas=math.floor(DOEdat.at[i,'UnloadingAreas']), 
                        parkSpaces=FLEET_SIZE, maintenanceResource=math.floor(DOEdat.at[i,'MaintenanceeResource']), 
                        avgUnloadRate=DOEdat.at[i,'AvgUnloadRate'], takeoffReseource =math.floor(DOEdat.at[i,'Runways']))
    
    random.seed(96)
    env = simpy.Environment()
    hub, cities, airshipFleet = setup_and_go(env)
    # Execute
    env.run(until=TIME_SIM)
    
    # STORE DATA FROM RUN
    # city data
    
        
    # airship data
    totalTakeoffWaitTime = 0
    totalLoadWaitTime = 0
    totalUnloadWaitTime = 0
    totalOverTimeWorked = 0
    totalUnderTimeWorked = 0
    totalDaysWorked = 0
    totalTrips = 0
    totalFailedMissions = 0
    totalHubVisits = 0
    for airship in airshipFleet:
        totalTakeoffWaitTime += airship.TakeoffWaitTime
        totalLoadWaitTime += airship.LoadWaitTime
        totalUnloadWaitTime += airship.UnloadWaitTime
        totalOverTimeWorked += airship.OverTimeWorked
        totalUnderTimeWorked += airship.UnderTimeWorked
        totalDaysWorked += airship.DaysWorked
        totalTrips += airship.NumTrips
        totalFailedMissions += airship.FailedMissionCount
        airshipRange = airship.Range_km
        totalHubVisits += airship.HubVisits
    avgTakeoffWaitTimePerAirshipPerDay =  (totalTakeoffWaitTime) / FLEET_SIZE / DAYS
    avgLoadWaitTimePerAirshipPerDay =  (totalLoadWaitTime) / FLEET_SIZE / DAYS
    avgUnloadWaitTimePerAirshipPerDay =  (totalUnloadWaitTime) / FLEET_SIZE / DAYS
    avgOverTimeWorkedPerAirshipPerDay =  (totalOverTimeWorked) / FLEET_SIZE / DAYS
    avgUnderTimeWorkedPerAirshipPerDay =  (totalUnderTimeWorked) / FLEET_SIZE / DAYS
    avgDaysWorkedPerAirship =  (totalDaysWorked) / FLEET_SIZE
    avgTripsPerAirshipPerDay = totalTrips / FLEET_SIZE / DAYS

    DOEdat.at[i,'AirshipUsefulPayload'] = airship.Payload
    DOEdat.at[i,'AirshipRange'] = airshipRange
    DOEdat.at[i,'TotalGoodsTransported'] = hub.GoodsReceived.level
    DOEdat.at[i,'FuelConsumedFlying'] = hub.FuelProvided.level
    DOEdat.at[i,'FuelConsumedWaitingUnload'] = hub.FuelProvidedWhileWaitingUnload.level
    DOEdat.at[i,'FuelConsumedWaitingLoad'] = hub.FuelProvidedWhileWaitingLoad.level
    DOEdat.at[i,'TotalTrips'] = totalTrips
    DOEdat.at[i,'DailyTripsAVG_pApD'] = avgTripsPerAirshipPerDay
    DOEdat.at[i,'AvgDailyGoodsPerAirship'] = hub.GoodsReceived.level / FLEET_SIZE / DAYS
    DOEdat.at[i,'TakeoffWaitTime'] = avgTakeoffWaitTimePerAirshipPerDay
    DOEdat.at[i,'LoadWaitTime'] = avgLoadWaitTimePerAirshipPerDay
    DOEdat.at[i,'UnloadWaitTime'] = avgUnloadWaitTimePerAirshipPerDay
    DOEdat.at[i,'OvertimeWorked'] = avgOverTimeWorkedPerAirshipPerDay
    DOEdat.at[i,'UndertimeWorked'] = avgUnderTimeWorkedPerAirshipPerDay
    DOEdat.at[i,'DaysWorked'] = DAYS
    DOEdat.at[i,'FailedTripsTotal'] = totalFailedMissions
    DOEdat.at[i,"DailyOperationalCost"] = Operational_Cost_PerDay(airshipFleet, cities, hub)
    DOEdat.at[i,"InvestmentCost"] = Investment_Cost(airshipFleet, cities, hub)
    DOEdat.at[i,'TotalFuelConsumed'] = hub.FuelProvided.level + hub.FuelProvidedWhileWaitingLoad.level + hub.FuelProvidedWhileWaitingUnload.level
   
    
    # DOEdat.at[i,'']
    placeholder=1 # print('\n\n')
    print(str(i) + ' ********************************* RUN DONE')
    placeholder=1 # print('\n\n')
    
# END FOR LOOP

DOEdat.to_csv(DOE_filename[:-4]+'10yr_output.csv')
# os.system(f'say -v {"Fiona"} {"I am done computing."}')
