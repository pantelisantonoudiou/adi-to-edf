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
from math import floor
from string import ascii_lowercase
import adi         # read labchart files
import pyedflib    # read/create EDF files
# User Defined
### ------------------------------------------------------------------------###


propeties = {
    "load_path": r'W:\Maguire Lab\Trina\2020\03- March\4641_4642_4815_4816\raw_data',
    "save_path": r'C:\Users\panton01\Desktop\sleep scoring files\edfs',
    "file_name": "030920",
    "ch_list": [4, 5, 6],
    "fs" : 4000,
    "new_fs": 250,             
    "ch_id":  ["lfp","eeg","emg"],
    "dimension": ["V","V","V"],
    "physical_max": [1, 1, 1],
    "physical_min": [-1, -1, -1],
    "digital_max": [10, 10, 10],
    "digital_min": [-10, -10, -10],
    "chunksize" : 4000000,
    }

def rem_array(start:int, stop:int, div:int):
    """
    rem_array(start,stop,div)
    idx =rem_array(start,stop,div)
    
    Parameters
    ----------
    start : int
    stop : INT
    div : INT
    
    Returns
    -------
    idx_array : numpy array
        DESCRIPTION.

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
        self.ch_list -= 1
        
        # get sampling rate and downsample factor
        self.down_factor = round(self.fs/self.new_fs)
        
        # get info for channels
        self.channel_info = []
        for i in self.ch_list:
            # get channel properties
            ch_dict = {'label': self.ch_id[i], 'dimension': self.dimension[i], 
               'sample_rate': self.fs, 'physical_max': self.physical_max[i],
               'physical_min': self.physical_min[i], 'digital_max': self.digital_max[i], 
               'digital_min': self.digital_min[i], 'transducer': '', 'prefilter':''}
            
            # append info
            self.channel_info.append(ch_dict)
            
            
        # Get adi file obj to retrieve settings
        self.file_obj = adi.read_file(os.path.join(self.load_path,self.file_name, '.adicht'))
        

        
        
    def convert_file(self):
    

        
        # all_blocks = len(file_obj.channels[0].n_samples) # get all blocks
        
        # get block length in samples
        block = 0
        file_len = self.file_obj.channels[self.ch_list[0]].n_samples[block]
        
        # get number of chunks
        chunks = floor(file_len/self.chunksize)
        
        
        
        # intialize EDF object
        edf = pyedflib.EdfWriter(os.path.join(self.save_path, self.file_name, '.edf'),
                                 len(self.ch_list), file_type = pyedflib.FILETYPE_EDF) 
        
        
        
        
        for i in range(len(self.ch_list)): ## Iterate over all animal channels ##
             

            
                     
            
        
            print(ch_obj)
        # write file to EDF object
        edf.setSignalHeaders(self.channel_info)
        

    
    # segment labchart file to numpy array
    def get_filechunks(self, chobj, block, idx):
        """
         get_filechunks(self, chobj, block, cols, idx)

        Parameters
        ----------
        chobj : ADI labchart chanel object
        block : Int, Block number of labchart file.
        idx : List, start and stop index in samples.

        Returns
        -------
        data : 2D numpy array (1D = time, 2D = channels)

        """
        
        # pre-allocate datqa
        data = np.zeros(idx[1]-idx[0]+1, len(self.ch_list))
        
        for ch in self.ch_list: # iterate over channels
        
            # get channel object
            ch_obj = self.file_obj.channels[self.ch_list[ch]] 
            
            # retrieve data
            data[:,ch] = ch_obj.get_data(block, start_sample = idx[0], stop_sample = idx[1])
            
            # decimate data
            data[:,ch] = signal.decimate(data[:,ch], self.down_factor)

        return data
    
    
    
    #     # save in chunks per animal
    # def save_chunks(self, file_obj, filename, ch_list):
    #     """
    #     save_chunks(self, file_obj, filename, ch_list)

    #     Parameters
    #     ----------
    #     file_obj : ADI file object
    #     filename : String
    #     ch_list : List of numpy arrays 
    #         Containing channels for each animal.
    #         e.g. [1,2,3], [4,5,6]...

    #     Returns
    #     -------
    #     None.

    #     """
        
    #     ch_list = ch_list - 1 # convert channel to python format
    #     all_blocks = len(file_obj.channels[0].n_samples) # get all blocks
        
    #     for block in range(all_blocks):
            
    #         # print file being analyzed
    #         print(self.cntr,'-> Converting block :', block, 'in File:', filename)
    #         self.increase_cntr() # increase object counter
            
    #         # get first channel (applies across animals channels)
    #         chobj = file_obj.channels[ch_list[0]] # get channel obj
            
            
    #         ### CHANNEL PARAMETERS ###
    #         length = chobj.n_samples[block] # get block length in samples
    #         win_samp = self.win * self.fs # get window size in samples
         
            
    #         ### SAVING PARAMETERS ###
    #         file_id  = filename + ascii_lowercase[block] + '.edf' # add extension
    #         full_path = os.path.join(self.save_path, file_id) # get full save path
          

            
    #          ##########################################################################
            
    #         ## Iterate over channel length ##
    #         for i in tqdm(range(len(idx)-1), desc = 'Progress', file=sys.stdout): # loop though index 
            
    #             # preallocate data
    #             data = np.zeros([idx[i+1] - idx[i], mat_shape[1], len(ch_list)])
                
    #             for ii in range(len(ch_list)): ## Iterate over all animal channels ##
    #                 # get channel obj
    #                 chobj = file_obj.channels[ch_list[ii]] 
                    
    #                 # get data per channel
    #                 data[:,:,ii] = self.get_filechunks(chobj,block+1,mat_shape[1],idx[i:i+2])
                    
                    

    
    #             # append data to datastore
    #             ds.append(data)
            
    #         # close table object
    #         fsave.close()
        
        
        
        
        
        
        
        
        