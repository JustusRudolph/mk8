"""

This file is for testing the calculations from calc and advanced calc
"""
import os  # for directory listing
import pandas

from datetime import date

from src.log import log_race as lr
from src.analysis import analysis as an

COMPS_PATH = "src/.comps/"
COMPS_PATH_ON = "src/.comps_online/"

def get_runs(today_only=False, is_online=False):
  
  if (is_online):
    runs = [COMPS_PATH_ON + run for run in os.listdir(COMPS_PATH_ON)]  # all paths
  else:
    runs = [COMPS_PATH + run for run in os.listdir(COMPS_PATH)]  # all paths

  today = str(date.today())

  if (today_only):
    runs = [run for run in runs if today in run]

  return runs

def get_all_tracks():
    all_tracks = lr.get_tracks("src/data/tracks.csv")  # dictionary of tracks
    return all_tracks

def print_prompts(analyse):
  total_string =  "Get data for each player:                        [1]\n"
  total_string += "Get favourite and least favourite tracks:        [2]\n"
  total_string += "Get the most frequent tracks:                    [3]\n"
  total_string += "Get which tracks have been played/not played:    [4]\n"
  total_string += "Get the average and standard deviation of full\n"
  total_string += "data (position, reds, blues) for each player:    [5]\n"
  total_string += "Plot occurences of tracks, positions or shells:  [6]\n"
  if (analyse.is_online):  # add those two options only if online data is used 
    total_string += "\nThe following are for online racing only:\n"
    total_string += "Add constraints to data:                         [7]\n"
    total_string += "Toggle constrained data usage:                   [8]\n\n"
  total_string += "Quit:                                            [q]\n"
  print(total_string)

def print_constraint_prompts():
  total_string =  "What do you want to add constraints to?\n"
  total_string += "CC:                  [1]\n"
  total_string += "Mirror flag:         [2]\n"
  total_string += "Number of players:   [3]\n"
  total_string += "Return to main menu: [r]\n"
  print(total_string)

def setup_analyse():
  print("\nThis is the Mario Kart track analyser.\n")

  online = input("Do you want to see the statistics from online?[y/n]: ") == "y"
  today = input("Do you want to use the tracks only of today?[y/n]: ") == "y"
  print()  # add an empty line

  runs = get_runs(today_only=today, is_online=online)

  all_tracks = get_all_tracks()
  
  analyse = an.Analysis(runs, all_tracks, online=online)
  return analyse

def run(analyse):
  quit = False
  constrained = False
  choices = ['q','1','2','3','4','5','6']  # current acceptable choices
  if (analyse.is_online):
    choices += ['7','8']  # these are only acceptable for online
  
  while (not quit):
    choice = 0
    while (choice not in choices):
      print("Hi! What do you want to do?")
      print_prompts(analyse)
      choice = input("Choose one of these options[1-6] or quit[q]: ")
      if (choice not in choices):
        print(f"Not recognised choice {choice}. Please try again.")
        print("\n\n\n\n")

    print("\n")
    if (choice == '1'):
      analyse.get_total_name_data(print_enabled=True, constr=constrained)

    elif (choice == '2'):
      analyse.get_fav_tracks(print_enabled=True, best=True, constr=constrained)
      analyse.get_fav_tracks(print_enabled=True, best=False, constr=constrained)

    elif (choice == '3'):
      # TODO(Justus) Check that only ints are accepted
      n = int(input("Number of most common tracks you want to see: "))
      analyse.get_n_freq_tracks(n, print_enabled=True, constr=constrained)

    elif (choice == '4'):
      val = input("Do you want to see the tracks played?[y/n]: ")
      played = val == "y"
      analyse.tracks_played(print_enabled=True, print_played=played, constr=constrained)

    elif (choice == '5'):
      check_track = input("Do you want to check for a specific track?[y/n]: ")
      if (check_track == "y"):
        track_choice = 0
        bool_2_chk = (track_choice not in analyse.tracks) 
        bool_2_chk |= (constrained and (track_choice not in analyse.constr_tracks))

        while (bool_2_chk):
          track_choice = input("Enter track abbreviation: ")
          if (bool_2_chk):
            print(f"Not recognised or played track: {track_choice}. Please try again.")

        analyse.get_avg_and_std(track=track_choice, print_enabled=True, constr=constrained)

      else:  # so if no specific track
        analyse.get_avg_and_std(print_enabled=True, constr=constrained)

    elif (choice == '6'):
      plot_track_val = input("Do you want to print track occurences?[y/n]: ")
      if (plot_track_val == 'y'):
        analyse.plot_track_occurences(constr=constrained)
    
      else:
        types = {'p': "position", 'r': "red", 'b': "blue", 'd': "drating"}
        print("Okay, opting to plot data instead.")
        tp = 0
        while (tp not in types.keys()):
          prompt = "What do you want to plot? Positions, "
          if (analyse.is_online):
            prompt += "difference in rating, reds or blues?[p/d/r/b]: "
          else:
            prompt += "reds or blues?[p/r/b]: "
          tp = input(prompt)

          if (tp not in types.keys()):
            print(f"Not recognised type to plot: {tp}. Please try again.")
        
        specific_name = input("Do you want to plot for a specific name?[y/n]: ")
        if (specific_name == 'y'):
          nm = 0
          while (nm not in analyse.names):
            nm = input("Enter name: ")
            if (nm not in analyse.names):
              print(f"No data available for name: {nm}. Please try again.")
          analyse.plot_data_occurences(name=nm, typ=types[tp], constr=constrained)

        else:  # don't care about specific name
          analyse.plot_data_occurences(typ=types[tp], constr=constrained)

    elif (choice == '7'):
      print_constraint_prompts()
      acc_answers = ['1','2','3','r']
      while (True):
        choice2 = input("Choose any of these options[1-3] or return[r]: ")
        ops = choice2.split()
        
        if (not all([op in acc_answers for op in ops])):  # answer must include
          print(f"Not recognised choice {choice2}. Please try again.")
          print("\n\n")
        elif ((len(ops) > 1) and ('r' in ops)):
          print("Cannot have regular choice and return command together.")
          print("\n\n")
        
        else:
          # set defaults
          ccs = an.ALLOWED_CCS
          mirror = None
          play_rng = (2,12)

          if ('1' in ops):
            ccs = analyse.constrain_cc()
          if ('2' in ops):
            mirror = analyse.constrain_mirror()
          if ('3' in ops):
            play_rng = analyse.constrain_players()

          analyse.constrain_data(ccs=ccs, mirror=mirror, player_range=play_rng)
          print("\n\n")  # just make some newlines for space
          break  # go out of while loop       
      

    elif (choice == '8'):
      constrained = not constrained
      print(f"Toggling the constrain flag to {constrained}.\n\n")

    elif (choice == 'q'):
      return 0  # quit programme


def main():
  analyse = setup_analyse()
  run(analyse)  

main()
