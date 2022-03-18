import numpy as np
# take hub and city coordinates

# get distances between each city and the hub

# get average distances between cities

# generate coordinates based on those distributions -- maybe just from hub, then if its too close to an already generated city, find a new one

def generate_new_cities(numberOfNewCities, hubLatLon, cityCoordinates):
    np.random.seed(68)
    # get lat distances and lon distances
    hubLat = hubLatLon[0]
    hubLon = hubLatLon[1]
    cityArray = np.asfarray(cityCoordinates)
    latdist = np.array([])
    londist = np.array([])
    for i in range(len(cityCoordinates)):
        # latdist = np.append(latdist, distance_between_coordinates(hubLatLon,[cityArray[i,0],hubLatLon[1]]))
        # londist = np.append(londist, distance_between_coordinates(hubLatLon,[hubLatLon[0],cityArray[i,1]]))
        latdist = np.append(latdist, abs(hubLat-cityArray[i,0]))
        londist = np.append(londist, abs(hubLon-cityArray[i,1]))
    latdistMEAN = np.mean(latdist)
    latdistSTD = np.std(latdist)
    londistMEAN = np.mean(londist)
    londistSTD = np.std(londist)
    randomseed = 70
    newCityDistances = np.zeros(numberOfNewCities)
    for i in range(numberOfNewCities):
        randomlatdist = np.abs(np.random.default_rng(randomseed).normal(latdistMEAN,latdistSTD))
        newLat = round(hubLat + randomlatdist,3)
        newLon = round(hubLon + np.random.choice([-1,1]) * np.random.default_rng(7*randomseed).normal(londistMEAN,londistSTD),3)
        cityCoordinates.append([newLat,newLon])
        newCityDistances[i] = np.round(distance_between_coordinates(hubLatLon, [newLat,newLon]),1)
        randomseed+=1
    return cityCoordinates,newCityDistances

def distance_between_coordinates(latlon1, latlon2):
        lat1 = latlon1[0] * np.pi / 180
        lon1 = latlon1[1] * np.pi / 180
        lat2 = latlon2[0] * np.pi / 180
        lon2 = latlon2[1] * np.pi / 180
        # distance in nm
        distanceBetweenCoord = 6371 * 2 * np.arcsin( np.sqrt( (np.sin((lat1-lat2)/2))**2 + np.cos(lat1)*np.cos(lat2)*(np.sin((lon1-lon2)/2))**2 ))
        return distanceBetweenCoord



# hubCoordinates = [-3.117, -60.025]
# cityCoordinates = [ [-3.196, -59.826],  # Careiro
#                     [-3.276, -60.190],  # Iranduba
#                     [-3.387, -60.344],  # Jutai
#                     [-3.441, -60.462]]  # Manaquiri
# numberOfNewCities = 10
# import matplotlib.pyplot as plt
# cityArray = np.asfarray(cityCoordinates)
# plt.scatter(cityArray[:,1],cityArray[:,0], c="b", alpha=1)
# newCityList,newCityDistances = generate_new_cities(numberOfNewCities, hubCoordinates, cityCoordinates)
# newcityarray = np.asfarray(newCityList)
# plt.scatter(hubCoordinates[1],hubCoordinates[0], c="r")
# plt.scatter(newcityarray[:,1],newcityarray[:,0], c="g", alpha=0.3)
# np.savetxt('cities.txt',newcityarray,delimiter=',')
# plt.show()

