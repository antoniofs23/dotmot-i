import numpy as np
import zmq
import msgpack as serializer
import socket
import sys
import os
import datetime
import matplotlib.pyplot as plt
import numpy.matlib
from math import pi
import pandas as pd
    
class VisualConversions:
    '''
    computes polar angle and converts from dva to pixels
    and vice-versa
    '''
    def __init__(self, resolution, viewing_distance, screen_width):
        self.resolution = resolution
        self.viewing_distance = viewing_distance
        self.screen_width = screen_width
        self.center_x = np.round(self.resolution[0]/2)
        self.center_y = np.round(self.resolution[1]/2)
        
    def pix2deg(self,pix):
        #convert from pixel coordinates to degrees of visual angle
        pixSize = self.screen_width/self.resolution[0]
        sz          = pix*pixSize
        ang       =  2*180*np.arctan(sz/(2*self.viewing_distance))/np.pi
        return ang
        
    def ang2pix(self,ang):
        #convert from degrees of visual angle to pixel coordinates
        pixSize=self.screen_width/self.resolution[0]
        sz=2*self.viewing_distance*np.arctan(np.pi*ang/(2*180))
        pix = np.round(sz/pixSize)
        return pix
        
    def polarAngle(self,a,b):
        #a,b in degrees
        #returns polar angle (hypotenuse)
        #a^2+b^2=c^2
        c2 = a**2+b**2
        return np.sqrt(c2)

class eyeTracking(VisualConversions):
    '''
    All things eye tracking e.g., recording, calibrating,
    outputing x,y coordinates in visual space
    * inherits VisualConversions class 
    '''
    def __init__(self, resolution, viewing_distance, screen_width, ip, port):
        ctx=zmq.Context()
        super().__init__(resolution,viewing_distance,screen_width) # inherited 
        self.ip = ip
        self.port = port
        self.pupil_remote = ctx.socket(zmq.REQ)
        self.sub = ctx.socket(zmq.SUB)
        self.pub = ctx.socket(zmq.PUB)

    def init_connect(self):
        self.pupil_remote.connect('tcp://'+self.ip+':'+self.port)
        print('Successfully connected')
    
    def start_recording(self,filename):
        #'R' to start recording
        self.pupil_remote.send_string('R '+filename)
        print(self.pupil_remote.recv_string())
        print('Recording started')
        
    def end_recording(self):
        # end recording
        self.pupil_remote.send_string('r')
        print(self.pupil_remote.recv_string())
        print('Recording ended')

    def start_calibration(self):
        #'C' to calibrate
        self.pupil_remote.send_string('C')
        print(self.pupil_remote.recv_string())
        print('Calibration started')
    
    def open_speak_port(self):
        # ask for sub port
        self.pupil_remote.send_string('SUB_PORT')
        sub_port = self.pupil_remote.recv_string()
        #open sub port to listen pupil
        self.sub.connect("tcp://{}:{}".format(self.ip, sub_port))
        self.sub.subscribe('gaze.')
        print('Successfully listening to pupil')
    
    def open_listen_port(self):
        self.pupil_remote.send_string('PUB_PORT')
        pub_port = self.pupil_remote.recv_string()
        self.pub.connect("tcp://{}:{}".format(self.ip, pub_port))
        
    def get_gaze_position(self):
        # get current eye-position
        from msgpack import loads
        opic, msg = self.sub.recv_multipart()
        return loads(msg, raw=False)
    
    def request_pupil_time(self):
        """Uses an existing Pupil Core software connection to request the remote time.
        Returns the current "pupil time" at the timepoint of reception.
        See https://docs.pupil-labs.com/core/terminology/#pupil-time for more information
        about "pupil time".
        """
        self.pupil_remote.send_string("t")
        pupil_time = self.pupil_remote.recv()
        return float(pupil_time)
    
    def measure_clock_offset(self, clock_function):
        """Calculates the offset between the Pupil Core software clock and a local clock.
        Requesting the remote pupil time takes time. This delay needs to be considered
        when calculating the clock offset. We measure the local time before (A) and
        after (B) the request and assume that the remote pupil time was measured at (A+B)/2,
        i.e. the midpoint between A and B.
        As a result, we have two measurements from two different clocks that were taken
        assumingly at the same point in time. The difference between them ("clock offset")
        allows us, given a new local clock measurement, to infer the corresponding time on
        the remote clock.
        """
        local_time_before = clock_function()
        pupil_time = self.request_pupil_time()
        local_time_after = clock_function()

        local_time = (local_time_before + local_time_after) / 2.0
        clock_offset = pupil_time - local_time
        return clock_offset
    
    def measure_clock_offset_stable(self, clock_function, n_samples=10):
        """Returns the mean clock offset after multiple measurements to reduce the effect
        of varying network delay.
        Since the network connection to Pupil Capture/Service is not necessarily stable,
        one has to assume that the delays to send and receive commands are not symmetrical
        and might vary. To reduce the possible clock-offset estimation error, this function
        repeats the measurement multiple times and returns the mean clock offset.
        The variance of these measurements is expected to be higher for remote connections
        (two different computers) than for local connections (script and Core software
        running on the same computer). You can easily extend this function to perform
        further statistical analysis on your clock-offset measurements to examine the
        accuracy of the time sync.
        """
        assert n_samples > 0, "Requires at least one sample"
        offsets = [
            self.measure_clock_offset(clock_function) for x in range(n_samples)
        ]
        return sum(offsets) / len(offsets)  # mean offset
    
    def notify(self, notification):
        """Sends ``notification`` to Pupil Remote"""
        topic = "notify." + notification["subject"]
        payload = serializer.dumps(notification, use_bin_type=True)
        self.pupil_remote.send_string(topic, flags=zmq.SNDMORE)
        self.pupil_remote.send(payload)
        return self.pupil_remote.recv_string()


    def send_trigger(self, trigger):
        """Sends annotation via PUB port"""
        payload = serializer.dumps(trigger, use_bin_type=True)
        self.pub.send_string(trigger["topic"], flags=zmq.SNDMORE)
        self.pub.send(payload)


    def new_trigger(label, duration, timestamp):
        """Creates a new trigger/annotation to send to Pupil Capture"""
        return {
            "topic": "annotation",
            "label": label,
            "timestamp": timestamp,
            "duration": duration,
        }
    
    def check_fixation(self,rad):
        # define fixation check radius
        rad_check =  self.ang2pix(rad)
        # get current gaze position
        currentGaze = self.get_gaze_position()
        # convert from normalized units to pixels 
        x_pix = self.resolution[0]*currentGaze['norm_pos'][0]
        y_pix = self.resolution[1]*currentGaze['norm_pos'][1]
        # check if current gaze falls within a theoretical circle of a given radius around screen center
        a = self.pix2deg(np.absolute(x_pix-self.center_x))
        b = self.pix2deg(np.absolute(y_pix-self.center_y))
        ecc = self.polarAngle(a,b)
        if ecc < rad:
           return (True, ecc)
        elif ecc > rad or ecc == rad:
           return (False, ecc)
     
class pupil_postprocessing(VisualConversions):
    '''processing of the pupil-core eye tracker data after its been recorded'''
    '''inherits visual confersions class'''
    def __init__(self,path,start_time,ang,screen_width,viewing_distance,resolution):
        super().__init__(resolution,viewing_distance,screen_width) # inherited
        self.path = path
        self.start_time = start_time #time at which experiment starts in seconds
        self.ang = ang # eye-jitter slack allowed in dva (typically 1.5 deg)
        
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
            
    def remove_low_conf(self,data):
        '''retuns only timestamps for which conf > 0.95'''
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
 
        
        
        
        
    
        

    
        
    