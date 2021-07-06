# This is a simple helper file to fulfill several conditions

ALLOWED_N_RACES=[4, 6, 8, 12, 16, 24, 32, 48]  # which number of races allowed
ALLOWED_CC = [50, 100, 150, 200]  # CC that is possible


def check_int(val):
  """
  Check if the value given can be converted to an integer.
  """
  try:
    int(val)
    return True

  except ValueError:
    print(f"{val} is not an valid integer. Please try again.\n")
    return False


def check_position(pos):
  return (pos <= 12) and (pos >= 1)

def check_positions(names, poss):
  """
  Check if all positions are ok
  """
  ind = all([check_position(pos) for pos in poss])
  dist = len(poss) == len(set(poss))  # distinct
  corr_n = len(names) == len(poss)  # ensure one position for one name
  return (ind and dist and corr_n)

def check_n_races(n):
  return (n in ALLOWED_N_RACES)

def run_n_races():
  """
  Asks user for the number of races to be played. Checks these and allows for amending.
  Returns the first accepted number of races.
  """
  n_ok = False  # check if number of races acceptable
  while (not n_ok):
    n_races_str = (input("Number of races: "))
    
    if (check_int(n_races_str)):
      n_races = int(n_races_str)  # cast to int after checking it's possible
      if (check_n_races(n_races)):
        n_ok = True
      else:
        print(f"Unacceptable number of races: {n_races}. " +
              f"Must be one of {ALLOWED_N_RACES}.")
  
  return n_races

def run_cc():
  """
  Asks the user for which cc the race is played at (if online) or what cc all races are played
  at if offline. It then returns the cc and a mirror flag
  """
  cc_accepted = False
  cc = 0
  is_mirror = False

  while (not cc_accepted): 
    cc_str = input("Which cc: ")
    if (check_int(cc_str)):  # first check if user submit is int
      cc = int(cc_str)

      if (cc in ALLOWED_CC):
        cc_accepted = True
      else:
        print(f"Not accepted, must be one of: {ALLOWED_CC}")

  if (cc == 150):
    mirror = input("Mirror?[y/n]: ")
    if (mirror == 'y'):
      is_mirror = True

  return (cc, is_mirror)

def run_n_players():
  """
  This is strictly for online playing. Just requests the user to enter
  how many players are participating in the race.
  """
  while (True):
    n = input("Number of players: ")
    
    if (check_int(n)):
      k = int(n)

      if ((2 <= k) and (k <= 12)):
        return k

      else:
        print(f"{k} is not between 2 and 12. Please try again.\n")

def run_tracks(tracks):
  """
  Asks user for the track. Checks if it is acceptable, gives the user options to amend,
  and returns the track.
  """

  track_ok = False  # check if acceptable track
  track = ""
  while(not track_ok):
    track = input("Enter Track: ")
    if (track in tracks):  # allowed abbreviation, since abbrevs are keys in dict
      acc = input(f"Logging as {tracks[track]}. Is this correct? [y/n]: ")
      if (acc == "y"):  # allow for changing track if typo
        track_ok = True 
      else:
        print("Ok. Try again.\n")
    else:
      print(f"Unknown track abbreviation: \"{track}\". Please try again.\n")

  return track

def run_init_ratings(names):
  """
  Asks user for the initial ratings of every player. This will only
  be called in online racing.
  """
  while(True):
    ratings = input(f"Initial ratings for {str(names)[1:-1]}: ").split()
    try:
      ratings_int = list(map(int, ratings))
      return ratings_int

    except ValueError:
      print("Non-integer entered. Please try again.\n")


def run_results(names):
  """
  Asks user for result input. Returns them as list of integers for positions
  """

  res_ok = False
  results = []
  while(not res_ok):
    try:
      results = [int(res) for res in input(f"Results for {str(names)[1:-1]}: ").split()]
      if (check_positions(names, results)):
        res_ok = True
      else:
        print("Those results are not acceptable. Must each be distinct and between 1 and 12.")

    except ValueError:
      print("Non-integer entered. Please try again.\n")

  return results


def run_RB_shells(names):
  """
  Asks user for shell input. Returns dictionary of the names corresponding
  to number of red and blue shells as tuple.
  """
  
  while (True):
    try:
      reds = [int(red) for red in input(f"Red shells for {str(names)[1:-1]}: ").split()]
      blues = [int(blue) for blue in input(f"Blue Shells for {str(names)[1:-1]}: ").split()]
      shells = dict(zip(names, zip(reds, blues)))
      rb_ok = "y" == input(f"We have: {shells}.\nIs this correct?[y/n] ")
      if (not rb_ok):
        print("Ok, try again.\n")

      else:
        return shells

    except ValueError:
      print("Non-integer entered. Please try again.\n")

def run_d_rating(names):
  """
  Asks user for rating changes post game for every player. This is
  only for online games.
  """

  while (True):
    try:
      d_rats = [int(rat) for rat in input(f"Rating change for {str(names)[1:-1]}: ").split()]
      d_rats_dict = dict(zip(names, d_rats))
      rat_ok = "y" == input(f"We have: {d_rats_dict}.\nIs this correct?[y/n] ")
      if (not rat_ok):
        print("Ok, try again.\n")

      else:
        return d_rats_dict

    except ValueError:
      print("Non-integer entered. Please try again.\n")
