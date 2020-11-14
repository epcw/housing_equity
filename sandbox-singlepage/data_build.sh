#!/bin/bash
#usage: ./data_build.sh {jsons/csvs}
#default behavior is to pull both graphs and

#set root directory for data files
#ROOTBEER="/home/ubuntu/housing_equity/sandbox-singlepage/" #production
ROOTBEER=""#local

#get_jsons=$(python3 build_graphs.py)
#get_csvs=$(python3 data_prep_tract.py)

if [[ "$1" = "jsons" ]]
then
  echo "building networkx graphs"
  echo $(python3 build_graphs.py)
elif [[ "$1" = "csvs" ]]
then
  echo "building dataframes and exporting to csv"
  echo $(python3 data_prep_tract.py)
else
  echo "building dataframes and exporting to csv"
  echo $(python3 data_prep_tract.py)
  echo "building networkx graphs"
  echo $(python3 build_graphs.py)
fi
