#!/usr/bin/python3
# bounce.py
# Demonstrates a simple animated rectangle program with pyglet
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Bounce.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initial square position and size
x = 0.0
y = 0.0
rsize = 25.0

# Step size in x and y directions
# (number of pixels to move each time)
xstep = 1.0
ystep = 1.0

# Keep track of windows changing width and height
windowWidth = 100.0
windowHeight = 100.0

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
    glRectf(x, y, x + rsize, y - rsize)
    
    # Flush drawing commands and swap
    # pyglet does this automatically when using pyglet.app.run()
    # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html
    
    glutSwapBuffers() 
    
def update(dy):
    global x, y, xstep, ystep
    # Reverse direction when you reach left or right edge
    if (x > windowWidth - rsize) or x < -windowWidth:
        xstep = -xstep
    
    # Reverse direction when you reach top or bottom edge
    if y > windowHeight or (y < -windowHeight + rsize):
        ystep = -ystep
        
    # Actually move the square
    x += xstep
    y += ystep
    
    # Check bounds.  This is in case the window is made
    # smaller while the rectangle is bouncing and the 
    # rectangle suddenly finds itself outside the new
    # clipping volume
    if x > windowWidth - rsize + xstep:
        x = windowWidth - rsize - 1.0
    elif x < -(windowWidth + xstep):
        x = -windowWidth - 1.0
        
    if y > windowHeight + ystep:
        y = windowHeight - 1.0
    elif y < -(windowHeight - rsize + ystep):
        y = -windowHeight + rsize - 1.0
    
    glutPostRedisplay()
    glutTimerFunc(  int(1/33.0), update, 0)
        
# Called when the window has changed size (including when the window is created)
def on_resize(w, h):
    
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
        windowWidth = 100.0
        windowHeight = 100.0 / aspectRatio
        glOrtho(-100.0, 100.0, -windowHeight, windowHeight, 1.0, -1.0)
    else:
        windowWidth = 100.0 * aspectRatio
        windowWidth = 100.0
        glOrtho(-windowWidth , windowWidth, -100.0, 100.0, 1.0, -1.0)
    
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
    window = glutCreateWindow("bounce")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    #####glutIdleFunc(DrawGLScene)
    glutTimerFunc( int(1/33.0), update, 0)
    
    glutReshapeFunc(on_resize)
    glutKeyboardFunc(keyPressed)

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()

    
    
    
    
    
    
    
    

