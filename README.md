Author: Henry Crute

# Python plotter for PA1000 Shapshots
##snapshot.py
Description: Takes a csv file from the PA1000 and plots all of the Voltage, Current, and Wattage harmonics

useage: snapshot.py [file.csv]
##plotall.py
Description: Recursively reads all files in subfolders of path for harmonic visualization. Normalization argument normalizes graph to 2, percentage increases numbers by a percentage amount of the first harmonic. Change absolute path in code with variable 'path'.

usage: plotall.py [-h] [--norm] [--per PER]

##Important additional information
Must have python numpy and matplotlib.pyplot python libraries installed to work

Development using iPython
