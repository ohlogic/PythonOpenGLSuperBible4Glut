#!/usr/bin/python3

# Triangle.py
# Demonstrates OpenGL Triangle Fans, backface culling, and depth testing
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Triangle.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.



import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = b'\033'


iCull = True
iDepth = True
iOutline = True

xRot = 0.0
yRot = 0.0

# TODO: needs user interface to set cull, depth, outline

def InitGL(Width, Height):

        # Setup the rendering state
        glClearColor(0, 0, 0, 1)
        
        # Set drawing color to green
        glColor3f(0, 1, 0)

        # Set color shading model to flat
        glShadeModel(GL_FLAT)
        
        # Clockwise wound polygons are front facing, this is reversed
        # because we are using triangle fans
        glFrontFace(GL_CW)
        
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





    # Called to draw scene
def DrawGLScene():
        
        # Clear the window and the depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Turn culling on if flag is set
        if (iCull):
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE)
        
        # Enable depth testing if flag is set
        if (iDepth):
            glEnable(GL_DEPTH_TEST)
        else:
            glDisable(GL_DEPTH_TEST)
            
        # Draw back side as a polygon only, if flag is set
        if (iOutline):
            glPolygonMode(GL_BACK, GL_LINE)
        else:
            glPolygonMode(GL_BACK, GL_FILL)
            
        # Save matrix state and do the rotation
        glPushMatrix()
        glRotatef(xRot, 1, 0, 0)
        glRotatef(yRot, 0, 1, 0)
        
        # Begin a triangle fan
        glBegin(GL_TRIANGLE_FAN)
        
        # Pinnacle of cone is shared vertex for fan, moved up Z axis
        # to produce a cone instead of a circle
        glVertex3f(0.0, 0.0, 75.0)
        
        # Loop around in a circle and specify even points along the circle
        # as the vertices of the triangle fan
        iPivot = 1
        angle = 0.0
        
        #BS - Had to hack the 2.0 to 2.1 for rounding issues. 
        #BS - probably better ways to do this?
        
        while (angle < 2.1 * 3.14159):
            x = 50.0 * math.sin(angle)
            y = 50.0 * math.cos(angle)
            
            # Alternate color between red and green
            if ((iPivot % 2) == 0):
                glColor3f(0.0, 1.0, 0.0)
            else:
                glColor3f(1.0, 0.0, 0.0)
            
            # increment pivot to alternate color
            iPivot += 1
            
            # Specify the next vertex for the triangle fan
            glVertex2f(x, y)
            angle += 3.14159 / 8.0
        
        # Done drawing fan for cone
        glEnd()
        
        # Begin a new triangle fan to cover the bottom
        glBegin(GL_TRIANGLE_FAN)
        
        # Center of the fan is at the origin
        glVertex2f(0.0, 0.0)
        
        angle = 0.0
        #BS - Had to hack the 2.0 to 2.1 for rounding issues. 
        #BS - probably better ways to do this?
        while angle < 2.1 * 3.14159:
            x = 50.0 * math.sin(angle)
            y = 50.0 * math.cos(angle)
            
            # Alternate color between red and green
            if ((iPivot % 2) == 0):
                glColor3f(0.0, 1.0, 0.0)
            else:
                glColor3f(1.0, 0.0, 0.0)
            
            # increment pivot to alternate color
            iPivot += 1
            
            # Specify the next vertex for the triangle fan
            glVertex2f(x, y)
            angle += 3.14159 / 8.0
            
        # Done drawing the fan that covers the bottom
        glEnd()
        
        # Restore transformations
        glPopMatrix()

        # Flush drawing commands
        # pyglet does this automatically when using pyglet.app.run()
        # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html
        glutSwapBuffers() 

# Main program entry point
if __name__ == '__main__':


    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Triangle Culling Example")
    
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






