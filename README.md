# adi-to-edf
- Converts labchart files to edf.
- Data can also be downsampled(decimated) to reduce file size.
- One labchart file will be converted to multiple edf files depending on the file format.
- Each block of the labchart file will be converted to a new edf file.

For example:
A labchart file that contains four animals will be converted to four edf files.

### Requirements
- Currenyl only runs on windows OS due to labchart toolbox dependency.
- Each animal in one labchart file has the same number of channels.

-> For batch analysis (batch_convert.py)
- All files have the same channel format.
- CSV file with paths (check eeg_paths_template.csv for detailed info)

### How to run
    python path to

### :snake: Dependencies

- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [scipy](https://www.scipy.org/)
- [tqdm](https://github.com/tqdm/tqdm)
- [pyedflib](https://github.com/holgern/pyedflib)
- [adi](https://github.com/JimHokanson/adinstruments_sdk_python)
- [beartype](https://github.com/beartype/beartype)
- [click](https://click.palletsprojects.com/en/8.0.x/)


---
### Configuration settings
    - save_path: Path to folder that 
    
    - fs : sampling rate (samples per second), Default = 4000.
    - new_fs : sampling rate after decimation (samples per second), Default = 250.
    - chunksize : Number of samples to load in memory during conversion.
    - ch_id : Channel names.
    - animal_ch_list : List containing smaller lists with indivdiual animal channels
    per labchart file.
    - save_path : Path to folder where edf files will be stored.
    
    edf attributes, click [here](https://pyedflib.readthedocs.io/en/latest/ref/edfwriter.html) for more information.
    --------------
    - physical_max
    - physical_min
    - digital_max
    - digital_min
    - dimension