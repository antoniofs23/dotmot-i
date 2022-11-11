import numpy as np
import zmq
import msgpack as serializer
import socket
import sys
    
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
     
        
        
        
        
        
    
        

    
        
    