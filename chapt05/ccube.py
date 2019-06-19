#!/usr/bin/python3

# Demonstrates primative RGB Color Cube
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

        glEnable(GL_DEPTH_TEST)	
        glEnable(GL_DITHER)
        glShadeModel(GL_SMOOTH)

    # Called to draw scene
def DrawGLScene():
        
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)


        # Draw six quads
        glBegin(GL_QUADS)

        # Front Face
        # White
        glColor3ub(255, 255, 255)
        glVertex3f(50.0,50.0,50.0)

        # Yellow
        glColor3ub(255, 255, 0)
        glVertex3f(50.0,-50.0,50.0)

        # Red
        glColor3ub(255, 0, 0)
        glVertex3f(-50.0,-50.0,50.0)

        # Magenta
        glColor3ub(255, 0, 255)
        glVertex3f(-50.0,50.0,50.0)


        # Back Face
        # Cyan
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(50.0,50.0,-50.0)

        # Green
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(50.0,-50.0,-50.0)
        
        # Black
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(-50.0,-50.0,-50.0)

        # Blue
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-50.0,50.0,-50.0)

        # Top Face
        # Cyan
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(50.0,50.0,-50.0)

        # White
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(50.0,50.0,50.0)

        # Magenta
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(-50.0,50.0,50.0)

        # Blue
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-50.0,50.0,-50.0)

        # Bottom Face
        # Green
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(50.0,-50.0,-50.0)

        # Yellow
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(50.0,-50.0,50.0)

        # Red
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-50.0,-50.0,50.0)

        # Black
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(-50.0,-50.0,-50.0)

        # Left face
        # White
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(50.0,50.0,50.0)

        # Cyan
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(50.0,50.0,-50.0)

        # Green
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(50.0,-50.0,-50.0)

        # Yellow
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(50.0,-50.0,50.0)

        # Right face
        # Magenta
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(-50.0,50.0,50.0)

        # Blue
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-50.0,50.0,-50.0)

        # Black
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(-50.0,-50.0,-50.0)

        # Red
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-50.0,-50.0,50.0)

        glEnd()

        glPopMatrix()
        
        glutSwapBuffers()
        
def ReSizeGLScene(w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        fAspect = float(w)/float(h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        gluPerspective(35.0, fAspect, 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -400.0)

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
        
        xRot = float(int(xRot) % 360)
        yRot = float(int(yRot) % 360)
            
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
    window = glutCreateWindow("RGB Cube")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    #glutIdleFunc(DrawGLScene)
    #glutTimerFunc( int(1.0/10.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()











