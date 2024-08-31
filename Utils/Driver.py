import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random

class Driver:
  
  def __init__(self,id=None,data=None,events=None,going=True,fixed_window=False,window_size=None):
    self.id = id
    self.window_size=window_size
    self.fixed_window=fixed_window
    print('got ',fixed_window)
    self.data = data
    self.going = going
    self.dir='AB' if self.going else 'BA'
    self.overtake_events = self.get_overtaking_events(events)
    self.df=pd.read_csv(data)
    self.num_events=len(self.overtake_events)
    self.imp_var=['Pedal_ACC_suvin','long_Accel_suvin','lat_Accel_suvin','velocity','Yaw_Rate_suvin','Pedal_BRK_suvin','time','heading_suvin']
    print('_______-----_______')

  ##############################################################################################

  def __str__(self):
    return f'''
    Driver:
    id: {self.id}
    going: {'A->B' if self.going else 'B->A'}
    '''
  ##############################################################################################

  def get_overtaking_events(self,path) :
    with open(path,'r') as f:
      data=f.read()
    def preprocess_time(time):
      start=time.split()[1].split(',')[0]
      end=time.split()[1].split(',')[1]
      start=int(start.split('-')[0])*60+float(start.split('-')[1])
      end=int(end.split('-')[0])*60+float(end.split('-')[1])
      return (round(start,1),round(end,1))

    times=data.split('\n')
    overtake_events=list(map(preprocess_time,times))
    if self.fixed_window:
      print(self.fixed_window)
      temp=[]
      print(f'making all events of length {self.window_size}')
      for event in overtake_events:
        if event[1]-event[0]>self.window_size:
          print('Found Bigger Event hence avoiding it')
          continue
        diff=self.window_size-(event[1]-event[0])
        first=event[0]-diff/2
        second=event[1]+diff/2
        temp.append((first,second))
      overtake_events=temp
      print('converted to fixed window!!')
    else:
      print('removing outliers')
      temp=[]
      for event in overtake_events:
        if event[1]-event[0]>30:
          print('Found Bigger Event hence avoiding it')
          continue
        temp.append((event[0],event[1]))
      overtake_events=temp
    return overtake_events

  ##############################################################################################

  def get_imp_features_data(self,imp_var,update_original=True):
    if update_original:
      self.df=self.df[imp_var]
      return self.df
    else:
      return self.df[imp_var]

  ##############################################################################################

  def plot_TS(self,var,start=None,end=None):
    if start is None:
      start=self.df.time.min()
    if end is None:
      end=self.df.time.max()
    plt.figure(figsize=(10,5))
    plt.plot(self.df.loc[self.df.time.between(start,end),var])
    plt.title(f'{var} over time')
    plt.xlabel('Time')
    plt.ylabel(var)
    plt.show()

  ##############################################################################################

  def get_overtake_df(self,overtake_events,imp_var):
    overtake_df=pd.DataFrame(columns=imp_var)
    for id,event in enumerate(overtake_events):
      mask=self.df['time'].between(event[0],event[1])
      event_df=self.df[mask]
      event_df['ID']=f'D{self.id}_{self.dir}_{id+1}'
      overtake_df=pd.concat([overtake_df,event_df])
      overtake_df.reset_index(drop=True,inplace=True)
    return overtake_df

  ##############################################################################################

  def get_non_overtake_df(self,imp_var,window_size=15,extra=0):
    NOE=[(self.overtake_events[i][1],self.overtake_events[i+1][0]) for i in range(len(self.overtake_events)-1)]
    NOE_TS1=[]
    random.seed(42)
    overtake_time_list=np.load('/content/drive/MyDrive/Dual Degree Project/Experimentations/overtake_time_array.npy')
    for event in NOE:
      i=event[0]
      while i+window_size<event[1]:
        #if random.randint(1,6)%2==0:
        NOE_TS1.append((i,i+window_size))
        i+=window_size
        window_size=np.random.choice(overtake_time_list)

    self.num_events=len(self.overtake_events)
    Non_overtaking_events=sorted(random.sample(NOE_TS1,k=self.num_events))
    Non_overtake_df=pd.DataFrame(columns=imp_var)
    for id,event in enumerate(Non_overtaking_events):
      mask=self.df['time'].between(event[0],event[1])
      event_df=self.df[mask]
      event_df['ID']=f'D{self.id}_{self.dir}_NO_{id+1}'
      Non_overtake_df=pd.concat([Non_overtake_df,event_df])
      Non_overtake_df.reset_index(drop=True,inplace=True)
    return Non_overtaking_events,Non_overtake_df

  ##############################################################################################

  def plot_all_vars(self,imp_var,start=None,end=None):
    if start is None:
      start=self.df.time.min()
    if end is None:
      end=self.df.time.max()
    plt.figure(figsize=(10,5),dpi=200)
    if 'time'in imp_var:
      imp_var.remove('time')
    for var in imp_var:
      plt.plot(self.df.loc[self.df.time.between(start,end),var],label=var)
    plt.legend()
    plt.title(f'All variables over time')
    plt.xlabel('Time elapsed')
    plt.show()

  ##############################################################################################

