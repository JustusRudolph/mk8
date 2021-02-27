import numpy as np
from statistics import mode

def get_avgs(name_data, tracks = [], track = 0):
  """
  Gets the averages for the given players.
  Returns dictionary with names as keys, averages as values.
  If a certain track is given, that is checked specifically.
  """
  avgs = {}
  names = name_data.keys()
  for name in names:
    if (track and len(tracks)):  # only if both are given we check for specific track
      ii = np.where(tracks == track)[0]  # get indices of track
      # get positions for those indices and that name
      data = np.array([name_data[name][i] for i in range(len(name_data[name])) if i in ii])

    else:
      data = name_data[name]
    
    avg = np.average(data.transpose()[0])
    avgs[name] = avg

  return avgs

def get_std_devs(name_data, tracks = [], track = 0):
  """
  Gets the standard deviations for the given players.
  Returns dictionary with names as keys, standard deviations as values.
  If a certain track is given, that is checked specifically.
  """
  stdds = {}
  names = name_data.keys()
  for name in names:
    if (track and len(tracks)):  # only if both are given we check for specific track
      ii = np.where(tracks == track)[0]  # get indices of track
      # get positions for those indices and that name
      data = np.array([name_data[name][i] for i in range(len(name_data[name])) if i in ii])

    else:
      data = name_data[name]
    
    stdd = np.std(data.transpose()[0])
    stdds[name] = stdd

  return stdds

def get_best_track(name_data, tracks, tracks_check):
  """
  Returns the best track for each player as a dictionary: name -> track
  Returns the position for that player as dictionary: name -> position
  Takes data for each player, corresponding tracks, and which tracks to check for.
  """
  eps = 1e-6  # this is to account for rounding errors when equating later
  avgs_per_track = {}  # this will contain all avgs for each tracks to check for
  best_tracks = {}  # contains best tracks for a name

  names = name_data.keys()
  for track in tracks_check:
    avgs = get_avgs(name_data, tracks, track)
    avgs_per_track[track] = avgs
    
  
  mins = {}
  # get all minimum values for each name
  for name in names:
    mins[name] = (min([avgs_per_track[track][name] for track in tracks_check]))

  # get tracks for which we get this minimum
  for name in names:
    mn = mins[name]
    best_tracks[name] = [track for track in tracks_check if abs(
                         mn - avgs_per_track[track][name]) <= eps]
  

  return(best_tracks, mins)

def get_n_most_occuring(lst, n=1):
  """
  Gets the n most occuring objects in list (or more if there are duplicates)
  Returns dictionary of object in list to number of occurences.
  """
  lst = list(lst)  # assert that it is a list not a numpy array
  assert(n <= len(lst))
  most_occ = {}
  lst_distinct = list(set(lst))
  n_occ = {}
  for elem in lst_distinct:
    n_occ[elem] = lst.count(elem)

  i = 0
  while (i < n):  # get n modes now
    mx = max(n_occ.values())
    elems_mx = list(set([elem for elem in lst_distinct if n_occ[elem] == mx]))  # all tracks w/ max
    for elem in elems_mx:
      most_occ[elem] = n_occ[elem]
      n_occ.pop(elem)  # remove this to find next maxes
      lst_distinct.remove(elem)  # so we don't check for it again
      i += 1  # increment for every element returned

  return most_occ


