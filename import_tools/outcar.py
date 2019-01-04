import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import poscar as pc

pd.options.mode.chained_assignment = None

def load_outcar(path):
    """ Opens OUTCAR file from 'path' and returns IOWrapper and number of lines """

    ### READ OUTCAR FILE
    # Open OUTCAR-file
    outcar = open(path, "r")

    # Count number of lines in OUTCAR-file
    number_of_lines = 0

    for line in outcar:
        number_of_lines += 1

    return outcar, number_of_lines



def get_charge_magnetisation(outcar, number_of_lines, poscar_path):

    # Open POSCAR file and extract dictionary and list of elements (type, order and number)
    poscar = pc.load_poscar(poscar_path)
    elements_dict, elements_list = pc.get_elements(poscar)

    # Count number of ions in POSCAR
    NIONS = 0

    for element in elements_dict:
        NIONS += int(elements_dict[element])

    # Reset IOWrapper to start 1000 lines above tail. (1000 is arbitrary choice to make sure it is
    # above the start, but not too much so it's not very inefficient)
    outcar.seek(number_of_lines - 1000)

    # Create list of only relevant information (after 'reached required accuracy')
    found = False
    outcar_list = []


    for line in outcar:
        # Check if 'reached required accuracy' is in line
        if 'reached required accuracy' in line:
            found = True

        # If the above line is found, start appending rows to 'outcar_list'
        if found == True:
            outcar_list.append(line)




    # Add total charge of ions to array 'total_charge'
    total_charge = []

    for i in range(10,NIONS+10):
        total_charge.append(outcar_list[i].split())


    # Add 'total_charge' to pandas dataframe charge_df
    charge_df = pd.DataFrame(total_charge, columns=["ion", "s", "p", "d", "tot"])
    charge_df.set_index("ion", inplace=True)
    charge_df = charge_df.astype(float)


    # Add element label to column 'element' in charge_df
    start = 0
    charge_df["element"] = "NaN"

    for element in elements_list:
        index = int(elements_dict[element])
        charge_df["element"][start:index+start] = element

        start += index

    ## Add magnetisation of ions to array 'magnetisation'
    magnetisation = []

    for i in range(NIONS+19,(2*NIONS)+19):
        magnetisation.append(outcar_list[i].split())

    magnetisation_df = pd.DataFrame(magnetisation, columns=["ion", "s", "p", "d", "tot"])
    magnetisation_df.set_index("ion", inplace=True)
    magnetisation_df = magnetisation_df.astype(float)

    # Add element label to column 'element' in charge_df
    start = 0
    magnetisation_df["element"] = "NaN"

    for element in elements_list:
        index = int(elements_dict[element])
        magnetisation_df["element"][start:index+start] = element

        start += index


    return charge_df, magnetisation_df






def calc_charge(charge_df, poscar_path, orbital='tot', element=0, avg=True):
    """ Returns the charge for a given element.

    Keyword arguments:
    charge_df -- pandas DataFrame containing total charge from OUTCAR
    orbital -- which orbital to get charge for. Choices: 's', 'p', 'd', 'tot'. (default='tot')
    element -- which element to get charge for. 0 = all, 1 = first element defined in POSCAR etc. (default=0)
    avg -- determines whether the average of the charge is returned (True) or total (False) (default=True)

    """

    charge = 0

    # Get elements list
    poscar = pc.load_poscar(poscar_path)
    elements_dict, elements_list = pc.get_elements(poscar)

    # Test if argument 'element' is valid. IN FUTURE MUST THROW ERROR

    if element > len(elements_list):
        return null

    # If avg == True, return the average of the charges
    if avg == True:
        # Return charge for all elements
        if element == 0:
            charge = charge_df[[orbital]].mean()
        # Return charge for specific element
        else:
            charge = charge_df[[orbital]].loc[charge_df['element'] == elements_list[element-1]].mean()

    # If avg == False, return the sum of the charges
    elif avg == False:
        # Return charge for all elements
        if element == 0:
            charge = charge_df[[orbital]].sum()
        # Return charge for specific element
        else:
            charge = charge_df[[orbital]].loc[charge_df['element'] == elements_list[element-1]].sum()

    # If avg is set to anything other than True or False, return null
    else: return null


    return charge



def calc_magnetisation(magnetisation_df, poscar_path, orbital='tot', element=0, avg=True):
    """ Returns the magnetisation for a given element.

    Keyword arguments:
    magnetisation_df -- pandas DataFrame containing total charge from OUTCAR
    orbital -- which orbital to get charge for. Choices: 's', 'p', 'd', 'tot'. (default='tot')
    element -- which element to get charge for. 0 = all, 1 = first element defined in POSCAR etc. (default=0)
    avg -- determines whether the average of the charge is returned (True) or total (False) (default=True)

    """

    charge = 0

    # Get elements list
    poscar = pc.load_poscar(poscar_path)
    elements_dict, elements_list = pc.get_elements(poscar)

    # Test if argument 'element' is valid. IN FUTURE MUST THROW ERROR

    if element > len(elements_list):
        return null

    # If avg == True, return the average of the charges
    if avg == True:
        # Return charge for all elements
        if element == 0:
            magnetisation = magnetisation_df[[orbital]].mean()
        # Return charge for specific element
        else:
            magnetisation = magnetisation_df[[orbital]].loc[magnetisation_df['element'] == elements_list[element-1]].mean()

    # If avg == False, return the sum of the charges
    elif avg == False:
        # Return charge for all elements
        if element == 0:
            magnetisation = magnetisation_df[[orbital]].sum()
        # Return charge for specific element
        else:
            magnetisation = magnetisation_df[[orbital]].loc[magnetisation_df['element'] == elements_list[element-1]].sum()

    # If avg is set to anything other than True or False, return null
    else: return null


    return magnetisation



def get_pulay_stress(outcar, number_of_lines):

        outcar.seek(number_of_lines - 1000)

        # Create list of only relevant information (after 'reached required accuracy')
        found = False

        ext_pressure_strings = []
        pulay_stress = {'external_pressure': 0,
                        'pulay_stress': 0}


        for line in outcar:
            # Check if 'reached required accuracy' is in line
            if 'external pressure =' in line:
                ext_pressure_strings.append(line)


        pulay_stress['external_pressure'] = ext_pressure_strings[-1][21:37]
        pulay_stress['pulay_stress'] = ext_pressure_strings[-1][53:69]
                
        return pulay_stress
