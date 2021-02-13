import numpy as np
import math
import datetime
import pandas

from . import mk_checks as chk

PATH_TO_TRACK_DICT = "../data/tracks.csv"  # path to tracks csv file
PATH_TO_COMPS = "../.comps/"  # path to competition directory
ALLOWED_N_RACES=[4, 6, 8, 12, 16, 24, 32, 48]  # which number of races allowed
NAMES = ["Henry", "Justus", "Lukas"]
red_blue_ACTIVE_ = False  # track red and blue shells


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

def get_tracks(dict_path):
  """
  Simple function to get all tracks as dictionary as abbreviation -> full name
  Takes dict_path, the path from the caller to the tracks file
  """
  # Engine Python because otherwise can't have two char separation
  data = pandas.read_csv(dict_path, sep=", ", engine="python")
  abbrevs = data["Abbreviation"]
  full = data["FullName"]
  
  # make into lists and then dictionary
  tracks = dict(zip(list(abbrevs), list(full)))

  return tracks

def setup(relative_path=PATH_TO_COMPS):
  """
  All initial setup. Creates logging file.
  
  Takes the relative path from where it is called to where
  we want to store the data

  Returns:
  names: names of racers
  n_races: number of races
  path: path to directory to which to write
  """
  n_races = chk.run_n_races()

  names = input("Names of racers (defaults to \'Henry\', \'Justus\', " +
                "\'Lukas\' if left blank):\n").split()

  if (not names):
    names = NAMES

  fname = input("Name of file (defaults to current date if left blank): ")

  if (fname == ""):
    date = datetime.date.today()    
    now = datetime.datetime.now()
    fname += str(date) + "_" + str(now.hour) + ":" + str(now.minute)

  fname += ".csv"
  
  path = relative_path + fname

  race = open(path, "w")
  race.write("Track")  # first column are the tracks
  [race.write(", " + name) for name in names]  # add names to column headers
  race.close()

  global red_blue_ACTIVE_
  red_blue_ACTIVE_ = "y" == input("Do you want to track the " +
                                  "number of red and blue shells?[y/n]: ")
  return names, n_races, path

def race_data(names, i, dict_path = PATH_TO_TRACK_DICT):
  """
  Regular Updating function for every race
  Returns the data for the new line to be added
  """
  print(f"\nRace {i+1}.")
  tracks = get_tracks(dict_path)
  track = chk.run_tracks(tracks)

  results = chk.run_results(names)
  
  if (red_blue_ACTIVE_):
    shells = chk.run_RB_shells(names)
    # get full results: place, reds, blues
    results = [[results[i]] + list(shells[names[i]]) for i in range(len(names))] 

  data = [track]
  data += results

  return data  # full line


def log(dict_path = PATH_TO_TRACK_DICT, comps_path=PATH_TO_COMPS):
  names, n, path = setup(comps_path)
  i = 0
  while(i < n):
    data = race_data(names, i, dict_path)
    line = create_line(data)
    add_line(line, path)  # write to path
    i += 1  # increase i


