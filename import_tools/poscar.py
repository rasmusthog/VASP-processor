def load_poscar(path):
    """ Loads POSCAR file into an array of lists """

    f = open(path, "r")

    # Initialise empty list 'rows'
    poscar = []

    # Add POSCAR-file line by line into list 'rows'
    for line in f:
        poscar.append(line)

    return poscar


def get_elements(poscar):
    """ Disects an array of rows from POSCAR into a dictionary containing elements
    and number of each, and a list containing elements (for order preservation)
    """

    # Get information on composition (atoms and number of atoms) from POSCAR
    elements_dict = dict(zip(poscar[5].split(), poscar[6].split())) # Dictionary to map element and number of elements
    elements_list = poscar[5].split() # List to retain order

    return elements_dict, elements_list
