import pandas as pd


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



def calc_diff_poscar_contcar(poscar, contcar):

    # Initalise lists for coordinates from POSCAR and CONTCAR
    poscar_lattice_coordinates = []
    contcar_lattice_coordinates = []


    # Extract POSCAR coordinates
    temp_list_poscar = [] # temp list for use in for-loop

    for i in range(2,5):
        temp_list_poscar = poscar[i].split()

        temp_list_poscar = [ float(x) for x in temp_list_poscar]

        poscar_lattice_coordinates.append(temp_list_poscar)


    # Extract CONTCAR coordinates
    temp_list_contcar = [] # temp list for use in for-loop

    for i in range(2,5):
        temp_list_contcar = contcar[i].split()

        temp_list_contcar = [ float(x) for x in temp_list_contcar]

        contcar_lattice_coordinates.append(temp_list_contcar)


    # Calculate differences


    a_diff = []
    b_diff = []
    c_diff = []



    for i in range(0,3):
        a_diff.append(contcar_lattice_coordinates[0][i] - poscar_lattice_coordinates[0][i])
        b_diff.append(contcar_lattice_coordinates[1][i] - poscar_lattice_coordinates[1][i])
        c_diff.append(contcar_lattice_coordinates[2][i] - poscar_lattice_coordinates[2][i])


    coordinates_diff_df = pd.DataFrame({"a": a_diff, "b": b_diff, "c": c_diff})

    return coordinates_diff_df
    #return a_diff, b_diff, c_diff
