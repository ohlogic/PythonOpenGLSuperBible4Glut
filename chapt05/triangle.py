#!/usr/bin/python3

# Demonstrates OpenGL color triangle
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# based heavily on ccube.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
ESCAPE = b'\033'


xRot = 0.0
yRot = 0.0

def InitGL(Width, Height):

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

    # Called to draw scene
def DrawGLScene():
        
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Enable smooth shading
        glShadeModel(GL_SMOOTH)

        # Draw the triangle
        glBegin(GL_TRIANGLES)

        # Red Apex
        glColor3ub(255,0,0)
        glVertex3f(0.0,200.0,0.0)

        # Green on the right bottom corner
        glColor3ub(0,255,0)
        glVertex3f(200.0,-70.0,0.0)

        # Blue on the left bottom corner
        glColor3ub(0,0,255)
        glVertex3f(-200.0, -70.0, 0.0)
        
        glEnd()

        glutSwapBuffers()
        
        
def ReSizeGLScene(w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glLoadIdentity()

        # Window is higher than wide
        if w <= h:
            windowHeight = 250.0 * h / w
            windowWidth = 250.0
        else:
            #window wider than high
            windowWidth = 250.0 * w/h
            windowHeight = 250.0
            
        # Set the clipping volume
        glOrtho(-windowWidth, windowWidth, -windowHeight, windowHeight, 1.0, -1.0)
        
        
def keyPressed(key, x, y):
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()
        
# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("RGB Triangle")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    #glutIdleFunc(DrawGLScene)
    #glutTimerFunc( int(1.0/60.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    #glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()









