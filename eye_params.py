class VisualConversions:
    '''
    computes polar angle and converts from dva to pixels
    and vice-versa
    '''
    def __init__(self, resolution, viewing_distance, screen_width):
        import numpy 
        self.resolution = resolution
        self.viewing_distance = viewing_distance
        self.screen_width = screen_width
        self.center_x = numpy.round(self.resolution[0]/2)
        self.center_y = numpy.round(self.resolution[1]/2)
        
    def pix2deg(self,pix):
        #convert from pixel coordinates to degrees of visual angle
        import numpy
        pixSize = self.screen_width/self.resolution[0]
        sz          = pix*pixSize
        ang       =  2*180*numpy.arctan(sz/(2*self.viewing_distance))/numpy.pi
        return ang
        
    def ang2pix(self,ang):
        #convert from degrees of visual angle to pixel coordinates
        import numpy
        pixSize=self.screen_width/self.resolution[0]
        sz=2*self.viewing_distance*numpy.arctan(numpy.pi*ang/(2*180))
        pix = numpy.round(sz/pixSize)
        return pix
        
    def polarAngle(self,a,b):
        #a,b in degrees
        #returns polar angle (hypotenuse)
        #a^2+b^2=c^2
        import numpy
        c2 = a**2+b**2
        return numpy.sqrt(c2)

class eyeTracking(VisualConversions):
    '''
    All things eye tracking e.g., recording, calibrating,
    outputing x,y coordinates in visual space
    * inherits VisualConversions class 
    '''
    def __init__(self, resolution, viewing_distance, screen_width, ip, port):
        import zmq 
        ctx=zmq.Context()
        super().__init__(resolution,viewing_distance,screen_width) # inherited 
        self.ip = ip
        self.port = port
        self.pupil_remote = ctx.socket(zmq.REQ)
        self.sub = ctx.socket(zmq.SUB)

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
        
    def get_gaze_position(self):
        # get current eye-position
        from msgpack import loads
        opic, msg = self.sub.recv_multipart()
        return loads(msg, raw=False)
        
    def check_fixation(self,rad):
        import numpy
        # define fixation check radius
        rad_check =  self.ang2pix(rad)
        # get current gaze position
        currentGaze = self.get_gaze_position()
        # convert from normalized units to pixels 
        x_pix = self.resolution[0]*currentGaze['norm_pos'][0]
        y_pix = self.resolution[1]*currentGaze['norm_pos'][1]
        # check if current gaze falls within a theoretical circle of a given radius around screen center
        a = self.pix2deg(numpy.absolute(x_pix-self.center_x))
        b = self.pix2deg(numpy.absolute(y_pix-self.center_y))
        ecc = self.polarAngle(a,b)
        print(ecc)
        if ecc < rad:
            print('fixating')
        elif ecc > rad:
            print('not_fixating')
        elif ecc == rad:
            print('not_fixating')
        
        
        
        
        
    
        

    
        
    