#!/usr/bin/python3

# Demonstrates Perspective Projection
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Perspect.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'


xRot = 0.0
yRot = 0.0

lightArrayType = GLfloat * 4

def InitGL(Width, Height):

        # Light values and coordinates
        
        whiteLight = lightArrayType(0.45, 0.45, 0.45, 1.0)
        sourceLight = lightArrayType(0.25, 0.25, 0.25, 1.0)
        lightPos = lightArrayType(-50.0, 25.0, 250.0, 0.0)

        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight)
        glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

    # Called to draw scene
def DrawGLScene():

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fZ = 100.0
        bZ = -100.0

        # Save the matrix state and do the rotations
        glPushMatrix()
        glTranslatef(0.0, 0.0, -300.0)
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Set material color, Red
        glColor3f(1.0, 0.0, 0.0)

        # Front Face #################
        glBegin(GL_QUADS)
        
        # Pointing straight out Z
        glNormal3f(0.0, 0.0, 1.0)

        # Left Panel
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(-50.0, -50.0, fZ)
        glVertex3f(-35.0, -50.0, fZ)
        glVertex3f(-35.0,50.0,fZ)

        # Right Panel
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(35.0, 50.0, fZ)
        glVertex3f(35.0, -50.0, fZ)
        glVertex3f(50.0,-50.0,fZ)

        # Top Panel
        glVertex3f(-35.0, 50.0, fZ)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, 50.0,fZ)

        # Bottom Panel
        glVertex3f(-35.0, -35.0, fZ)
        glVertex3f(-35.0, -50.0, fZ)
        glVertex3f(35.0, -50.0, fZ)
        glVertex3f(35.0, -35.0,fZ)

        # Top length section ##############
        # Normal points up Y axis
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(50.0, 50.0, bZ)
        glVertex3f(-50.0,50.0,bZ)
        
        # Bottom section
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-50.0, -50.0, fZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(50.0, -50.0, bZ)
        glVertex3f(50.0, -50.0, fZ)

        # Left section
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(50.0, 50.0, fZ)
        glVertex3f(50.0, -50.0, fZ)
        glVertex3f(50.0, -50.0, bZ)
        glVertex3f(50.0, 50.0, bZ)

        # Right Section
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-50.0, 50.0, fZ)
        glVertex3f(-50.0, 50.0, bZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(-50.0, -50.0, fZ)
        
        glEnd()

        glFrontFace(GL_CW)		# clock-wise polygons face out

        glBegin(GL_QUADS)
        
        # Back section
        # Pointing straight out Z
        glNormal3f(0.0, 0.0, -1.0)	

        # Left Panel
        glVertex3f(-50.0, 50.0, bZ)
        glVertex3f(-50.0, -50.0, bZ)
        glVertex3f(-35.0, -50.0, bZ)
        glVertex3f(-35.0,50.0,bZ)

        # Right Panel
        glVertex3f(50.0, 50.0, bZ)
        glVertex3f(35.0, 50.0, bZ)
        glVertex3f(35.0, -50.0, bZ)
        glVertex3f(50.0,-50.0,bZ)

        # Top Panel
        glVertex3f(-35.0, 50.0, bZ)
        glVertex3f(-35.0, 35.0, bZ)
        glVertex3f(35.0, 35.0, bZ)
        glVertex3f(35.0, 50.0,bZ)

        # Bottom Panel
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(-35.0, -50.0, bZ)
        glVertex3f(35.0, -50.0, bZ)
        glVertex3f(35.0, -35.0,bZ)
    
        # Insides ##############/
        glColor3f(0.75, 0.75, 0.75)

        # Normal points up Y axis
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, 35.0, bZ)
        glVertex3f(-35.0,35.0,bZ)
        
        # Bottom section
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-35.0, -35.0, fZ)
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(35.0, -35.0, bZ)
        glVertex3f(35.0, -35.0, fZ)

        # Left section
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(-35.0, 35.0, fZ)
        glVertex3f(-35.0, 35.0, bZ)
        glVertex3f(-35.0, -35.0, bZ)
        glVertex3f(-35.0, -35.0, fZ)

        # Right Section
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(35.0, 35.0, fZ)
        glVertex3f(35.0, -35.0, fZ)
        glVertex3f(35.0, -35.0, bZ)
        glVertex3f(35.0, 35.0, bZ)
            
        glEnd()

        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out

        # Restore the matrix state
        glPopMatrix()
        
        glutSwapBuffers()  
        
def ReSizeGLScene(w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h);
        fAspect = float(w)/float(h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        gluPerspective(60.0, fAspect, 1.0, 400.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

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
            
        #glutPostRedisplay()
            
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
    window = glutCreateWindow("Perspective Projection")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    glutIdleFunc(DrawGLScene)
    #glutTimerFunc( int(1.0/10.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()








