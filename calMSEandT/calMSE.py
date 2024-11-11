import sys
import os
import numpy as np
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter
from util.calculator import *


if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseIdx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    convolMethod = "fft"
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    zc3D = zc[:, np.newaxis, np.newaxis]
    piBar3D = vvmLoader.loadPIBAR()[:-1][:, np.newaxis, np.newaxis]
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)
    mseWriter = DataWriter(outputPath=f"{config.msePath}{caseName}/")

    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        thData = vvmLoader.loadThermoDynamic(tIdx)
        th = np.array(thData["th"][0])
        qv = np.array(thData["qv"][0])
        temp = getTemperature(th, piBar=piBar3D)
        mse = getMSE(temp, zc3D, qv)
        mse = mse[np.newaxis, :, :, :]
        
        mseWriter.toNC(fname=f"mse-{tIdx:06d}.nc",
                       data=mse, 
                       coords = {"time": np.array([1]), "zc": zc, "yc": yc, "xc": xc}, 
                       dims = ["time", "zc", "yc", "xc"], 
                       varName = "mse")
