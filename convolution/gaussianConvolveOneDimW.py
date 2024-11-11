import sys
import os
import numpy as np
import xarray as xr
import netCDF4 as nc
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter
from util.calculator import *


if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseIdx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    convolMethod = "fft"#chooseConvolMethod(std)
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    piBar3D = vvmLoader.loadPIBAR()[:-1][:, np.newaxis, np.newaxis]
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)
    stdList = [round(float(x), 1) for x in [1, 4, 16, 32, 64]]
    outputPaths = [config.convolveWPath + f"{caseName}/gaussian-{std}/" for std in stdList]
    dataWriters = [DataWriter(outputPath) for outputPath in outputPaths]
    gaussianWeights = [np.sum(getGaussianWeight(len(yc)*6, std=std), axis=0, keepdims=True) for std in stdList] # (1, 768)
    print([x.max() for x in gaussianWeights])
    print([x.sum() for x in gaussianWeights])
    newYc = np.array([1500 * 3 * y for y in range(len(yc)*6)])
    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        dyData = vvmLoader.loadDynamic(tIdx)
        var = np.array(dyData["w"][0])
        var = (np.roll(var, 1, axis=0) + var) / 2        
        var = np.mean(var, axis=1, keepdims=True)
        for i, std in enumerate(stdList):
            print(tIdx, std)
            convVar = getGaussianConvolve1D(var, gaussianWeights[i], method=convolMethod)[np.newaxis, :, :, :]
            dataWriters[i].toNC(fname=f"w-{tIdx:06d}.nc",
                               data=convVar, 
                               coords = {"time": np.array([1]), "zc": zc, "yc": np.array([1]), "xc": xc}, 
                               dims = ["time", "zc", "yc", "xc"], 
                               varName = "w")
