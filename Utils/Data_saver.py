import argparse
import sys
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random
pd.options.mode.chained_assignment = None
sys.path.append('/content/drive/MyDrive/Dual Degree Project/Utils')
from Driver import Driver
imp_var=['Pedal_ACC_suvin','long_Accel_suvin','lat_Accel_suvin','velocity','Yaw_Rate_suvin','Pedal_BRK_suvin','time','heading_suvin']
def main():
  parser = argparse.ArgumentParser(description="This file is used to process the data of the drivers and store the events in csv format")
  parser.add_argument('--id',type=int,help='Enter the id of the driver')
  parser.add_argument('--data1',type=str,help='Enter the data file path for A to B')
  parser.add_argument('--events1',type=str,help='Enter the events file path for A to B')
  parser.add_argument('--data2',type=str,help='Enter the data file path B to A')
  parser.add_argument('--events2',type=str,help='Enter the events file path B to A')
  parser.add_argument('--fixed_window',type=bool,help='Is the event should be fixed window?')
  parser.add_argument('--window_size',type=int,help='size of window')
  # Parse the arguments
  args = parser.parse_args()
  id=args.id
  data1=args.data1
  events1=args.events1
  data2=args.data2
  events2=args.events2
  fixed_window=False
  window_size=args.window_size
  #getting driver data
  driver1=Driver(id=id,data=data1,events=events1,going=True,fixed_window=fixed_window,window_size=window_size)
  print('A->B',driver1)
  driver2=Driver(id=id,data=data2,events=events2,going=False,fixed_window=fixed_window,window_size=window_size)
  print('B->A',driver2)
  # processing for AB
  overtake_events1=driver1.get_overtaking_events(events1)
  df1=driver1.get_imp_features_data(imp_var)
  Overtakedf1=driver1.get_overtake_df(overtake_events1,imp_var)
  print(f'For A->B Overtaking events found : {len(overtake_events1)}')
  NO_events1,non_overtaking_df1=driver1.get_non_overtake_df(imp_var)
  print('Processed Overtaking and non overtaking events for A->B')
  #processing for BA
  overtake_events2=driver2.get_overtaking_events(events2)
  df2=driver2.get_imp_features_data(imp_var)
  Overtakedf2=driver2.get_overtake_df(overtake_events2,imp_var)
  print(f'For B->A Overtaking events found : {len(overtake_events2)}')
  NO_events2,non_overtaking_df2=driver2.get_non_overtake_df(imp_var)
  print('Processed Overtaking and non overtaking events for B->A')
  #saving the files
  pd.concat([Overtakedf1,Overtakedf2]).reset_index(drop=True).to_csv(f'/content/drive/MyDrive/Dual Degree Project/Drivers/Driver_{id}/D{id}_Overtaking_events.csv',index=False)
  pd.concat([non_overtaking_df1,non_overtaking_df2]).reset_index(drop=True).to_csv(f'/content/drive/MyDrive/Dual Degree Project/Drivers/Driver_{id}/D{id}_Non_Overtaking_events.csv',index=False)
  
  print(f'Saved All events for Driver_{id}')

if __name__=='__main__':
  main()  
