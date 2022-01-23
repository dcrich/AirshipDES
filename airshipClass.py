"""
Airship Class
"""
import numpy as np

class Airship:
    """"""
    def __init__(self, env, airshipID, airshipAttributes, hub,cities, StartHourWorkday, EndHourWorkday):
        self.env = env
        self.ID = airshipID
        self.CurrentDay = 0
        self.StartHourWorkday = StartHourWorkday
        self.EndHourWorkday = EndHourWorkday
        self.hub = hub
        self.cities = cities
        self.StillWorkday = True
        # Airship Design Parameters
        
        # airship capabilities/capacities
        self.UsefulPayload = airshipAttributes[0]
        self.FuelCapacity = airshipAttributes[1]
        self.FuelLevel = airshipAttributes[1]
        self.Footprint = airshipAttributes[2]

        # tracking variables
        self.PayloadLevel = 0.0
        self.GoodsTransported = np.zeros(360)
        self.FuelLevel = airshipAttributes[1]
        self.FuelUsed = 0.0


    # Action Functions
    def working(self): # main operation loop
        while True: # run until sim is over
            self.start_working()
            self.stop_working()

    def start_working(self):
        while self.env.now < self.EndHourWorkday:
            self.hub_to_city()
            self.city_to_hub()

    def stop_working(self):
        gotosleep = 1

    def hub_to_city(self):
        # choose city
        self.choose_city()
        # fly
        # land, load cargo, etc.
        self.choose_city_activity()
        # choose city or hub
        self.choose_city()
        NextCityBool = False
        while NextCityBool: # continue to other cities until full or no fuel
            self.city_to_city()


    def city_to_hub(self):
        goback = 1

    def city_to_city(self):
        addthis = 0

    def unload_cargo(self):
        dropload = 1

    def load_cargo(self):
        getload = 1

    def wait(self):
        waitduration = 1
    
    
    # Behavioral/Decision Functions
    def in_range_time(self):
        check = 1
    def in_range_fuel(self):
        check = 1
    def choose_city(self):
        choose = 1
    def choose_city_activity(self):
        self.load_cargo()

    def choose_hub_activity(self):
        choose = 1


    # General Calculations
    def work_clock(self):
        time = 1
        self.CurrentDay = 1

    def calculate_range(self):
        numberofkm = 1
