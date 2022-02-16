"""
Airship Class
Test Logic: 
- Re-test logic of simulation, esp choose_city and load_cargo
"""
import this
import numpy as np
import random

class Airship:
    """"""
    def __init__(self, env, airshipID, airshipAttributes, hub,cities, Workday):
        self.env = env
        self.ID = airshipID
        self.CurrentDay = 0
        self.StartHourWorkday = Workday[0]-1.0
        self.EndHourWorkday = Workday[1]-1.0
        self.Hub = hub
        self.Cities = cities
        self.maxfruit = np.zeros(4)
        i = 0
        for city in cities:
            self.maxfruit[i] = np.mean(city.AvailableGoods)
            i += 1

        # airship design parameters
        self.UsefulPayload = airshipAttributes[0]
        self.FuelCapacity = airshipAttributes[1]
        self.Footprint = airshipAttributes[2]
        self.AirshipVolume_ft = airshipAttributes[3]
        self.CruiseSpeed = airshipAttributes[4]
        
        self.Diameter = airshipAttributes[5]
        self.Length = airshipAttributes[6]
        self.CylinderFraction = 0.0 # not using
        self.RequiredHorsepower = 0.0 # set in fuel used function
        self.Payload = airshipAttributes[7]
        self.PayloadFraction = airshipAttributes[8]
        self.FuelTankFraction = airshipAttributes[9]
        
        # tracking variables
        self.PayloadRemaining = airshipAttributes[0]
        self.GoodsTransported = np.zeros(365, dtype=float)
        self.FuelRemaining = airshipAttributes[1]
        # self.FuelUsed = 0.0
        self.TimeToNextCity = 0.0
        self.FuelToNextCity = 0.0
        self.TimeUtilized = np.zeros(365,dtype=float)
        self.TimeEndedWorkday = np.zeros(365,dtype=float)
        self.DailyFuelConsumption = np.zeros(365,dtype=float)
        # 0 = start working
        # 1 = to_city
        # 2 = to_hub
        # 3 = end_day
        self.SimulationLogic = [0]
        
        
        
        # status variables
        self.StillWorkday = True
        self.AtHub = True
        self.CitySelected = False
        self.CurrentLatLon = self.Hub.LatLon
        self.NextCity = 0
        self.CurrentCity = 0
        self.WorkSchedule = np.ones(365)
        sundayIndex = np.arange(6,365,7)
        np.put(self.WorkSchedule, sundayIndex, np.zeros(np.size(sundayIndex)))
        self.citiesVisitedInTrip = 0

        self.CostToOperate = 0.0
        self.FuelCost = 0.0

        # queue simulation for airship instance
        self.env.process(self.start_working())


    # Action Functions
    def start_working(self): # main operation loop
        yield self.env.timeout(self.StartHourWorkday)
        #print(self.ID + ' starting sim at %.3f'%self.env.now)
        while True: # run until sim is over
            self.SimulationLogic.append(0)
            if self.WorkSchedule[self.CurrentDay] == 1:
                self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, -1, self.PayloadRemaining, self.FuelRemaining]], axis = 0)
                yield self.env.process(self.working())
                self.SimulationLogic.append(3)
            yield self.env.process(self.stop_working())
            

    def working(self):
        """
        """
        self.StillWorkday = bool(self.env.now < self.EndHourWorkday)
        while self.StillWorkday: # work until end of the day
            self.StillWorkday = bool(self.env.now < self.EndHourWorkday)
            self.choose_city()
            #print(self.ID + ' choosing city at %.2f'%self.env.now)
            
            if self.AtHub and not self.CitySelected: # at hub, no city chosen
                break # leave loop and to go to stop working

            elif self.AtHub and self.CitySelected: # at hub, city choice
                self.SimulationLogic.append(1)
                yield self.env.process(self.hub_to_city())
            
            elif not self.AtHub and self.CitySelected: # not at hub, city chosen
                self.SimulationLogic.append(1)
                yield self.env.process(self.city_to_city())
           
            elif not self.AtHub and not self.CitySelected: # not at hub and no city chosen
                self.SimulationLogic.append(2)
                yield self.env.process(self.city_to_hub())

    def stop_working(self):
        #print(self.ID + ' done working at %.2f'%self.env.now)
        self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, -6.9, self.PayloadRemaining, self.FuelRemaining]], axis=0)
        self.TimeEndedWorkday[self.CurrentDay] = self.env.now
        self.work_clock()
        timeUntilNextWorkday = self.StartHourWorkday - self.env.now
        self.NextCity = 0 # start each day trying to go to city 1
        self.CurrentCity = 0
        yield self.env.timeout(timeUntilNextWorkday) # do nothing working until next day
        
    def hub_to_city(self):
        """
        Track what cities have been visited each day in City instance. 
        Maybe store in airship the order of cities visited each day
        """
        # if fleet, incorporate resource, add 'waiting'
        # fly
        yield self.env.timeout(self.TimeToNextCity)
        #print(self.ID + ' arriving at ' + self.Cities[self.CurrentCity].ID + ' at %.2f'%self.env.now)
        self.CurrentCity = self.NextCity
        self.CurrentLatLon = self.Cities[self.CurrentCity].LatLon
        self.AtHub = False
        self.FuelRemaining = self.FuelRemaining - self.FuelToNextCity

        # land, load cargo, etc.
        yield self.env.process(self.choose_city_activity())
        self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, self.CurrentCity, self.PayloadRemaining, self.FuelRemaining]], axis=0)


    def city_to_city(self):
        yield self.env.timeout(self.TimeToNextCity)
        #print(self.ID + ' arriving at' + self.Cities[self.CurrentCity].ID + ' at %.2f'%self.env.now)

        self.CurrentCity = self.NextCity
        self.CurrentLatLon = self.Cities[self.CurrentCity].LatLon
        self.AtHub = False
        self.FuelRemaining = self.FuelRemaining - self.FuelToNextCity

        # land, load cargo, etc.
        yield self.env.process(self.choose_city_activity())
        self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, self.CurrentCity, self.PayloadRemaining, self.FuelRemaining]], axis=0)

    def city_to_hub(self):
        # fly
        distanceToHubFromCity = self.distance_between_coordinates(self.Cities[self.CurrentCity].LatLon, self.Hub.LatLon)
        timeToHubFromCity = distanceToHubFromCity / self.CruiseSpeed
        yield self.env.timeout(timeToHubFromCity)

        fuelToHubFromCity = self.calculate_fuel_used(timeToHubFromCity)
        self.FuelRemaining = self.FuelRemaining - fuelToHubFromCity

        #print(self.ID + ' arriving at Hub at %.2f'%self.env.now)
        self.CurrentLatLon = self.Hub.LatLon
        self.AtHub = True
        self.citiesVisitedInTrip = 0
        self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, -1, self.PayloadRemaining, self.FuelRemaining]], axis=0)
        # land, unload cargo, refuel, maintenance, etc.
        yield self.env.process(self.choose_hub_activity())
        self.Hub.SimulationTracker = np.append(self.Hub.SimulationTracker,[[self.env.now, self.ID, -1, self.PayloadRemaining, self.FuelRemaining]], axis=0)


    def load_cargo(self):
        """ 
        - Decide how much cargo should be loaded
        - Make timeToLoad be from a distribution
        - Add Loading Resource
        """
        if self.CurrentDay > 0.0:
            yesterdaysGoods = self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay-1]
        else:
            yesterdaysGoods = 0.0
        goodsToLoad = self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay] + yesterdaysGoods
        if goodsToLoad > self.PayloadRemaining:
            goodsLoaded = self.PayloadRemaining  #* random.random()
            self.PayloadRemaining -= goodsLoaded
        else:
            goodsLoaded = goodsToLoad  #* random.random()
            self.PayloadRemaining -= goodsLoaded
        timeToLoad = goodsLoaded * self.Cities[self.CurrentCity].LoadingRate
        
        if self.env.now + timeToLoad + self.timeToHubFromNextCity > self.EndHourWorkday: # if it will take to long to load, then load what it can
            timeToLoad = self.EndHourWorkday - self.env.now - self.timeToHubFromNextCity
            goodsLoaded = timeToLoad /  self.Cities[self.CurrentCity].LoadingRate
            
        yield self.env.timeout(timeToLoad)

        #print(self.ID + ' done loading at %.2f'%self.env.now)

        self.Cities[self.CurrentCity].NumberOfVisits[self.CurrentDay] += 1
        self.Cities[self.CurrentCity].LoadingTime[self.CurrentDay] += timeToLoad
        self.Cities[self.CurrentCity].LoadedGoods[self.CurrentDay] += goodsLoaded
        if yesterdaysGoods > 0: 
            if yesterdaysGoods > goodsLoaded:
                self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay-1] -= goodsLoaded
            else:
                self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay-1] = 0.0
                goodsLoaded -= yesterdaysGoods
                self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay] -= goodsLoaded
        else:
            self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay] -= goodsLoaded


    def unload_cargo(self):
        """
        - Make timeToUnload be from a distribution
        """
        with self.Hub.UnloadingResource.request() as unloadReq:
            yield unloadReq

            goodsUnloaded = self.UsefulPayload - self.PayloadRemaining
            timeToUnload = goodsUnloaded * self.Hub.UnloadingRate
            yield self.env.timeout(timeToUnload)

            #print(self.ID + ' done unloading at %.2f'%self.env.now)

            self.PayloadRemaining = self.UsefulPayload
            self.Hub.RecievedGoods[self.CurrentDay] += goodsUnloaded

    def refuel(self):
        """
        - Make time to refuel be from a distribution
        """
        with self.Hub.RefuelResource.request() as refuelReq:
            yield refuelReq
            yield self.env.timeout(self.Hub.AvgRefuelTime)

            #print(self.ID + ' done refueling at %.2f'%self.env.now)

            fuelUsed = self.FuelCapacity - self.FuelRemaining
            self.DailyFuelConsumption[self.CurrentDay] += fuelUsed
            self.FuelRemaining = self.FuelCapacity

    def maintenance_check(self):
        """
        Decide if and how much maintenance is required
        """
        with self.Hub.RepairResource.request() as repairReq:
            yield repairReq
            yield self.env.timeout(self.Hub.AvgRepairTime)
            #print(self.ID + ' done maintenance at %.2f'%self.env.now)
            
        
    def wait(self):
        waitduration = 1

    
    # Behavioral/Decision Functions
    def choose_city(self):
        """
        Add check for payload remaining
        If adding fleets, add check for if city is occupied
        """
        if not self.StillWorkday:
            self.CitySelected = False
        else:
            for i in range(len(self.Cities)):
                self.next_city()
                self.in_range()
                if self.CurrentDay > 0:
                    goodsAtCity = self.Cities[self.NextCity].AvailableGoods[self.CurrentDay] + self.Cities[self.NextCity].AvailableGoods[self.CurrentDay-1]
                else:
                    goodsAtCity = self.Cities[self.NextCity].AvailableGoods[self.CurrentDay]
                if self.InRange                                          \
                    and self.PayloadRemaining > 0.5                      \
                    and goodsAtCity > 0.5                                \
                    and self.citiesVisitedInTrip < np.size(self.Cities,0)   \
                    and not self.CurrentCity == self.NextCity:
                    self.CitySelected = True
                    self.citiesVisitedInTrip += 1
                    break
                else:
                    self.CitySelected = False

    def next_city(self):
        self.NextCity +=1
        # self.NextCity = random.randint(0,len(self.Cities))
        if self.NextCity >= len(self.Cities):
            self.NextCity = 0
    
    def in_range(self):
        tempvar = self.Cities[self.NextCity].LatLon
        distanceToDestination = self.distance_between_coordinates(self.CurrentLatLon, self.Cities[self.NextCity].LatLon)
        distanceToHubFromNextCity = self.distance_between_coordinates(self.Cities[self.NextCity].LatLon, self.Hub.LatLon)
        self.TimeToNextCity = distanceToDestination / self.CruiseSpeed
        self.timeToHubFromNextCity = distanceToHubFromNextCity / self.CruiseSpeed
        self.FuelToNextCity = self.calculate_fuel_used(self.TimeToNextCity)
        fuelToHubFromNextCity = self.calculate_fuel_used(self.timeToHubFromNextCity)
        timeToLoad = 2.0 #1.0 / self.Cities[self.NextCity].LoadingRate #should be able to load for at least 2 hours

        InRangeFuel = (self.FuelToNextCity + fuelToHubFromNextCity) < self.FuelRemaining
        InRangeTime = (self.TimeToNextCity + self.timeToHubFromNextCity + timeToLoad) < (self.EndHourWorkday - self.env.now)
        
        if InRangeFuel and InRangeTime:
            self.InRange = True
        else:    
            self.InRange = False
   
    def choose_city_activity(self):
        # if fleet, incorporate resource, add 'waiting'
        yield self.env.process(self.load_cargo())

    def choose_hub_activity(self):
        # unload cargo, refuel, maybe maintenance
        yield self.env.process(self.unload_cargo())
        yield self.env.process(self.refuel())
        yield self.env.process(self.maintenance_check())


    # Miscellaneous Calculations
    def work_clock(self):
        #print(self.ID + ' ending day %.0f'%self.CurrentDay)
        self.CurrentDay += 1
        self.StartHourWorkday += 24
        self.EndHourWorkday += 24 
        if self.CurrentDay > 364:
            stophere = 1

    def calculate_fuel_used(self,cruiseTime):
        # in imperial units
        # fuelTankSize_imperial = 1.1 * self.FuelTankSize #convert to imperial
        propEfficiency = 0.7  #prop efficiency
        dragCoeff = 0.025   # Drag Coefficient
        SFC = 0.41    #lb/hp/hr
        headwindSpeed_knots = 10    # knots headwind
        speedKnots = self.CruiseSpeed * 0.539957    # knots cruise speed
        totalAirshipVolume = self.AirshipVolume_ft * 10 ** -6    #M ft**3

         #Constants and Conversion Factors
        knots2fps = 1.68780986 
        lbsPerSlug = 32.1740486 
        hpPerFtLbPerSec = 550 
        rhoAir = 0.072 #densityAltitude at 2000 ft

        # Calculate fuel per mile based on cruise speed, altitude, and wind
        v = speedKnots * knots2fps    # ft/s cruise speed
        HpFuelCalc = dragCoeff * (totalAirshipVolume * 10 ** 6) ** (2 / 3) * rhoAir *        \
                        v ** 3 / (2 * propEfficiency * hpPerFtLbPerSec * lbsPerSlug)    #propulsion horsepower
        tonsPerHour = HpFuelCalc * SFC / 2000    # tons of fuel per hour
        fuelUsed = tonsPerHour * cruiseTime
        self.RequiredHorsepower = HpFuelCalc
        # tonsPerMile = tonsPerHour / (speedKnots - headwindSpeed_knots)    #tons of fuel per mile        
        # safetyFactor = 1.1
        # self.Range_km = fuelTankSize_imperial / (safetyFactor * tonsPerMile)
        return fuelUsed
    
    def distance_between_coordinates(self, latlon1, latlon2):
        lat1 = latlon1[0] * np.pi / 180
        lon1 = latlon1[1] * np.pi / 180
        lat2 = latlon2[0] * np.pi / 180
        lon2 = latlon2[1] * np.pi / 180
        # distance in nm
        distanceBetweenCoord = 6371 * 2 * np.arcsin( np.sqrt( (np.sin((lat1-lat2)/2))**2 + np.cos(lat1)*np.cos(lat2)*(np.sin((lon1-lon2)/2))**2 ))
        
    
        return distanceBetweenCoord

    def return_airship_parameters(self):
        NotImplementedYet = 0
        return NotImplementedYet