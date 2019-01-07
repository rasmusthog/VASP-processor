# VASP-processor
Process VASP output files for analysis use with pandas.

Will include (near future):

- DOSCAR-reader
  - Extract data from DOSCAR
  - Plot density of states
  - Return band gap
  
- OUTCAR-reader
  - Extract total charge and magnetisation from converged structure
  - Average bond lengths (with standard deviation)
  
 
 - INCAR-reader
  - Add all (relevant) tags to a dictionary for use in other functions, e.g. MAGMOM true or false, PROCAR = 10 or 11 etc.
 
 
 May include (distant future):
 
 - Animation of evolution of atomic positions during relaxation (from OUTCAR)
 - Python-implementation of Bader charge analysis
 
