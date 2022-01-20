# Airship Class

import airshipDesignCalculator as ADC

class Airship:
    """"""
    def __init__(self, env, airshipID, airshipAttributes, hub,cities):
        self.capacity = 1
        # Airship Design Parameters
        
        # airship capabilities/capacities

        # tracking variables

        # Calculation Functions
        self.z = ADC.testthis(1,1)
    
    # Behavioral/Decision Functions

    # Action Functions

    def working(self):
        while(1):
            do=1

    def start_working(self):
        wakeup = 1

    def stop_working(self):
        gotosleep = 1

    def hub_to_city(self):
        leave = 1

    def city_to_hub(self):
        goback = 1

    def city_to_city(self):
        addthis = 0

    def unload_cargo(self):
        dropload = 1

    def load_cargo(self):
        getload = 1

    def get_wait_results(self):
        waitduration = 1

    

x = Airship(1,1,1,1,1)
print(x.z)