import poscar as pc

poscar = pc.load_poscar('OUTCAR/POSCAR')

dict, list = pc.get_elements(poscar)

print(list)
print(dict)
