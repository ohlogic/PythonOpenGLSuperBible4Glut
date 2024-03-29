#!/usr/bin/python3

# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Nurbc.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import time 

ESCAPE = b'\033'


import sys
sys.path.append("../shared")

# NURBS object
global pNurb

# The number of control points for this curve
nNumPoints = 4

# Mesh extends four units -6 to +6 along x and y axis
# Lies in Z plane
#                 u  v  (x,y,z)	
ctrlPoints = (GLfloat * 3 * 4)((-6.0, -6.0, 0.0),
                                (2.0, -2.0, 8.0),
                                (2.0, 6.0, 0.0),
                                (6.0, 6.0, 0.0))

# Knot sequence for the NURB
Knots = (GLfloat * 8)(0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0)

# Called to draw the control points in Red over the NURB
def DrawPoints():
    # Large Red Points
    glPointSize(5.0)
    glColor3ub(255,0,0)

    # Draw all the points in the array
    glBegin(GL_POINTS)
    for i in range(0, nNumPoints):
       glVertex2fv( (ctrlPoints[i][0], ctrlPoints[i][1]) )
    glEnd()
    
def InitGL(Width, Height):

        global pNurb
        
        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        # Setup the Nurbs object
        pNurb = gluNewNurbsRenderer()
        gluNurbsProperty(pNurb, GLU_SAMPLING_TOLERANCE, 25.0)
        gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, float(GLU_FILL))


    # Called to draw scene
def DrawGLScene():

        # Draw in Blue
        glColor3ub(0,0,220)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the modelview matrix stack
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Rotate the mesh around to make it easier to see
        glRotatef(330.0, 1.0,0.0,0.0)
        
        # Render the NURB
        # Begin the NURB definition
        gluBeginCurve(pNurb)
        
        # Evaluate the surface
        gluNurbsCurve(pNurb, 
            Knots,
            
            ctrlPoints, 
            
            GL_MAP1_VERTEX_3)
        
        # Done with surface
        gluEndCurve(pNurb)
        
        # Show the control points
        DrawPoints()

        # Restore the modelview matrix
        glPopMatrix()

        glutSwapBuffers() 



def ReSizeGLScene(w, h):

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Perspective view
        gluPerspective (45.0, float(w)/float(h), 1.0, 40.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Viewing transformation, position for better view
        glTranslatef (0.0, 0.0, -20.0)

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
    window = glutCreateWindow("NURBS Curve")
    
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






