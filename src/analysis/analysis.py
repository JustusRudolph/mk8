import numpy as np

from . import read_data as rd
from . import stats as st

ALLOWED_CCS = [50, 100, 150, 200]

class Analysis:

  def __init__(self, paths, track_dict, names=None, online=False):
    """
    paths: paths from which to get data
    names: List of names for which to check. Defaults to None
           and just uses all names from the given paths.
    """

    tracks, name_data, race_data = rd.get_all_name_data(paths, names, is_online=online)

    self.n_races = len(tracks)  # integer
    self.names = list(name_data.keys())  # list of strings
    self.tracks = tracks  # list of strings
    self.name_data = name_data  # dictionary of name -> 2d np.array of size (n_races, 3+is_online)
    self.track_dict = track_dict  # dictionary of string -> string (abbreviation to full name)
    
    # online fields
    self.is_online = online  # boolean
    self.race_data = race_data  # np.array of tuples of length 3: (int, bool(0/1), int)

    # these will change throughout, constrained data
    self.constr_name_data = name_data.copy()
    self.constr_race_data = race_data.copy()
    self.constr_tracks = tracks.copy()


    print(f"Setup of Analysis complete. {self.n_races} races have been played.\n")
  
  def constrain_data(self, ccs=ALLOWED_CCS, mirror=None, player_range=(2,12)):
    """
    This is a simple function to constrain name data based on arguments
    given by the user. The constraints are based on the three fields 'cc',
    'mirror' and 'n_players'. These can be extended later on to include
    newer fields, as it is not difficult to add another constraint. E.g.
    reds and blues could be added.

    Note that if Mirror is set to true, only 150cc will be recorded. However if it
    is false, the system assumes that the user might want to compare for all ccs with
    all tracks non-mirrored. The user must then set 

    This function writes over self.constr_* fields which can then be
    accessed by other functions.
    """
    print("In constrain_data in analysis.py")
    print(f"ccs: {ccs}, mirror: {mirror}, range: {player_range}")

    assert(self.is_online)  # this should only be called with online
    ii = np.arange(self.n_races)  # baseline is no constraint

    # first check if there is a constraint on mirror
    if (mirror is not None):
      ii_mirror = np.where(np.array(self.race_data[:, 1]) == mirror)[0]  # 1st index is mirror flag
      ii = ii_mirror

    if (not mirror):
      # then check the races with correct cc if mirror is not set to true
      if (ccs != ALLOWED_CCS):
        ii_cc = []
        for cc in ccs:
          ii_cc += list(np.where(np.array(self.race_data[:, 0]) == cc)[0])  # 0th index is cc

        ii = ii[ii_cc]  # select only those
      
    if ((player_range[0] > 2) or player_range[1] < 12):
      ii_del = []  # the indices to delete from ii. This is the INDEX of INDICES of RACES

      for i in range(self.n_races):
        n_players = self.race_data[i][2]  # nPlayers is the 2nd field (CC, Mirror, nPlayers)

        if (n_players < player_range[0]) or (n_players > player_range[1]):  # if outside bounds
          ii_del.append(np.where(ii == i)[0][0])  # the index of the index stored in ii

      ii = np.delete(ii, ii_del)  # deletes the necessary indices from the list of indices

    for name in self.names:
      self.constr_name_data[name] = self.name_data[name][ii]  # select those indives

    self.constr_race_data = self.race_data[ii]

    print(f"\nName_data: {self.constr_name_data}")
    input()

    self.constr_tracks = [self.tracks[i] for i in ii]

    return 0
  
  def get_total_name_data(self, print_enabled=False, constr=False):
    """
    Returns the total data for each player, as well as the
    average data per game. Data is position, number of reds
    and number of blues.

    User can select if they wish to print result or not. If print is
    requested, nothing is returned either.

    The constr field is used for the user to select whether they want
    to use previously constrained data or the full data.
    """

    data = {}  # will contain [points, (d_rat), n_reds, n_blues] for each player dep. on online
    data_per_game = {}  # the above but per game

    if (constr):
      name_data = self.constr_name_data

    else:
      name_data = self.name_data

    for name in self.names:
      pts = rd.get_points(name_data[name].transpose()[0])
      n_reds = sum(name_data[name].transpose()[-2])  # Reds always 2nd last
      n_blues = sum(name_data[name].transpose()[-1])  # Blues always last
      
      if (self.is_online):
        d_rat = sum(name_data[name].transpose()[1])

        data[name] = [pts, d_rat, n_reds, n_blues]
        data_per_game[name] = [float(pts)/self.n_races, float(d_rat)/self.n_races,
                               float(n_reds)/self.n_races, float(n_blues)/self.n_races]

      else:
        data[name] = [pts, n_reds, n_blues]
        data_per_game[name] = [float(pts)/self.n_races, float(n_reds)/self.n_races,
                               float(n_blues)/self.n_races]
        

    if (print_enabled):
        for name in self.names:
          # print totals
          print(f"{name} got {data[name][0]} points. Hit by red " +
          f"{data[name][-2]} times. Hit by blue {data[name][-1]} times.", end='')
          if (self.is_online):
            print(f" Total rating change: {data[name][1]}")
          
          else:
            print()  # still need newline
          
          # Now per game
          print("This corresponds to averages of: Score: "+
                f"{data_per_game[name][0]:.2f}, Reds: {data_per_game[name][-2]:.2f}"+
                f", Blues: {data_per_game[name][-1]:.2f}.", end='')
          if (self.is_online):
            print(f" Rating change: {data_per_game[name][1]}.\n")
          else:
            print("\n")
        
        print("\n")  # Just add a newline at the end

    else:
      return data, data_per_game

  def get_fav_tracks(self, print_enabled=False, best=True, constr=False):
    """
    Gets the favourite tracks of each player. Also here,
    the user can select to print or not. If user decides
    to print, nothing will be returned.

    best bool checks if we want to find best or worst tracks

    constr field is to ensure user can select constrained or full data
    """
    # select which data to use
    if (constr):
      name_data = self.constr_name_data
      tracks = self.constr_tracks

    else:
      name_data = self.name_data
      tracks = self.tracks

    distinct_tracks = list(set(tracks))

    best_tracks, pos = st.get_best_worst_track(name_data, tracks,
                                              distinct_tracks, best=best)
    if (print_enabled):
      for name in self.names:
        fav_tracks = [self.track_dict[track] for track in best_tracks[name]]
        to_print = "The "
        if (not best):
          to_print += "least "
        to_print += f"favourite track(s) of {name}, with an average position"
        to_print += f" of {pos[name]:.2f} are: {fav_tracks}."
        print(to_print)
    
      print("\n")  # add double newline at the end

    else:
      return best_tracks, pos

  def get_n_freq_tracks(self, n, print_enabled=False, constr=False):
    """
    Get the n most frequent tracks from central data.
    print_enabled can be set by user if print is requested. This
    will mean that nothing is returned either.

    constr field is to ensure user can select constrained or full data
    """
    if (constr):
      tracks = self.constr_tracks
    
    else:
      tracks = self.tracks

    common_tracks = st.get_n_most_occuring(tracks, n)
    
    if (print_enabled):
      common_tracks_full = {}
      for trk in common_tracks.keys():
        common_tracks_full[self.track_dict[trk]] = common_tracks[trk]
      
      print(f"Most played track(s): {common_tracks_full}.\n\n")


    else:
      return common_tracks

  def tracks_played(self, print_enabled=False, print_played=False, constr=False):
    """
    Returns which tracks have been played. The print_enabled flag
    determines whether or not to print the tracks at all. If enabled,
    nothing will be returned. The print_played flag determines whether 
    to print the played tracks (True) or the not played tracks (False).
    
    constr field is to ensure user can select constrained or full data
    """
    if (constr):
      tracks = self.constr_tracks
    else:
      tracks = self.tracks

    distinct_tracks = list(set(tracks))

    if (print_enabled):
      tracks_to_print = []
      for track in self.track_dict.keys():
        n_occs = list(tracks).count(track)
        # Note for below: will only enter either if statement, can
        # never enter both for any n_occs. Depends on the initial flag
        if ((not n_occs) and (not print_played)):  # print the non played ones
          tracks_to_print.append(self.track_dict[track])

        elif (n_occs and print_played):  # print the played ones
          tracks_to_print.append(self.track_dict[track])
      
      # choose what to print based on whether played or not played
      if (print_played):
        print(f"Played the following track(s): {tracks_to_print}.")
      else:
        print(f"Did not play the following track(s): {tracks_to_print}.")
      
      print("\n")

    else:
      return distinct_tracks

  def get_avg_and_std(self, track=0, print_enabled=False, constr=False):
    """
    Returns average and standard deviations for a given track for a player.
    If the track is not given, the player's average and standard deviations
    are returned for every single race played taken into account.
    If print_enabled is set, then this will print, but not return.

    constr field is to ensure user can select constrained or full data

    Returns:
    avg: Dictionary of name -> avgs, where avgs is average position, reds, blues
    std: Same as above but for standard deviations
    """
    if (constr):
      name_data = self.constr_name_data
      tracks = self.constr_tracks
    else:
      name_data = self.name_data
      tracks = self.tracks

    if (not track):
      avg = st.get_avgs(name_data)
      std = st.get_std_devs(name_data)

      if (print_enabled):
          print("Averages for all tracks:")
          for name in self.names:
            print(f"{name}:\nPosition: {avg[name][0]:.2f} +- {std[name][0]:.2f}"+
                  f" || Reds: {avg[name][-2]:.2f} +- {std[name][-2]:.2f} || " +
                  f"Blues: {avg[name][-1]:.2f} +- {std[name][-1]:.2f}", end='')
            
            if (self.is_online):
              print(f" || Rating change: {avg[name][1]:.2f} +- {std[name][1]:.2f}")
            else:
              print()

          print("\n")  # add newline at end

      else:
        return avg, std

    elif (track not in self.tracks):
      print("Track not played yet.")
      return (-1, -1)  # to simulate issue
    
    else:
      avg = st.get_avgs(name_data, tracks, track)
      std = st.get_std_devs(name_data, tracks, track)
      
      if (print_enabled):
          print(f"Averages for {self.track_dict[track]}:")
          for name in self.names:
            print(f"{name}:\nPosition: {avg[name][0]:.2f} +- {std[name][0]:.2f}" +
                  f" || Reds: {avg[name][-2]:.2f} +- {std[name][-2]:.2f} || " +
                  f"Blues: {avg[name][-1]:.2f} +- {std[name][-1]:.2f}", end='')

            if (self.is_online):
              print(f" || Rating change: {avg[name][1]:.2f} +- {std[name][1]:.2f}")
            else:
              print()

          print("\n")  # add newline at end
      
      else:
        return avg, std

  def plot_track_occurences(self, constr=False):
    """
    Just a little cheeky plotter calling a function which basically already does
    all of the work.

    constr field is to ensure user can select constrained or full data
    """
    if (constr):
      tracks = self.constr_tracks
    else:
      tracks = self.tracks

    st.plot_occurences([tracks], plot_tracks=True, typ="track")

  def plot_data_occurences(self, name=0, typ="position", constr=False):
    """
    If no name is given, then occurences of everyone
    is plotted.
    The typ indicates what is to be plotted. Allowed values
    are "position", "red", "blue" and "drating" in case of online
    """
    if (typ == "position"):
      i = 0
    elif (typ == "red"):
      i = -2
    elif (typ == "blue"):
      i = -1
    elif (typ == "drating" and self.is_online):
      i = 1
    elif (typ == "rating"):  # this will only be if not online
      print("Cannot choose rating change because these races are not online. " +
            "Please try again")
      return -2
    else:
      to_print = f"{typ} is not an accepted type of data. "
      to_print += "Choose from: \"position\", \"red\", \"blue\""
      to_print += ", \"rating change\"" * self.is_online
      print()
      return -1

    if (constr):
      name_data = self.constr_name_data
    else:
      name_data = self.name_data

    # print("Name_data in plot_data_occurences in analysis.py")
    # print(name_data)
    # input()

    if (not name):
      data = []
      for nm in self.names:
        data_i = name_data[nm].transpose()[i]
        data.append(data_i)  # individual data per name

      subhders = self.names
      st.plot_occurences(data, subheaders=subhders, typ=typ, plt_total=True)

    else:

      st.plot_occurences([name_data[name].transpose()[i]], subheaders=[name], typ=typ)

    
  def constrain_cc(self):
    """
    Function to be called from analyse.py to constrain the cc to only include
    that which the user requests. Returns the ccs.
    """
    while (True):
      ccs = input("Please enter the CCs you would like to keep: ").split()
      ccs = [int(cc) for cc in ccs]
      if (all([cc in ALLOWED_CCS for cc in ccs])):
        return ccs

      else:
        print(f"Not all CCs you entered were accepted: {ccs}.")
        print("Please try again.\n")

  def constrain_mirror(self):
    """
    Function to be called from analyse.py to constrain the mirror flag to only include
    that which the user requests. Returns the flag.
    """
    mirror = input("Set mirror flag to true?[y/n]: ")
    return mirror == 'y'

  def constrain_players(self):
    """
    Function to be called from analyse.py to constrain the number of players
    to only include the range which the user requests. Returns the range.
    """
    while (True):
      rng = input("Please enter a range of players: ").split()
      rng = list(map(int, rng))

      if (len(rng) > 2):
        print("More than two arguments entered. Ignoring all but the first two.")
      
      low = min(rng[:2])
      upp = max(rng[:2])

      if ((low >= 2) and (upp <= 12)):
        return (low, upp)

      else:
        print(f"Not acceptable range: ({low}, {upp}). Please try again.")
        print("\n")