import poscar as pc
import outcar as oc
import os


poscar_path = 'import_tools/testfiles/POSCAR'
outcar_path = 'import_tools/testfiles/OUTCAR'
contcar_path = 'import_tools/testfiles/CONTCAR'

# Test pc.load_poscar
poscar = pc.load_poscar(poscar_path)
contcar = pc.load_contcar(contcar_path)

#print(poscar)

# Test pc.get_elements
#dict, list = pc.get_elements(poscar)

#print(list)
#print(dict)

# Test oc.load_outcar
#outcar, no_lines = oc.load_outcar(outcar_path)

#charge_df, mag_df = oc.get_charge_magnetisation(outcar, no_lines, poscar_path)
#pulay_stress = oc.get_pulay_stress(outcar, no_lines)


coords = pc.get_lattice_constants(poscar)
print(coords)


#print(charge_df.head())
#print(mag_df.head())


# Test oc.calc_charge

#print(oc.calc_charge(charge_df, poscar_path, orbital="d", element=1, avg=True))

# Test oc.calc_magnetisation

#print(oc.calc_magnetisation(mag_df, poscar_path, orbital="d", element=1, avg=False))


# Test oc.get_pulay_stress

#print(pulay_stress["external_pressure"])
#print(pulay_stress["pulay_stress"])




# Close all files

#outcar.close()
