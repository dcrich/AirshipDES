"""
Unit tests for:
- Boat Model
- Social impact metrics

Run in terminal using command:
'pytest -q unit_test.py'
OR 
For detailed output:
'pytest -v -rN --tb=no --no-header'
"""
import pytest # not used but needs to be installed
import numpy as np
import random
import simpy

import airshipClass
import cityClass
import hubClass
import airshipDesignCalculator as ADC
import AirshipImpactMetrics as aim
import AirshipCostModel as ACM
import fruit as fp
import BoatModel as bm

@pytest.fixture # make it so environment can be used in each test function
def sim_env():
    
    return hub,city,airship,fruit

"""BOAT TESTS"""
def test_boat_class(sim_env):

    hub,city,airship,fruit = sim_env
    boat = bm.Boats(city,workdaylength,fruit)



"""IMPACT TESTS"""