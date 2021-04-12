import numpy as np
from . import read_data as rd
from . import stats as st

class Analysis:

  def __init__(self, paths, track_dict, names=None):
    """
    paths: paths from which to get data
    names: List of names for which to check. Defaults to None
           and just uses all names from the given paths.
    """
    tracks, name_data = rd.get_all_name_data(paths, names)

    self.n_races = len(tracks)
    self.names = name_data.keys()
    self.tracks = tracks
    self.name_data = name_data
    self.track_dict = track_dict

    print(f"Setup of Analysis complete. {self.n_races} races have been played.")
  
  def get_total_name_data(self, print_enabled=False):
    """
    Returns the total data for each player, as well as the
    average data per game. Data is position, number of reds
    and number of blues.

    User can select if they wish to print result or not. If print is
    requested, nothing is returned either.
    """
    data = {}  # will contain [points, n_reds, n_blues] for each player
    data_per_game = {}  # the above but per game

    for name in self.names:
      pts = rd.get_points(self.name_data[name].transpose()[0])
      n_reds = sum(self.name_data[name].transpose()[1])
      n_blues = sum(self.name_data[name].transpose()[2])
      data[name] = [pts, n_reds, n_blues]
      data_per_game[name] = [float(pts)/self.n_races, float(n_reds)/self.n_races, 
                             float(n_blues)/self.n_races]

    if (print_enabled):
        for name in self.names:
          print(f"{name} got {data[name][0]} points. Hit by red " +
          f"{data[name][1]} times. Hit by blue {data[name][2]} times.")
          print("This corresponds to averages of: Score: "+
                f"{data_per_game[name][0]:.2f}, Reds: {data_per_game[name][1]:.2f}"+
                f", Blues: {data_per_game[name][2]:.2f}.\n")
        
        print("\n")  # Just add a newline at the end

    else:
      return data, data_per_game

  def get_fav_tracks(self, print_enabled=False, best=True):
    """
    Gets the favourite tracks of each player. Also here,
    the user can select to print or not. If user decides
    to print, nothing will be returned.

    best bool checks if we want to find best or worst tracks
    """
    distinct_tracks = list(set(self.tracks))
    # check for best tracks for each person
    best_tracks, pos = st.get_best_worst_track(self.name_data, self.tracks,
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

  def get_n_freq_tracks(self, n, print_enabled=False):
    """
    Get the n most frequent tracks from central data.
    print_enabled can be set by user if print is requested. This
    will mean that nothing is returned either.
    """
    common_tracks = st.get_n_most_occuring(self.tracks, n)
    
    if (print_enabled):
      common_tracks_full = {}
      for trk in common_tracks.keys():
        common_tracks_full[self.track_dict[trk]] = common_tracks[trk]
      
      print(f"Most played track(s): {common_tracks_full}.\n\n")


    else:
      return common_tracks

  def tracks_played(self, print_enabled=False, print_played=False):
    """
    Returns which tracks have been played. The print_enabled flag
    determines whether or not to print the tracks at all. If enabled,
    nothing will be returned. The print_played flag determines whether 
    to print the played tracks (True) or the not played tracks (False).
    """
    distinct_tracks = list(set(self.tracks))

    if (print_enabled):
      tracks_to_print = []
      for track in self.track_dict.keys():
        n_occs = list(self.tracks).count(track)
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

  def get_avg_and_std(self, track=0, print_enabled=False):
    """
    Returns average and standard deviations for a given track for a player.
    If the track is not given, the player's average and standard deviations
    are returned for every single race played taken into account.
    If print_enabled is set, then this will print, but not return.

    Returns:
    avg: Dictionary of name -> avgs, where avgs is average position, reds, blues
    std: Same as above but for standard deviations
    """
    if (not track):
      avg = st.get_avgs(self.name_data)
      std = st.get_std_devs(self.name_data)

      if (print_enabled):
          print("Averages for all tracks:")
          for name in self.names:
            print(f"{name}:\nPosition: {avg[name][0]:.2f} +- {std[name][0]:.2f}"+
                  f" || Reds: {avg[name][1]:.2f} +- {std[name][1]:.2f} || " +
                  f"Blues: {avg[name][2]:.2f} +- {std[name][2]:.2f}")

          print("\n")  # add newline at end

      else:
        return avg, std

    elif (track not in self.tracks):
      print("Track not played yet.")
      return (-1, -1)  # to simulate issue
    
    else:
      avg = st.get_avgs(self.name_data, self.tracks, track)
      std = st.get_std_devs(self.name_data, self.tracks, track)
      
      if (print_enabled):
          print(f"Averages for {self.track_dict[track]}:")
          for name in self.names:
            print(f"{name}:\nPosition: {avg[name][0]:.2f} +- {std[name][0]:.2f}" +
                  f" || Reds: {avg[name][1]:.2f} +- {std[name][1]:.2f} || " +
                  f"Blues: {avg[name][2]:.2f} +- {std[name][2]:.2f}")

          print("\n")  # add newline at end
      
      else:
        return avg, std

  def plot_track_occurences(self):
    st.plot_occurences(self.tracks, plot_tracks=True, typ="track")

  def plot_data_occurences(self, name=0, typ="position"):
    """
    If no name is given, then occurences of everyone
    is plotted.
    The typ indicates what is to be plotted. Allowed values
    are "position", "red", "blue"
    """
    if (typ == "position"):
      i = 0
    elif (typ == "red"):
      i = 1
    elif (typ == "blue"):
      i = 2
    else:
      print(f"{typ} is not an accepted type of data. Choose from:" +
            "\"position\", \"red\", \"blue\"")
      return -1

    if (not name):
      data = []
      for nm in self.names:
        data_i = self.name_data[nm].transpose()[i]
        data += list(data_i)

      st.plot_occurences(data, typ=typ)

    else:
      st.plot_occurences(self.name_data[name].transpose()[i], typ=typ)

    

