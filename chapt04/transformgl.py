#!/usr/bin/python3

# Demonstrates OpenGL coordinate transformation
# This is unsurprisingly slower than the c++ implementation, even with the timer changed
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Transformgl.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import time 

ESCAPE = b'\033'

import sys
sys.path.append("../shared")

from math import cos, sin

from math3d import M3D_PI, M3DVector3f, M3DMatrix44f, m3dTransformVector3, m3dDegToRad, m3dRotationMatrix44
from gltools import gltDrawTorus

xRot = 0.0
yRot = 0.0

def InitGL(Width, Height):
        
        # Bluish background
        glClearColor(0, 0, 0.5, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
def update(blah):
        global yRot
        yRot += 0.5

        glutPostRedisplay()
        glutTimerFunc( int(1.0/75.0), update, 0)

        time.sleep(1/75.0) #VERY simplistically run the app at ~75 fps, avoids high CPU usage!



    # Called to draw scene
def DrawGLScene():
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        transformationMatrix = M3DMatrix44f()
        # Build a rotation matrix
        m3dRotationMatrix44(transformationMatrix, m3dDegToRad(yRot), 0.0, 1.0, 0.0)
        transformationMatrix[12] = 0.0
        transformationMatrix[13] = 0.0
        transformationMatrix[14] = -2.5
            
        glLoadMatrixf(transformationMatrix)
        gltDrawTorus(0.35, 0.15, 40, 20)
        
        glutSwapBuffers()  
        
def keyPressed(*args):
        if args[0] == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()


    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        fAspect = float(w) / float(h)
        
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluPerspective(35.0, fAspect, 1.0, 50.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Manual Transformations Demo")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    #glutIdleFunc(DrawGLScene)
    glutTimerFunc( int(1.0/75.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    #glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()






