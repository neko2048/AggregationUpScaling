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
from matplotlib.colors import from_levels_and_colors


if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseIdx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    caseName = config.caseNames[caseIdx]
    if endTimeIdx > int(config.lastTimeStep[caseName]): endTimeIdx = int(config.lastTimeStep[caseName]) + 1
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    rho3D = vvmLoader.loadRHO()[:-1][:, np.newaxis, np.newaxis]
    piBar = vvmLoader.loadPIBAR()[:-1][:, np.newaxis, np.newaxis]
    zc3D = zc[:, np.newaxis, np.newaxis]
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)

    mseRecord = np.zeros(shape=(len(timeArange), len(zc)))
    
    for i, tIdx in enumerate(timeArange):
        print(f"========== {tIdx:06d} ==========")
        mse = np.array(nc.Dataset(f"{config.msePath}{caseName}/mse-{tIdx:06d}.nc")["mse"][0]) / 1004
        w = np.array(vvmLoader.loadDynamic(tIdx)["w"][0])
        w = (np.roll(w, 1, axis=0) + w) / 2
        
        w = w - np.mean(w, axis=(1, 2), keepdims=True)
        mse = mse - np.mean(mse, axis=(1, 2), keepdims=True)
        mseProf = np.mean(rho3D * (mse * w), axis=(1, 2))
        mseRecord[i] = mseProf

    np.save(f"{config.mseHovProfPath}{caseName}/mseProf.npy", mseRecord)