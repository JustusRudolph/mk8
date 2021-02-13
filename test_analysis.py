"""
This file is for testing the calculations from calc and advanced calc
"""
import os  # for directory listing

from datetime import date

from src.analysis import read_data as rd
from src.analysis import stats as st

COMPS_PATH = "src/.comps/"

def main():
  all_runs = [COMPS_PATH + run for run in os.listdir(COMPS_PATH)]  # all paths
  
  today = str(date.today())

  runs_today = [COMPS_PATH + run for run in os.listdir(COMPS_PATH) if today in run]
  
  names = ["Lukas", "Henry", "Justus"]
  assert(rd.check_names(all_runs[0], names))  # names need to be accepted

  name_data = rd.get_all_name_data(runs_today, names)

  print("Today:")
  for name in names:
    # column 0 is place, 1 is reds, 2 is blues
    # make it rows so numpy is happy and it looks neat

    pts = rd.get_points(name_data[name].transpose()[0])
    n_reds = sum(name_data[name].transpose()[1])
    n_blues = sum(name_data[name].transpose()[2])
    print(f"{name} got {pts} points. Hit by red {n_reds} times. Hit by blue {n_blues} times.")


main()
