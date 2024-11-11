import sys
import os
import json
import numpy as np
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter
from util.calculator import *
from matplotlib.colors import from_levels_and_colors
from util.dataPloter import truncate_colormap, getCmapAndNorm

if __name__ == "__main__":
    caseIdx = 17 # int(sys.argv[1])
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    intersection = [200, 400, 600]#json.load(open("./closestHour.json"))[caseName]
    titles = ["(a) 200hr (s=12km)", "(b) 400hr (s=12km)", "(c) 600hr (s=12km)", 
              "(d) 200hr (s=288km)", "(e) 400hr (s=288km)", "(f) 600hr (s=288km)", 
              "(g) 200hr (s=576km)", "(h) 400hr (s=576km)", "(i) 600hr (s=576km)", ]
    stdList = [1.0, 16.0, 32.0]
    levels = np.arange(0, 0.055, 0.005)
    levels = np.unique(np.hstack((levels, -levels)))
    #cmap, norm = getCmapAndNorm("RdBu_r",
    #                            levels=levels,
    #                            extend="both")
    
    cmap = plt.cm.turbo #plt.cm.twilight_shifted
    left, right = 0.4, 0.6
    cmap_list = [cmap(i) for i in np.linspace(0.15, left, 128)] + [cmap(i) for i in np.linspace(right, 0.85, 128)]
    cmap = ListedColormap(cmap_list)
    cmap.set_under("#466BE3")
    cmap.set_over("#D23004")
    # Define the boundaries and norm
    norm = BoundaryNorm(levels, cmap.N)

    fs = 35
    lw = 4
    print(intersection)
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(32, 19))
    for itsIdx in range(len(intersection)):
        #if itsIdx % 2 != 0: continue
        for stdIdx in range(len(stdList)):
            print(stdList[stdIdx], intersection[itsIdx], itsIdx, stdIdx)
            if intersection[itsIdx] != 0:
                wPath = f"{config.convolveWPath}{caseName}/gaussian-{stdList[stdIdx]:.1f}/w-{intersection[itsIdx]:06d}.nc"
                w = np.array(nc.Dataset(wPath)["w"][0])
                w = np.array(w - np.mean(w, axis=(1, 2), keepdims=True))[:, 0, :]
            else:
                w = np.zeros(shape=(len(zc), len(xc)))
                w = np.ma.masked_array(w, w == 0)
            plt.sca(axs[stdIdx, itsIdx])
            #im=plt.pcolormesh(xc/1e5, zc/1e3, w, cmap=cmap, norm=norm)
            im=plt.contourf(xc/1e6, zc/1e3, w, cmap=cmap, norm=norm, levels=levels, extend="both")
            #plt.contour(xc/1e5, zc/1e3, w, levels=levels, colors="black")
            #plt.contour(xc/1e5, zc/1e3, w, levels=[0], colors="black", linewidths=4)
            plt.title(f"{titles[stdIdx*3+itsIdx]}", fontsize=fs, y=1.025)
            if stdIdx == 2:
                plt.xlabel(r"X [$\times$1000 km]", fontsize=fs)
            if itsIdx == 0:
                plt.ylabel("Z [km]", fontsize=fs)
            plt.xticks(np.linspace(0, 6, 7), fontsize=fs)
            plt.yticks(np.linspace(0, 14, 8), fontsize=fs)
            plt.ylim(0, 11)

    cbar_ax = fig.add_axes([0.935, 0.075, 0.015, 0.88-0.075])
    cb=fig.colorbar(im, cax=cbar_ax, ticks=levels[::2])
    cb.ax.tick_params(labelsize=fs)
    fig.suptitle(r"$\widetilde{w}$ [$m\cdot s^{-1}$]" + f" in {config.caseNameMapTitles[caseName]}", fontsize=fs*1.5, x=0.5375)
    plt.subplots_adjust(left=0.05, right=0.925, top=0.88, bottom=0.075, wspace=0.15, hspace=0.3)
    plt.savefig(f"./tildeW.png", dpi=300)

