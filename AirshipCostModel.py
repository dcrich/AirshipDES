""" 
Need to Test 
"""

import numpy as np

def calculate_operational_cost(airship, fleetsize):
    farmerAmortizationFraction = 0.1
    operationalCostForFarmers = airship_costs(airship,fleetsize,farmerAmortizationFraction)
    airship.CostToOperate = operationalCostForFarmers

def airship_costs(airship,fleetsize,percentAmortizationPayedByFarmers):
	"""
	Cost Function adapted from DELTAS DES cost function
	"""

	diameter = airship.Diameter
	length = airship.Length
	cylinderFraction = airship.CylinderFraction
	requiredHorsepower = airship.RequiredHorsepower
	payload = airship.Payload
	payloadFraction = airship.PayloadFraction
	volume_ft3 = airship.AirshipVolume_ft
	# Weights
	# Envelope Weight
	envelopeMaterial_lbPerFt2 = 0.04
	surfaceAreaCapsule = 2 * np.pi * diameter/2 * length # capsule surface area
	noseLengthC = length * (1-cylinderFraction) / (1+np.sqrt(2)) 
	cylinderLengthC = length * cylinderFraction
	tailLengthC = length - cylinderLengthC - noseLengthC
	airshipRadiusC = diameter / 2
	surfaceAreaHalfSphere =  2 * np.pi * (diameter /2)**2 # simplifying from ellipsoid to half of a sphere
	surfaceAreaOuterCylinder = cylinderLengthC * np.pi * diameter
	surfaceAreaParaboloid = np.pi * airshipRadiusC * ((airshipRadiusC**2 + 4* tailLengthC**2)**(3/2) - airshipRadiusC **3) / (6*tailLengthC**2)
	envelopeSurfaceArea_ft2 = surfaceAreaHalfSphere + surfaceAreaOuterCylinder + surfaceAreaParaboloid
	envelopeWeight_lb = envelopeMaterial_lbPerFt2 * envelopeSurfaceArea_ft2
	
	# Engine Weight
	engineHP = 500 # RED A03 v12
	numberOfEngines = np.ceiling(requiredHorsepower / engineHP)
	engineUnitWeight_lbPerHP = 3.086 # Khoury 225-226
	engineWeight_lb = numberOfEngines * engineHP * engineUnitWeight_lbPerHP # engines
	# Airship & Structure Weights
	airshipWeight_lb = payload / payloadFraction # whole airship
	structureWeight_lb = (1-payloadFraction) * airshipWeight_lb - engineWeight_lb - envelopeWeight_lb
	#

	# Helium
	heliumPricePerThousandFt3 = 200 # $USD$ per thousand Ft**3
	heliumFillCost = heliumPricePerThousandFt3 * volume_ft3 * 0.001
	#

	# Structure
	aluminumPricePerPound = 1.4 # $USD$ per pound
	additionalCostFactor = 250
	structureCost = additionalCostFactor * aluminumPricePerPound * structureWeight_lb

	# Engines
	engineUnitPrice = 200000 # RED A03 v12
	additionalPowerCostFactor = 15
	engineCost = additionalPowerCostFactor * engineUnitPrice * numberOfEngines
	#
	
	intermediateAirshipCost = heliumFillCost + structureCost + engineCost

	# Envelope
	# fit of surface area from payload**1/3, scaled to the desired 0 to 0.1 range
	scalingFunction = 0.094 * ((-0.5 + 0.2 * (payload/2000)**(1/3) + 0.02 * ((payload/2000)**(1/3) -5.5)**2)-0.1) 
	if payload/2000 > 400:
		scalingFunction = 0.1
	envelopeFractionOfTotalCost = 0.2-scalingFunction # from Khoury p455 range of 0.1 to 0.2
	
	envelopeCost = intermediateAirshipCost * envelopeFractionOfTotalCost / (1-envelopeFractionOfTotalCost)
	

	# AIRSHIP
	airshipCostIndividual = envelopeCost + intermediateAirshipCost
	tempFleetVar = 0
	for i in np.arange(1,fleetsize+1,1):
		tempFleetVar = tempFleetVar + i**(-0.234)
	airshipFleetCost = airshipCostIndividual * tempFleetVar # cost curve 85% slope # Cost Estimating by Mislick & Nussbaum, p184 & 189
	airshipCostPerAirshipInFleet = airshipFleetCost / fleetsize
	percentHeliumFillCost = 100*heliumFillCost / airshipCostIndividual
	percentEnvelopeCost = 100*envelopeCost / airshipCostIndividual
	percentStructureCost = 100*structureCost / airshipCostIndividual
	percentEngineCost =  100*engineCost / airshipCostIndividual
	
	
	# # LAND
	# landCost_usd_ft2 = 286932 / 43560 # usd per acre / acres to ft2 # avg commercial/industrial land price in US 2012-2016
	# hangarLandCost = fleetsize * landCost_usd_ft2 * length * diameter * 1.25
	
	# ACQUISITION
	# acquisitionCost = hangarLandCost + airshipFleetCost
	
	##############################
	###### OPERATIONAL COST ######
	##############################
	# Fuel Cost
	fuelPricePerTon = 641.4 # USD per ton as of 1 Oct 21  iata.org
	fuelCost = np.sum(airship.DailyFuelConsumption) * fuelPricePerTon
	airship.FuelCost = fuelCost
	
	# ignoring these costs, assuming airship company pays for this
	# # Time Cost -- maybe ignore and describe how it will scale with airship size and flight duration
    # # Assume that the crew can rest en-route and only needs to rest at the end of a trip	# 
	# timeToRefuel_hr = 2 # c-17 - 1.75, c-5 - 2.75
	# timeToUnload_hr = 3 # c-17 - 2.75, c-5 - 3.75
	# timeForCrewRest_hr = 16
	# if numberoftrips > 1:
	# 	totalMissionTimeToClose = flightTimeMission + numberoftrips * (timeToRefuel_hr * (totalStopsWithReturn - 2) + timeToUnload_hr)      \
	# 								+ (numberoftrips-1) * timeForCrewRest_hr
	# else:
	# 	totalMissionTimeToClose = flightTimeMission + timeToRefuel_hr * (totalStopsWithReturn - 2) + timeToUnload_hr
	# crewSize = fleetsize * 3
	# crewMemberSalaryPlusBenefits = 200000
	# crewHourlyRate = crewSize * crewMemberSalaryPlusBenefits * 0.000114155251142 # salary / (356*24) # should it be salary / (50weeks*40hours)
	# timeCost = crewHourlyRate * totalMissionTimeToClose
	# # Ground handling cost - linear fit of data from flight costs paper by Chao and Hsu
	# groundHandlingCost = numberoftrips * fleetsize * (4.12*payload/2000+321) # linear fit has R**2 of 0.72
	# # Amortization of land cost
	# landAmortizationCost = hangarLandCost * 0.0000114155251142 * totalMissionTimeToClose


	totalMissionTimeToClose = 365.0 * 24.0 # hourse in a year

	# Amortization of airship cost
	airshipAmortizationCost = airshipCostPerAirshipInFleet * 0.0000114155251142 * totalMissionTimeToClose # airship cost over 10 years (10*365*24)
	
	# Helium Refill
	heliumLossPerDay_Ft3perFt2 = 1.14 * 0.00328 # liters/(meters**2 day) converted to ft**3/(ft**2 day) # Assuming constant atm
	poundsHeliumLostPerday = heliumLossPerDay_Ft3perFt2 * envelopeSurfaceArea_ft2 * 0.06
	# price per thousand to price per ft**3 * hours to days * surface area * volume lost per unit surface area per day
	heliumRefillCost = heliumPricePerThousandFt3 * 0.001 * totalMissionTimeToClose * 0.0416667 * envelopeSurfaceArea_ft2 * heliumLossPerDay_Ft3perFt2 
	
	operationalCostForFarmers = heliumRefillCost + fuelCost + airshipAmortizationCost * percentAmortizationPayedByFarmers
	return operationalCostForFarmers
	# missionCostNoCrew = heliumRefillCost + fuelCost + airshipAmortizationCost + landAmortizationCost + groundHandlingCost # autonomous option
	# percentHeliumCostAuton = 100*heliumRefillCost/missionCostNoCrew
	# percentFuelCostAuton = 100*fuelCost/missionCostNoCrew
	# percentAirshipAmortizationCostAuton = 100*airshipAmortizationCost/missionCostNoCrew
	# percentLandAmortizationCostAuton = 100*airshipAmortizationCost/missionCostNoCrew
	# percentHandlingCostAuton = 100 * groundHandlingCost / missionCostNoCrew
	
	# missionCostWithCrew = heliumRefillCost + fuelCost + timeCost + airshipAmortizationCost + landAmortizationCost + groundHandlingCost # manned option
	# percentHeliumCostCrew = 100*heliumRefillCost/missionCostWithCrew
	# percentFuelCostCrew = 100*fuelCost/missionCostWithCrew
	# percentTimeCostCrew = 100*timeCost/missionCostWithCrew
	# percentAirshipAmortizationCostCrew = 100*airshipAmortizationCost/missionCostWithCrew
	# percentLandAmortizationCostCrew = 100*landAmortizationCost/missionCostWithCrew
	# percentHandlingCost = 100 * groundHandlingCost / missionCostWithCrew

	
	
	# costPerFlightHour = missionCostWithCrew / flightTimeMission
	# AF_CPFH_timesFlightTime = (heliumRefillCost + fuelCost + timeCost + groundHandlingCost)
