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
    convolMethod = "fft"#chooseConvolMethod(std)
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)
    stdList = [round(float(x), 1) for x in [128]]
    outputPaths = [config.convolveWPath + f"{caseName}/gaussian-{std}/" for std in stdList]
    dataWriters = [DataWriter(outputPath) for outputPath in outputPaths]
    gaussianWeights = [getGaussianWeight(len(yc), std=std) for std in stdList]
    
    
    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        dyData = vvmLoader.loadDynamic(tIdx)
        w = np.array(dyData["w"][0])
        w = (np.roll(w, 1, axis=0) + w) / 2
        for i, std in enumerate(stdList):
            convVar = getGaussianConvolve(w, gaussianWeights[i], method=convolMethod)
            convVar = convVar[np.newaxis, :, :, :]
            dataWriters[i].toNC(fname=f"w-{tIdx:06d}.nc",
                               data=convVar, 
                               coords = {"time": np.array([1]), "zc": zc, "yc": yc, "xc": xc}, 
                               dims = ["time", "zc", "yc", "xc"], 
                               varName = "w")


