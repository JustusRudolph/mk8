from src.log import log_race as lr



def main():

  dict_path = "src/data/tracks.csv"
  comps_path = "src/.comps"
  is_online = False

  if (input("Are you playing online?[y/n]: ") == 'y'):
    is_online = True
  
  lr.log(dict_path, comps_path, is_online=is_online)

  return 0


main()

