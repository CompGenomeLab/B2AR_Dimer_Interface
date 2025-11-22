# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:26:15 2023

@author: selcuk.1
"""

import os
import glob

# Define the directory paths for Active-Inactive and Inactive-Inactive folders
ai_dir = r"C:\Users\selcuk.1\Desktop\dimer project\Active-Inactive"
ii_dir = r"C:\Users\selcuk.1\Desktop\dimer project\Inactive-Inactive"



pdb_dir=r"C:/Users/selcuk.1/OneDrive - The Ohio State University/Desktop/dimer project/"
os.chdir(pdb_dir)
# Define the command to run your script
cmd = "python RRCS.py"

os.system(f"{cmd} V34A_S41A_II_2_2")
# Loop through all pdb files in Active-Inactive and Inactive-Inactive folders
for pdb_file in glob.iglob(os.path.join(ai_dir, "*/*.pdb"), recursive=True):
    os.system(f"{cmd} {pdb_file}")

for pdb_file in glob.iglob(os.path.join(ii_dir, "*/*.pdb"), recursive=True):
    os.system(f"{cmd} {pdb_file}")

