userName = "atmenu10246"
vvmPath = f"/data/{userName}/VVM/DATA/"
caseNames = list([
             "HW22_P3_1p5K_0p5m",         # 00: NonAgg
             "HW22_P3_1p5K_1p0m",         # 01: HafAgg
             "HW22_P3_1p5K_2p0m",         # 02: Agg
             "HW22_P3_0p5K_2p0m",         # 03: Agg
             "HW22_P3_0p5K_3p0m",         # 04: Agg
             "HW22_P3_1p0K_1p0m",         # 05: Agg
             "HW22_P3_1p0K_2p0m",         # 06: Agg
             "HW22_P3_1p0K_3p0m",         # 07: Agg
             "HW22_P3_2p0K_0p5m",         # 08:
             "HW22_P3_3p0K_0p5m",         # 09:
             "HW22_P3_3p0K_1p0m",         # 10:
             "HW22_LIN_1p5K_2p0m",        # 11
             "HW22_LIN_1p5K_3p0m",        # 12
             "HW22_LIN_3p0K_1p0m",        # 13
             "HW22_LIN_3p0K_2p0m",        # 14
             "RCE_300K_d6144r3km_2p5_e2", # 15
             "RCE_300K_d6144r3km_e2",     # 16
             "rcemip_mg"                  # 17
             ])

caseNameMapTitles = dict({
             "HW22_P3_1p5K_0p5m": "Non-Aggregated",
             "HW22_P3_1p5K_1p0m": "H01",
             "HW22_P3_1p5K_2p0m": "Aggregated",
             "HW22_P3_0p5K_2p0m": "P3-0.5K-2.0m",
             "HW22_P3_0p5K_3p0m": "P3-0.5K-3.0m",
             "HW22_P3_1p0K_1p0m": "P3-1.0K-1.0m",
             "HW22_P3_1p0K_2p0m": "P3-1.0K-2.0m",
             "HW22_P3_1p0K_3p0m": "P3-1.0K-3.0m",
             "HW22_P3_2p0K_0p5m": "P3-2.0K-0.5m",
             "HW22_P3_3p0K_0p5m": "P3-3.0K-0.5m",
             "HW22_P3_3p0K_1p0m": "P3-3.0K-1.0m",
             "HW22_LIN_1p5K_2p0m": "LIN-1.5K-2.0m",
             "HW22_LIN_1p5K_3p0m": "LIN-1.5K-3.0m",
             "HW22_LIN_3p0K_1p0m": "LIN-3.0K-1.0m",
             "HW22_LIN_3p0K_2p0m": "LIN-3.0K-2.0m",
             "RCE_300K_d6144r3km_2p5_e2": "RCE_300K",
             "RCE_300K_d6144r3km_e2": "RCEMIP1"
             })

lastTimeStep = {
             "HW22_P3_1p5K_0p5m" :        904,
             "HW22_P3_1p5K_1p0m" :       1112,
             "HW22_P3_1p5K_2p0m" :       1200,
             "HW22_P3_0p5K_2p0m" :        751,
             "HW22_P3_0p5K_3p0m" :        663,
             "HW22_P3_1p0K_1p0m" :       1154,
             "HW22_P3_1p0K_2p0m" :       1176,
             "HW22_P3_1p0K_3p0m" :       1200,
             "HW22_P3_2p0K_0p5m" :       1179,
             "HW22_P3_3p0K_0p5m" :       1138,
             "HW22_P3_3p0K_1p0m" :        491,
             "HW22_LIN_1p5K_2p0m":       1200,
             "HW22_LIN_1p5K_3p0m":       1200,
             "HW22_LIN_3p0K_1p0m":       1200,
             "HW22_LIN_3p0K_2p0m":       1200,
             "HW22_LIN_3p0K_2p0m":       1200,
             "RCE_300K_d6144r3km_2p5_e2": 353,
             "RCE_300K_d6144r3km_e2":    2411,
}
minPerTimeIdx = 60

buoyancyPath          = f"/data/{userName}/scaleTransit/dat/buoyancy/"
laplacePath           = f"/data/{userName}/scaleTransit/dat/laplace/"
vertAccePath          = f"/data/{userName}/scaleTransit/dat/vertAcce/"

qvBuoyancyPath        = f"/data/{userName}/scaleTransit/dat/qvBuoyancy/"
qvLaplacePath         = f"/data/{userName}/scaleTransit/dat/qvLaplace/"
qvVertAccePath        = f"/data/{userName}/scaleTransit/dat/qvVertAcce/"

thBuoyancyPath        = f"/data/{userName}/scaleTransit/dat/thBuoyancy/"
thLaplacePath         = f"/data/{userName}/scaleTransit/dat/thLaplace/"
thVertAccePath        = f"/data/{userName}/scaleTransit/dat/thVertAcce/"

msePath               = f"/data/{userName}/scaleTransit/dat/mse/"
convolveMsePath       = f"/data/{userName}/scaleTransit/dat/convolveMse/"
mseHovProfPath        = f"/data/{userName}/scaleTransit/dat/mseHovProfiles/"
convolveBuoyancyPath  = f"/data/{userName}/scaleTransit/dat/convolveBuoyancy/"

convolveWPath         = f"/data/{userName}/scaleTransit/dat/convolveW/"

perturbBuoyancyPath   = f"/data/{userName}/scaleTransit/dat/perturbBuoyancy/"
tildeBuoyancyPath     = f"/data/{userName}/scaleTransit/dat/tildeBuoyancy/"
perturbQvBuoyancyPath = f"/data/{userName}/scaleTransit/dat/perturbQvBuoyancy/"
tildeQvBuoyancyPath   = f"/data/{userName}/scaleTransit/dat/tildeQvBuoyancy/"
perturbThBuoyancyPath = f"/data/{userName}/scaleTransit/dat/perturbThBuoyancy/"
tildeThBuoyancyPath   = f"/data/{userName}/scaleTransit/dat/tildeThBuoyancy/"

perturbLaplacePath    = f"/data/{userName}/scaleTransit/dat/perturbLaplace/"
tildeLaplacePath      = f"/data/{userName}/scaleTransit/dat/tildeLaplace/"
perturbQvLaplacePath  = f"/data/{userName}/scaleTransit/dat/perturbQvLaplace/"
tildeQvLaplacePath    = f"/data/{userName}/scaleTransit/dat/tildeQvLaplace/"
perturbThLaplacePath  = f"/data/{userName}/scaleTransit/dat/perturbThLaplace/"
tildeThLaplacePath    = f"/data/{userName}/scaleTransit/dat/tildeThLaplace/"

perturbVertAccePath   = f"/data/{userName}/scaleTransit/dat/perturbVertAcce/"
tildeVertAccePath     = f"/data/{userName}/scaleTransit/dat/tildeVertAcce/"
perturbQvVertAccePath = f"/data/{userName}/scaleTransit/dat/perturbQvVertAcce/"
tildeQvVertAccePath   = f"/data/{userName}/scaleTransit/dat/tildeQvVertAcce/"
perturbThVertAccePath = f"/data/{userName}/scaleTransit/dat/perturbThVertAcce/"
tildeThVertAccePath   = f"/data/{userName}/scaleTransit/dat/tildeThVertAcce/"
