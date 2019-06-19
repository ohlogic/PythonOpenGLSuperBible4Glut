#!/usr/bin/python3

# Demonstrates OpenGL evaluators to draw bezier curve
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Bezier.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import time 

ESCAPE = b'\033'


from random import randint

import sys
sys.path.append("../shared")

# The number of control points for this curve
nNumPoints = 3

ctrlPoints = (GLfloat * 3 * 4)(   (-4.0, 0.0, 0.0),	# End Point
                                            (-6.0, 4.0, 0.0),	# Control Point
                                            (6.0, -4.0, 0.0),	# Control Point
                                            (4.0, 0.0, 0.0)) 	# End Point



# This function is used to superimpose the control points over the curve
def DrawPoints():
    # Set point size larger to make more visible
    glPointSize(5.0)

    # Loop through all control points for this example
    glBegin(GL_POINTS)
    for i in range(0, nNumPoints):
       glVertex2fv( (ctrlPoints[i][0], ctrlPoints[i][1]))
    glEnd()


def InitGL(Width, Height):

        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        # Draw in Blue
        glColor3f(0.0, 0.0, 1.0)	


    # Called to draw scene
def DrawGLScene():

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Sets up the bezier
        # This actually only needs to be called once and could go in
        # the setup function

        glMap1f(GL_MAP1_VERTEX_3,  # Type of data generated
        0.0,                                    # Lower u range
        100.0,                                 # Upper u range
        ctrlPoints)                  # array of control points

        # Enable the evaluator
        glEnable(GL_MAP1_VERTEX_3)

        # Use a line strip to "connect-the-dots"
        glBegin(GL_LINE_STRIP)
        
        for i in range (0, 101):
            # Evaluate the curve at this point
            glEvalCoord1f(i) 
        glEnd()

        # Use higher level functions to map to a grid, then evaluate the
        # entire thing.
        # Put these two functions in to replace above loop

        # Map a grid of 100 points from 0 to 100
        #glMapGrid1d(100,0.0,100.0)

        # Evaluate the grid, using lines
        #glEvalMesh1(GL_LINE,0,100)

        # Draw the Control Points
        DrawPoints()

        glutSwapBuffers() 

    ###################/
    # Set 2D Projection negative 10 to positive 10 in X and Y
    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

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
    window = glutCreateWindow("2D Bezier Curve")
    
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




