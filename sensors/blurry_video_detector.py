"""
Based on this blur detector:
https://github.com/WillBrennan/BlurDetection2


Demonstrates this detector running on mechnet
"""




class Application:
    def on_init(self, config):
        self.hist = []
        self.threshold = config.get("threshold", self.threshold)
        self.max_hsize = config.get("histogram_size", 5)
        self.event_blurry = config.get("event_name","video-blurry")
        self.is_blurry = False

    def on_frame(self, menshnet, frame):
        """ 
        apply a laplacian transform on each frame, take the variance of
         
        """ 
        cv2 = menshnet.lib.cv2
        numpy = menshnet.lib.numpy

        blur_map = cv2.Laplacian(frame, cv2.CV_64F)
        score = numpy.var(blur_map)
        self.hist.append(score)

        # use Laplacian transform as a high pass filter 
        if len(self.hist) == self.max_hsize: 
            ave = sum(self.hist)/len(self.max_hsize)
            # if the average variance of samples falled below threshold then
            # then consider the image to be blurry.
            if ave < self.threshold:
                if not self.is_blurry:
                    self.is_blurry = True
                    menshnet.event.emit(self.event_blurry,self.is_blurry)
            else:
                if self.is_blurry:                   
                    self.is_blurry = False
                    menshnet.event.emit(self.event_blurry,self.is_blurry)
            del self.hist[0]


App = Application()


def on_init(menshnet, config):
    # must declare globals in python restricted execution mode
    global App
    App.on_init(config)


def on_frame(menshnet, frame):
    # must declare globals in python restricted execution mode
    global App

    App.on_frame(menshnet, frame)


