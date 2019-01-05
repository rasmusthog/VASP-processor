import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None


## Here read_DOSCAR_sp.py and read_DOSCAR.py will be refactored as functions

def load_doscar(doscar_path):
    """ Loads POSCAR file into an array of lists """

    # Open DOSCAR-file
    doscar = open(doscar_path)

    # Initialise empty list 'rows'
    doscar_rows = []

    # Read each line into the array 'rows'
    for line in doscar:
        doscar_rows.append(line)

    # Close DOSCAR-file
    doscar.close()


    # Extract information from POSCAR

    params = {
            "NIONS": int(doscar_rows[0].split()[0]), # extracting number of ions
            "ENMAX": float(doscar_rows[5].split()[0]), # extracting maximum energy
            "ENMIN": float(doscar_rows[5].split()[1]), # extracting minimum energy
            "NEDOS": int(doscar_rows[5].split()[2]), # extracting NEDOS (number of discreet points energy is calculated for) from the file
            "ENFERMI": float(doscar_rows[5].split()[3])} # extracting the Fermi level


    return doscar_rows, params



def get_DOS(doscar, params, spin_polarised=True, PDOS=True):
    # Initalise empty list 'array'

    array = []

    DOS_spin_polarised_cols = ["E", "DOS", "DOS_down", "int_DOS_up", "int_DOS_down"]
    DOS_spin_polarised_down = ["DOS_down", "int_DOS_down"]
    DOS_non_spin_polarised_cols = ["E", "DOS" "int_DOS"]

    PDOS_spin_polarised_cols = ["E", "s_up", "s_down", "p_y_up", "p_y_down", "p_z_up", "p_z_down", "p_x_up", "p_x_down", "d_xy_up", "d_xy_down", "d_yz_up", "d_yz_down", "d_z2-r2_up", "d_z2-r2_down", "d_xz_up", "d_xz_down", "d_x2-y2_up", "d_x2-y2_down"]
    PDOS_spin_polarised_down = ["s_down", "p_y_down", "p_z_down", "p_x_down", "d_xy_down", "d_yz_down", "d_z2-r2_down", "d_xz_down", "d_x2-y2_down"]
    PDOS_non_spin_polarised_cols = ["E", "s", "p", "d"]

    # Create DataFrame and add list 'array' as rows
    if PDOS == True:

        # Loop to add all PDOS for each atom to array. Outer loop loops NIONS times to get from all atoms,
        # inner loop loops NEDOS times to get all entries per atom.
        for i in range(1, params["NIONS"]):
            for j in range(i*params["NEDOS"]+6+i, i*params["NEDOS"]+params["NEDOS"]+6+i):
                array.append(doscar[j].split())


        if spin_polarised == True:
            DOS_df = pd.DataFrame(array, columns=PDOS_spin_polarised_cols) # define columns according to VASP wiki
            DOS_df = DOS_df.astype(float) # convert all numbers from string to float
            DOS_df[PDOS_spin_polarised_down] = DOS_df[PDOS_spin_polarised_down].apply(lambda x: x*(-1)) # multiply down spin channel by negative 1 for plotting reasons

            # Adjust energy scale to be aligned to Fermi level and set E to be index
            DOS_df["E"] = DOS_df["E"].apply(lambda x: x-params["ENFERMI"])

        elif spin_polarised == False:
            DOS_df = pd.DataFrame(array, columns=PDOS_non_spin_polarised_cols) # define columns according to VASP wiki
            DOS_df = DOS_df.astype(float) # convert all numbers from string to float

            # Adjust energy scale to be aligned to Fermi level and set E to be index
            DOS_df["E"] = DOS_df["E"].apply(lambda x: x-params["ENFERMI"])


    elif PDOS == False:
        # Loop to fetch all the DOS. Loops from first line (6) and NEDOS lines down.
        for i in range(6, params["NEDOS"]+6):
            array.append(doscar[i].split())

        if spin_polarised == True:
            DOS_df = pd.DataFrame(array, columns=DOS_spin_polarised_cols) # define columns according to VASP wiki
            DOS_df = DOS_df.astype(float) # convert all numbers from string to float
            DOS_df[DOS_spin_polarised_down] = DOS_df[DOS_spin_polarised_down].apply(lambda x: x*(-1)) # multiply down spin channel by negative 1 for plotting reasons

            # Adjust energy scale to be aligned to Fermi level and set E to be index
            DOS_df["E"] = DOS_df["E"].apply(lambda x: x-params["ENFERMI"])
            DOS_df = DOS_df.set_index("E")

        elif spin_polarised == False:
            DOS_df = pd.DataFrame(array, columns=DOS_non_spin_polarised_cols) # define columns according to VASP wiki
            DOS_df = DOS_df.astype(float) # convert all numbers from string to float

            # Adjust energy scale to be aligned to Fermi level and set E to be index
            DOS_df["E"] = DOS_df["E"].apply(lambda x: x-params["ENFERMI"])
            DOS_df = DOS_df.set_index("E")

        else: return null

    else: return null

    return DOS_df

def plot_dos(dos_df, elements_list, option="total", spin_polarised=True):
    """ Plot DOS for elements or orbitals.

    Keyword arguments:
    dos_df = dataframe containing DOS-data
    elements_list = list of elements in the dataframe (is this necessary?)
    option = options for plotting. Choices: "total", "orbital",

    """


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


def plot_dos(dos_df, spin_polarised=False):

    # Open POSCAR file and extract dictionary and list of elements (type, order and number)
    poscar = pc.load_poscar(poscar_path)
    elements_dict, elements_list = pc.get_elements(poscar)

    return null
