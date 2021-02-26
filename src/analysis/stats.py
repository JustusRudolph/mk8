import numpy as np

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
