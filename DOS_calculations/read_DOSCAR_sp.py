import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None


## GET ELEMENT ORDER AND NUMBER OF ELEMENTS FROM POSCAR

# Open POSCAR file
poscar = open("DOS_calculations/POSCAR", "r")

# Initialise empty list 'rows'
rows = []

# Add POSCAR-file line by line into list 'rows'
for line in poscar:
    rows.append(line)

# Get information on composition (atoms and number of atoms) from POSCAR
elements_dict = dict(zip(rows[5].split(), rows[6].split())) # Dictionary to map element and number of elements
elements_list = rows[5].split() # List to retain order

# Close POSCAR-file
poscar.close()

## GET DOS FROM DOSCAR

# Open DOSCAR-file
doscar = open("DOS_calculations/DOSCAR", "r")

# Initialise empty list 'rows'
rows = []

# Read each line into the array 'rows'
for line in doscar:
    rows.append(line)

# Close DOSCAR-file
doscar.close()


# Extract information from POSCAR

NIONS = int(rows[0].split()[0]) # extracting number of ions
ENMAX = float(rows[5].split()[0]) # extracting maximum energy
ENMIN = float(rows[5].split()[1]) # extracting minimum energy
NEDOS = int(rows[5].split()[2]) # extracting NEDOS (number of discreet points energy is calculated for) from the file
ENFERMI = float(rows[5].split()[3]) # extracting the Fermi level


# Initalise empty list 'array'
array = []

# Loop to fetch all the partial DOS. Loops from first line (6) and NEDOS lines down.
for i in range(6, NEDOS+6):
    array.append(rows[i].split())

# Create DataFrame and add list 'array' as rows
DOS_df = pd.DataFrame(array, columns=["E", "DOS", "DOS_down", "int_DOS_up", "int_DOS_down"]) # define columns according to VASP wiki
DOS_df = DOS_df.astype(float) # convert all numbers from string to float
DOS_df[["DOS_down", "int_DOS_down"]] = DOS_df[["DOS_down", "int_DOS_down"]].apply(lambda x: x*(-1)) # multiply down spin channel by negative 1 for plotting reasons


# Adjust energy scale to be aligned to Fermi level and set E to be index
DOS_df["E"] = DOS_df["E"].apply(lambda x: x-ENFERMI)
DOS_df = DOS_df.set_index("E")



###  GET PDOS FOR EACH ATOM FROM DOSCAR

# Initialise empty 'array'
array = []

# Loop to add all PDOS for each atom to array. Outer loop loops NIONS times to get from all atoms,
# inner loop loops NEDOS times to get all entries per atom.
for i in range(1, NIONS):
    for j in range(i*NEDOS+6+i, i*NEDOS+NEDOS+6+i):
        array.append(rows[j].split())

# Create dataframe of array that contains PDOS for all atoms from 'array'
PDOS_df = pd.DataFrame(array, columns=["E", "s_up", "s_down", "p_y_up", "p_y_down", "p_z_up", "p_z_down", "p_x_up", "p_x_down", "d_xy_up", "d_xy_down", "d_yz_up", "d_yz_down", "d_z2-r2_up", "d_z2-r2_down", "d_xz_up", "d_xz_down", "d_x2-y2_up", "d_x2-y2_down"])

# Convert all numbers from string to float
PDOS_df = PDOS_df.astype(float)

# Multiply all down spin channel with -1 for plotting reasons.
PDOS_df[["s_down", "p_y_down", "p_z_down", "p_x_down", "d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"]] = PDOS_df[["s_down", "p_y_down", "p_z_down", "p_x_down", "d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"]].apply(lambda x: x*(-1))

# Adjust energy scale to be 0 at Fermi level
PDOS_df["E"] = PDOS_df["E"].apply(lambda x: x-ENFERMI)

## SUM 'PDOS_df' FOR ALL SIMILAR ATOMS AND FOR TYPE OF ORBITAL

# Create new column 'elements' and initialise with NaN
PDOS_df["element"] = "NaN"

# Loop over elements_list to get the correct order. Fetch number of atoms for that element from
# the element list
start = 0
for element in elements_list:
    index = int(elements_dict[element])*NEDOS
    PDOS_df["element"][start:index+start] = element

    start += index


## Sum all atoms of same element into single value
df_list = []
df_list_combined = []


# Extract dataframes with only data from each element and add to 'df_list'
for element in elements_list:
    df_list.append(PDOS_df.loc[PDOS_df["element"] == element].groupby("E").sum())

# Add columns for total DOS for up and down channels
for df in df_list:
    df["total_up"] = df[["s_up", "p_x_up", "p_y_up", "p_z_up", "d_xy_up", "d_yz_up", "d_z2-r2_up", "d_xz_up", "d_x2-y2_up"]].sum(axis=1)
    df["total_down"] = df[["s_down", "p_x_down", "p_y_down", "p_z_down", "d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"]].sum(axis=1)


# Combine all orbitals of one type into single value
for element in df_list:
    df = pd.DataFrame(element)

    df["p_up"] = element[["p_x_up", "p_y_up", "p_z_up"]].sum(axis=1)
    df["p_down"] = element[["p_x_down", "p_y_down", "p_z_down"]].sum(axis=1)

    df["d_up"] = element[["d_xy_up", "d_yz_up", "d_z2-r2_up", "d_xz_up", "d_x2-y2_up"]].sum(axis=1)
    df["d_down"] = element[["d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"]].sum(axis=1)

    df.drop(columns=["p_x_up", "p_y_up", "p_z_up", "d_xy_up", "d_yz_up", "d_z2-r2_up", "d_xz_up", "d_x2-y2_up",
    "p_x_down", "p_y_down", "p_z_down", "d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"], inplace=True)
    df_list_combined.append(df)



# Plot separate plots for each element
for i in range(len(elements_list)):
    ax = df_list_combined[i][["s_up", "s_down", "p_up", "p_down", "d_up", "d_down"]].plot(xlim=[-ENMAX+ENFERMI,ENMAX-ENFERMI], ylim=[-20,20])
    ax.set_title(elements_list[i] + " - Density of States")
    plt.show()

# Plot one plot with total from each element

# Initalise empty array 'elements_list_sp' to make column names for the below dataframe 'temp_df'
elements_list_sp = []
for element in elements_list:
    temp1 = element + "_up"
    temp2 = element + "_down"
    elements_list_sp.append(temp1)
    elements_list_sp.append(temp2)

# Create a new dataframe with column names from 'elements_list_sp'
temp_df = pd.DataFrame(columns=elements_list_sp)


# Loop through 'elements_list', and add the total DOS for up and down spin channels to their
# respective columns in 'temp_df'. (i*2) because it loops through 'elements_list',
# but gets the names from 'elements_list_sp'
for i in range(len(elements_list)):
    temp_df[elements_list_sp[(i*2)]] = df_list_combined[i]["total_up"]
    temp_df[elements_list_sp[(i*2)+1]] = df_list_combined[i]["total_down"]
    ax2 = temp_df[elements_list_sp[(i*2)]].plot(xlim=[-ENMAX+ENFERMI,ENMAX-ENFERMI], ylim=[-20,20], legend=True)
    temp_df[elements_list_sp[(i*2)+1]].plot(xlim=[-ENMAX+ENFERMI,ENMAX-ENFERMI], ylim=[-20,20], legend=True, ax=ax2)


ax2.set_title("Total Density of States")
plt.show()
