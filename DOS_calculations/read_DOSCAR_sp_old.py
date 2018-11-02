import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

poscar = open("POSCAR", "r")

rows = []

for line in poscar:
    rows.append(line)

# Get information on composition in
elements = dict(zip(rows[5].split(), rows[6].split()))

poscar.close()

doscar = open("DOSCAR", "r")

rows = []

for line in doscar:
    rows.append(line)

#Extract information

NIONS = int(rows[0].split()[0]) # extracting number of ions
ENMAX = float(rows[5].split()[0]) # extracting maximum energy
ENMIN = float(rows[5].split()[1]) # extracting minimum energy
NEDOS = int(rows[5].split()[2]) # extracting NEDOS from the file
ENFERMI = float(rows[5].split()[3]) # extracting the Fermi level


array = []
for i in range(6, NEDOS+6):
    array.append(rows[i].split())

# Create DataFrame to get DOS
DOS_df = pd.DataFrame(array, columns=["E", "DOS_up", "DOS_down", "int_DOS_up", "int_DOS_down"])
DOS_df = DOS_df.astype(float)
DOS_df = DOS_df.set_index("E")
DOS_df["DOS_down"] = DOS_df["DOS_down"].apply(lambda x: x*(-1))
DOS_df["int_DOS_down"] = DOS_df["int_DOS_down"].apply(lambda x: x*(-1))


# Get PDOS

array = []

for i in range(1, NIONS):
    for j in range(i*NEDOS+6+i, i*NEDOS+NEDOS+6+i):
        array.append(rows[j].split())

PDOS_df = pd.DataFrame(array, columns=["E", "s_DOS_up", "s_DOS_down", "p_DOS_up", "p_DOS_down", "d_DOS_up", "d_DOS_down"])
PDOS_df = PDOS_df.astype(float)
PDOS_df[["s_DOS_down", "p_DOS_down", "d_DOS_down"]] = PDOS_df[["s_DOS_down", "p_DOS_down", "d_DOS_down"]].apply(lambda x: x*(-1))

print(PDOS_df["s_DOS_down"])


PDOS_df["element"] = "NaN"


# Label the atoms
total = 0
for element in elements:
    index = int(elements[element])*NEDOS
    PDOS_df["element"][total:index+total] = element

    total += index


df_list = []
for element in elements:
    df_list.append(PDOS_df.loc[PDOS_df["element"] == element].groupby("E").sum())


df_list[2].plot(xlim=[-10,10], ylim=[-20,20])
plt.show()

doscar.close()
