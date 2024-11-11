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

    #buoyRecord = np.zeros(shape=(len(timeArange), len(zc))
    mseRecord = np.zeros(shape=(len(timeArange), len(zc)))
    #thvRecord = np.zeros(shape=(len(timeArange), len(zc))) 
    #tmpRecord = np.zeros(shape=(len(timeArange), len(zc)))
    #qvRecord = np.zeros(shape=(len(timeArange), len(zc))) 

    for i, tIdx in enumerate(timeArange):
        print(f"========== {tIdx:06d} ==========")
        #thData = vvmLoader.loadThermoDynamic(tIdx)
        #th = np.array(thData["th"][0])
        #qv = np.array(thData["qv"][0])
        #qc = np.array(thData["qc"][0])
        #qi = np.array(thData["qi"][0])
        #qr = np.array(thData["qr"][0])
        #temperature = getTemperature(th, piBar)
        mse = np.array(nc.Dataset(f"{config.msePath}{caseName}/mse-{tIdx:06d}.nc")["mse"][0]) / 1004
        #getMSE(temperature, zc3D, qv) / 1004
        #thv = th * (1 + 0.61 * qv - qc - qi - qr)
        w = np.array(vvmLoader.loadDynamic(tIdx)["w"][0])
        w = (np.roll(w, 1, axis=0) + w) / 2
        
        #buoyProf = np.mean(buoyancy, axis=(1, 2))
        #buoyRecord[i] = buoyProf
        w = w - np.mean(w, axis=(1, 2), keepdims=True)
        mse = mse - np.mean(mse, axis=(1, 2), keepdims=True)
        w = np.mean(w, axis=(1), keepdims=True)
        mse = np.mean(mse, axis=(1), keepdims=True)
        mseProf = np.mean(rho3D * (mse * w), axis=(1, 2))
        mseRecord[i] = mseProf
        #temperature = temperature - np.mean(temperature, axis=(1, 2), keepdims=True)
        #tmpProf = np.mean(rho3D * (temperature * w), axis=(1, 2))
        #tmpRecord[i] = tmpProf
        #thv = thv - np.mean(thv, axis=(1, 2), keepdims=True)
        #thvProf = np.mean(rho3D * (thv * w), axis=(1, 2))
        #thvRecord[i] = thvProf
        #qv = qv - np.mean(qv, axis=(1, 2), keepdims=True)
        #qvProf  = np.mean(rho3D * (qv * w), axis=(1, 2))
        #qvRecord[i] = qvProf
    #np.save(f"./{caseName}/buoyProf.npy", buoyRecord)
    np.save(f"{config.mseHovProfPath}{caseName}/mseProf.npy", mseRecord)
    #np.save(f"./{caseName}/tmpProf.npy", tmpRecord)
    #np.save(f"./{caseName}/thvProf.npy", thvRecord)
    #np.save(f"./{caseName}/qvProf.npy",  qvRecord)
    """
    records = [ttRecord, ppRecord, tpRecord, ptRecord]
    print([x.max() for x in records])
    names = [r"$\tilde{b} \tilde{w}$", r"$b' w'$", r"$\tilde{b} w'$", r"$b' \tilde{w}$"]
    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(16, 8), sharex=True, sharey=True)
    for i in range(4):
        im=ax[i].pcolormesh(timeArange, zc/1e3, records[i].transpose(), cmap=cmap, norm=norm)
        plt.sca(ax[i])
        plt.ylabel(names[i], fontsize=20, rotation=0, labelpad=40)
        plt.yticks(fontsize=20)
        plt.ylim(0, 12.5)
        if i == 3:
            plt.xlabel("hr", fontsize=20, labelpad=0)
            plt.xticks(timeArange[::10], fontsize=20)
    fig.subplots_adjust(bottom=0.175, top=0.9)
    fig.suptitle(f"{caseName} | {int(config.minPerTimeIdx * tIdx / 60)} hr", fontsize=20)
    cbar_ax = fig.add_axes([0.125, 0.065, 0.775, 0.03])
    cb = fig.colorbar(im, cax=cbar_ax, orientation='horizontal', extend="both")
    cb.ax.set_xticks(levels)
    cb.ax.set_xticklabels([str(x) for x in levels])
    cb.ax.tick_params(labelsize=20)
    plt.savefig(f"{caseName}-mse-{std}.jpg", dpi=200)

    """
