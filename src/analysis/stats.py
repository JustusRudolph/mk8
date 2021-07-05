import numpy as np
from statistics import mode
import matplotlib.pyplot as plt


def get_avgs(name_data, tracks = [], track = 0, is_online=False):
  """
  Gets the averages for the given players. Rating only returned for online.
  Returns dictionary with names -> averages (pos, rating, reds, blues).
  If a certain track is given, that is checked specifically.
  """
  avgs = {}
  names = name_data.keys()
  for name in names:
    if (track and len(tracks)):  # only if both are given we check for specific track
      ii = np.where(np.array(tracks) == track)[0]  # get indices of track
      # get positions for those indices and that name
      data = np.array([name_data[name][i] for i in ii])

    else:
      data = name_data[name]
    
    avg = []
    n_fields = 3 + is_online  # TODO: len(name_data[name][0]), check what this is
    for i in range(n_fields):
      avg.append(np.average(data.transpose()[i]))
    avgs[name] = avg  # now [avg_pos, avg_reds, avg_blues]

  return avgs

def get_std_devs(name_data, tracks = [], track = 0, is_online=False):
  """
  Gets the standard deviations for the given players. Rating only returned for online.
  Returns dictionary with names -> standard deviations (pos, rating, reds, blues).
  If a certain track is given, that is checked specifically.
  """
  stdds = {}
  names = name_data.keys()
  for name in names:
    if (track and len(tracks)):  # only if both are given we check for specific track
      ii = np.where(np.array(tracks) == track)[0]  # get indices of track
      # get positions for those indices and that name
      data = np.array([name_data[name][i] for i in ii])

    else:
      data = name_data[name]
    
    stdd = []
    n_fields = 3 + is_online  # TODO: len(name_data[name][0]), check what this is
    for i in range(n_fields):
      stdd.append(np.std(data.transpose()[i]))
    
    stdds[name] = stdd

  return stdds

def get_best_worst_track(name_data, tracks, tracks_check, best=True):
  """
  Returns the best/worst track for each player as a dictionary: name -> track
  Returns the position for that player as dictionary: name -> position
  Takes data for each player, corresponding tracks, and which tracks to check for.
  The last bool states whether to check for best or worst track
  """
  eps = 1e-6  # this is to account for rounding errors when equating later
  avgs_per_track = {}  # this will contain all avgs for each tracks to check for
  best_tracks = {}  # contains best tracks for a name

  names = name_data.keys()
  for track in tracks_check:
    avgs = get_avgs(name_data, tracks, track)
    avgs_per_track[track] = {}  # initialise empty
    for name in names:  # write avg position for each name for that track
      avgs_per_track[track][name] = avgs[name][0]  # 0th field is position
    
  min_max = {}
  if (best):
    # get minimum avg osition for each name
    for name in names:
      min_max[name] = min([avgs_per_track[track][name] for track in tracks_check])

  else:  # so if we want worst
    # get maximum avg position for each name
    for name in names:
      min_max[name] = (max([avgs_per_track[track][name] for track in tracks_check]))

  
  # get tracks for which we get this min/max position
  for name in names:
    mn = min_max[name]
    best_tracks[name] = [track for track in tracks_check if abs(
                        mn - avgs_per_track[track][name]) <= eps]


  return (best_tracks, min_max)  # best_tracks can be "worst tracks" too

def get_n_most_occuring(lst, n=1):
  """
  Gets the n most occuring objects in list (or more if there are duplicates)
  Returns dictionary of object (from lst) -> number of its occurences in lst.
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

def plot_occurences(data, subheaders=[], plot_tracks=False, typ="position", plt_total=False):
  """
  Takes a 2d list/array and plots the number occurences of elements
  in each row. Different rows will be plotted next to each other.
  The subheaders field is required for the subplots in case of several rows.
  These will just appear on top of the plots.
  plot_tracks is to see how many tracks have not been played. Hence
  this is set to true if tracks are to be plotted
  """
  distinct_elems = []
  ns = []
  for i in range(len(data)):
    lst = list(data[i])  # ensure list to enable counting
    #print(lst)
    #input()
    distinct_elems.append(list(set(lst)))
    ns.append([])  # list of occurence of certain element
    for elem in distinct_elems[i]:
      #print(elem)
      #input()
      n = lst.count(elem)
      ns[i].append(n)



  if (plot_tracks):
    distinct_ns = list(set(ns[0]))  # tracks will always only be one list
    freqs = [] # frequency of certain occurence of elements

    for n in distinct_ns:
      freqs.append(ns[0].count(n))

    if (sum(freqs) < 48):
      f_zero = 48 - sum(freqs)
      freqs.insert(0, f_zero)
      distinct_ns.insert(0, 0)

    # have freqs and distinct_ns now as dependend/independent
    # This is for tracks only, which are not numbers
    plt.plot(distinct_ns, freqs, "o")
    plt.xlabel(f"Occurence of {typ}")
    plt.ylabel("Frequency")
    plt.title(f"Frequency sketch: Frequency of number of {typ} occurences.")
    plt.show()

  else:
    if (len(data) > 1):
      # ax1 will have all the initial one, with ax2 having the total
      fig, (ax1, ax2) = plt.subplots(1, 2)
      fig.suptitle(f"Frequency sketch: Frequency of number of {typ} occurences.")
      
      for i in range(len(data)):
        ax1.plot(distinct_elems[i], ns[i], "o", )
        ax1.set(xlabel=f"Occurence of {typ}", ylabel="Frequency")
      if (len(data) > 1):  # if we have more than one name
        ax1.legend(subheaders)
        ax1.set_title("Individual")

      if (plt_total):
        # now get total data:
        all_distincts = []
        for dist in distinct_elems:
          for elem in dist:
            if elem not in all_distincts:
              all_distincts.append(elem)

        all_ns = np.zeros(len(all_distincts), dtype=np.int64)
        for ns_for_each in ns:
          for i in range(len(ns_for_each)):
            all_ns[i] += ns_for_each[i]

        ax2.plot(all_distincts, all_ns, "ko")
        ax2.set(xlabel=f"Occurence of {typ}", ylabel="Frequency")
        ax2.set_title("Total")

    else:
      plt.plot(distinct_elems[0], ns[0], 'o')
      plt.xlabel("Occurence of {typ}")
      plt.ylabel("Frequency")
      title = f"Frequency sketch: Frequency of number of {typ} occurences."
      if (len(subheaders) > 0):
        title += f"\nThis is for {subheaders[0]}."
      plt.title(title)

    plt.show()


