#!/usr/bin/python3

# single.py
# Single buffer rendering
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Bounce.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com


from math import cos, sin

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'

# TODO: actually use single buffering

radius = 0.1
angle = 0.0

def InitGL(Width, Height):	
    pass
    
    # Called to draw scene
def DrawGLScene():
        glClearColor(0, 0, 1, 0)
        if angle == 0.0:
            glClear(GL_COLOR_BUFFER_BIT)
        
        glBegin(GL_POINTS)
        glVertex2d(radius * cos(angle), radius * sin(angle))
        glEnd()
            
        glFlush()
        
def update(dy):
        global radius, angle
        radius *= 1.01
        angle += 0.1
        
        if angle > 30.0:
            radius = 0.1
            angle = 0.0
        
        glutTimerFunc(  int(1.0/20.0), update, 0)
        
    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Set the perspective coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set the 2D Coordinate system
        gluOrtho2D(-4.0, 4.0, -3.0, 3.0)
        
        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
def keyPressed(*args):
        if args[0] == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()

# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Single Buffering")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    glutIdleFunc(DrawGLScene)
    
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    #glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    glutTimerFunc( int(1.0/20.0), update, 0)
        
    # Start Event Processing Engine	
    glutMainLoop()




    
