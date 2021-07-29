# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:27:20 2021

@author: panton01
"""

### ------------------------ IMPORTS -------------------------------------- ###
from beartype import beartype
import json, os, click, string
import pandas as pd
from adi_to_edf import Adi2Edf

# get ASCII characters only
printable = set(string.printable)
### ------------------------------------------------------------------------###

@beartype
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

@beartype
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


@click.command()
@click.argument('csv_path', type = str)
def main(csv_path:str):
    """
    Convert labchart files to EDFs.

    Parameters
    ----------
    csv_path : str, file containing paths to labchart files and channels to analyze .

    Returns
    -------
    None.

    """
    
    if not os.path.exists(os.path.dirname(csv_path)):
        click.secho(f"\n -> '{csv_path}' was not found\n" , fg = 'red', bold = True)
        return
        
    # get csv file with eeg file paths
    filepaths = pd.read_csv(csv_path)
    
    # load config file 
    try:
        properties = open('config.json', 'r').read()
        properties = json.loads(properties)
    except Exception as err:
        raise FileNotFoundError(f'Unable to read the config file.\n{err}')

    # iterate over labchart files
    for i in range(len(filepaths)):
        
        # print file converted
        print_str = '-> Initiating conversion in File '+ str(i+1) + ' out of ' + str(len(filepaths)) + ':\n'
        click.secho(print_str , fg = 'green', bold = True)

        # separate file path with the file name
        cleaned_path = list(filter(lambda x: x in printable, filepaths.file_path[i]))   # get only ascii characters
        file_path, file_name = sep_dir(''.join(cleaned_path)) 
        
        # find position of animal in list
        pos = find_position(filepaths.animals[i], str(filepaths.animalID[i]), '_')
        
        # update properties for each animal
        properties.update({
            'load_path' : file_path,
            'file_name' : file_name.replace('.adicht','') ,
            'subject' : filepaths.animalID[i],
            'ch_list' : properties['animal_ch_list'][pos]
            })
        
        # init object
        obj = Adi2Edf(properties)
        
        # convert file
        obj.convert_file()
        
    click.secho('\n----------------- EDF conversion completed -----------------\n', fg = 'white', bold = True)
    
# Execute if module runs as main program
if __name__ == '__main__': 
    main()

   
    


        

            

       

