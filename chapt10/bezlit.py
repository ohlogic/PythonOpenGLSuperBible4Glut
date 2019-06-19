#!/usr/bin/python3

# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on bezlit.cpp
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

ctrlPoints = (GLfloat * 3 * 3 * 3) (((  -4.0, 0.0, 4.0),
                               ( -2.0, 4.0, 4.0),
                               ( 4.0, 0.0, 4.0 )),

                             ((  -4.0, 0.0, 0.0),
                              ( -2.0, 4.0, 0.0),
                              (  4.0, 0.0, 0.0 )),

                             ((  -4.0, 0.0, -4.0),
                              ( -2.0, 4.0, -4.0),
                              (  4.0, 0.0, -4.0 )))


# This function is used to superimpose the control points over the curve
def DrawPoints():
    # Set point size larger to make more visible
    glPointSize(5.0)

    # Loop through all control points for this example
    glBegin(GL_POINTS)
    for i in range(0, nNumPoints):
        for j in range(0, 3):
            glVertex3fv(ctrlPoints[i][j])
    glEnd()


def InitGL(Width, Height):

        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        # Draw in Blue
        glColor3f(0.0, 0.0, 1.0)	

        glEnable(GL_AUTO_NORMAL)
        
    # Called to draw scene
def DrawGLScene():
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Save the modelview matrix stack
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Rotate the mesh around to make it easier to see
        glRotatef(45.0, 0.0, 1.0, 0.0)
        glRotatef(60.0, 1.0, 0.0, 0.0)


        # Sets up the bezier
        # This actually only needs to be called once and could go in
        # the setup function
        glMap2f(GL_MAP2_VERTEX_3,	# Type of data generated
        0.0,						# Lower u range
        10.0,						# Upper u range
        0.0,						# Lover v range
        10.0,						# Upper v range
        ctrlPoints)		# array of control points

        # Enable the evaluator
        glEnable(GL_MAP2_VERTEX_3)

        # Use higher level functions to map to a grid, then evaluate the
        # entire thing.

        # Map a grid of 10 points from 0 to 10
        glMapGrid2f(10,0.0,10.0,10,0.0,10.0)

        # Evaluate the grid, using lines
        glEvalMesh2(GL_FILL,0,10,0,10)

        glPopMatrix()

        glutSwapBuffers() 

    ###################
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

        glOrtho(-10.0, 10.0, -10.0, 10.0, -10.0, 10.0)

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





