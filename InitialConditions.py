# InitialConditions.py
# This code creates the initial conditions for numerical simulations using SI3D.
# Copy Right Sergio A. Valbuena 2021
# UC Davis - TERC
# February 2021

# For a CTD profile, it is recommended that the user modifies the code within the if statement for TempProf = 'variable'. Where one can load the CTD profile and assign to the corresponding variables z_CTD and T_CTD to run the code.

# Library Import
import sys
import os
import datetime
import numpy as np
import pandas as pd
import datetime as Dt
import matplotlib.pyplot as plt
import scipy.io as spio

# Import functions
root = "C://Users/"
user = "SV"
func = "/Documents/Github/si3dInputs/"
FuncPath = root + user + func
sys.path.append(FuncPath)
from si3dInputs import initCond4si3d
del root, user, func, FuncPath

# --------------------- User variables declaration ----------------------------
root = "S:/"
PathProject = "si3D/"
# Chose the name of folder for the simulation
SimFolder = 'L10_H100_W15_N10_f40'
# Chose path to save bathymetry file
PathSave = root+PathProject+SimFolder
# Specify the name of the Lake
LakeName = 'Stratification 1 for canonical basin'
# Specify the start date of the simulation
SimStartDate = '2018-05-26 00:00:00'
TimeZone = 'America/Los_Angeles'
# Define depth of lake
H = 100 #[m] deep
# Chosse number of tracers
NTracers = 0
# Chose the type of thickness in layers and the profile of temperature in the vertical direction. Options are 'constant' and 'variable'
DeltaZ = 'constant'
TempProf = 'variable'
# DeltaZ = 'variable'
# TempProf = 'variable'

if DeltaZ == 'constant':
    dz = 1 #[m] constant thickness of layers
elif DeltaZ == 'variable':
    # Chose the layer thickness method. Current options are: 'sbconc' and 'exp' where the first concentrates the specified minimum thickess at surface and bottom, and the latter has the finest layers at the surface.
    spacingMethod = 'exp'
    # Initial dx of top and bottom layers. Where the bottom is only used if sbconc method is used.
    dz0s = 0.1
    dz0b = 0.1
    # Specify constant spacing as layer thickness increases
    dzxs = 1.03
    dzxb = 1.03
    # H/n will be the depth at which the thickness of layers start to decrease until reaching the bottom thicness of dz0b
    n = 3
if TempProf == 'constant':
    Tc = 15 #[C] Temperature of whole water column
elif TempProf == 'variable':
    PathFile = "G:/My Drive/Lake_Tahoe/Projects/Upwelling_3DModel/CTD_data/Processed_0"
    FileName = 'LakeTahoe_CTD.csv'
    os.chdir(PathFile)
    data = pd.read_csv(FileName)
    z_CTD = data['depth'].to_numpy()
    T_CTD = data['T'].to_numpy()
    del data
    if np.max(z_CTD) < H/2:
        z_CTD = np.append(z_CTD,(H/2,H))
        T_CTD = np.append(T_CTD,(T_CTD[-1],T_CTD[-1]))
    elif np.max(z_CTD) > H/2 and np.max(z_CTD) < H:
        z_CTD = np.append(z_CTD,H)
        T_CTD = np.append(T_CTD,T_CTD[-1])

plt.plot(T_CTD,-z_CTD)
# -------------- Beginning of code to create initial condition file --------------------
if DeltaZ == 'constant':
    if TempProf == 'constant':
        [T,z] = initCond4si3d(LakeName,SimStartDate,DeltaZ,TempProf,PathSave,NTracers,H,dz,Tc)
    elif TempProf == 'variable':
        [T,z] = initCond4si3d(LakeName,SimStartDate,DeltaZ,TempProf,PathSave,NTracers,H,dz,z_CTD,T_CTD)
elif DeltaZ == 'variable':
    if TempProf == 'constant':
        [T,z] = initCond4si3d(LakeName,SimStartDate,DeltaZ,TempProf,PathSave,NTracers,H,Tc,spacingMethod,dz0s,dz0b,dzxs,dzxb,n)
    elif TempProf == 'variable':
        [T,z] = initCond4si3d(LakeName,SimStartDate,DeltaZ,TempProf,PathSave,NTracers,H,z_CTD,T_CTD,spacingMethod,dz0s,dz0b,dzxs,dzxb,n)
plt.show()
