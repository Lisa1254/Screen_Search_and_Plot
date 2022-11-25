#!/usr/bin/env python3

'''
Script to crawl through screen data folders and extract all file information.
Will output text document list of all files, list of MAGeCK files, list of DrugZ files.
Currently going to work through MAGeCK and DrugZ. Plan to inlclude other analysis types in the future. 
Commenting out lists for mageck and drugZ in order to have next step in analysis in separate script.
If you wish to utilize this within another script, and prefer to keep list instead of reading in text outputs,
simply comment out the write to file, and remove # from lines for the lists.
Add the parent folder that you wish to search to the command line after calling the script
e.g.
python3 get_file_structure_fromDB.py "/Users/lhoeg/Durocher Lab Dropbox/ScreenData"
Optional, add location to save output files after the parent folder. 
e.g.
python3 get_file_structure_fromDB.py "/Users/lhoeg/Durocher Lab Dropbox/ScreenData" "/Users/lhoeg/Documents/30_Screens/"
'''

import os
import sys

#Will need to run from office computer which is DropBox connected
parent_folder = [sys.argv[1]]

#This will allow for indentation in main file output document to help keep track of file structure
start_folder_levels = parent_folder[0].count("/")

#If using, get output prefix
if len(sys.argv) == 3:
    out_prefix = sys.argv[2]
else:
    out_prefix = ""

#Initialize main output document
main_out = out_prefix+"all_files.txt"
main_out_open = open(main_out, 'w')

#Initialize Mageck document
mageck_out = out_prefix+"mageck_files.txt"
mageck_out_open = open(mageck_out, 'w')

#Initialize DrugZ document
drugz_out = out_prefix+"drugz_files.txt"
drugz_out_open = open(drugz_out, 'w')

#If doing lists instead of save to document:
#mageck_list = []
#drugz_list = []

for pf in parent_folder:
    parent_objects = os.scandir(pf)
    #These 4 commands for saving current folder locations to main_out
    current_folder_levels = pf.count("/")
    current_indent = current_folder_levels - start_folder_levels
    tabs = "\t"*current_indent
    main_out_open.write(pf+"\n")
    #Continue to check what is in the current folder
    for entry in parent_objects :
        if entry.is_file():
            #Write all files to the main_out if using
            main_out_open.write(tabs+entry.name+"\n")
            if "gene_summary" in entry.name.lower():
                #Finding gene_summary files for MAGeCK
                #Write to mageck file
                mageck_out_open.write(pf+"/"+entry.name+"\n")
                #Or save to list
                #mageck_list.append(pf+"/"+entry.name)
            elif "drugz" in entry.name.lower():
                #Finding drugz outputs, expect to have drugz (case-insensitive) in name
                #Write to drugz file
                drugz_out_open.write(pf+"/"+entry.name+"\n")
                #Or save to list
                #drugz_list.append(pf+"/"+entry.name)
        elif entry.is_dir():
            #If subdirectory is found, add it to the list of where to search.
            new_dir = pf+"/"+entry.name
            loc_to_add  = parent_folder.index(pf)
            parent_folder.insert(loc_to_add+1, new_dir)

#Close files
main_out_open.close()
mageck_out_open.close()
drugz_out_open.close()


#
