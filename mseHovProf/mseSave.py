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

def getCmapAndNorm(cmapName, levels, extend="neither"):
    cmap = plt.get_cmap(cmapName)
    if extend == "both":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels)+1)],
                         extend=extend)
    elif extend == "max" or extend == "min":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels))],
                         extend=extend)
    elif extend == "neither":
        cmap, norm = from_levels_and_colors(
                         levels=levels,
                         colors=[cmap(i/len(levels)) for i in range(len(levels)-1)])
    return cmap, norm


if __name__ == "__main__":
    iniTimeIdx, endTimeIdx, caseIdx, std = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), round(float(sys.argv[4]), 1)
    caseName = config.caseNames[caseIdx]
    if endTimeIdx > int(config.lastTimeStep[caseName]): endTimeIdx = int(config.lastTimeStep[caseName]) + 1
    vvmLoader = VVMLoader(dataDir=f"{config.vvmPath}{caseName}/", subName=caseName)
    thData = vvmLoader.loadThermoDynamic(0)
    xc, yc, zc = np.array(thData["xc"]), np.array(thData["yc"]), np.array(thData["zc"])
    rho3D = vvmLoader.loadRHO()[:-1][:, np.newaxis, np.newaxis]
    piBar = vvmLoader.loadPIBAR()[:-1][:, np.newaxis, np.newaxis]
    zc3D = zc[:, np.newaxis, np.newaxis]
    timeArange = np.arange(iniTimeIdx, endTimeIdx, 1)

    ttRecord = np.zeros(shape=(len(timeArange), len(zc)))
    ppRecord = np.zeros(shape=(len(timeArange), len(zc))) 
    tpRecord = np.zeros(shape=(len(timeArange), len(zc)))
    ptRecord = np.zeros(shape=(len(timeArange), len(zc))) 
    levels = np.sort([-0.001, -0.005, -0.01, -0.05, -0.1, 0, 0.001, 0.005, 0.01, 0.05, 0.1])
    cmap, norm = getCmapAndNorm("coolwarm", 
                                levels=levels, 
                                extend="both")

    for i, tIdx in enumerate(timeArange):
        print(f"========== {tIdx:06d} ==========")
        thData = vvmLoader.loadThermoDynamic(tIdx)
        mse = np.array(nc.Dataset(f"{config.msePath}{caseName}/mse-{tIdx:06d}.nc")["mse"][0]) / 1004
        #getMSE(temperature, zc3D, qv) / 1004
        w = np.array(vvmLoader.loadDynamic(tIdx)["w"][0])
        w = (np.roll(w, 1, axis=0) + w) / 2
        w = np.mean(w, axis=(1), keepdims=True)
        var = mse
        var = np.mean(var, axis=(1), keepdims=True)
        
        varTild = np.array(nc.Dataset(f"{config.convolveMsePath}{caseName}/gaussian-{std:.1f}/mse-{tIdx:06d}.nc")["mse"][0]) / 1004
        wTild = np.array(nc.Dataset(f"{config.convolveWPath}{caseName}/gaussian-{std:.1f}/w-{tIdx:06d}.nc")["w"][0])
        varTild, varPert = getTildeAnomalyAndPerturb(var, varTild)
        wTild, wPert = getTildeAnomalyAndPerturb(w, wTild)

        ttRatio = np.mean(rho3D * (varTild * wTild), axis=(1, 2))
        ttRecord[i] = ttRatio
        ppRatio = np.mean(rho3D * (varPert * wPert), axis=(1, 2))
        ppRecord[i] = ppRatio
        tpRatio = np.mean(rho3D * (varTild * wPert), axis=(1, 2)) 
        tpRecord[i] = tpRatio
        ptRatio = np.mean(rho3D * (varPert * wTild), axis=(1, 2))
        ptRecord[i] = ptRatio
    

    #ttRecord[np.isnan(ttRecord)] = 0
    #ppRecord[np.isnan(ppRecord)] = 0
    #tpRecord[np.isnan(tpRecord)] = 0
    #ptRecord[np.isnan(ptRecord)] = 0
    np.save(f"{config.mseHovProfPath}{caseName}/mse-ttRecord-{std}.npy", ttRecord)
    np.save(f"{config.mseHovProfPath}{caseName}/mse-ppRecord-{std}.npy", ppRecord)
    np.save(f"{config.mseHovProfPath}{caseName}/mse-tpRecord-{std}.npy", tpRecord)
    np.save(f"{config.mseHovProfPath}{caseName}/mse-ptRecord-{std}.npy", ptRecord)
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
