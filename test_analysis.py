"""
This file is for testing the calculations from calc and advanced calc
"""
import os  # for directory listing
import pandas

from datetime import date

from src.log import log_race as lr
from src.analysis import analysis as an

COMPS_PATH = "src/.comps/"

def get_runs(today_only=False):
  runs = [COMPS_PATH + run for run in os.listdir(COMPS_PATH)]  # all paths

  today = str(date.today())

  if (today_only):
    runs = [run for run in all_runs if today in run]

  return runs

def get_all_tracks():
    all_tracks = lr.get_tracks("src/data/tracks.csv")  # dictionary of tracks
    return all_tracks

def print_prompts():
  total_string =  "Get data for each player:                        [1]\n"
  total_string += "Get favourite tracks for each player:            [2]\n"
  total_string += "Get the most frequent tracks:                    [3]\n"
  total_string += "Get which tracks have been played/not played:    [4]\n"
  total_string += "Get the average and standard deviation of full\n"
  total_string += "data (position, reds, blues) for each player:    [5]\n"
  total_string += "Plot occurences of tracks, positions or shells:  [6]\n"
  total_string += "Quit:                                            [q]\n"
  print(total_string)

def setup_analyse():
  print("This is the Mario Kart track analyser.")

  runs = get_runs(input("Do you want to use the tracks only of today?[y/n]: ") == "y")
  all_tracks = get_all_tracks()
  
  analyse = an.Analysis(runs, all_tracks)
  return analyse

def run(analyse):
  quit = False
  choices = ['1','2','3','4','5','6','q']  # current acceptable choices
  while (not quit):
    choice = 0
    while (choice not in choices):
      print("Hi! What do you want to do?")
      print_prompts()
      choice = input("Choose one of these options[1-6] or quit[q]: ")
      if (choice not in choices):
        print(f"Not recognised choice {choice}. Please try again.")
        print("\n\n\n\n")

    print("\n\n")
    if (choice == '1'):
      analyse.get_total_name_data(print_enabled=True)

    elif (choice == '2'):
      analyse.get_fav_tracks(print_enabled=True)

    elif (choice == '3'):
      # TODO(Justus) Check that only ints are accepted
      n = int(input("Number of most common tracks you want to see: "))
      analyse.get_n_freq_tracks(n, print_enabled=True)

    elif (choice == '4'):
      val = input("Do you want to see the tracks played?[y/n]: ")
      played = val == "y"
      analyse.tracks_played(print_enabled=True, print_played=played)

    elif (choice == '5'):
      check_track = input("Do you want to check for a specific track?[y/n]: ")
      if (check_track == "y"):
        track_choice = 0
        while (track_choice not in analyse.tracks):
          track_choice = input("Enter track abbreviation: ")
          if (track_choice not in analyse.tracks):
            print(f"Not recognised track: {track_choice}. Please try again.")

        analyse.get_avg_and_std(track=track_choice, print_enabled=True)

      else:  # so if no specific track
        analyse.get_avg_and_std(print_enabled=True)

    elif (choice == '6'):
      plot_track_val = input("Do you want to print track occurences?[y/n]: ")
      if (plot_track_val == 'y'):
        analyse.plot_track_occurences()
    
      else:
        types = {'p': "position", 'r': "red", 'b': "blue"}
        print("Okay, opting to plot data instead.")
        tp = 0
        while (tp not in types.keys()):
          tp = input("What do you want to plot? Positions, reds or blues?[p/r/b]: ")
          if (tp not in types.keys()):
            print(f"Not recognised type to plot: {tp}. Please try again.")
        
        specific_name = input("Do you want to plot for a specific name?[y/n]: ")
        if (specific_name == 'y'):
          nm = 0
          while (nm not in analyse.names):
            nm = input("Enter name: ")
            if (nm not in analyse.names):
              print(f"No data available for name: {nm}. Please try again.")
          analyse.plot_data_occurences(name=nm, typ=types[tp])

        else:  # don't care about specific name
          analyse.plot_data_occurences(typ=types[tp])

    elif (choice == 'q'):
      return 0  # quit programme


def main():
  analyse = setup_analyse()
  run(analyse)  

main()
