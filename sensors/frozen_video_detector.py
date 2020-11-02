"""
Simple module that compares frames of video using a structural
similarity index, this function returns a score between -1.0 
(totaly different) and 1.0 (exactly the same). The scores are
saved in a histogram and a moving average is created. If this
moving average goes over a threshold an event called 'frozen-video'
is generated with a value of true (meaning frozen) or false (no 
longer frozen).

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
NOTE: This is code gets executed in menshnet's cloud servers as 
foreign untrusted code. You cannot use import or manipulate disk
IO. You are given an object called 'menshnet' which is a server API
that gives you access to the following hardware accelerated libraries:

    skimage
    numpy
    scipy
    math
    cv2 
    sklearn
    statsmodel
    time

They are accessable by using menshnet.lib.<libname>
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    

"""

ABOVE_THRESHOLD = 1
BELOW_THRESHOLD = 0

class FrozenVideoSensor:
    

    def __init__(self):
        # must declare globals in python restricted execution mode
        global BELOW_THRESHOLD

        self.threshold = 0.95
        self.histogram = []
        self.max_hsize = 8
        self.last_frame = None
        self.frame_count = 0
        self.ssi = None
        self.event_trigger = "frozen-video"
        self.event_ssim = "ssim-value" 
        self.last_state = BELOW_THRESHOLD

    def on_init(self, menshnet, config):
        self.threshold = config.get("threshold", self.threshold)
        self.max_hsize = config.get("histogram_size", self.max_hsize)
        self.event_trigger = config.get("event_trigger",self.event_trigger)
        self.event_ssim = config.get("event_ssim",self.event_ssim)
        self.ssi = menshnet.lib.fpga.ssim
        
        menshnet.log.info("frozen video detector now initialized.") 

    def on_frame(self, menshnet, frame):
        # must declare globals in python restricted execution mode
        global BELOW_THRESHOLD, ABOVE_THRESHOLD
       
        menshnet.log.debug("frame %d" % self.frame_count)

        if self.frame_count > 0:
            similarity = self.ssi(frame, self.last_frame)
            menshnet.log.debug("ssi %f" % similarity)
            self.histogram.append(similarity)
            if len(self.histogram) == self.max_hsize:
                ave = sum(self.histogram)/self.max_hsize

                # send event
                menshnet.event.emit(self.event_ssim, ave)

                if ave >= self.threshold and self.last_state == BELOW_THRESHOLD:
                    # state transition sent event
                    self.last_state = ABOVE_THRESHOLD 
                    # tell any listening clients that this video is suspected 
                    # to be frozen
                    menshnet.event.emit(self.event_name,self.last_state) 

                elif ave <= self.threshold and self.last_state == ABOVE_THRESHOLD:
                    # state transition sent event
                    self.last_state = BELOW_THRESHOLD 
                    # tell any listening clients that this video is no longer frozen
                    menshnet.event.emit(self.event_name,self.last_state) 
          
                # remove oldest sample
                del self.histogram[0]

        self.frame_count += 1
        self.last_frame = frame 





# Create singleton
App = FrozenVideoSensor()

# --------------------------#
## External access methods ##
#---------------------------#

def on_init(menshnet, config):
    # must declare globals in python restricted execution mode
    global App

    App.on_init(menshnet, config)

def on_frame(menshnet, frame):
    # must declare globals in python restricted execution mode
    global App

    App.on_frame(menshnet, frame)








