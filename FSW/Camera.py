#from FSW.Main import EXPOSURE_TIME
from os import *
import RPi.GPIO as GPIO
#from RPi.GPIO import GPIO
from pathlib import Path, WindowsPath

import serial
import threading

# =====================================
# ==         GLOBAL VARS         ==
# =====================================

out_path = "\home\pi\InspectionSatCV\FSW" # file path to the directory that will store the image from camera

class Camera():
    """ Camera Class implements functionality in order to support Arducam by using the libcamera library.
        It is currently hardcoded in order to interact with a Linux-based operating system that supports
        libcamera. It offers Camera object instantiation and camera picture taking functionality.

        exposure_time : int
            Describes the total exposure time (ms) for the camera.
        delay : int
            Provides the camera with a certain delay time (ms).
        shutter_speed : int
            Determines how many frames per second are set when taking an image or video.
        gain : int
            Describes how much saturation the camera will experience.
        pxl_height : int
            Describes the resulting image height in pixels.
        pxl_width : int
            Describes the resulting image width in pixels.
        timeout : int
            Tells the image capture to take a picture, regardless of state, after a set amount of time (ms).
        config : str
            Contains the full libcamera Command Line Interface command that the shell parses.
        mode : str
            Libcamera has many different image capture modes. Users can specify which mode they prefer here.
        encoding : str
            Tells Libcamera which file type (.png, .jpg, ect.) for image capture to export as.
        flush : str
            Describes how well the pictures will wrap about the center focus.
        preview_mode : str
            Allows libcamera to create a small GUI that shows the current camera image input.
        height : int
            Describes the image height.
        width : int
            Describes the image width.
    """
    exposure_time = 0
    delay = 0
    shutter_speed = 0
    gain = 0
    pxl_height = 0
    pxl_width = 0
    timeout = 0
    config = ''
    mode = ''
    encoding = ''
    flush = ' --wrap '
    preview_mode = ''
    height= 600
    width = 600

    num_pics_taken = 0
    # --timeout from libcamera provides cmd line time of cam timeout, useful for try-catch

    def __init__(self, exp, timeout, gain, delay, height, width):
        """ Used to instantiate a Camera object with user-defined preferences for debugging.
        """
        self.pxl_height = height
        self.pxl_width = width
        self.exposure_time = " --shutter {0}".format(exp)                #set the exposure time in (ms)
        '''set shutter speed numerically closest to the lens focal length
         For example, for handheld use of a 35 mm camera with a 50 mm normal lens, 
         the closest shutter speed is 1/60 s (closest to "50"), while for a 200 mm lens 
         it is recommended not to choose shutter speeds below 1/200 of a second.'''
        self.delay = delay
        self.timeout = timeout #5000 # 5 second MAX for timeout                   #takes picture after 5s of previewing
        self.encoding = 'jpg'
        self.mode = 'libcamera-still '
        self.preview_mode = ' --nopreview ' # used only for debugging
        self.outpath = out_path
        self.output = ""
        self.out_encoding = ""
        self.height = ""
        self.width = ""
        self.num_pics_taken = 0
        self.num_gain = 0
        self.gain = " --gain {0}".format(gain)
        self.ev = " --ev {0}".format(6) 
        self.awb = " --awb {0}".format("auto")           #awb = (auto, incandescent, tungsten, fluorescent)
        self.gain_value = gain
       
        #self.focus = " --autofocus"

        """self.exposure_mode = " --exposure {0}".format()               # may be either normal, sport or long
        self.ev = " --ev {0}".format()                                   # Sets the EV compensation of the image in units of stops, in the range -10 to 10. Default is 0.
        self.gain = " --gain {0}".format() 
        self.image_sharpness = " --sharpness {0}".format()               # image post-processing/calibration
        self.image_contrast = " --contrast {0}".format() 
        self.image_brightness = " --brightness {0}".format() 
        self.image_saturation = " --saturation {0}".format() 
        self.image_iso = "" 
        self.framerate = " --framerate {0}".format() """


    def takePicture(self, file_name):
        """ Used by Camera object to take a picture with libcamera. A file name is specified so that the 
            output path will generate a unique image file in said output path. Uses CLI to generate the 
            image. 

            Returns True if the image was taken succesfully. Returns False if an exception was raised 
            while attempting to take the image.
        """
        print("Taking a picture!")

        self.output = "".join('-o ' + self.outpath + '\\' + file_name + ' ')
        self.out_encoding = "".join(' -e ' + self.encoding)
        self.timeout = "".join('-t ' + str(self.timeout))
        self.height = "".join(' --height ' +  str(self.pxl_height) + ' ')
        self.width = "".join('--width ' + str(self.pxl_width) + ' ')

        self.param = (self.mode, self.output, self.timeout, self.height, self.width, self.gain, self.exposure_time, self.ev, self.out_encoding)
        self.config = "".join(self.param)

        try:
            system(self.config)
        except Exception:
            print("Failed to take picture due to raised exception: ", system.exec_info()[2])
            return False
        #system('libcamera-jpeg -o handrail-input.jpg -t 5000 --width 800 --height 600')
        self.num_pics_taken += 1
        self.num_gain +=1
        
        print(self.config)
        return True

    def getNumPicsTake(self):
        """ Returns the number of images successfully captured by the Camera object.
        """
        return self.num_pics_taken
    
    def getNumGain(self):
        """ Returns the number of images successfully captured by the Camera object.
        """
        return self.gain_value

# For debugging purposes only
if __name__ == "__main__":
    picam = Camera(exp = 8000, timeout = 10000, gain = 10, delay = 3000, height = 1080, width = 1920)

    picam.takePicture("test{num}_{gain}".format(num = picam.getNumPicsTake(), gain = picam.getNumGain()))
    #picam.takePicture("test6.jpg")
    
    



    

