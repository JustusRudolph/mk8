import numpy as np
import math
import datetime
import pandas

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
  n_ok = False  # check if number of races acceptable
  while (not n_ok):
    n_races = int(input("Number of races: "))
    if (n_races in ALLOWED_N_RACES):
      n_ok = True
    else:
      print(f"Unacceptable number of races: {n_races}. " +  
            f"Must be one of {ALLOWED_N_RACES}.")
  
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
  track_ok = False  # check if acceptable track
  tracks = get_tracks(dict_path)
  while(not track_ok):
    track = input("Enter Track: ")
    if (track in tracks):  # allowed abbreviation, since abbrevs are keys in dict
      acc = input(f"Logging as {tracks[track]}. Is this correct? [y/n]: ")
      if (acc == "y"):  # allow for changing track if typo
        track_ok = True
      else:
        print("Ok. Try again.\n")
    else:
      print(f"Unknown track abbreviation: \"{track}\". Please try again.")
  
  res_ok = False
  results = []
  while(not res_ok):
    results = [int(res) for res in input(f"Results for {str(names)[1:-1]}: ").split()]
    np_res = np.array(results)
    if (all((np_res > 0)*(np_res < 13))):  # check if between 1st and 12th place    
      res_ok = True
    else:
      print("Those results are not acceptable. Must be between 1 and 12.")
  
  #print(red_blue_ACTIVE_)
  #input()
  if (red_blue_ACTIVE_):
    rb_ok = False
    while (not rb_ok):
      reds = [int(red) for red in input(f"Red shells for {str(names)[1:-1]}: ").split()]
      blues = [int(blue) for blue in input(f"Blue Shells for {str(names)[1:-1]}: ").split()]
      shells = dict(zip(names, zip(reds, blues)))
      rb_ok = "y" == input(f"We have: {shells}.\nIs this correct?[y/n] ")
      if (not rb_ok):
        print("Ok, try again.\n")
    
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


