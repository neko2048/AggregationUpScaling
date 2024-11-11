import os
import glob

targetPath = "/data/C.shaoyu/mog/simulation/"
targetExpName = ["rcemip_mg"]
targetExpName += [f"rcemip_mg_{x}" for x in range(1, 2)]
# note that the link files follow the first targetExpName
expName = targetExpName[0]
linkPath = f"/data/atmenu10246/VVM/DATA/{expName}/archive/"
targetEndTimeStep = [382, 305]
#                   [442, 108, 308, 302, 397, 405, 124, 133, 153, 39]
#                    0        2        3        4        5        6        7        8        9        10
# targetEndTimeStep: 0 - 442, 1 - 108, 1 - 308, 1 - 302, 1 - 397, 1 - 405, 1 - 124, 1 - 133, 1 - 153,  1 - 39

dataTypes = {"Thermodynamic": ".L.Thermodynamic", 
             "Dynamic": ".L.Dynamic", 
             "Radiation": ".L.Radiation", 
             "Surface": ".C.Surface"}

if not os.path.exists(outputPath):
    print("Path is not exist, created")
    os.makedirs(linkPath)

# Link fort.98
targetDataPath = f"{targetPath}{targetExpName[0]}/fort.98"
linkDataPath = f"{linkPath[:-9]}/fort.98"
os.symlink(targetDataPath, linkDataPath)

# Link all nc files
mPointer = 0
i = 0
continueI = 0
while mPointer <= len(targetExpName) - 1:
    if i == targetEndTimeStep[mPointer]+1: 
        mPointer += 1
        i = 1
        if mPointer == len(targetExpName): break
    for dataType in dataTypes.keys():
        targetDataPath = f"{targetPath}{targetExpName[mPointer]}/archive/{targetExpName[mPointer]}{dataTypes[dataType]}-{i:06d}.nc"
        linkDataPath = f"{linkPath}{expName}{dataTypes[dataType]}-{continueI:06d}.nc"
        os.symlink(targetDataPath, linkDataPath)

    i += 1
    continueI += 1
