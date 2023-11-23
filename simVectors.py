import numpy as np

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

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #set size of window
        self.setGeometry(0, 0, 600, 600)

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
        self.timer.start(100)

        #keeps track of all of the widgets in Main Window
        self.widgets = []

        self.muscleGroup = None
        self.percent = None
    
    #adds widgets to the main window
    def addWidgetToLayout(self, widget):
        self.layout.addWidget(widget)
        self.widgets = self.widgets + [widget]
    
    def animation(self):
        for w in self.widgets:
            w.moveWidget()
        self.update()
        self.timeElapsed += 1
        # Capture and save the frame
        self.capture_frame()

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
    mouthVectors = [ [((238, 373), (237, 362), "Levator Labii"), ((238, 373), (218, 357),"Zygomaticus"), ((238, 373), (224, 380),"Buccinator"), ((238, 373), (238, 373), "Orbicularis Oris"), ((238, 373), (239, 386), "Depressor Anguli Oris"), ((238, 373),(237, 410), "Jaw")],
                    [((265, 377), (258, 371),"Zygomaticus"), ((265, 377),(254, 381), "Buccinator"), ((265, 377), (277, 377), "Orbicularis Oris"), ((265, 377), (263, 383), "Depressor Anguli Oris"), ((265, 377),(265, 369),"Mentalis"), ((265, 377),(265, 426), "Jaw")],
                    [((293, 377), (293, 370), "Mentalis"), ((293, 377),(291, 426), "Jaw")],
                    [((320, 377), (327, 371), "Zygomaticus"), ((320, 377), (324, 381), "Buccinator"), ((320, 377), (308, 376), "Orbicularis Oris"), ((320, 377), (323, 383),"Depressor Anguli Oris"), ((320, 377),(318, 370), "Mentalis"), ((320, 377),(316, 426), "Jaw")],
                    [((347, 373), (347, 362), "Levator Labii"), ((347, 373), (369, 357), "Zygomaticus"), ((347, 373),(360, 380), "Buccinator"), ((347, 373), (330, 374), "Orbicularis Oris"), ((347, 373), (347, 386), "Depressor Anguli Oris"), ((347, 373),(344, 410), "Jaw")],
                    [((320, 373), (321, 348), "Levator Labii"), ((320, 373), (324, 377), "Buccinator"), ((320, 373), (308, 372), "Orbicularis Oris"), ((320, 373),(317, 358), "Mentalis"), ((320, 373),(319, 388), "Jaw")],
                    [((293, 373), (293, 351), "Levator Labii"), ((293, 373), (293, 360), "Mentalis")],
                    [((265, 373), (263, 348), "Levator Labii"), ((265, 373),(254, 376), "Buccinator"), ((265, 373),(277, 372), "Orbicularis Oris"), ((265, 373),(268, 358), "Mentalis"), ((265, 373),(263, 388),"Jaw")],
                    [((238, 373), (237, 362), "Levator Labii"), ((238, 373), (218, 357),"Zygomaticus"), ((238, 373), (224, 380),"Buccinator"), ((238, 373), (238, 373), "Orbicularis Oris"), ((238, 373), (239, 386), "Depressor Anguli Oris"), ((238, 373),(237, 410), "Jaw")],
                    ]
    chinPoints = [(282, 425), (292, 423),(303, 425)]
    chinVectors = [[((282, 425), (283, 412), "Mentalis"), ((282, 425), (281, 457), "Jaw")],
                   [((292, 423), (293, 411), "Mentalis"), ((292, 423),(292, 454), "Jaw")],
                   [((303, 425), (302, 412), "Mentalis"), ((303, 425),(301, 457), "Jaw")]
                   ]
    #[(x,y), w, h is rect beginning at (x,y) with width w and height h
    leftPupilPoints = [(210, 212), 20, 20]
    rightPupilPoints = [(360, 212), 20, 20]

    eyebrowLeft = FaceFeature(eyebrowLeftPoints, eyebrowLeftVectors, "eyebrowLeft")
    eyebrowRight = FaceFeature(eyebrowRightPoints, eyebrowRightVectors, "eyebrowRight")
    rightEye = FaceFeature(rightEyePoints,rightEyeVectors, "rightEye")
    leftEye = FaceFeature(leftEyePoints,leftEyeVectors, "leftEye")
    nose = FaceFeature(nosePoints, noseVectors, "nose")
    mouth = FaceFeature(mouthPoints, mouthVectors, "mouth")
    chin = FaceFeature(chinPoints, chinVectors, "chin")
    leftPupil = FaceFeature(leftPupilPoints, [], "leftPupil")
    rightPupil = FaceFeature(rightPupilPoints, [], "rightPupil")

    #facePoints = [eyebrowLeftPoints, eyebrowRightPoints, rightEyePoints, leftEyePoints, nosePoints, mouthPoints, chinPoints]
    #faceVectors = [eyebrowLeftVectors, eyebrowRightVectors, rightEyeVectors, leftEyeVectors, noseVectors, mouthVectors, chinVectors]
    faceFeatures = [eyebrowLeft, eyebrowRight, rightEye, leftEye, nose, mouth, chin, leftPupil, rightPupil]
    face = FaceAnimation(faceFeatures)
    window.addWidgetToLayout(face)
    window.setCentralWidget(window.widget)
    window.show()
    
    app.exec_()

if __name__ == '__main__':
    main()


