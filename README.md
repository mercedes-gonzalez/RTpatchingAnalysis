# RTpatchingAnalysis
This tool should be used during a patch clamp experiment in which you are trying to plot the firing frequency vs the current density. GUI checks the selected directory for new files every 2 seconds. The controls for the GUI are as follows: 

Select: 
Prompts user to select a directory in which abf files will be populated. 

Auto Mode: 
After a directory is selected, all data in all ABF files will be plotted. Files added to the selected directory will automatically be plotted and added to the file list. 

Manual Mode:
After a directory is selected, only selected ABF files will be plotted. Files added to the selected directory will automatically be added to the file list. 

Save: 
Saves plotted data ONLY in a single csv file with FILENAME, CURRENT DENSITY, and FIRING FREQUENCY as the columns

Reset: 
Resets GUI to its initial state. 

Toolbar: 
Interact with plot by zooming, probing data, or saving the plot. 
