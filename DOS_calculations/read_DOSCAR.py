import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

poscar = open("POSCAR", "r")

rows = []

for line in poscar:
    rows.append(line)

# Get information on composition in
elements_dict = dict(zip(rows[5].split(), rows[6].split()))
elements_list = rows[5].split()

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
DOS_df = pd.DataFrame(array, columns=["E", "DOS", "int_DOS"])
DOS_df = DOS_df.astype(float)


# Adjust energy scale to be aligned to Fermi level and set E to be index
DOS_df["E"] = DOS_df["E"].apply(lambda x: x-ENFERMI)
DOS_df = DOS_df.set_index("E")



# Get PDOS

array = []

for i in range(1, NIONS):
    for j in range(i*NEDOS+6+i, i*NEDOS+NEDOS+6+i):
        array.append(rows[j].split())

PDOS_df = pd.DataFrame(array, columns=["E", "s", "p_y", "p_z", "p_x", "d_xy", "d_yz", "d_z2-r2", "d_xz", "d_x2-y2"])
PDOS_df = PDOS_df.astype(float)

# Adjust energy scale to be 0 at Fermi level
PDOS_df["E"] = PDOS_df["E"].apply(lambda x: x-ENFERMI)

PDOS_df["element"] = "NaN"

# Label all the atoms as the correct type according to POSCAR definition
total = 0
for element in elements_list:
    index = int(elements_dict[element])*NEDOS
    PDOS_df["element"][total:index+total] = element

    total += index




## Sum all atoms of same element into single value
df_list = []
df_list_combined = []

for element in elements_list:
    df_list.append(PDOS_df.loc[PDOS_df["element"] == element].groupby("E").sum())

for df in df_list:
    df["total"] = df[["s", "p_x", "p_y", "p_z", "d_xy", "d_yz", "d_z2-r2", "d_xz", "d_x2-y2"]].sum(axis=1)

# Combine all orbitals of one type into single value
for element in df_list:
    df = pd.DataFrame(element)

    df["p"] = element[["p_x", "p_y", "p_z"]].sum(axis=1)
    df["d"] = element[["d_xy", "d_yz", "d_z2-r2", "d_xz", "d_x2-y2"]].sum(axis=1)

    df.drop(columns=["p_x", "p_y", "p_z", "d_xy", "d_yz", "d_z2-r2", "d_xz", "d_x2-y2"], inplace=True)
    df_list_combined.append(df)



# Plot separate plots for each element
for i in range(len(elements_list)):
    ax = df_list_combined[i][["s", "p", "d"]].plot(xlim=[-ENMAX+ENFERMI,ENMAX-ENFERMI], ylim=[-5,20])
    ax.set_title(elements_list[i] + " - Density of States")
    plt.show()

# Plot one plot with total from each element
temp_df = pd.DataFrame(columns=elements_list)

for i in range(len(elements_list)):
    temp_df[elements_list[i]] = df_list_combined[i]["total"]
    ax2 = temp_df[elements_list[i]].plot(xlim=[-ENMAX+ENFERMI,ENMAX-ENFERMI], ylim=[-5,20], legend=True)


ax2.set_title("Total Density of States")
plt.show()

doscar.close()
