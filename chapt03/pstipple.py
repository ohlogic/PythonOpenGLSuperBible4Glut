#!/usr/bin/python3

# pstipple.py
# Demonstates OpenGL Polygon Stippling
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: PStipple.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'

xRot = 0.0
yRot = 0.0
fireType = GLubyte * 128

fire = fireType(0x00, 0x00, 0x00, 0x00, 
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0xc0,
                        0x00, 0x00, 0x01, 0xf0,
                        0x00, 0x00, 0x07, 0xf0,
                        0x0f, 0x00, 0x1f, 0xe0,
                        0x1f, 0x80, 0x1f, 0xc0,
                        0x0f, 0xc0, 0x3f, 0x80,	
                        0x07, 0xe0, 0x7e, 0x00,
                        0x03, 0xf0, 0xff, 0x80,
                        0x03, 0xf5, 0xff, 0xe0,
                        0x07, 0xfd, 0xff, 0xf8,
                        0x1f, 0xfc, 0xff, 0xe8,
                        0xff, 0xe3, 0xbf, 0x70, 
                        0xde, 0x80, 0xb7, 0x00,
                        0x71, 0x10, 0x4a, 0x80,
                        0x03, 0x10, 0x4e, 0x40,
                        0x02, 0x88, 0x8c, 0x20,
                        0x05, 0x05, 0x04, 0x40,
                        0x02, 0x82, 0x14, 0x40,
                        0x02, 0x40, 0x10, 0x80, 
                        0x02, 0x64, 0x1a, 0x80,
                        0x00, 0x92, 0x29, 0x00,
                        0x00, 0xb0, 0x48, 0x00,
                        0x00, 0xc8, 0x90, 0x00,
                        0x00, 0x85, 0x10, 0x00,
                        0x00, 0x03, 0x00, 0x00,
                        0x00, 0x00, 0x10, 0x00
                        )
                    
                    
def InitGL(Width, Height):	

        # Setup the rendering state
        glClearColor(0, 0, 0, 1)
        
        # Set drawing color to red
        glColor3f(1, 0, 0)
        
        # Enable polygon stippling
        glEnable(GL_POLYGON_STIPPLE)

        glPolygonStipple(fire)
        
def DrawGLScene():
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Save matrix state and do the rotation
        glPushMatrix()
        glRotatef(xRot, 1, 0, 0)
        glRotatef(yRot, 0, 1, 0)
        
        # Begin the stop sign shape,
        # use a standard polygon for simplicity
        glBegin(GL_POLYGON)

        glVertex2f(-20.0, 50.0)
        glVertex2f(20.0, 50.0)
        glVertex2f(50.0, 20.0)
        glVertex2f(50.0, -20.0)
        glVertex2f(20.0, -50.0)
        glVertex2f(-20.0, -50.0)
        glVertex2f(-50.0, -20.0)
        glVertex2f(-50.0, 20.0)

        glEnd()
        
        # Restore transformations
        glPopMatrix()
        
        # Flush drawing commands
        # pyglet does this automatically when using pyglet.app.run()
        # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html
        glutSwapBuffers() 


    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):
        nRange = 100.0
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        if w <= h:
            glOrtho (-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
        else:
            glOrtho (-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

        # Reset Model view matrix stack
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
        
        if xRot > 356.0:
            xRot = 0.0
        elif xRot < -1.0:
            xRot = 355.0
        if yRot > 356.0:
            yRot = 0.0
        if yRot < -1.0:
            yRot = 355.0
            
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
    window = glutCreateWindow("Polygon Stippling")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    glutIdleFunc(DrawGLScene)
    
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()




