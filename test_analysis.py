"""
This file is for testing the calculations from calc and advanced calc
"""
import os  # for directory listing
import pandas

from datetime import date

from src.log import log_race as lr
from src.analysis import read_data as rd
from src.analysis import stats as st

COMPS_PATH = "src/.comps/"

def main():
  today_only = False
  all_runs = [COMPS_PATH + run for run in os.listdir(COMPS_PATH)]  # all paths
  all_tracks = lr.get_tracks("src/data/tracks.csv")  # dictionary of tracks


  today = str(date.today())

  runs_today = [run for run in all_runs if today in run]
  runs_with_redblues = [run for run in all_runs if "2021" in run]
  
  names = ["Lukas", "Henry", "Justus"]
  assert(rd.check_names(all_runs[0], names))  # names need to be accepted

  tracks, name_data = rd.get_all_name_data(runs_with_redblues, names)

  if (today_only):
    tracks, name_data = rd.get_all_name_data(runs_today, names)

  n_races = len(tracks)

  print(f"Number of races: {n_races}")
  for name in names:
    # column 0 is place, 1 is reds, 2 is blues
    # make it rows so numpy is happy and it looks neat

    pts = rd.get_points(name_data[name].transpose()[0])
    n_reds = sum(name_data[name].transpose()[1])
    n_blues = sum(name_data[name].transpose()[2])
    print(f"{name} got {pts} points. Average: {pts/float(n_races):.2f}. "+
          f"Hit by red {n_reds} times. Hit by blue {n_blues} times.")

  print()
  input()
  distinct_tracks = list(set(tracks))
  # check for best tracks for each person
  best_tracks, best_pos = st.get_best_track(name_data, tracks, distinct_tracks)

  
  for name in names:
    fav_tracks = [all_tracks[track] for track in best_tracks[name]]
    print(f"The favourite track(s) of {name}, with an average position"+
          f" of {best_pos[name]:.2f} are: {fav_tracks}.")


  print()
  common_tracks = st.get_n_most_occuring(tracks, 1)
  common_tracks_full = {}
  for key in common_tracks.keys():
    common_tracks_full[all_tracks[key]] = common_tracks[key]

  print(f"Most played track(s): {common_tracks_full}")
  
  not_played_yet = []
  for track in all_tracks:
    n_occs = list(tracks).count(track)
    if (not n_occs):
      not_played_yet.append(all_tracks[track])

  print(f"Did not play the following track(s): {not_played_yet}")

  ex = "ccb"
  avg_example = st.get_avgs(name_data, tracks, ex)
  print()
  print(f"{all_tracks[ex]}")
  for name in names:
    print(f"{name} got on average position {avg_example[name]} in {all_tracks[ex]}.")
 
  if (input("\nDo you want to view the frequency plot?[y/n]: ") == "y"):
    st.plot_occurences(tracks)

main()
