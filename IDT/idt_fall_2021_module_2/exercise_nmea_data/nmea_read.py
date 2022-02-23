#!/usr/bin/env python3
#/****************************************************************************
# nmea read function
# Copyright (c) 2018-2020, Kjeld Jensen <kj@kjen.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************/
'''
2018-03-13 Kjeld First version, that reads in CSV data
2020-02-03 Kjeld Python 3 compatible
2020-09-17 Kjeld Changed first line to python3
'''

import matplotlib.pyplot as plt

class nmea_class:
  def __init__(self):
    self.data = []

  def import_file(self, file_name):
    file_ok = True
    try:
      # read all lines from the file and strip \n
      lines = [line.rstrip() for line in open(file_name)] 
    except:
      file_ok = False
    if file_ok == True:
      pt_num = 0
      for i in range(len(lines)): # for all lines
        if len(lines[i]) > 0 and lines[i][0] != '#': # if not a comment or empty line
          csv = lines[i].split (',') # split into comma separated list
          self.data.append(csv)

  def print_data(self):
    for i in range(len(self.data)):
      print (self.data[i])

  def alt_time(self):
    alt = []
    time = []
    #start_time = 0
    for i in range(len(self.data) - 1):
        if i % 2 == 0:
            alt.append(float(self.data[i][9]))
            time.append(float(self.data[i][1]) - float(self.data[0][1]))
    return alt, time

  def num_sat(self):
    num = []
    for i in range(len(self.data) - 1):
      num.append(int(self.data[i][7]))
    return num

  def lat_lon(self):
    lat = []
    lon = []
    for i in range(len(self.data) - 1):
        if self.data[i][0] == "$GPGLL" and len(self.data[i]) == 8 and self.data[i][1] != '':
            print(self.data[i])
            a = float(self.data[i][1])
            deg = int(float(self.data[i][1])/100)
            min = (a % 100) / 60
            res = deg + min
            lat.append(res)
            a = float(float(self.data[i][3]))
            deg = int(float(self.data[i][3])/100)
            min = (a % 100) / 60
            res = deg + min
            lon.append(res)
        if self.data[i][0] == "$GPGGA":
            a = float(self.data[i][2])
            deg = int(float(self.data[i][2])/100)
            min = (a % 100) / 60
            res = deg + min
            lat.append(res)
            a = float(float(self.data[i][4]))
            deg = int(float(self.data[i][4])/100)
            min = (a % 100) / 60
            res = deg + min
            lon.append(res)
    return lat, lon

if __name__ == "__main__":
  print ('Importing file')
  nmea = nmea_class()
  nmea.import_file ('nmea_trimble_gnss_eduquad_flight.txt')
  #lat, lon = nmea.lat_lon()
  #plt.title('Map')
  #plt.plot(lat, lon)
  #plt.savefig('map.png')
  #alt, time = nmea.alt_time()
  #plt.title('Altitude')
  #plt.plot(time, alt)
  #plt.savefig('Altitude.png')
  #num = nmea.num_sat()
  #plt.title('Num satellites')
  #plt.plot(num)
  #plt.savefig('sat.png')
