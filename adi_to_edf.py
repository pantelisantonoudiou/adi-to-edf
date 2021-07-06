# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 11:02:32 2021

@author: panton01
"""

### ------------------------ IMPORTS -------------------------------------- ###
import os, sys, json
from tqdm import tqdm
import numpy as np
from scipy import signal
from string import ascii_lowercase
import adi         # read labchart files
import pyedflib    # EDF file writer
### ------------------------------------------------------------------------###


def rem_array(start:int, stop:int, div:int):
    """
    Creates an array using np linspace, can also handle last segment smaller than div
    
    Parameters
    ----------
    start : int
    stop : int
    div : int
    
    Returns
    -------
    idx_array : numpy array

    """

    rem = stop % div
    trim_stop = (stop - rem)
    idx_array = np.linspace(start, trim_stop, round(trim_stop/div)+1,dtype = int)
    idx_array = np.append(idx_array, stop)
    
    return idx_array


class Adi2Edf:
    """
    Base class for converting and decimating labchart files to edf format
    
    1) One labchart file may contain multiple animals
    2) Each animal may have multiple channels
    3) For example one file -> 1-12 channels and 4 animals
    4) One EDF file will contain all channels for 1 animal (eg. 1-3)
    5) One labchart file could also be divided into multiple blocks
    ---------------------------------------------------------------
    For example a file foo.adicht with two block will be converted to
    foo_a.edf and foo_b.edf. It will include channels specified in the
    ch_list.
    
    """
   
    # class constructor
    def __init__(self, propeties:dict):
        """
        
        Parameters
        ----------
        propeties : dict

        Returns
        -------
        None.

        """

        # get values from dictionary
        for key, value in propeties.items():
               setattr(self, key, value)
        
        # get channel numbers in python format
        self.ch_list = np.array(self.ch_list) - 1
        
        # get sampling rate and downsample factor
        self.down_factor = round(self.fs/self.new_fs)

        # get info for channels
        self.channel_info = []
        
        for i in range(self.ch_list.shape[0]):
            
            # get channel properties
            ch_dict = {'label': self.ch_id[i], 'dimension': self.dimension[i], 
               'sample_rate': self.new_fs, 'physical_max': self.physical_max[i],
               'physical_min': self.physical_min[i], 'digital_max': self.digital_max[i], 
               'digital_min': self.digital_min[i], 'transducer': '', 'prefilter':''}
            
            # append info
            self.channel_info.append(ch_dict)
            
        # Get adi file obj to retrieve settings
        self.file_obj = adi.read_file(os.path.join(self.load_path, self.file_name + '.adicht'))

        
        
    def convert_file(self):
        """
        Converts labchart file to EDF in blocks.

        Returns
        -------
        None.

        """
    

        all_blocks = len(self.file_obj.channels[0].n_samples) # get all blocks
        
        # get block length in samples
        block = 0
        file_len = self.file_obj.channels[self.ch_list[0]].n_samples[block]
        
        # get number of chunks
        idx = rem_array(0, file_len, self.chunksize) # get index
        idx = np.unique(idx) # remove duplicates
        
        # intialize EDF object
        with pyedflib.EdfWriter(os.path.join(self.save_path, self.file_name + '.edf'),
                                 len(self.ch_list), file_type = pyedflib.FILETYPE_EDF) as edf:
            
            # write headers
            edf.setSignalHeaders(self.channel_info)

            for i in tqdm(range(idx.shape[0]-1)): # iterate over channel length in chuncks
                
                # retrieve data across selected channels in self.ch_list
                data = self.get_filechunks(block, [idx[i], idx[i+1]])
                
                # write data block to edf file       
                edf.writeSamples(data)
    
            # close
            edf.close()
            

    

    def get_filechunks(self, block:int, idx:list):
        """
        Retrieves data from labchart file and decimates

        Parameters
        ----------
        block : int, Block number of labchart file.
        idx : list, start and stop index in samples.
        
        Returns
        -------
        data : list, contains channels as 1D numpy arrays,
        list length = self.ch_list.

        """

        # pre-allocate data
        data = []
        
        for i in range(self.ch_list.shape[0]): # iterate over channels
        
            # get channel object
            ch_obj = self.file_obj.channels[self.ch_list[i]] 
            
            # retrieve data
            temp_data = ch_obj.get_data(block+1, start_sample = idx[0], stop_sample = idx[1]-1)

            # decimate data in two steps if downsampling factor is large
            if self.down_factor > 8:
                temp_data = signal.decimate(temp_data, int(self.down_factor/2))
                data.append(signal.decimate(temp_data, 2))
            else:
                data.append(signal.decimate(temp_data, self.down_factor))
            
        return data
    
# Execute if module runs as main program
if __name__ == '__main__':   
    
    # define dictionary
    propeties = {
       "load_path": r'W:\Maguire Lab\Trina\2020\03- March\4641_4642_4815_4816\raw_data',
       "save_path": r'C:\Users\panton01\Desktop\sleep scoring files\edfs',
       "file_name": "030920",
       "ch_list": [6, 8, 7],
       "fs" : 4000,
       "new_fs": 250,             
       "ch_id":  ["lfp","eeg","emg"],
       "dimension": ["V","V","V"],
       "physical_max": [0.1, 0.1, 0.01],
       "physical_min": [-0.1, -0.1, -0.01],
       "digital_max": [32000, 32000, 32000],
       "digital_min": [-32000, -32000, -32000],
       "chunksize" : 5000000,
       }
    
    
    # init object
    obj = Adi2Edf(propeties)
    
    # convert file
    from time import time
    
    tic = time()
    obj.convert_file()
    print(time()-tic)
    
    
    
    
    
    
    
    
        
        