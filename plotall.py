#!/usr/bin/python
# -*- coding: utf-8 -*-
# ============================================================
# File: snapshot.py
# Description: parses data to trim only things needed
#              Usage: snapshot.py [source]
# Created by Henry Crute
# 7/30/2014
# ============================================================

import re
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import random
import argparse

path='/home/seads/SEADS-Projects/SnapshotData'

#finds a string between two strings
def find_between(s, first, last):
   try:
      start = s.index( first ) + len( first )
      end = s.index( last, start )
      return s[start:end]
   except ValueError:
      return ""

#
def normalize_list(word, v_list, a_list, w_list):
   #print word
   if word.find("mV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' mV')) * 0.001)
   elif word.find("mA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' mA')) * 0.001)
   elif word.find("mW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' mW')) * 0.001)
   elif word.find('μV') != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' μV')) * 0.000001)
   elif word.find('μA') != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' μA')) * 0.000001)
   elif word.find('μW') != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' μW')) * 0.000001)
   elif word.find("nV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' nV')) * 0.000000001)
   elif word.find("nA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' nA')) * 0.000000001)
   elif word.find("nW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' nW')) * 0.000000001)
   elif word.find("V") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' V')))
      #print "units already normalized"
   elif word.find("A") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' A')))
      #print "units already normalized"
   elif word.find("W") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' W')))
      #print "units already normalized"
   else:
      print "none"

#creates a bar graph from a list of numbers with a random color
def bar_graph(data, graph_type, arraysizes, colorpicker):
   #defines x axis
   ind = np.arange(max(arraysizes))
   #defines width of each bar
   width = 0.95/len(arraysizes)*3
   fig, ax = plt.subplots()
   rects = []
   filenames = []
   i = 0
   for folder in data:
      for filename in data[folder]:
         for harmonics in data[folder][filename]:
            if harmonics == graph_type:
               rects.append(ax.bar(ind + i*width, data[folder][filename][graph_type], width, color = colorpicker[i]))
               #print colorpicker[i]
               filenames.append(filename)
               i = i + 1
   ax.set_ylabel(graph_type)
   ax.set_title('Amplitudes of ' + graph_type + ' harmonics')
   ax.set_xticks(ind + 0.95/2)
   ax.set_xticklabels(ind)
   colors = []
   for x in rects:
      colors.append(x[0])
   ax.legend(colors, filenames)

   plt.show()
#plots everything given dictionary datastructure
def plot_all(signature_dictionary):
   #gets the sizes of each subsequential array
   arraysizes = []
   for folder in signature_dictionary:
      #print folder, 'is the folder with'
      for filename in signature_dictionary[folder]:
         #print '   ', filename
         for harmonics in signature_dictionary[folder][filename]:
            #print '      ', signature_dictionary[folder][filename][harmonics]
            arraysizes.append(len(signature_dictionary[folder][filename][harmonics]))
   
   #randomized color picker for graphs
   colorpicker = []
   for x in range(0, len(arraysizes)/3):
      colorpicker.append((random.random(), random.random(), random.random()))
   #bar graphs one at a time for voltage, amperage, and wattage
   bar_graph(signature_dictionary, 'Voltage', arraysizes, colorpicker)
   bar_graph(signature_dictionary, 'Amperage', arraysizes, colorpicker)
   bar_graph(signature_dictionary, 'Wattage', arraysizes, colorpicker)

#gets all of the data, and puts it into signatures
def process(directory, signatures, currentDevice, filename, args):
   #reads in file from the directory
   read = open(directory,'r')
   #regex for dissecting the voltage, amperage, or wattage harmonics
   regex = re.compile('Vh[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_μ]+|'
                      'Ah[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_μ]+|'
                      'Wh[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_μ]+')
   voltage = []
   amperage = []
   wattage = []
   
   for line in read:
      usefuldata = regex.findall(line)
      for word in usefuldata:
         #print word
         normalize_list(word, voltage, amperage, wattage)

   #percentage of first harmonic
   if args.per != None:
      for i in range(len(voltage)):
         if i!=0:
            voltage[i] = voltage[0]*voltage[i]*int(args.per[0])/100
      for i in range(len(amperage)):
         if i!=0:
            amperage[i] = amperage[0]*amperage[i]*int(args.per[0])/100
      for i in range(len(wattage)):
         if i!=0:
            wattage[i] = wattage[0]*wattage[i]*int(args.per[0])/100
   #normalizes
   if args.norm == True:
      maxVoltage = max(voltage)
      maxAmperage = max(amperage)
      maxWattage = max(wattage)
      for i in range(len(voltage)):
         voltage[i] = voltage[i]/maxVoltage
      for i in range(len(amperage)):
         amperage[i] = amperage[i]/maxAmperage
      for i in range(len(wattage)):
         wattage[i] = wattage[i]/maxWattage

   #add wattage, voltage, and amperage into device
   signatures[currentDevice][filename] = {'Voltage': voltage,
                  'Amperage': amperage, 'Wattage': wattage}
   #closes file from processing
   read.close()

def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

#returns the args from the program input
def get_args():
   parser = argparse.ArgumentParser(description='Harmonic visualization. ' +
                    'Normalization argument normalizes graph to 1,' +
                    'Percentage increases numbers by % amount of the ' +
                    'first harmonic.')
   parser.add_argument('--norm', action='store_true')
   parser.add_argument('--per', nargs=1)
   args = parser.parse_args()
   #printing for debugging args
#   if args.per == None:
#      print args.per
#   else:
#      print args.per[0]

#   print args.norm
   return args
#gets args
args = get_args()
signatures = {}
currentDevice = 'None'

for d in get_immediate_subdirectories(path):
   for f in os.listdir(d):
      full_path = d+'/'+f
      deviceName = os.path.basename(os.path.normpath(d))
      if deviceName not in signatures:
         signatures[deviceName] = {}
         currentDevice = deviceName
      #print(full_path)
      if deviceName == 'Combos':
         continue
      if deviceName == 'Base':
         process(full_path, signatures, currentDevice, f, args)
      if re.search('_on', f, re.IGNORECASE):
         #print f
         process(full_path, signatures, currentDevice, f, args)

plot_all(signatures)
#print signatures['Computers']['Computer_1_on.csv']['Amperage']


