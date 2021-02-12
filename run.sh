#!/bin/bash
echo "STARTING PYTHON SCRIPT"
LOC=which python3
if [$LOC]
then
  python3 #race.py
else
  echo "Python 3 not installed. Cannot run."
fi
