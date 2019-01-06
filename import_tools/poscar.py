import pandas as pd
import numpy as np


def load_poscar(path):
    """ Loads POSCAR file into an array of lists """

    f = open(path, "r")

    # Initialise empty list 'rows'
    poscar = []

    # Add POSCAR-file line by line into list 'rows'
    for line in f:
        poscar.append(line)


    f.close()

    return poscar

def load_contcar(path):
    """ Loads CONTCAR file into an array of lists """

    f = open(path, "r")

    # Initialise empty list 'rows'
    contcar = []

    # Add POSCAR-file line by line into list 'rows'
    for line in f:
        contcar.append(line)


    f.close()

    return contcar


def get_elements(poscar):
    """ Disects an array of rows from POSCAR into a dictionary containing elements
    and number of each, and a list containing elements (for order preservation)
    """

    # Get information on composition (atoms and number of atoms) from POSCAR
    elements_dict = dict(zip(poscar[5].split(), poscar[6].split())) # Dictionary to map element and number of elements
    elements_list = poscar[5].split() # List to retain order

    return elements_dict, elements_list


def get_lattice_constants(poscar):

    poscar_lattice_coordinates = [] # initialise list
    temp_list_poscar = [] # temp list for use in for-loop


    # Iterate over POSCAR-file to get out lines containing lattice constants
    for i in range(2,5):
        temp_list_poscar = poscar[i].split() # make list from string, split on whitespace

        temp_list_poscar = [ float(x) for x in temp_list_poscar] # convert strings to float

        poscar_lattice_coordinates.append(temp_list_poscar) # append list to a list of lists contianing all coordinates


    a_coordinates = poscar_lattice_coordinates[0]
    b_coordinates = poscar_lattice_coordinates[1]
    c_coordinates = poscar_lattice_coordinates[2]

    coordinates_df = pd.DataFrame({"a": a_coordinates, "b": b_coordinates, "c": c_coordinates})

    return coordinates_df

def calc_angles(poscar):
    lattice_constants = get_lattice_constants(poscar)
    lattice_vector_lengths = calc_lattice_vector_lengths(poscar)
    angles = []

    angles.append(np.round(np.arccos((np.dot(lattice_constants["b"],lattice_constants["c"]))/(lattice_vector_lengths[1]*lattice_vector_lengths[2])) * 180/np.pi, decimals=2))
    angles.append(np.round(np.arccos((np.dot(lattice_constants["a"],lattice_constants["c"]))/(lattice_vector_lengths[0]*lattice_vector_lengths[2])) * 180/np.pi, decimals=2))
    angles.append(np.round(np.arccos((np.dot(lattice_constants["a"],lattice_constants["b"]))/(lattice_vector_lengths[0]*lattice_vector_lengths[1])) * 180/np.pi, decimals=2))


    return angles


def determine_unit_cell_type(poscar):

    unit_cell = "NaN"
    lattice_constants = get_lattice_constants(poscar)
    lattice_vector_lengths = calc_lattice_vector_lengths(poscar)
    angles = calc_angles(poscar)

    if (angles[0] == 90 and angles[1] == 90 and angles[2] == 90):
        if (lattice_vector_lengths[0] == lattice_vector_lengths[1]) and (lattice_vector_lengths[0] == lattice_vector_lengths[2]):
            unit_cell = "c"

        elif (lattice_vector_lengths[0] == lattice_vector_lengths[1] and lattice_vector_lengths[0] != lattice_vector_lengths[2]) or (lattice_vector_lengths[0] == lattice_vector_lengths[2] and lattice_vector_lengths[0] != lattice_vector_lengths[1]) or (lattice_vector_lengths[1] == lattice_vector_lengths[2] and lattice_vector_lengths[1] != lattice_vector_lengths[0]):
            unit_cell = "t"

        else:
            unit_cell = "o"


    elif (angles[0] == 90 and angles[1] == 90 and angles[2] == 120) or (angles[0] == 90 and angles[2] == 90 and angles[1] == 120) or (angles[1] == 90 and angles[2] == 90 and angles[0] == 120):
        unit_cell = "h"

    elif (angles[0] != 90) and (angles[0] == angles[1] and angles[0] == angles[2]):
        unit_cell = "r"

    elif (angles[0] == 90.0 and angles[1] != 90.0 and angles[2] == 90.0)  or (angles[0] == 90 and angles[1] == 90 and angles[2] != 90) or (angles[0] != 90 and angles[1] == 90 and angles[2] == 90):
        unit_cell = "m"

    else:
        unit_cell = "a"


    return unit_cell


def calc_lattice_vector_lengths(poscar):
    """ Takes a dataframe of coordinates (obtained from POSCAR through get_lattice_constants()),
    and returns a list of lattice vector lengths using the formula sqrt(x^2 + y^2 + z^2)"""

    ## Might be able to simplify this by calculating the dot product directly from the dataframe.

    lattice_vector_lengths = [] # initialise empty list

    lattice_constants_df = get_lattice_constants(poscar)
    lattice_constants_df = lattice_constants_df ** 2 # square all numbers

    # loop over all columns and add x, y and z components
    for column in lattice_constants_df:
        lattice_vector_lengths.append(lattice_constants_df[column].sum())


    # return square root of the sums
    return np.sqrt(lattice_vector_lengths)


def calc_lattice_constant_diff(poscar, contcar):

    poscar_coordinates = get_lattice_constants(poscar)
    contcar_coordinates = get_lattice_constants(contcar)

    return contcar_coordinates - poscar_coordinates
    #return a_diff, b_diff, c_diff


def calc_lattice_vector_lengths_diff(poscar, contcar):
    poscar_lengths = calc_lattice_vector_lengths(poscar)
    contcar_lengths = calc_lattice_vector_lengths(contcar)

    return contcar_lengths - poscar_lengths
