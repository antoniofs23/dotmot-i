import os
import datetime
import matplotlib.pyplot as plt
import numpy.matlib
import numpy as np
from math import pi
import pandas as pd

class pupil_postprocessing:
    '''processing of the pupil-core eye tracker data after its been recorded'''
    def __init__(self,path,start_time,ang,screen_width,viewing_distance,resolution):
        self.path = path
        self.start_time=start_time #time at which experiment starts in seconds
        self.ang = ang # eye-jitter slack allowed in dva
        self.screen_width = screen_width
        self.viewing_distance = viewing_distance
        self.resolution = resolution
        
    def print_file_struc(self):
        '''prints all contents of a folders in path'''
        for root, dirs, files in os.walk(self.path):
            level = root.replace(self.path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (level + 1)
            for f in sorted(files):
                print(f'{subindent}{f}')
    
    def get_gaze_pos(self):
        # get gaze data
        exported_gaze_csv = os.path.join(self.path, 'exports', '000', 'gaze_positions.csv')
        gaze_pd_frame = pd.read_csv(exported_gaze_csv)
        #exlcude time before experiment begins
        start = gaze_pd_frame.gaze_timestamp.iloc[0]+self.start_time
        return gaze_pd_frame[gaze_pd_frame.gaze_timestamp > start]
        
    def check_jitter_window(self):
        '''check what a given jitter window looks like in degrees of visual angle'''
        pixSize=self.screen_width/self.resolution[0]
        sz=2*self.viewing_distance*np.arctan(np.pi*self.ang/(2*180))
        pix = np.round(sz/pixSize)
        #convert from pix to norm units on screen
        return pix/self.resolution[0]
        
    def conv_time_to_wall(self,gaze_pd_dataframe):
        '''convert timestamp from arbitrary time to wall-time (hours/minutes/seconds'''
        x_time = []
        for timestamp in gaze_pd_dataframe:
            wall_time = datetime.datetime.fromtimestamp(timestamp)
            HMS = int(wall_time.strftime("%H%M%S"))
            x_time.append(HMS/100)
        return x_time
            
    def remove_low_conf(self):
        '''retuns only timestamps for which conf > 0.95'''
        data = self.get_gaze_pos()
        return data[data['confidence']>0.95]
    
    def plt_gaze_pos(self,data):
        time_data_temp = self.conv_time_to_wall(data['gaze_timestamp'])
        time_data = np.linspace(0,(time_data_temp[-1]-time_data_temp[0])*60,len(time_data_temp))
        x_pos = data['norm_pos_x']
        y_pos = data['norm_pos_y']
        
        # add jitter window
        jitter = self.check_jitter_window()
        
        plt.figure()
        plt.plot(time_data,x_pos,label='x loc')
        plt.plot(time_data,y_pos,label='y_loc')
        plt.plot(time_data, numpy.matlib.repmat(0.5,len(time_data),1),'--',label='center')
        plt.plot(time_data, numpy.matlib.repmat(0.5+jitter,len(time_data),1),'--',color='black',label='jitter')
        plt.plot(time_data, numpy.matlib.repmat(0.5-jitter,len(time_data),1),'--',color='black')
        plt.xlabel('timestamps(s)')
        plt.ylabel('norm_pos')
        plt.ylim([0,1])
        plt.title('eye0')
        plt.legend()
        plt.show()
        
    def plt_gaze_scatter(self,data):
        jitter = self.check_jitter_window()
        u = 0.5 # x-center
        v = 0.5 # y-center
        a = jitter # radius on the x-axis
        b = jitter # radius on the y-axis
        
        plt.figure(figsize=(5,5))
        t = np.linspace(0,2*pi,100)
        plt.plot(u+a*np.cos(t) , v+b*np.sin(t),color='black',label='eye-jitter 1.5deg')
        
        plt.scatter(data['norm_pos_x'], data['norm_pos_y'], c=data['gaze_timestamp'])
        plt.plot([0.5+jitter,0.5+jitter],[0,1],'-',color='black')
        plt.plot([0.5-jitter,0.5-jitter],[0,1],'-',color='black')
        plt.plot([0.5+jitter,0.5+jitter],[0,1],'-',color='black')
        plt.plot([0,1],[0.5+jitter,0.5+jitter],'-',color='black')
        plt.plot([0,1],[0.5-jitter,0.5-jitter],'-',color='black')
        plt.plot(0.5+jitter,1,'-',color='black')
        #plt.colorbar().ax.set_ylabel('Timestamps')
        plt.xlabel('norm_pos_x')
        plt.ylabel('norm_pos_y')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.title('eye_position')
        plt.legend()
        plt.show()        
