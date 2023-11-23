import numpy as np

import sys
import math
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from vectors import Vector
from faceFeature import FaceFeature

class FaceAnimation(QWidget):
    #faceFeatures is a list of faceFeatures
    #points come in the form of a 2D list containing tuples (x,y)
    #vectors are a list of lists, where each list corresponds to a specific facial feature (i.e. eyebrow, mouth)
    #each list of vectors at index i should correspond to the vectors that pull on the same point at index i in points
    #vectors are in the form (p1, p2, muscleGroup)
    def __init__(self, faceFeatures):
        super().__init__()
        self.faceFeatures = faceFeatures
        self.points = []
        vectors = []
        for faceFeature in self.faceFeatures:
            if faceFeature.name != "leftPupil" and faceFeature.name != "rightPupil":
                self.points.append(faceFeature.points)
                vectors.append(faceFeature.vectors)
                
        self.vectors = [[[] for j in range(len(self.points[i]))] for i in range(len(self.points))]
        #convert vectors to type Vector and store in self.vectors
        for faceFeatureIndex in range(len(vectors)):
            for point in range(len(vectors[faceFeatureIndex])):
                for v in range(len(vectors[faceFeatureIndex][point])):
                    vector = vectors[faceFeatureIndex][point][v]
                    newVector = Vector(vector[0], vector[1], vector[2])
                    self.vectors[faceFeatureIndex][point].append(newVector)

        #convert points to QPointF
        for faceFeatureIndex in range(len(self.points)):
            for i in range(len(self.points[faceFeatureIndex])):
                point = self.points[faceFeatureIndex][i]
                self.points[faceFeatureIndex][i] = QPointF(point[0],point[1])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen for drawing points
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        # #draw the vectors
        # for faceFeatureIndex in range(len(self.vectors)):
        #     for p in range(len(self.vectors[faceFeatureIndex])):
        #         for v in self.vectors[faceFeatureIndex][p]:
        #             p1 = QPointF(v.p1[0], v.p1[1])
        #             p2 = QPointF(v.p2[0], v.p2[1])
        #             painter.drawLine(p1,p2)

        # Set the pen for drawing points
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)
        #draw the eyes which are circles
        for faceFeature in self.faceFeatures:
            if faceFeature.name == "leftPupil" or faceFeature.name == "rightPupil":
                painter.drawEllipse (faceFeature.points[0][0], faceFeature.points[0][1],faceFeature.points[1], faceFeature.points[2])
        #draw the other facial Features
        for faceFeatureIndex in range(len(self.points)):
            for i in range (len(self.points[faceFeatureIndex])-1):
                painter.drawLine(self.points[faceFeatureIndex][i], self.points[faceFeatureIndex][i+1])

    def moveWidget(self):
        percentage = 1.0
        muscleGroup = ["Outer Occipitofrontalis"]
        speed = 4
        for faceFeatureIndex in range(len(self.points)):
            faceFeaturePoints = self.points[faceFeatureIndex]
            faceFeatureVectors = self.vectors[faceFeatureIndex]
            for i in range(len(faceFeaturePoints)):
                currPoint = faceFeaturePoints[i]
                #pullingVectors = []
                for vector in faceFeatureVectors[i]:
                        if vector.muscleGroup in muscleGroup:
                            vector.updatePercentageOfVector(percentage)
                            if self.checkPointPosition(i, currPoint, vector):
                                # Calculate the new position
                                newPoint = self.pullOnPoint(i, currPoint, vector.unitVector, speed, 1)
                                self.points[faceFeatureIndex][i] = newPoint
                #use the vector in the correct muscleGroup
            #     if vector.muscleGroup in muscleGroup:
            #         pullingVectors.append(vector)
            # if len(pullingVectors) != 0:
            #     if len(pullingVectors) == 1:
            #         netVector = pullingVectors[0]
            #     else:
            #         netVector = self.createNetForce(pullingVectors)
            #     print(i, currPoint, netVector.x, netVector.y, netVector.unitVector)
            #     netVector.updatePercentageOfVector(percentage)
            #     if self.checkPointPosition(i, currPoint, vector):
            #         # Calculate the new position
            #         newPoint = self.pullOnPoint(i, currPoint, vector.unitVector, speed, 1)
            #         self.points[i] = newPoint
    

    #given a point, change the points location using a vector
    def pullOnPoint(self, i, point, vector, speed, direction):
        # Define a point's initial position
        point = np.array([point.x(), point.y()])
        # Define a force vector that represents the pull
        force = np.array(vector * speed * direction)  # Adjust the values as needed

        # Update the point's location by applying the force
        new_position = point + force
        #return the new position
        return QPointF(new_position[0], new_position[1])


    #if there are multiple forces pulling on one point
    #takes in list of forces aka unit vectors
    def createNetForce(self, forces):
        netForce = np.array([0.0, 0.0])
        for f in forces:
            netForce += np.array([f.x, f.y])
        p2 = (forces[0].p1[0] + netForce[0],forces[0].p1[1] + netForce[1])
        netVector = Vector(forces[0].p1, p2, "combined")
        return netVector #netForce should be a unit vector

    def checkPointPosition(self, i, point, vector):
        initialPos = np.array(vector.p1)
        currPos = np.array([point.x(), point.y()])
        distanceTraveled = np.linalg.norm(currPos - initialPos)
        if distanceTraveled >= vector.getVectorLength(): return False
        return True

