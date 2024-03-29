#!/usr/bin/python3

# Demonstrates OpenGL coordinate transformation
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Atom.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'

xRot = 0.0
yRot = 0.0

# Angle of revolution around the nucleus
fElect1 = 0.0

def InitGL(Width, Height):

        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW) # counter-clockwise polygons face out
        glEnable(GL_CULL_FACE) # Do not calculate inside of jet(?)
        
        # Black background
        glClearColor(0, 0, 0, 1)

def update(blah):
        global fElect1
        
        # Increment the angle of revolution
        fElect1 += 10.0
        if(fElect1 > 360.0):
            fElect1 = 0.0

        glutTimerFunc( int(1.0/10.0), update, 0)

    # Called to draw scene
def DrawGLScene():
        global fElect1
        
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Red Nucleus
        glColor3ub(255, 0, 0)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 10.0, 15, 15)
        gluDeleteQuadric(sphere)

        # Yellow Electrons
        glColor3ub(255, 255, 0)

        # First Electron Orbit
        # Save viewing transformation
        glPushMatrix()
        
        # Rotate by angle of revolution
        glRotatef(fElect1, 0.0, 1.0, 0.0)
        
        # Translate out from origin to orbit distance
        glTranslatef(90.0, 0.0, 0.0)
        
        # Draw the electron
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 6.0,15, 15)    
        gluDeleteQuadric(sphere)
        
        # Restore the viewing transformation
        glPopMatrix()
        
        # Second Electron Orbit
        glPushMatrix()
        glRotatef(45.0, 0.0, 0.0, 1.0)
        glRotatef(fElect1, 0.0, 1.0, 0.0)
        glTranslatef(-70.0, 0.0, 0.0)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 6.0, 15, 15)    
        gluDeleteQuadric(sphere)
        glPopMatrix()

        # Third Electron Orbit
        glPushMatrix()
        glRotatef(360.0-45.0,0.0, 0.0, 1.0)
        glRotatef(fElect1, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.0, 60.0)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 6.0, 15, 15)    
        gluDeleteQuadric(sphere)
        glPopMatrix()

        glutSwapBuffers() 

    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect = float(w) / float(h)
        gluPerspective(45.0, aspect, 1.0, 500.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -250.0)
        
def specialkeyPressed(key, x, y):
        global xRot, yRot
        if key == GLUT_KEY_UP:
            xRot -= 5.0
        elif key == GLUT_KEY_DOWN:
            xRot += 5.0
        elif key == GLUT_KEY_LEFT:
            yRot -= 5.0
        elif key == GLUT_KEY_RIGHT:
            yRot += 5.0
        
        if xRot > 356.0:
            xRot = 0.0
        elif xRot < -1.0:
            xRot = 355.0
        if yRot > 356.0:
            yRot = 0.0
        if yRot < -1.0:
            yRot = 355.0
            
        glutPostRedisplay()
            
def keyPressed(*args):
        if args[0] == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()



# Main program entry point
if __name__ == '__main__':


    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("OpenGL Atom")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    #glutIdleFunc(DrawGLScene)
    glutTimerFunc( int(1.0/10.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()




