import numpy as np
import netCDF4 as nc
import sys
import xarray as xr
sys.path.insert(0, "../")
import config
from util.vvmLoader import VVMLoader
from util.dataWriter import DataWriter

if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseIdx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    caseName = config.caseNames[caseIdx]
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    dataWriter = DataWriter(outputPath = f"{config.buoyancyPath}{caseName}/")
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)
    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        thData = vvmLoader.loadThermoDynamic(tIdx)
        th = np.array(thData["th"])
        qv = np.array(thData["qv"])
        qc = np.array(thData["qc"])
        qi = np.array(thData["qi"])
        qr = np.array(thData["qr"])
        thBar = np.tile(np.mean(th, axis=(2, 3), keepdims=True), reps=(1, 1, len(yc), len(xc)))
        #buoyancy = 9.81 * ((th - thBar) / thBar + 0.61 * qv - qc - qi - qr - qg)
        buoyancy = 9.81 * ((th - thBar) / thBar + 0.61 * qv - qc - qi - qr)
        buoyancy = buoyancy - np.tile(np.mean(buoyancy, axis=(2, 3), keepdims=True), reps=(1, 1, len(yc), len(xc)))
        dataWriter.toNC(f"buoyancy-{tIdx:06d}.nc", buoyancy, 
                        coords = {'time': np.ones(shape=(1,)), 'zc': zc, 'yc': yc, 'xc': xc},
                        dims = ["time", "zc", "yc", "xc"],
                        varName = "buoyancy")
