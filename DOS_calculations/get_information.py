import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

outcar = open("POSCAR", "r")

rows = []

for line in outcar:
    rows.append(line)

# Get information on composition in
elements = dict(zip(rows[5].split(), rows[6].split()))
