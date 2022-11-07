class VisualDegrees:
    '''
    computes polar angle and converts from dva to pixels
    and vice-versa
    '''
    def __init__(self, resolution, viewing_distance, screen_width):
        self.resolution = resolution
        self.viewing_distance = viewing_distance
        self.screen_width = screen_width
        
    def pix2deg(self,pix):
        #convert from pixel coordinates to degrees of visual angle
        pixSize = self.screen_width/self.resolution[0]
        sz          = [num*pixSize for num in pix]
        ang       =  [2*180*np.arctan(num/(2*self.viewing_distance))/np.pi for num in sz]
        return ang
        
    def ang2pix(self,deg):
        #convert from degrees of visual angle to pixel coordinates
        pixSize=scr['width']/scr['resolution'][0]
        sz=[2*scr['dist']*np.arctan(np.pi*num/(2*180)) for num in ang]
        pix = [np.round(num/pixSize) for num in sz]
        return pix
        
    def polarAngle(self,a,b):
        #a,b in degrees
        #returns polar angle (hypotenuse)
        #a^2+b^2=c^2
        c2 = a**2+b**2
        return np.sqrt(c2)


class eyeTracking(VisualDegrees):
    '''
    All things eye tracking e.g., recording, calibrating,
    outputing x,y coordinates in visual space
    
    * inherits VisualDegrees class 
    '''
    def init_connect(self,ip='127.0.0.1:50020'):
        import zmq 
        ctx=zmq.Context()
        pupil_remote=ctx.socket(zmq.REQ)
        pupil_remote.connect('tcp://'+ip)
        print('Successfully connected')

    
    def start_recording(self,filename):
        #'R' to start recording
        pupil_remote.send_string('R '+filename)
        print(pupil_remote.recv_string())
        print('Recording started')
    
    def start_calibration(self):
        #'C' to calibrate
        pupil_remote.send_string('C')
        print(pupil_remote.recv_string())
        print('Calibration started')
    
    def open_speak_port(self):
        # ask for sub port
        pupil_remote.send_string('SUB_PORT')
        sub_port = pupil_remote.recv_string()
    
        #open sub port to listen pupil
        sub = ctx.socket(zmq.SUB)
        sub.connect("tcp://{}:{}".format('127.0.0.1', sub_port))
        sub.subscribe('gaze.')
        print('Successfully listening to pupil')
        
    def get_gaze_position(self):
        # get current eye-position
        from msgpack import loads
        opic, msg = sub.recv_multipart()
        return loads(msg, raw=False)
        

    
        
    