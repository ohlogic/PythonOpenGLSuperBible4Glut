#!/usr/bin/python3
# simple.py
# The Simplest OpenGL program with pyglet
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Simple.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'

def InitGL(Width, Height):	
        
    # Setup the rendering state
    glClearColor(0, 0, 1, 1)

    # Called to draw scene
def DrawGLScene():
    # Clear the window with the current clearing color
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Flush drawing commands
    glFlush()

    glutSwapBuffers() 

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()
        

# Main program entry point
if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("simple")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    #glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()

