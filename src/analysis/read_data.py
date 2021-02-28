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

def get_all_name_data(paths, names):
  """
  Appends all the runs to each other to create larger data sets
  returns the array of all tracks, and a dictionary of name to positions
  """
  tracks = []
  name_data = {}
  for name in names:
    name_data[name] = []  # empty list to be appended

  for path in paths:
    full_data = get_data(path)
    tracks += list(full_data["Track"])
    for name in names:
      # ast used to make string to list representation
      name_data[name] += list(ast.literal_eval(entry) for entry in full_data[name])

  # make into np arrays
  tracks = np.array(tracks)
  for name in names:
    name_data[name] = np.array(name_data[name])

  return tracks, name_data
