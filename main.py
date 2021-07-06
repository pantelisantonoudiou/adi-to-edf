# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:27:20 2021

@author: panton01
"""

### ------------------------ IMPORTS -------------------------------------- ###
import json, os
import pandas as pd
from adi_to_edf import Adi2Edf
### ------------------------------------------------------------------------###

def sep_dir(file_path:str, sepint:int = 1):
    """
    Separates string to two segments based on os separator.
    
    e.g.___________________________________________________________
    file_path = Z:\\documents\\user\\2018\\12-December\\fileone.csv
    output = sep_dir(file_path) 
    
    Parameters
    ----------
    file_path : str
    sepint : int, Defines the number of folders away from the innermost.

    Returns
    -------
    first_path : str
    inner_dir : str

    """
    
    # get path separator
    separator = os.sep
    
    # split based on operating system
    x = file_path.split(separator)
    
    # get inner directory
    inner_dir = separator.join(x[-sepint:])

    # join based on separator
    first_path =  separator.join(x[0:-sepint])
    
    return first_path, inner_dir


def find_position(input_str:str, match_str:str, sep:str):
    """
    Separates input_str with sep and finds position of match_str in the separated list.

    Parameters
    ----------
    input_str : str, string to be separated to list and searched
    match_str : str, search string
    sep : str, string to split input_str 

    Returns
    -------
    pos : int.

    """
    
    # separate str
    str_list  = input_str.split('_')
    
    # find position
    pos = str_list.index(match_str)
    
    return pos
    

# Execute if module runs as main program
if __name__ == '__main__': 

    # Load config file 
    try:
        config = open('config.json', 'r').read()
        config = json.loads(config)
    except Exception as err:
        raise FileNotFoundError(f"Unable to read the config file.\n{err}")

    # read csv file with eeg file paths
    filepaths = pd.read_csv('eeg_paths.csv')
    
    # define channel list
    animal_ch_list = [[0,1,2], [3,4,5], [6,7,8], [9,10,11]] 
    
    # pass config to properties and update with animal settings
    properties = config
    
    for i in range(len(filepaths)): # iterate over files
        print('-> Initiating conversion in File', i+1, 'out of', str(len(filepaths)) + ':\n')
        
        # separate file path with the file name
        file_path, file_name = sep_dir(filepaths.file_path[i]) 
        
        # find position of animal in list
        pos = find_position(filepaths.animals[i], str(filepaths.animalID[i]), '_')
        
        # update properties for each animal
        properties.update({
            "load_path" : file_path,
            "file_name": file_name.replace('.adicht','') ,
            "subject": filepaths.animalID[i],
            "ch_list" : animal_ch_list[pos]
            })
    
        # init object
        obj = Adi2Edf(properties)

        # convert file
        obj.convert_file()
        
    print('\n----------------- EDF conversion completed -----------------\n')

            






       

