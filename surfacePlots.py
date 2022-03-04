from unicodedata import decimal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy.interpolate import griddata

data_filename = "ExperimentImpacts2022-03-01_10-22-02-AM.csv"
data = pd.read_csv(data_filename)
surfaceColor = cm.turbo

fig = plt.figure()
# ############################# Interpolate for surface
# ax = fig.add_subplot(236, projection= "3d")
# X = np.round(data["Payload"].to_numpy(),decimals=0)
# Y = np.round(data["CruiseSpeed"].to_numpy(),decimals=0)
# grid_x, grid_y = np.mgrid[np.min(X):np.max(X), np.min(Y):np.max(Y)]
# xint = np.round(data[["Payload","CruiseSpeed"]].to_numpy(),decimals=0)
# z = data["Time Savings"].to_numpy()
# zint = griddata(xint, z, (grid_x, grid_y), method='nearest')
# # Plot the surface.
# surf = ax.plot_surface(grid_x, grid_y, zint, cmap=surfaceColor, linewidth=0, antialiased=False)
# ax.zaxis.set_major_locator(LinearLocator(10))
# # A StrMethodFormatter is used automatically
# ax.zaxis.set_major_formatter('{x:.0f}')
# ax = fig.gca(projection='3d')
# ax.set_xlabel('Payload')
# ax.set_ylabel('Speed')
# ax.set_zlabel('Time Savings')
# #############################
############################# Interpolate for surface
ax = fig.add_subplot(236, projection= "3d")
X = np.round(data["Payload"].to_numpy(),decimals=0)
Y = np.round(data["CruiseSpeed"].to_numpy(),decimals=0)
grid_x, grid_y = np.mgrid[np.min(X):np.max(X), np.min(Y):np.max(Y)]
xint = np.round(data[["Payload","CruiseSpeed"]].to_numpy(),decimals=0)
z = data["Airship Revenue"].to_numpy()
zint = griddata(xint, z, (grid_x, grid_y), method='nearest')
# Plot the surface.
surf = ax.plot_surface(grid_x, grid_y, zint, cmap=surfaceColor, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Airship Revenue')
#############################

ax = fig.add_subplot(231, projection= "3d")
# Make data.
X = data["Payload"].to_numpy()
Y = data["CruiseSpeed"].to_numpy()
Z = data["Time Savings"].to_numpy()

# Plot the surface.
# surf = ax.plot_trisurf(X-X.mean(), Y-Y.mean(), Z, cmap=surfaceColor, linewidth=0, antialiased=False)
surf = ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)
# Customize the z axis.
# ax.set_zlim(np.min(Z), np.max(Z))
# ax.set_xlim(0,15)
# ax.set_ylim(0,50)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Time Savings')
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)


ax = fig.add_subplot(232, projection= "3d")
# Make data.
X = data["Payload"].to_numpy()
Y = data["CruiseSpeed"].to_numpy()
Z = data["Income"].to_numpy()
# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Income')
# X = np.array([0,20,0,20])
# Y = np.array([0,0,100,100])
# Z = np.array([0,0,0,0])
# ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)

ax = fig.add_subplot(233, projection= "3d")
# Make data.
X = data["Payload"].to_numpy()
Y = data["CruiseSpeed"].to_numpy()
Z = data["Crop Loss"].to_numpy()
# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Crop Loss')


ax = fig.add_subplot(234, projection= "3d")
# Make data.
X = data["Payload"].to_numpy()
Y = data["CruiseSpeed"].to_numpy()
Z = data["Boat Job Loss"].to_numpy()
# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Boat Job Loss')



ax = fig.add_subplot(235, projection= "3d")
# Make data.
X = data["Payload"].to_numpy()
Y = data["CruiseSpeed"].to_numpy()
Z = data["Forest Loss"].to_numpy()
# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=surfaceColor, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.0f}')
ax = fig.gca(projection='3d')
ax.set_xlabel('Payload')
ax.set_ylabel('Speed')
ax.set_zlabel('Forest Loss')

plt.show()