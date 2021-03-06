import poscar as pc
import outcar as oc
import os


# Define paths for general files
poscar_path = 'import_tools/testfiles/POSCAR'
outcar_path = 'import_tools/testfiles/OUTCAR'
contcar_path = 'import_tools/testfiles/CONTCAR'

# Define paths for POSCARs with different unit cell types
poscar_c_path = 'import_tools/testfiles/POSCAR_c' # cubic
poscar_t_path = 'import_tools/testfiles/POSCAR_t' # tetragonal
poscar_o_path = 'import_tools/testfiles/POSCAR_o' # orthorhombic
poscar_r_path = 'import_tools/testfiles/POSCAR_r' # rhombohedral
poscar_h_path = 'import_tools/testfiles/POSCAR_h' # hexagonal
poscar_m_path = 'import_tools/testfiles/POSCAR_m' # monoclinic
poscar_a_path = 'import_tools/testfiles/POSCAR_a' # triclinic (anorthic)



# Test pc.load_poscar
poscar = pc.load_poscar(poscar_path)
contcar = pc.load_contcar(contcar_path)

poscar_c = pc.load_poscar(poscar_c_path)
poscar_t = pc.load_poscar(poscar_t_path)
poscar_o = pc.load_poscar(poscar_o_path)
poscar_r = pc.load_poscar(poscar_r_path)
poscar_h = pc.load_poscar(poscar_h_path)
poscar_m = pc.load_poscar(poscar_m_path)
poscar_a = pc.load_poscar(poscar_a_path)

#print(poscar)

# Test pc.get_elements
#dict, list = pc.get_elements(poscar)

#print(list)
#print(dict)

# Test oc.load_outcar
#outcar, no_lines = oc.load_outcar(outcar_path)

#charge_df, mag_df = oc.get_charge_magnetisation(outcar, no_lines, poscar_path)
#pulay_stress = oc.get_pulay_stress(outcar, no_lines)


coords = pc.calc_lattice_constant_diff(poscar, contcar)
#print(coords)


lattice_vectors_cont = pc.calc_lattice_vector_lengths(contcar)
lattice_vectors_pos = pc.calc_lattice_vector_lengths(poscar)
lattice_vectors_diff = pc.calc_lattice_vector_lengths_diff(poscar, contcar)

#print(lattice_vectors_cont)
#print(lattice_vectors_pos)
#print(lattice_vectors_diff)

# Test calculations of angles.
print("Cubic:")
print(pc.calc_angles(poscar_c)) # should be 90, 90, 90
print(pc.calc_lattice_vector_lengths(poscar_c))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_c)) + " Angstrom")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_c))

print("Tetragonal:")
print(pc.calc_angles(poscar_t)) # should be 90, 90, 90
print(pc.calc_lattice_vector_lengths(poscar_t))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_t)) + " Angstrom")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_t))

print("Orthorhombic:")
print(pc.calc_angles(poscar_o)) # should be 90, 90, 90
print(pc.calc_lattice_vector_lengths(poscar_o))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_o)) + " Angstorm")
print("Unit cell:  " +pc. determine_unit_cell_type(poscar_o))

print("Rhomohedral")
print(pc.calc_angles(poscar_r)) # should be alpha, alpha, alpha - alpha != 90
print(pc.calc_lattice_vector_lengths(poscar_r))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_r)) + " Angstorm")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_r))

print("Hexagonal:")
print(pc.calc_angles(poscar_h)) # should be 90, 90, 120
print(pc.calc_lattice_vector_lengths(poscar_h))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_h)) + " Angstrom")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_h))

print("Monoclinic:")
print(pc.calc_angles(poscar_m)) # should be 90, 90, alpha, alpha != 90
print(pc.calc_lattice_vector_lengths(poscar_m))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_m)) + " Angstrom")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_m))

print("Triclinic:")
print(pc.calc_angles(poscar_a)) # should be
print(pc.calc_lattice_vector_lengths(poscar_a))
print("Volume: " + str(pc.calc_unit_cell_volume(poscar_a)) + " Angstrom")
print("Unit cell:  " + pc.determine_unit_cell_type(poscar_a))




print(pc.calc_unit_cell_volume_diff(poscar, contcar))

# Test of unit cell types










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
