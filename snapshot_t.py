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
path='/Users/ali/phd/Data/Devices_signature'
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
   if word.find("mV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' mV')) * 0.001)
   elif word.find("mA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' mA')) * 0.001)
   elif word.find("mW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' mW')) * 0.001)
   elif word.find("μV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' μV')) * 0.000001)
   elif word.find("μA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' μA')) * 0.000001)
   elif word.find("μW") != -1:
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
def bar_graph(v_list, title, colorstring, totalPlots, plotNum):
   ind1 = np.arange(len(v_list))    # the x locations for the groups   
   #subplots bar graph   
   plt.subplot(100 + totalPlots * 10 + plotNum)   
   width = .5

   p1 = plt.bar(ind1 + 0.75, v_list, width, color=colorstring, hold=True)
   
   plt.ylabel('Nor`malized Units')
   plt.title('Harmonics Amplitude of ' + title)

   plt.xticks(ind1 + 1)
   maxY = max(v_list)
   if maxY!=0 :
      plt.yticks(np.arange(-maxY/10, maxY + maxY/10, maxY/6))

   #plt.legend((p1[0], p2[0]), ('Voltage', 'Amperage'))

def process(filename):
   #checks for arguments, given usage
   # if len(sys.argv) < 2:
   #    print "Usage: " + sys.argv[0] + " [source]"
   #    exit(1)
   #path_filename=path+'/'+filename
   read = open(filename,'r')
   #read = open(sys.argv[1], 'r')
   #write = open(sys.argv[2], 'w')

   #main regex loop
   regex = re.compile('Vh[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_]+|'
                      'Ah[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_]+|'
                      'Wh[0-9]+m,-?[0-9]+\.[0-9]+\s[A-Za-z_]+')
   voltage = []
   amperage = []
   wattage = []

   for line in read:
      usefuldata = regex.findall(line)
      for word in usefuldata:
         #print word
         normalize_list(word, voltage, amperage, wattage)
   #usage, specify total number of plots, because I modified bar_graph to subplot
   

   for i in range(len(voltage)):
        if i!=0:
         voltage[i]=math.floor(voltage[i]*100000)/100000#*.50*voltage[0]

   for i in range(len(amperage)):
        if i!=0:
         amperage[i]=math.floor(amperage[i]*100000)/100000#*.50*amperage[0]
   
   for i in range(len(wattage)):
        if i!=0:
         wattage[i]=math.floor(wattage[i]*100000)/100000#*.50*wattage[0]
   f=open('samplefile.txt','w')
 #  for i in range(0,voltage.len):
 #     print >>f, voltage 
 #     print >>f, amperage
 #     print >>f, wattage
      # print voltage
   # print amperage
   # print wattage
   totalPlots = 3

   plt.figure(num=1, figsize=(26,6))
   bar_graph(voltage, 'Voltage','r', totalPlots, 1)
   bar_graph(amperage, 'Amperage', 'g', totalPlots, 2)
   bar_graph(wattage, 'Wattage', 'b', totalPlots, 3)
   plt.suptitle(filename, fontsize=16)
  
   plt.show()
   read.close()

# for root,dirs, files in os.walk(path):
#     print root
#     print dirs
#     print files
    #process(f)
def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

for d in get_immediate_subdirectories(path):
   for f in os.listdir(d):
      full_path = d+'/'+f
      #print(full_path)
      process(full_path)


#for item in voltage:
#   print item

#write.close()

