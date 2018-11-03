import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### GET INFORMATION ABOUT THE COMPOSITION. SHOULD PROBABLY MAKE THIS A SEPARATE FUNCTION

# Open POSCAR file
poscar = open("OUTCAR/POSCAR", "r")

# Initialise empty list 'rows'
rows = []

# Add POSCAR-file line by line into list 'rows'
for line in poscar:
    rows.append(line)

# Get information on composition (atoms and number of atoms) from POSCAR
elements_dict = dict(zip(rows[5].split(), rows[6].split())) # Dictionary to map element and number of elements

# Close POSCAR-file
poscar.close()

# Count number of ions in POSCAR
NIONS = 0

for element in elements_dict:
    NIONS += int(elements_dict[element])


### READ OUTCAR FILE


# Open OUTCAR-file
outcar = open("OUTCAR/OUTCAR", "r")

# Count number of lines in OUTCAR-file
number_of_lines = 0

for line in outcar:
    number_of_lines += 1

# Reset IOWrapper to 
outcar.seek(number_of_lines - 1000)



# Find 'total charge'
found = False
outcar_list = []

for line in outcar:
    if 'reached required accuracy' in line:
        found = True

    if found == True:
        outcar_list.append(line)

## Add total charge of ions to array 'total_charge'

total_charge = []

for i in range(10,NIONS+10):
    total_charge.append(outcar_list[i].split())

charge_df = pd.DataFrame(total_charge, columns=["ion", "s", "p", "d", "tot"])
charge_df.set_index("ion", inplace=True)
charge_df = charge_df.astype(float)

print(charge_df["d"].iloc[1:8].sum())

## Add magnetisation of ions to array 'magnetisation'
magnetisation = []

for i in range(NIONS+19,(2*NIONS)+19):
    magnetisation.append(outcar_list[i].split())

magnetisation_df = pd.DataFrame(magnetisation, columns=["ion", "s", "p", "d", "tot"])
magnetisation_df.set_index("ion", inplace=True)
magnetisation_df = magnetisation_df.astype(float)




outcar.close()
