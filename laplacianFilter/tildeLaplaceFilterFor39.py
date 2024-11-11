import sys
import os
import numpy as np
import xarray as xr
import netCDF4 as nc
import scipy.ndimage as ndmg
import matplotlib.pyplot as plt
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter
from util.calculator import *


if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseNameIdx, numFrameX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), round(float(sys.argv[4]), 1)
    caseName = config.caseNames[caseNameIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    dx = xc[1] - xc[0]
    dy = yc[1] - yc[0]
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)

    dataWriter = DataWriter(outputPath=f"{config.tildeThLaplacePath}{caseName}/gaussian-{numFrameX}/")

    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        buoyancy = np.array(nc.Dataset(config.tildeThBuoyancyPath + f"{caseName}/gaussian-{numFrameX}/buoyancy-{tIdx:06d}.nc")["buoyancy"][0])
        lpcBuoyancy = getHrzLaplacian(buoyancy) / (dx * dy)
        lpcBuoyancy = lpcBuoyancy[np.newaxis, :, :, :]
        lpcBuoyancy[:, 0, :, :] = 0
        lpcBuoyancy[:, -1, :, :] = 0
        dataWriter.toNC(fname=f"buoyancy-{tIdx:06d}.nc",
                        data=lpcBuoyancy, 
                        coords = {"time": np.array([1]), "zc": zc, "yc": yc, "xc": xc}, 
                        dims = ["time", "zc", "yc", "xc"], 
                        varName = "buoyancy", format="NETCDF3_64BIT")
        # format is specified for 39
