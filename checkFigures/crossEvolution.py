import sys
import os
import numpy as np
import xarray as xr
import netCDF4 as nc
from scipy import interpolate
import matplotlib.pyplot as plt
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter
from util.calculator import *
from matplotlib.colors import from_levels_and_colors

def runningMean(data, windowLength):
    meanData = np.zeros(shape=(data.shape[0]-(windowLength-1), data.shape[1]))
    for i in range(meanData.shape[0]):
        meanData[i] = np.nanmean(data[i:i+windowLength], axis=0)
    return meanData

def simpleMean(data, windowLength):
    meanData = np.zeros(shape=(data.shape[0]//windowLength, data.shape[1]))
    for i in range(meanData.shape[0]):
        meanData[i] = np.nanmean(data[i*windowLength:(i+1)*windowLength], axis=0)
    return meanData

def getCmapAndNorm(cmapName, levels, extend="neither"):
    cmap = plt.get_cmap(cmapName)
    if extend == "both":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels)+1)],
                         extend=extend)
    elif extend == "max" or extend == "min":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels))],
                         extend=extend)
    elif extend == "neither":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels)-1)])
    return cmap, norm

def sizeTo25Days(data):
    if data.shape[0] > 700:
        return data[:601, :]
    else:
        return data


if __name__ == "__main__":
    caseIdx = int(sys.argv[1])
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    stdList = [1.0, 16.0, 64.0, 128.0]
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    #[1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]
    #[6.0, 8.0, 10.0, 12.0, 14.0]
    #[1.0, 2.0, 4.0, 8.0, 16.0]

    cmap = plt.get_cmap("jet")
    windowLength = 24
    totalProf = np.load(f"{config.mseHovProfPath}{caseName}/mseProf.npy")
    print(totalProf)
    totalProf = np.abs(totalProf)
    #print(totalProf[120, np.argmin(np.abs(zc/1e3-3))])
    totalProf = simpleMean(totalProf, windowLength=windowLength)
    timeArange = np.arange(0, totalProf.shape[0], 1)
    ttRecords = []
    ppRecords = []
    closestHour = []#[75, 149, 281, -1, -1]
    argz = np.argmin(np.abs(zc/1e3-6))

    for std in np.array(stdList):
        ttRecord = np.load(f"{config.mseHovProfPath}{caseName}/mse-ttRecord-{std}.npy")
        ttRecord = simpleMean(ttRecord, windowLength=windowLength) #/ totalProf
        ttRecord = np.abs(ttRecord)
        print(ttRecord)
        ppRecord = np.load(f"{config.mseHovProfPath}{caseName}/mse-ppRecord-{std}.npy")
        ppRecord = simpleMean(ppRecord, windowLength=windowLength) #/ totalProf
        ppRecord = np.abs(ppRecord)
        total = ttRecord + ppRecord
        ttRecord /= (total)
        ppRecord /= (total)
        #ttRecord[np.abs(ttRecord)>=10] = np.nan
        ttRecords.append(ttRecord)
        #ppRecord[np.abs(ppRecord)>=10] = np.nan
        ppRecords.append(ppRecord)
    names = [fr"${int(x*18)}km$" for x in stdList]

    for i in range(len(names)):
        oldHours = np.arange(len(ppRecords[i])) * 24
        newHours = np.arange((len(ppRecords[i])-1)*24)
        f = interpolate.interp1d(oldHours, ppRecords[i][:, argz] - ttRecords[i][:, argz])
        interpDelta = f(newHours)
        try:
            closestHour.append(int(newHours[np.where(interpDelta<0)][0]))
            print(closestHour)
        except IndexError:
            closestHour.append(-1)
    print(closestHour)
    dailyTimeArange = np.arange(0, totalProf.shape[0])
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
    for i in range(len(names)):
        #color = cmap((2*i+1) / (len(names)+9)) # 0 1 2 3 4 5 6 7 8 9 / 9 -> 1 3 5 7 9 11 13 15 17 / (9+9)
        color = cmap((2*i+1) / (len(names)+5)) # 0 1 2 3 4 5 6 7 8 9 / 9 -> 1 3 5 7 9 11 13 15 17 / (9+9)
        print(ttRecords[i][:, np.argmin(np.abs(zc/1e3-3))].shape)
        ax.plot(dailyTimeArange, ttRecords[i][:, argz], label=names[i], color=colors[i], linewidth=3)
        ax.plot(dailyTimeArange, ppRecords[i][:, argz], linestyle="--", color=colors[i], linewidth=3)
        ax.vlines(closestHour[i]/24, ymin=-0.1, ymax=1.1, color=colors[i], linewidth=3, alpha=0.5)
        
    plt.yticks([-1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0], fontsize=15)
    plt.xlabel("days", fontsize=15)
    plt.xticks(np.arange(0, ppRecords[i].shape[0])[::5], fontsize=15)
    plt.ylim(-0.1, 1.1)
    plt.grid(True)
    plt.xlim(0, dailyTimeArange[-1])
    plt.legend(fontsize=15, loc="lower right")
    #plt.title(f"{caseName}", fontsize=15)
    plt.savefig(f"crossEvolution.jpg", dpi=300)
