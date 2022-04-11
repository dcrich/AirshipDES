import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def getCoordinates(a,abefore,aafter):
    if a == -6:
        LatLon = [-3.117, -60.025]
    elif a == -1:
        LatLon = [-3.117, -60.025]
    elif a == 0:
        LatLon = [-3.196, -59.826]
    elif a == 1:
        LatLon = [-3.276, -60.190]
    elif a == 2:
        LatLon = [-3.387, -60.344]
    elif a == 3:
        LatLon = [-3.441, -60.462]
    elif a == -2:
        if not abefore == -2:
            LatLon = getCoordinates(abefore,999,999)
            return LatLon
        elif not aafter == -2:
            LatLon = getCoordinates(aafter,999,999)
            return LatLon
        else:
            raise Exception("Missed a case")
    else:
        print(a)
        raise Exception("Missed a case")
    return np.array(LatLon)


def create_new_data_array(data1):
    oldwindow = 8760
    newStep = 0.01
    newwindowLength = int(oldwindow/newStep)
    # time, activity, lat, lon, payload level, fuel level
    newdata1 = -99999 * np.ones((newwindowLength,6))
    for i in range(np.size(data1,0)-1):
        # look at current and next value, interoplate position and activity, add to new matrix
        currentTime = data1[i,1]
        nextTime = data1[i+1,1]
        newCurrentTimeInd = int(currentTime / newStep)
        newNextTimeInd = int(nextTime / newStep)

        lengthIntData = int(newNextTimeInd-newCurrentTimeInd)
        interpolatedData = -99999 * np.ones((lengthIntData,6))

        # interpolate time
        tempvar = np.arange(data1[i,1],data1[i+1,1],newStep)
        interpolatedData[0:lengthIntData,0] = tempvar[0:lengthIntData]
        # interpolate Lat, Lon, activity
        if i == 207:
            stophere = 1
        if i == 0:
            coord1 = getCoordinates(data1[i,3],999,data1[i+1,3])
        else:
            coord1 = getCoordinates(data1[i,3],data1[i-1,3],data1[i+1,3])
        try:
            coord2 = getCoordinates(data1[i+1,3],data1[i,3],data1[i+2,3])
        except:
            coord2 = getCoordinates(data1[i+1,3],data1[i,3],999)

        if np.allclose(coord1,coord2):
            interpolatedData[0:lengthIntData,2] = coord1.item(0) * np.ones((lengthIntData))
            interpolatedData[0:lengthIntData,3] = coord1.item(1) * np.ones((lengthIntData))
            interpolatedData[0:lengthIntData,1] = data1[i,3] * np.ones((lengthIntData))
        else:
            interpolatedData[0:lengthIntData,2] = np.linspace(coord1.item(0),coord2.item(0),lengthIntData)
            interpolatedData[0:lengthIntData,3] = np.linspace(coord1.item(1),coord2.item(1),lengthIntData)
            interpolatedData[0,1] = data1[i,3]
            interpolatedData[1:lengthIntData,1] = 99

        # interpolate payload
        interpolatedData[0:lengthIntData,4] = data1[i,4] * np.ones((lengthIntData))
        # interpolate fuel
        interpolatedData[0:lengthIntData,5] = np.linspace(data1[i,5],data1[i+1,5],lengthIntData)

        therange = np.arange(newCurrentTimeInd,newNextTimeInd,1)
        

        newdata1[therange,:] = interpolatedData

    deleterows = np.argwhere(newdata1[:,0]==-99999)
    newdata1 = np.delete(newdata1,deleterows,0)
    return newdata1



def plot_simulation(newdata1,newdata2):
    lengthnewdata1 = np.size(newdata1,0)
    lengthnewdata2 = np.size(newdata2,0)
    minlength = min([lengthnewdata1,lengthnewdata2])
    import glob # Need this to load photos (better than holding them in RAM forever)
    import time
    from PIL import Image
    # from mpl_toolkits.basemap import Basemap
    import matplotlib
    matplotlib.use('TkAgg')

    rx, ry = 30., 15.
    area = rx * ry * np.pi
    theta = np.arange(0, 2 * np.pi + 0.01, 0.1)
    verts = np.column_stack([rx / area * np.cos(theta), ry / area * np.sin(theta)])
    indstart1 = np.argwhere(newdata1[:,0]==6895)
    indend1 = np.argwhere(newdata1[:,0]==6991)
    indstart2 = np.argwhere(newdata2[:,0]==6895)
    indend2 = np.argwhere(newdata2[:,0]==6991)
    indstart = np.min(np.array([indstart1,indstart2]))
    indend = np.max(np.array([indend1,indend2]))
    for i in np.arange(indstart,indend,1):
        a1Lat = newdata1[i,2]
        a1Lon = newdata1[i,3]
        a1Act = newdata1[i,1]

        a2Lat = newdata2[i,2]
        a2Lon = newdata2[i,3]
        a2Act = newdata2[i,1]

        plt.clf() # clear the frame.
        plt.gca().set_aspect(1.3, adjustable='box')
        plt.xlim((-60.6,-59.6))
        plt.ylim((-3.5,-3.1))
        plt.scatter(-60.025, -3.117, s=75,c='k',marker="o") #plot manaus
        plt.text(-60.025, -3.117,'  Manaus', fontsize=12)
        plt.scatter(-59.826, -3.196, s=75,c='k',marker="o") #plot c
        plt.text(-59.826, -3.196,'  Careiro', fontsize=12)
        plt.scatter(-60.190, -3.276, s=75,c='k',marker="o") #plot i
        plt.text(-60.190, -3.276,'  Iranduba', fontsize=12)
        plt.scatter(-60.344, -3.387, s=75,c='k',marker="o") #plot j
        plt.text(-60.344, -3.387,'  Jutai', fontsize=12)
        plt.scatter(-60.462, -3.441, s=75,c='k',marker="o") #plot m
        plt.text(-60.462, -3.441,'  Manaquiri', fontsize=12)
        plt.scatter(a1Lon,a1Lat, s=1000,c='b',alpha = 0.5,marker=verts)
        plt.scatter(a2Lon,a2Lat, s=1000,c='r',alpha = 0.5,marker=verts)
        plt.savefig("gif/frame_" + str(i).zfill(7) + ".png",dpi=300, bbox_inches = 'tight',pad_inches = 0.05)
        # plt.gcf().canvas.draw() # interactive plotting is weird, but force it to execute here
        # time.sleep(0.01)
        # imgData = np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8) # Extra image data from the plot
        # w, h = plt.gcf().canvas.get_width_height() # Determine the dimensions
        # mod = np.sqrt(imgData.shape[0]/(3*w*h)) # multi-sampling of pixels on high-res displays does weird things, account for it.
        # im = imgData.reshape((int(h*mod), int(w*mod), -1)) # Create our image array in the right shape
        # Image.fromarray(im).save("gif/frame_" + str(i).zfill(5) + ".png",dpi=300) # And pass it to PIL to save it.
        plt.gcf().canvas.flush_events() # Make sure the canvas is ready to go for the next step

    # print("starting gif making")
    # from PIL import Image
    
    # # Create the frames
    frames = [] # This holds each image
    imgs = glob.glob("gif/frame_*.png") # load 'em in
    imgs.sort() # Make sure they're in the right order
    for i in imgs: # For each one, we'll open and append
        new_frame = Image.open(i)
        frames.append(new_frame)
        # print("imported img " + str(i))
    # print("about to save")
    # Save into a GIF file that loops forever
    frames[0].save('gif/output.gif', format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    duration=len(imgs)*0.005, loop=1)
    # print("saved")


# loop through data, create new matrix that interpolates where each airship is at a time step
data = pd.read_csv('8.0-20.0-2.0_outputTimeSeries2022-04-11_09-35-16-AM.csv')
data = data.drop([0])
dataArray = data.to_numpy()
lengthdata = np.size(dataArray,0)
tempvar1 = dataArray[:,2]
tempvar2 = dataArray[:,2]==0
data1 = dataArray[np.argwhere(dataArray[:,2]==0),:].reshape(-1,6)
data2 = dataArray[np.argwhere(dataArray[:,2]==1),:].reshape(-1,6)

newdata1 = create_new_data_array(data1)
newdata2 = create_new_data_array(data2)


plot_simulation(newdata1,newdata2)