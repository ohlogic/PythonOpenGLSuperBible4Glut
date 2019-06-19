#!/usr/bin/python3

# scissor.py
# Demonstates OpenGL Primitive GL_POINTS
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Scissor.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com


import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'

def InitGL(Width, Height):	
    pass

    # Called to draw scene
def DrawGLScene():
        # Clear the window with the current clearing color
        glClearColor(0, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Now set scissor to smaller red sub region
        glClearColor(1, 0, 0, 0)
        glScissor(100, 100, 600, 400)
        glEnable(GL_SCISSOR_TEST)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Finally, an even smaller green rectangle
        glClearColor(0, 1, 0, 0)
        glScissor(200, 200, 400, 200)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Turn scissor back off for next render
        glDisable(GL_SCISSOR_TEST)
        

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
    window = glutCreateWindow("Lines Example")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    glutIdleFunc(DrawGLScene)
    
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    #glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()







