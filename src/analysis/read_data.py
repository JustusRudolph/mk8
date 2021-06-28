import pandas
import numpy as np
import ast  # list in string representation to list

# define main dictionary
PLACE_POINT = {1:15, 2:12, 3:10, 4:9, 5:8, 6:7, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}

def get_data(path):
  """
  Returns the data from the given path
  """
  # use semicolon to avoid clash with normal list
  full_data = pandas.read_csv(path, sep="; ", engine="python")
  return full_data
  
def check_names(path, names):
  """
  Checks if all names are represented in the data
  """
  full_data = get_data(path)
  headers = list(full_data.columns)

  # check if names are available
  for name in names:
    if (name not in headers):
      print(f"\"{name}\" is not part of the names of this data set: {headers[1:]}.")
      return False

  return True

def get_points(places):
  """
  Assume places is n dimensional array
  """
  tot = sum([PLACE_POINT[place] for place in places])
  return tot

def get_all_name_data(paths, names=None, is_online=False):
  """
  Appends all the runs to each other to create larger data sets
  returns the array of all tracks, and a dictionary of name to positions
  
  Additionally, if the online flag is set to true, then race data
  is also returned. This includes cc, if it is mirror, and number of players.
  """
  tracks = []
  race_data = []
  name_data = {}
  names_init = False  # to check whether name entries in dictionary exists

  if (names is not None):
    names_init = True  # names initialised
    for name in names:
      name_data[name] = []  # initialise empty list for each name to which append data

  for path in paths:
    full_data = get_data(path)
    if (not names_init):
      headers = full_data.columns
      if (is_online):
        names = headers[4:]  # track, cc, mirror, n_players, then it's names
      else:
        names = headers[1:]  # first will be track, from then on it's names

      for name in names:
        name_data[name] = []  # empty list initialised for every name

      names_init = True

    tracks += list(full_data["Track"])

    if (is_online):  # add more data for all the races if online
      for i in range(full_data.shape[0]):  # number of entries
        race_data.append((full_data["CC"][i], full_data["Mirror"][i],
        full_data["nPlayers"][i]
        ))
  
    for name in names:
      # ast used to make string to list representation
      name_data[name] += list(ast.literal_eval(entry) for entry in full_data[name])

  for name in names:
    name_data[name] = np.array(name_data[name])


  return tracks, name_data, race_data  # the latter will be empty for offline