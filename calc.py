import pandas
import numpy
from log_race import get_tracks

# define main dictionary
PLACE_POINT = {1:15, 2:12, 3:10, 4:9, 5:8, 6:7, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}

def get_data(path):
  """
  Returns the data from the given path
  """
  full_data = pandas.read_csv(path, sep=", ", engine="python")
  return full_data
  
def check_names(full_data, names):
  """
  Checks if all names are represented in the data
  """
  headers = list(full_data.columns)

  # check if names are available
  for name in names:
    if (name not in headers):
      print(f"{name} is not part of the names of this data set: {headers_stripped}.")
      return False

  return True

def get_tot_points(places):
  """
  Assume places is n dimensional array
  """
  tot = sum[PLACE_POINT[place] for place in places]
  return tot

def name_with_tot():
  
