"""
This file is for testing the calculations from calc and advanced calc
"""
import os  # for directory listing

import calc
import adv_calc as acalc

def main():
  all_runs = ["comps/" + run for run in os.listdir("comps/")]  # all paths

  names = ["Lukas", "Henry", "Justus"]
  assert(calc.check_names(all_runs[0], names))  # names need to be accepted

  name_data = calc.get_all_positions(all_runs, names)
  #print(name_data)

  for name in names:
    pts = calc.get_points(name_data[name])
    print(f"{name} got {pts} points.")


main()
