# InitialConditions.py
# This code creates the initial conditions for numerical simulations using SI3D.
# Copy Right Sergio A. Valbuena 2021
# UC Davis - TERC
# August 2021

# For a CTD profile, it is recommended that the user modifies the code within the if statement for TempProf == 'variable'. Where one can load the CTD profile and assign to the corresponding variables z_CTD and T_CTD to run the code.

# Library Import
import sys
import os
# import datetime
import numpy as np
# import pandas as pd
# import datetime as Dt
import matplotlib.pyplot as plt
# import scipy.io as spio
import platform

# Import functions
if platform.system() == 'Windows':
    root = "C://Users/"
    user = os.getlogin()
else:
    root = ''
    user = os.getlogin()

func = "/Documents/Github/si3dInputs/pythonlibrary/"
FuncPath = root + user + func
sys.path.append(FuncPath)
from surfbc4si3d import *
from initCond4si3d import *
from bathy4si3d import *
from openbc4si3d import *
del root, user, func, FuncPath

plt.close('all')
# --------------------- User variables declaration ----------------------------
root = 'S:/si3D/'
PathProject = 'LakeMassawippi/'
# Chose the name of folder for the simulation
SimFolder = 'Lake_R70'
# Chose path to save bathymetry file
PathSave = root + PathProject + SimFolder
# Specify the name of the Lake
LakeName = 'Stratification for Lake Massawippi'
# Specify the start date of the simulation
SimStartDate = '2019-06-01 04:00:00'  # IN UTC BUT CONSIDER SIMS ARE IN LOCAL TIME
TimeZone = 'America/Toronto'
# Define depth of lake
H = 60  # [m] deep
# Choose number of tracers
NTracers = 2
# Chose the type of thickness in layers and the profile of temperature in the vertical direction. Options are 'constant' and 'variable'
DeltaZ = 'constant'
TempProf = 'constant'

if DeltaZ == 'constant':
    dz = 1  # [m] constant thickness of layers
elif DeltaZ == 'variable':
    # Chose the layer thickness method. Current options are: 'sbconc', 'surfvarBotconsta' and 'exp' where the first concentrates the specified minimum thickess at surface and bottom, and the latter has the finest layers at the surface.
    spacingMethod = 'surfvarBotconsta'
    # Initial dz of top and bottom layers. Where the bottom is only used if sbconc method is used.
    dz0s = 0.2
    dz0b = 0.5
    # Specify constant spacing as layer thickness increases
    dzxs = 1.02
    dzxb = 1.03
    # H/n will be the depth at which the thickness of layers start to decrease until reaching the bottom thicness of dz0b
    n = 3
    Hn = H / 1.5
    dzc = 2  # This value will be saved in si3d_inp.txt

if TempProf == 'constant':
    Tc = 15  # [C] Temperature of whole water column
elif TempProf == 'variable':
    PathFile = 'G:/My Drive/Lake_Tahoe/Projects/Lake_Massawippi/Data_Forcing/02_ProcessStep/01_TData'

if NTracers != 0:
    PathTr = 'G:/My Drive/Lake_Tahoe/Projects/Lake_Massawippi/Data_Forcing/02_ProcessStep/01_TData'
    z_Tr = np.reshape(np.array([0, 10, 20, 30, 40, 50, 60]), (7, 1))
    z_Tr = np.repeat(z_Tr, 2, axis=1)
    conc_Tr = np.reshape(np.array([10, 9.5, 8, 7, 6, 5, 4]), (7, 1))
    conc_Tr = 0.5 * np.repeat(conc_Tr, 2, axis=1)
    conc_Tr[:, 0] *= 2
    name_Tr = ['Hg0', 'HgII']
elif NTracers == 0:
    z_Tr = 0
    conc_Tr = 0
    name_Tr = []

# -------------- Beginning of code to create initial condition file --------------------
# To load the data and create variables for creating initial conditions file.
if TempProf == 'variable':
    StartDateS = SimStartDate[0:10] + '_' + SimStartDate[11:13] + 'Hrs'
    print(StartDateS)
    FileName = 'CTD_' + StartDateS + '.npy'
    os.chdir(PathFile)
    data = np.load(FileName, allow_pickle=True).item()
    z_CTD = data['z']
    T_CTD = data['T']
    del data
    if np.max(z_CTD) < H / 2:
        z_CTD = np.append(z_CTD, (H / 2, H))
        T_CTD = np.append(T_CTD, (T_CTD[-1], T_CTD[-1]))
    elif np.max(z_CTD) > H / 2 and np.max(z_CTD) < H:
        z_CTD = np.append(z_CTD, H)
        T_CTD = np.append(T_CTD, T_CTD[-1])
    if np.min(z_CTD) > 0.5:
        z_CTD = np.append(0, z_CTD)
        T_CTD = np.append(T_CTD[0], T_CTD)

# plt.plot(T_CTD,-z_CTD)
if DeltaZ == 'constant':
    if TempProf == 'constant':
        [T, z] = initCond4si3d(LakeName, SimStartDate, DeltaZ, TempProf, PathSave, NTracers, z_Tr=z_Tr, conc_Tr=conc_Tr, name_Tr=name_Tr, H=H, dz=dz, Tc=Tc)
    elif TempProf == 'variable':
        [T, z] = initCond4si3d(LakeName, SimStartDate, DeltaZ, TempProf, PathSave, NTracers, z_Tr=z_Tr, conc_Tr=conc_Tr, name_Tr=name_Tr, H=H, dz=dz, z_CTD=z_CTD, T_CTD=T_CTD)
elif DeltaZ == 'variable':
    if TempProf == 'constant':
        [T, z] = initCond4si3d(LakeName, SimStartDate, DeltaZ, TempProf, PathSave, NTracers, z_Tr=z_Tr, conc_Tr=conc_Tr, name_Tr=name_Tr, H=H, Tc=Tc, spacingMethod=spacingMethod, dz0s=dz0s, dz0b=dz0b, dzxs=dzxs, dzxb=dzxb, n=n, Hn=Hn, dzc=dzc)
    elif TempProf == 'variable':
        [T, z] = initCond4si3d(LakeName, SimStartDate, DeltaZ, TempProf, PathSave, NTracers, z_Tr=z_Tr, conc_Tr=conc_Tr, name_Tr=name_Tr, H=H, z_CTD=z_CTD, T_CTD=T_CTD, spacingMethod=spacingMethod, dz0s=dz0s, dz0b=dz0b, dzxs=dzxs, dzxb=dzxb, n=n, Hn=Hn, dzc=dzc)

exit()
fidinp = open('si3d_inp.txt', "r+")
lines = fidinp.readlines()

txt_idz = str(dz)

if DeltaZ == 'constant':
    while len(txt_idz) <= 13:
        txt_idz += ' '
    lines[18] = ' idz         !      ' + txt_idz + '! Cell size (m) in vertical\n'
    lines[23] = 'ibathf       !        0           ! How bathy file is read 0(General) 1(SDWSC) 2(SHR)\n'
    H = -1 * z[-1] + dz / 2
    H = np.ceil(H)
    H = str(H)
    while len(H) <= 13:
        H += ' '
    lines[14] = 'zl           !      ' + H + '!   "    "    "    (m) in vertical\n'
else:
    while len(txt_idz) <= 13:
        txt_idz += ' '
    lines[18] = ' idz         !      ' + txt_idz + '! Cell size (m) in vertical\n'
    lines[23] = 'ibathf       !        -1          ! How bathy file is read 0(General) 1(SDWSC) 2(SHR)\n'
    H = -1 * z[-1]
    H = np.ceil(H)
    H = str(H)
    while len(H) <= 13:
        H += ' '
    lines[14] = 'zl           !      ' + H + '!   "    "    "    (m) in vertical\n'
# To write the new lines into input file
fidinp = open('si3d_inp.txt', 'w+')
fidinp.writelines(lines)
fidinp.close()

plt.show()
