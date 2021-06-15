import numpy as np
import math
import datetime
import pandas

from . import mk_checks as chk

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
      line += "; "  # delimiter

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


def setup(relative_path, is_online=False):
  """
  All initial setup. Creates logging file.
  
  Takes the relative path from where it is called to where
  we want to store the data

  Returns:
  names: names of racers
  n_races: number of races
  path: path to directory to which to write
  """
  n_races = 1  # necessary for checking if online in log()
  if (not is_online):
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

  if (not is_online):  # only check which CC if not online
    cc, is_mirror = chk.run_cc()

    fname += "_"
    fname += str(cc)
    fname += "M" * is_mirror  # add M in case of mirror

  fname += ".csv"

  if (is_online):
    relative_path += "_online/"
  else:
    relative_path += "/"  # the slash is important bro
  
  path = relative_path + fname

  race = open(path, "w")
  race.write("Track")  # first column are the tracks

  if (is_online):
    race.write("; CC; Mirror; AvgRating")  # these fields are not necessary offline

  [race.write("; " + name) for name in names]  # add names to column headers
  race.close()

  global red_blue_ACTIVE_
  red_blue_ACTIVE_ = "y" == input("Do you want to track the " +
                                  "number of red and blue shells?[y/n]: ")
  return names, n_races, path

def race_data(names, i, dict_path, is_online=False):
  """
  Regular Updating function for every race
  Returns the data for the new line to be added
  """
  print(f"\nRace {i+1}.")
  tracks = get_tracks(dict_path)

  track = chk.run_tracks(tracks)
  data = [track]

  if (is_online):  # Three fields only used in online
    cc, is_mirror = chk.run_cc()
    avg_rat = chk.run_avg_rat()
    
    data.append(cc)
    data.append(int(is_mirror))
    data.append(avg_rat)


  results = chk.run_results(names)
  
  if (red_blue_ACTIVE_):
    shells = chk.run_RB_shells(names)
    # get full results: place, reds, blues
    results = [[results[i]] + list(shells[names[i]]) for i in range(len(names))]

  data += results

  return data  # full line


def log(dict_path, comps_path, is_online=False):
  names, n, path = setup(comps_path, is_online=is_online)
  i = 0
  while(i < n):
    data = race_data(names, i, dict_path, is_online=is_online)
    line = create_line(data)
    add_line(line, path)  # write to path
    
    if (is_online):
      n += 1  # increase n if playing online so never timeout
    
    i += 1


