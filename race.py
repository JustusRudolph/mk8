import numpy as np
import math
import csv
import datetime
import pandas

def add_line(ln, filename):
  with open(filename, "a") as f:
    f.write("\n" + ln)

def create_line(data):
  """
  Assumes data is a list/array
  """
  n = len(data)
  if (not n):
    return 1  # do nothing
 
  line = ""
  for i in range(n):
    line += str(data[i])
    if (i != n-1):
      line += ", "

  return line

def get_track_abbrevs():
  """
  Simple function to get all abbreviations of tracks
  """
  data = pandas.read_csv("tracks.csv", delimiter=",")
  abbrevs = data["Abbreviation"]

  return list(abbrevs)  # make into list

def setup():
  n_ok  # check if number of races acceptable
  while (not n_ok):
    n_races = int(input("Number of races: "))
    if ((n_races > 3) and (n_races < 49)):
      n_ok = True
    else:
      print(f"Unacceptable number of races: {n_races}. Must be between 4 and 48").
  
  fname = input("Name of file (defaults to current date if left blank): ")
  # TODO(Justus) add functionality for who is playing

  if (fname == ""):
    date = datetime.date.today()    
    now = datetime.datetime.now()
    fname += str(date) + "_" + str(now.hour) + ":" + str(now.minute)

  fname += ".csv"
  path = "comps/" + fname

  race = open(path, "w")
  
  race.write("Track, Henry, Justus, Lukas")
  race.close()

  return n_races, path

def update(i):
  """
  Regular Updating function for every race
  Returns the new line to be added
  """
  print(f"Race {i+1}.")
  track_ok = False  # check if acceptable track
  tracks = get_track_abbrevs()
  while(not track_ok):
    track = input("Enter Track: ")
    if (track in tracks):  # is it an allowed abbreviation
      track_ok = True
    else:
      print(f"Unknown track abbreviation: \"{track}\". Please try again.")
  
  res_ok = False
  results = []
  while(not res_ok):
    results = [int(res) for res in input("Results for Henry, Justus, Lukas. ").split()]
    np_res = np.array(results)
    if (all((np_res > 0)*(np_res < 13))):  # check if between 1st and 12th place    
      res_ok = True
    else:
      print("Those results are not acceptable. Must be between 1 and 12.")
  
  data = [track]
  data += results

  return data  # full line

def main():
  
  n, path = setup()
  i = 0
  while(i < n):
    data = update(i)
    line = create_line(data)
    add_line(line, path)  # write to path
    i += 1  # increase i
  
  return 0


main()



