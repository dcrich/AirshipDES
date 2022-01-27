"""
Airship Class
"""
from time import time
import numpy as np

class Airship:
    """"""
    def __init__(self, env, airshipID, airshipAttributes, hub,cities, StartHourWorkday, EndHourWorkday):
        self.env = env
        self.ID = airshipID
        self.CurrentDay = 0
        self.StartHourWorkday = StartHourWorkday
        self.EndHourWorkday = EndHourWorkday
        self.Hub = hub
        self.Cities = cities

        # airship design parameters
        self.UsefulPayload = airshipAttributes[0]
        self.FuelCapacity = airshipAttributes[1]
        self.Footprint = airshipAttributes[2]
        self.CruiseSpeed = airshipAttributes[3]
        self.AirshipVolume_ft = airshipAttributes[4]

        # tracking variables
        self.PayloadRemaining = airshipAttributes[0]
        self.GoodsTransported = np.zeros(360, dtype=float)
        self.FuelRemaining = airshipAttributes[1]
        self.FuelUsed = 0.0
        self.TimeToNextCity = 0.0
        self.FuelToNextCity = 0.0
        self.TimeUtilized = np.zeros(360,dtype=float)
        
        # status variables
        self.StillWorkday = True
        self.AtHub = True
        self.CitySelected = False
        self.CurrentLatLon = [0,0]
        self.NextCity = 0
        self.CurrentCity = 0


        # queue simulation for airship instance
        self.env.process(self.start_working)
    # Action Functions
    def start_working(self): # main operation loop
        while True: # run until sim is over
            yield self.env.process(self.working())
            yield self.env.process(self.stop_working())

    def working(self):
        """
        ?????????????? HOW DOES PAYLOAD AVAILABILTY FACTOR IN ??????????????
        What happens if city doesn't have any fruit left that day????
        """
        self.StillWorkday = self.env.now < self.EndHourWorkday
        while self.StillWorkday: # work until end of the day
            self.StillWorkday = self.env.now < self.EndHourWorkday
            self.choose_city()
            
            if self.AtHub and self.CitySelected: # at hub, city choice
                yield self.env.process(self.hub_to_city())
            
            elif self.AtHub and not self.CitySelected: # at hub, no city chosen
                break # leave loop and to go to stop working
            
            elif not self.AtHub and self.CitySelected: # not at hub, city chosen
                yield self.env.process(self.city_to_city())
           
            elif not self.AtHub and not self.CitySelected: # not at hub and no city chosen
                yield self.env.process(self.city_to_hub())

    def stop_working(self):
        self.work_clock()
        yield self.env.timeout(self.StartHourWorkday) # do nothing working until next day
        
    def hub_to_city(self):
        # if fleet, incorporate resource, add 'waiting'
        # fly
        yield self.env.timeout(self.TimeToNextCity)
        self.CurrentCity = self.NextCity
        self.CurrentLatLon = self.Cities[self.CurrentCity].LatLon
        self.AtHub = False
        self.FuelRemaining = self.FuelRemaining - self.FuelToNextCity
        # land, load cargo, etc.
        yield self.env.process(self.choose_city_activity())

    def city_to_hub(self):
        # fly
        distanceToHubFromNextCity = self.distance_between_coordinates(self.Cities[self.CurrentCity].LatLon, self.Hub.LatLon)
        timeToHubFromCity = distanceToHubFromNextCity / self.CruiseSpeed
        yield self.env.timeout(timeToHubFromCity)
        self.CurrentLatLon = self.Hub.LatLon
        self.AtHub = True
        # land, unload cargo, refuel, maintenance, etc.
        yield self.env.process(self.choose_hub_activity())

    def city_to_city(self):
        yield self.env.timeout(self.TimeToNextCity)
        self.CurrentCity = self.NextCity
        self.CurrentLatLon = self.Cities[self.CurrentCity].LatLon
        self.AtHub = False
        self.FuelRemaining = self.FuelRemaining - self.FuelToNextCity
        # land, load cargo, etc.
        yield self.env.process(self.choose_city_activity())


    def load_cargo(self):
        """ 
        - Decide how much cargo should be loaded 
        - Make timeToLoad be from a distribution
        - Add Loading Resource
        """
        goodsToLoad = self.Cities[self.CurrentCity].AvailableGoods[self.CurrentDay]
        if goodsToLoad > self.UsefulPayload:
            goodsLoaded = self.UsefulPayload
            self.PayloadRemaining = 0.0
        elif goodsToLoad > self.PayloadRemaining:
            goodsLoaded = self.PayloadRemaining
            self.PayloadRemaining = 0.0
        else:
            goodsLoaded = goodsToLoad
            self.PayloadRemaining = self.UsefulPayload - goodsLoaded
        
        timeToLoad = goodsLoaded / self.Cities[self.CurrentCity].LoadingRate
        yield self.env.timeout(timeToLoad)
        self.Cities[self.CurrentCity].LoadingTime[self.CurrentDay] += timeToLoad
        self.Cities[self.CurrentCity].LoadedGoods[self.CurrentDay] += goodsLoaded
        self.Cities[self.CurrentCity].LostGoods[self.CurrentDay] -= goodsLoaded


    def unload_cargo(self):
        """
        - Make timeToUnload be from a distribution
        - Add unloading resource
        """
        goodsUnloaded = self.UsefulPayload - self.PayloadRemaining
        timeToUnload = goodsUnloaded / self.Hub.UnloadingRate
        yield self.env.timeout(timeToUnload)
        self.PayloadRemaining = self.UsefulPayload

    def refuel(self):
        refuel = 1

    def wait(self):
        waitduration = 1

    def maintenance(self):
        repair = 1
    
    
    # Behavioral/Decision Functions
    def choose_city(self):
        if not self.StillWorkday:
            self.CitySelected = False
        else:
            for i in range(len(self.Cities)):
                self.next_city()
                self.in_range()
                if self.InRange:
                    self.CitySelected = True
                    break
                else:
                    self.CitySelected = False

    def next_city(self):
        self.NextCity +=1
        if self.NextCity > len(self.Cities):
            self.NextCity = 0
    
    def in_range(self):
        distanceToDestination = self.distance_between_coordinates(self.CurrentLatLon, self.Cities[self.NextCity].LatLon)
        distanceToHubFromNextCity = self.distance_between_coordinates(self.Cities[self.NextCity].LatLon, self.Hub.LatLon)
        self.TimeToNextCity = distanceToDestination / self.CruiseSpeed
        timeToHubFromNextCity = distanceToHubFromNextCity / self.CruiseSpeed
        self.FuelToNextCity = self.calculate_fuel_used(self.TimeToNextCity)
        fuelToHubFromNextCity = self.calculate_fuel_used(timeToHubFromNextCity)
        timeToLoad = self.PayloadRemaining / self.Cities[self.NextCity].LoadingRate

        InRangeFuel = (self.FuelToNextCity + fuelToHubFromNextCity) < self.FuelRemaining
        InRangeTime = (self.TimeToNextCity + timeToHubFromNextCity + timeToLoad) < (self.EndHourWorkday - self.env.now)
        
        if InRangeFuel and InRangeTime:
            self.InRange = True
        else:    
            self.InRange = False
   
    def choose_city_activity(self):
        # if fleet, incorporate resource, add 'waiting'
        yield self.env.process(self.load_cargo())

    def choose_hub_activity(self):
        # unload cargo, refuel, maybe maintenance
        choose = 1
        yield self.env.process(self.unload_cargo())
        yield self.env.process(self.refuel())
        if maintenceRequired:
            yield self.env.process(self.maintenance())


    # General Calculations
    def work_clock(self):
        self.CurrentDay += 1
        self.StartHourWorkday += 24
        self.EndHourWorkday += 24 

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
        rhoAir = np.NaN #densityAltitude at 2000 ft

        # Calculate fuel per mile based on cruise speed, altitude, and wind
        v = speedKnots * knots2fps    # ft/s cruise speed
        HpFuelCalc = dragCoeff * (totalAirshipVolume * 10 ** 6) ** (2 / 3) * rhoAir *        \
                        v ** 3 / (2 * propEfficiency * hpPerFtLbPerSec * lbsPerSlug)    #propulsion horsepower
        tonsPerHour = HpFuelCalc * SFC / 2000    # tons of fuel per hour
        fuelUsed = tonsPerHour * cruiseTime
        
        # tonsPerMile = tonsPerHour / (speedKnots - headwindSpeed_knots)    #tons of fuel per mile        
        # safetyFactor = 1.1
        # self.Range_km = fuelTankSize_imperial / (safetyFactor * tonsPerMile)
        return fuelUsed
    
    def distance_between_coordinates(latlon1, latlon2):
        lat1 = latlon1[0] * np.pi / 180
        lon1 = latlon1[1] * np.pi / 180
        lat2 = latlon2[0] * np.pi / 180
        lon2 = latlon2[1] * np.pi / 180
        # distance in nm
        distanceBetweenCoord = 3440 * 2 * np.arcsin(np.sqrt((np.sin((lat1-lat2)/2))**2 + 
                                np.cos(lat1)*np.cos(lat2)*(np.sin((lon1-lon2)/2))**2))
        return distanceBetweenCoord

#   LEFT OFF 
# - city to hub
# - city to city
# - making city decision also based on payload fill
