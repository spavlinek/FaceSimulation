import sys
import math
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #set size of window
        self.setGeometry(10, 10, 600, 600)


        self.setWindowTitle('Face Simulation')
        self.layout = QVBoxLayout(self)
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
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timeElapsed = 0
        self.timer.start(100)

        #keeps track of all of the widgets in Main Window
        self.widgets = []
    
    #adds widgets to the main window
    def addWidgetToLayout(self, widget):
        self.layout.addWidget(widget)
        self.widgets.append(widget)
    
    #useful for point specification
    def mousePressEvent(self, event):
        print("clicked at:", event.pos())
    
    def animation(self):
        for w in self.widgets:
            print(w)
            w.move()
        self.update()
        self.timeElapsed += 1
        # Capture and save the frame
        self.capture_frame()

    def capture_frame(self):
        pixmap = self.widget.grab()  # Capture the current frame
        frame_path = os.path.join(self.output_dir, f"frame_{self.frame_number:04d}.png")
        pixmap.save(frame_path)  # Save the frame as an image
        self.frame_number += 1


class Nose(QWidget):
    def __init__(self):
        super().__init__()
        self.smileSize = 0.5 #percentage of how full the smile should be
        #set up animation
        self.totalFrames = 10 #the amount of time in seconds we want it to take times the fps
        #neutral smile
        self.startPoints = [(245, 400),(300, 415),(355, 400)]
        
        #full smile default maximum values
        self.endPoints = [(245, 400),(300, 415),(355, 400)]
        
        
        #get the distance that each point should travel per second
        self.distancePointTravelsPerFrame = [0 for i in range(len(self.startPoints))]

        #convert points to QPointF
        for point in range(len(self.startPoints)):
            startX, startY = self.startPoints[point][0],self.startPoints[point][1]
            endX, endY = self.endPoints[point][0],self.endPoints[point][1]
            self.startPoints[point] = QPointF(startX, startY)
            self.endPoints[point] = QPointF(endX, endY)
        
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen for drawing
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)

        for i in range (len(self.startPoints)-1):
            print(self.startPoints[i])
            painter.drawLine(self.startPoints[i], self.startPoints[i+1])
        
    def move(self):
        #do nothing
        self.startPoints = self.startPoints

class Eyebrows(Nose):
    def __init__(self):
        super().__init__()
        self.startPoints = [(50,140), (100,120), (230,140)]
        self.endPoints = [(50,140), (100,120), (230,140)]
        #eyebrow2
        #[(370,140), (500,120), (550,140)]
        #eye 1
        #[(90,220),(120,190),(180,190),(210,220)]
        #eye2 
        #[(390,220),(420,190),(480,190),(510,220)]


class Mouth(QWidget):
    def __init__(self):
        super().__init__()
        self.smileSize = 0.5 #percentage of how full the smile should be
        #set up animation
        self.totalFrames = 10 #the amount of time in seconds we want it to take times the fps
        #neutral smile
        self.startPoints = [(260, 518),(280, 520),(300, 520), (320, 520), (340, 518), (320, 515),
                (300, 515), (280, 515), (260, 518)]
        
        #full smile default maximum values
        self.endPoints = [(150, 470), (235, 520),(300, 530), (370, 520),(450, 470),(385, 495),
                          (300, 510), (215, 495),(150, 470)]
        
        #full shocked "O" smile
        self.endPointsO = [(150, 470), (235, 520),(300, 530), (370, 520),(450, 470),(385, 460),
                          (300, 440), (215, 460),(150, 470)]
        
        #get the distance that each point should travel per second
        self.distancePointTravelsPerFrame = [0 for i in range(len(self.startPoints))]

        #convert points to QPointF
        for point in range(len(self.startPoints)):
            startX, startY = self.startPoints[point][0],self.startPoints[point][1]
            endX, endY = self.endPoints[point][0],self.endPoints[point][1]
            self.startPoints[point] = QPointF(startX, startY)
            self.endPoints[point] = QPointF(endX, endY)
        
        #change endPoints if the smileSize is different
        if self.smileSize != 1.0:
            self.endPoints = self.generateNewEndPoints(self.startPoints, self.endPoints, self.smileSize)
        
        #get the amount that each point must change by based on 
        for point in range(len(self.startPoints)):
            dist = self.getDistance(self.startPoints[point], self.endPoints[point])
            self.distancePointTravelsPerFrame[point] = dist/self.totalFrames

    def generateNewEndPoints(self, startPoints, endPoints, fraction):
        newEndPoints = []
        for i in range(len(startPoints)):
            startX, startY = startPoints[i].x(), startPoints[i].y()
            newX = (fraction *  (endPoints[i].x() - startX)) + startX
            newY = (fraction *  (endPoints[i].y() - startY)) + startY
            newEndPoints.append(QPointF(newX, newY))
            print(newX, newY)
        return newEndPoints
        
    

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen for drawing
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)

        for i in range (len(self.startPoints)-1):
            painter.drawLine(self.startPoints[i], self.startPoints[i+1])

    def move(self):
        for i in range(len(self.startPoints)):
            newPoint = self.changePointPos(i, self.startPoints[i])
            newX, newY = newPoint.x(), newPoint.y()
            #change the x,y coordinates only if they are less than the endPoints
            if not self.checkPointHasReachedEndValue(i, newX, newY):
                self.startPoints[i] = newPoint
    
    def checkPointHasReachedEndValue(self, i, newX, newY):
        endX = self.endPoints[i].x()
        endY = self.endPoints[i].y()
        #point0 and point8 moves along y = 0.43636x + 404.54
        if i == 0 or i == 8:
            return newX <= endX and newY <= endY
        #point1 moves along y = 520, with x decreasing 
        if i == 1:
            return newX <= endX and newY <= endY
        #point2 moves along x = 300 with y increasing 
        if i == 2:
            return newX <= endX and newY >= endY
        #point3 moves along y = 520, with x increasing
        if i == 3:
            return newX >= endX and newY >= endY
        #point4 moves along y = -0.4363x + 666.36363
        if i == 4:
            return newX >= endX and newY <= endY
        #point5 moves along y = -0.30769x + 613.4615
        if i == 5:
            return newX >= endX and newY <= endY
        #point6 moves along x = 300 with y decreasing 
        if i == 6:
            return newX >= endX and newY <= endY
        #point7 moves along y = 0.30769x + 428.846
        if i == 7:
            return newX <= endX and newY <= endY

    def getDistance(self, a, b):
        return (math.sqrt(((b.x()- a.x())**2)+((b.y() - a.y())**2)))
    
    def changePointPos(self, i, point):
        x = point.x()
        y = point.y()
        dist = self.distancePointTravelsPerFrame[i]
        #point0 and point8 moves along y = -0.43636x + 404.54
        if i == 8: return self.startPoints[0] #Point0 was already changed and 8 should be the same
        if i == 0:
            x = x-dist
            y = 404.54 + (0.43636*x)
            return QPointF(x,y)
        #point1 moves along y = 520, with x decreasing 
        if i == 1:
            return QPointF(x - dist, 520)
        #point2 moves along x = 300 with y increasing 
        if i == 2:
            return QPointF(300, y + dist)
        #point3 moves along y = 520, with x increasing
        if i == 3:
            return QPointF(x + dist, 520)
        #point4 moves along y = -0.4363x + 666.36363
        if i == 4:
            x = x+dist
            y = (-0.4363*x) + 666.36363
            return QPointF(x,y)
        #point5 moves along y = -0.30769x + 613.4615
        if i == 5:
            x = x+dist
            y = (-0.30769*x) + 613.4615
            return QPointF(x,y)
        #point6 moves along x = 300 with y decreasing 
        if i == 6:
            return QPointF(300, y - dist)
        #point7 moves along y = 0.30769x + 428.846
        if i == 7:
            x = x-dist
            y = 428.846 + (0.30769*x)
            return QPointF(x,y)
        
    def getSlope(point1, point2): #returns the slope or None if line is vertical
        x1, y1 = point1.x(), point1.y()
        x2, y2 = point2.x(), point2.y()

        # Calculate the slope
        if x2 - x1 != 0:
            m = (y2 - y1) / (x2 - x1)
        else:
            # Handle the case where the line is vertical (infinite slope)
            m = None
        return m

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # mouth = Mouth()
    # nose = Nose()
    #eyebrow = Eyebrows()
    window.addWidgetToLayout(mouth)
    window.addWidgetToLayout(nose)
    #window.addWidgetToLayout(eyebrow)
    window.setCentralWidget(window.widget)
    window.show()
    
    app.exec_()

if __name__ == '__main__':
    main()
