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
    qvDataWriter = DataWriter(outputPath = f"{config.qvBuoyancyPath}{caseName}/")
    thDataWriter = DataWriter(outputPath = f"{config.thBuoyancyPath}{caseName}/")
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)
    for tIdx in timeArange:
        print(f"========== {tIdx:06d} ==========")
        thData = vvmLoader.loadThermoDynamic(tIdx)
        th = np.array(thData["th"])
        qv = np.array(thData["qv"])
        thBar = np.tile(np.mean(th, axis=(2, 3), keepdims=True), reps=(1, 1, len(yc), len(xc)))
        qvBuoyancy = 9.81 * (0.61 * qv)
        thBuoyancy = 9.81 * ((th - thBar) / thBar)
        qvDataWriter.toNC(f"buoyancy-{tIdx:06d}.nc", qvBuoyancy, 
                        coords = {'time': np.ones(shape=(1,)), 'zc': zc, 'yc': yc, 'xc': xc},
                        dims = ["time", "zc", "yc", "xc"],
                        varName = "buoyancy")
        thDataWriter.toNC(f"buoyancy-{tIdx:06d}.nc", thBuoyancy, 
                        coords = {'time': np.ones(shape=(1,)), 'zc': zc, 'yc': yc, 'xc': xc},
                        dims = ["time", "zc", "yc", "xc"],
                        varName = "buoyancy")
