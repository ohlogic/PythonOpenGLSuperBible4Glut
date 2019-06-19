#!/usr/bin/python3
# glrect.py
# Just draw a single rectangle in the middle of the screen
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: GLRect.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

#import pyglet
#from pyglet.gl import *
#from pyglet import window

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
    
    # Set current drawing color to red
    #               R,      G,      B
    glColor3f(1.0, 0.0, 0.0)
    
    # Draw a filled rectangle with current color
    glRectf(-25.0, 25.0, 25.0, -25.0)
    
    # Flush drawing commands
    glFlush()
        
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
    
    # Establish clipping volume (left, right, bottom, top, near, far)
    aspectRatio = float(w) / float(h)
    if w <= h:
        glOrtho(-100.0, 100.0, -100.0/aspectRatio, 100.0/aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
        
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
    window = glutCreateWindow("3D Effects Demo")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()

