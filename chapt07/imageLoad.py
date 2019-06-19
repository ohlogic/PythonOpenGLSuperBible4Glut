#!/usr/bin/python3

# Demonstrates loading and displaying bitmaps
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on Bitmaps.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.


import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

ESCAPE = b'\033'


def InitGL(Width, Height):

        # Black background
        glClearColor(0.0, 0.0, 0.0, 0.0)

    # Called to draw scene
def DrawGLScene():
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)
        
        img = Image.open("fire.jpg").convert("RGB")
        
        # Use window coordinates to set raster position.
        glRasterPos2i(0, 0)
        
        raw_image = img.rotate(180).tobytes()

        glDrawPixels(img.width, img.height, GL_RGB, GL_UNSIGNED_BYTE, raw_image)
        
        glutSwapBuffers() 
    # For this example, it really doesn't matter what the 
    # projection is since we are using glWindowPos

def ReSizeGLScene(w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
            
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluOrtho2D(0.0, float(w), 0.0, float(h))

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
    window = glutCreateWindow("OpenGL Image Loading")
    
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










