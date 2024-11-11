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
    stdList = [round(float(x), 1) for x in [1, 4, 16, 32, 64]]
    outputPaths = [f"{config.tildeQvBuoyancyPath}{caseName}/gaussian-{std}/" for std in stdList]
    tildeWriters = [DataWriter(op) for op in outputPaths]
    outputPaths = [f"{config.perturbQvBuoyancyPath}{caseName}/gaussian-{std}/" for std in stdList]
    perturbWriters = [DataWriter(op) for op in outputPaths]


    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        thData = vvmLoader.loadThermoDynamic(tIdx)
        #th = np.array(thData["th"][0])
        qv = np.array(thData["qv"][0])
        
        #thv = th * (1 + 0.608 * qv - qc - qi - qr)
        #thvBar = np.mean(thv, axis=(1, 2), keepdims=True)
        thv = 0.608 * qv
        thvBar = np.mean(thv, axis=(1, 2), keepdims=True)

        for stdIdx, std in enumerate(stdList):
            gaussianWeight = getGaussianWeight(len(yc), std=std)

            convolveThv = getGaussianConvolve(thv, gaussianWeight, method=convolMethod)
            convBuoyancy = g * (convolveThv - thvBar)# / (thvBar)
            convBuoyancy = convBuoyancy[np.newaxis, :, :, :]
            tildeWriters[stdIdx].toNC(fname=f"buoyancy-{tIdx:06d}.nc",
                            data=convBuoyancy, 
                            coords = {"time": np.array([1]), "zc": zc, "yc": yc, "xc": xc}, 
                            dims = ["time", "zc", "yc", "xc"], 
                            varName = "buoyancy")

            pertBuoyancy = g * (thv - convolveThv)# / (thvBar)
            pertBuoyancy = pertBuoyancy[np.newaxis, :, :, :]
            perturbWriters[stdIdx].toNC(fname=f"buoyancy-{tIdx:06d}.nc",
                            data=pertBuoyancy,
                            coords = {"time": np.array([1]), "zc": zc, "yc": yc, "xc": xc},
                            dims = ["time", "zc", "yc", "xc"],
                            varName = "buoyancy")
