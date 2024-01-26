import numpy as np

import random
import sys
import math
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from vectors import Vector
from faceAnimation import FaceAnimation
from faceFeature import FaceFeature
from emotions import Emotion
#from worker import Worker, WorkerSignals

class MainWindow(QMainWindow):
    userInputRequested = pyqtSignal()
    def __init__(self):
        super().__init__()
        #set size of window
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet("background-color: white;") 
        self.setWindowTitle('Face Simulation')
        self.layout = QVBoxLayout()
        self.widget = QWidget(self)

        self.widget.setLayout(self.layout)
        
        # Initialize frame number
        self.frame_number = 0
        # Specify the output directory
        self.output_dir = "/afs/andrew.cmu.edu/usr7/spavline/private/FaceSimulationProject/Frames"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        #TIMER
        #specify frames per second
        self.fps = 15
        self.animationDuration = 20 #how long does animation take
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timeElapsed = 0
        self.timer.start(10)
        self.userInputRequested.connect(self.getUserInput)

        #keeps track of all of the widgets in Main Window
        self.widgets = []

        #keep track of all of the properties that will be changing with each call to function
        #number of seconds to hold the emotion
        self.numSecondsToHoldEmotion = 50
        #number of seconds for face to move from neutral to target position
        
        #TODO: get speed from time to show emotion
        self.speed = 2
        self.timeToShowEmotion = 10

        #direction of movement - negative when moving back to neutral 
        self.direction = 1

        #define the emotions
        self.joy = Emotion("joy", {"Inner Occipitofrontalis": 0.3, "Outer Occipitofrontalis": 0.3, 
        "Orbicularis Oculi": 0.8, "Levator Labii":0.5, "Zygomaticus": 1.0})
        self.sadness = Emotion("sadness", {"Inner Occipitofrontalis": 1.0, "Outer Occipitofrontalis":0.2, 
           "Corrugator": 0.1, "Procerus": 1.0, "Orbicularis Oculi": 1.0, 
           "Levator Labii": 0.5, "Levator Palpabrae": 0.8, "Buccinator":0.5, 
           "Orbicularis Oris": 0.5, "Depressor Anguli Oris": 1.0, "Mentalis":1.0})
        self.anger = Emotion("anger", {"Corrugator": 1.0, "Procerus":1.0, "Orbicularis Oculi":0.5, "Levator Labii":1.0,
         "Buccinator":0.8, "Orbicularis Oris": 0.5, "Depressor Anguli Oris":0.3})
        self.disgust = Emotion("disgust",{"Corrugator":1.0, "Procerus":0.5,"Orbicularis Oculi":0.8, "Levator Labii":1.0, 
           "Orbicularis Oris":1.0, "Depressor Anguli Oris": 1.0, "Mentalis":1.0})
        self.fear = Emotion("fear",{"Inner Occipitofrontalis":0.8, "Outer Occipitofrontalis":0.3, "Corrugator":1.0, 
        "Procerus":0.5, "Orbicularis Oculi": 0.8, "Levator Labii":1.0, "Levator Palpabrae":1.0,
        "Buccinator":0.8, "Orbicularis Oris":0.5, "Depressor Anguli Oris":0.7, 
        "Mentalis":1.0, "Jaw":0.8})
        self.surprise = Emotion("surprise",{"Inner Occipitofrontalis":0.5, "Outer Occipitofrontalis":0.8, "Levator Labii": 0.8, 
            "Levator Palpabrae":0.7, "Orbicularis Oris":1.0, "Depressor Anguli Oris":0.3, "Mentalis":0.3,
            "Jaw":1.0})
        
        self.currEmotion = self.joy
        self.currPercentOfEmotion = 1.0


        #have a bank of starting neutral positions?
        #TODO: have the ability to start at different neutral positions
        #change the vector start points according to the end points of an emotion
        self.startingNeutral = None
    
    #adds widgets to the main window
    def addWidgetToLayout(self, widget):
        self.layout.addWidget(widget)
        self.widgets = self.widgets + [widget]
    
    def animation(self):
        for w in self.widgets:
            if self.timeElapsed >= self.numSecondsToHoldEmotion + self.timeToShowEmotion:
                self.direction = -1
            w.moveWidget(self.currEmotion, self.direction, self.speed, self.currPercentOfEmotion)
        self.update()
        self.timeElapsed += 1
        # Capture and save the frame
        self.capture_frame()
        # Check if it's time to request user input
        if self.timeElapsed >= 2*(self.numSecondsToHoldEmotion + self.timeToShowEmotion):
            QTimer.singleShot(0, self.getUserInput)
    
    def getUserInput(self):
        # Get user input
        inputEmotion = input("Enter emotion: ")
        inputPercentage = input("Enter percentage: ")

        # Restart the animation
        self.direction = 1  # or set it to the appropriate direction
        
        if inputEmotion == 'joy':
            self.currEmotion = self.joy
        elif inputEmotion == 'sadness':
            self.currEmotion = self.sadness
        elif inputEmotion == 'anger':
            self.currEmotion = self.anger
        elif inputEmotion == 'disgust':
            self.currEmotion = self.disgust
        elif inputEmotion == 'surprise':
            self.currEmotion = self.surprise
        else:
            print("not valid emotion")
        
        self.currPercentOfEmotion = float(inputPercentage)
        self.update()

    def capture_frame(self):
        pixmap = self.widget.grab()  # Capture the current frame
        frame_path = os.path.join(self.output_dir, f"frame_{self.frame_number:04d}.png")
        pixmap.save(frame_path)  # Save the frame as an image
        self.frame_number += 1


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    eyebrowLeftPoints = [(164,186),(192,177), (257,188)]
    #each list of vectors at index i should correspond to the vectors that pull on the same point at index i
    eyebrowLeftVectors = [[((164,186), (164,172), "Outer Occipitofrontalis")],
                          [((192,177),(189,161),"Outer Occipitofrontalis"), ((192,177),(199,156), "Inner Occipitofrontalis"), ((192,177),(210, 182), "Corrugator"), ((192, 177),(218,197), "Procerus")],
                          [((257,188),(255,180), "Outer Occipitofrontalis"), ((257,188),(257,154), "Inner Occipitofrontalis"), ((257,188),(274,194), "Corrugator"),((257,188),(254,208), "Procerus")] ]

    eyebrowRightPoints = [(330,188),(395,177), (422,186)]
    eyebrowRightVectors = [[((330,188),(343,180), "Outer Occipitofrontalis"), ((330,188),(331,154), "Inner Occipitofrontalis"), ((330,188),(311,194), "Corrugator"), ((330,188),(337,208), "Procerus")],
                           [((395,177),(398,161), "Outer Occipitofrontalis"), ((395,177),(388,156), "Inner Occipitofrontalis"), ((395,177),(375, 182), "Corrugator"), ((395,177),(370, 197), "Procerus")],
                           [((422,186), (423,172), "Outer Occipitofrontalis")]
                           ]

    rightEyePoints = [(185,224), (198,206), (235, 206), (248,224)]
    leftEyePoints = [(338,224), (352, 206), (389,206), (400,224)]

    rightEyeVectors = [[((185,224), (191, 224), "Orbicularis Oculi")],
                       [((198,206), (200, 211), "Orbicularis Oculi"), ((198,206), (205, 199), "Levator Palpabrae")],
                       [((235, 206), (230, 211), "Orbicularis Oculi"), ((235, 206), (226, 198), "Levator Palpabrae")],
                       [((248,224), (242, 224), "Orbicularis Oculi")]
                       ]
    
    leftEyeVectors = [[((338,224), (344, 224), "Orbicularis Oculi")],
                       [((352, 206), (356, 211), "Orbicularis Oculi"), ((352, 206), (360, 198), "Levator Palpabrae")],
                       [((389,206), (385, 211), "Orbicularis Oculi"), ((389,206), (380, 199), "Levator Palpabrae")],
                       [((400,224), (394, 224), "Orbicularis Oculi")]
                       ]
    
    nosePoints = [(267, 321), (292, 325), (320, 321)]
    noseVectors = [[((267, 321), (264, 310),"Levator Labii")],
                   [((292, 325), (292, 324), "Levator Labii")],
                   [((320, 321), (323, 310), "Levator Labii")]
                   ]
    mouthPoints = [(238, 373), (265, 377), (293, 377),(320, 377), (347, 373),(320, 373), (293, 373),(265, 373),(238, 373)]
    mouthVectors = [ [((238, 373), (237, 362), "Levator Labii"), ((238, 373), (218, 357),"Zygomaticus"), ((238, 373), (224, 380),"Buccinator"), ((238, 373), (250, 373), "Orbicularis Oris"), ((238, 373), (239, 386), "Depressor Anguli Oris"), ((238, 373),(237, 410), "Jaw")],
                    [((265, 377), (258, 371),"Zygomaticus"), ((265, 377),(261, 380), "Buccinator"), ((265, 377), (277, 377), "Orbicularis Oris"), ((265, 377), (263, 383), "Depressor Anguli Oris"), ((265, 377),(265, 369),"Mentalis"), ((265, 377),(265, 426), "Jaw")],
                    [((293, 377), (293, 370), "Mentalis"), ((293, 377),(291, 426), "Jaw")],
                    [((320, 377), (327, 371), "Zygomaticus"), ((320, 377), (324, 380), "Buccinator"), ((320, 377), (308, 377), "Orbicularis Oris"), ((320, 377), (323, 383),"Depressor Anguli Oris"), ((320, 377),(318, 370), "Mentalis"), ((320, 377),(316, 426), "Jaw")],
                    [((347, 373), (347, 362), "Levator Labii"), ((347, 373), (369, 357), "Zygomaticus"), ((347, 373),(361, 380), "Buccinator"), ((347, 373), (335, 373), "Orbicularis Oris"), ((347, 373), (347, 386), "Depressor Anguli Oris"), ((347, 373),(344, 410), "Jaw")],
                    [((320, 373), (321, 348), "Levator Labii"), ((320, 373), (324, 376), "Buccinator"), ((320, 373), (308, 373), "Orbicularis Oris"), ((320, 373),(317, 358), "Mentalis"), ((320, 373),(319, 388), "Jaw")],
                    [((293, 373), (293, 351), "Levator Labii"), ((293, 373), (293, 360), "Mentalis")],
                    [((265, 373), (263, 348), "Levator Labii"), ((265, 373),(261, 376), "Buccinator"), ((265, 373),(277, 373), "Orbicularis Oris"), ((265, 373),(268, 358), "Mentalis"), ((265, 373),(263, 388),"Jaw")],
                    [((238, 373), (237, 362), "Levator Labii"), ((238, 373), (218, 357),"Zygomaticus"), ((238, 373), (224, 380),"Buccinator"), ((238, 373), (250, 373), "Orbicularis Oris"), ((238, 373), (239, 386), "Depressor Anguli Oris"), ((238, 373),(237, 410), "Jaw")],
                    ]
    chinPoints = [(282, 425), (292, 423),(303, 425)]
    chinVectors = [[((282, 425), (283, 412), "Mentalis"), ((282, 425), (281, 457), "Jaw")],
                   [((292, 423), (293, 411), "Mentalis"), ((292, 423),(292, 454), "Jaw")],
                   [((303, 425), (302, 412), "Mentalis"), ((303, 425),(301, 457), "Jaw")]
                   ]
    #[(x,y), w, h is rect beginning at (x,y) with width w and height h
    leftPupilPoints = [(210, 212), 20, 20]
    rightPupilPoints = [(360, 212), 20, 20]
    leftIrisPoints = [(217, 219), 5, 5]
    rightIrisPoints = [(367, 219), 5, 5]
    #[(x,y), w, h, d, dt, t  is white rect beginning at (x,y) with width w and height h 
    # for blinking: direction d, and time to hold eyes open dt, and timer which decreases
    width = 22
    height = 1
    direction = 1
    defaultBlinkTime = 30 #TODO
    timer = defaultBlinkTime
    leftEyelidPoints = [(209, 207), width, height, direction, defaultBlinkTime, timer]
    rightEyelidPoints = [(359, 207), width, height, direction, defaultBlinkTime, timer]

    eyebrowLeft = FaceFeature(eyebrowLeftPoints, eyebrowLeftVectors, "eyebrowLeft")
    eyebrowRight = FaceFeature(eyebrowRightPoints, eyebrowRightVectors, "eyebrowRight")
    rightEye = FaceFeature(rightEyePoints,rightEyeVectors, "rightEye")
    leftEye = FaceFeature(leftEyePoints,leftEyeVectors, "leftEye")
    nose = FaceFeature(nosePoints, noseVectors, "nose")
    mouth = FaceFeature(mouthPoints, mouthVectors, "mouth")
    chin = FaceFeature(chinPoints, chinVectors, "chin")
    leftPupil = FaceFeature(leftPupilPoints, [], "leftPupil")
    rightPupil = FaceFeature(rightPupilPoints, [], "rightPupil")
    rightIris = FaceFeature(rightIrisPoints, [], "rightIris")
    leftIris = FaceFeature(leftIrisPoints, [], "leftIris")
    rightEyelid = FaceFeature(rightEyelidPoints, [], "rightEyelid")
    leftEyelid= FaceFeature(leftEyelidPoints, [], "leftEyelid")
    
    faceFeatures = [eyebrowLeft, eyebrowRight, rightEye, leftEye, nose, mouth, chin, leftPupil, rightPupil, leftIris, rightIris, rightEyelid, leftEyelid]
    face = FaceAnimation(faceFeatures)
    window.addWidgetToLayout(face)
    window.setCentralWidget(window.widget)
    window.show()
    
    app.exec_()

if __name__ == '__main__':
    main()


