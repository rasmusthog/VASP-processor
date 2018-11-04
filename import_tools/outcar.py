import pandas as pd
import numpy as np
import matplotlib.pyplot as plt










def get_charge(charge_df, orbital='tot', element=0, avg=True):
    """ Returns the charge for a given element.

    Keyword arguments:
    charge_df -- pandas DataFrame containing total charge from OUTCAR
    orbital -- which orbital to get charge for. Choices: 's', 'p', 'd', 'tot'. (default='tot')
    element -- which element to get charge for. 0 = all, 1 = first element defined in POSCAR etc. (default=0)
    avg -- determines whether the average of the charge is returned (True) or total (False) (default=True)

    """

    charge = 0

    # Get elements list
    poscar = load_poscar('OUTCAR/POSCAR')
    elements_dict, elements_list = get_elements(poscar)

    # Test if argument 'element' is valid

    if element > len(elements_list):
        return null

    if element = 0:
        charge = charge_df[orbital].sum()
    else:
        charge = charge_df[orbital].iloc[charge_df['element'] == elements_list[element-1]]
