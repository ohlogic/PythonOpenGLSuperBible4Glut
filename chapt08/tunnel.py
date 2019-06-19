#!/usr/bin/python3

# Demonstrates mipmapping and using texture objects
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on Tunnel.cpp
# OpenGL SuperBible
# Richard S. Wright Jr.


import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import time 

ESCAPE = b'\033'

zPos = -60.0

# Texture Objects
TEXTURE_BRICK   = 0
TEXTURE_FLOOR   = 1
TEXTURE_CEILING = 2
TEXTURE_COUNT   = 3

textures = (GLuint * TEXTURE_COUNT)()

szTextureFiles = ['brick.jpg', 'floor.jpg', 'ceiling.jpg']

def InitGL(Width, Height):

        # Black Background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # Textures applied as decals, no lighting or coloring effects
        glEnable(GL_TEXTURE_2D)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        # Load textures
        glGenTextures(TEXTURE_COUNT, textures)
        for iLoop in range (0, TEXTURE_COUNT):
            # Bind to next texture object
            glBindTexture(GL_TEXTURE_2D, textures[iLoop])
            
            # Load texture, set filter and wrap modes
            img = Image.open(szTextureFiles[iLoop]).convert("RGB")
            raw_image = img.tobytes()
            
            # Load texture, set filter and wrap modes
            gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.width, img.height, GL_RGB, GL_UNSIGNED_BYTE, raw_image)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
        
        
    # Called to draw scene
def DrawGLScene():
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Save the matrix state and do the rotations
        glPushMatrix()
        # Move object back and do in place rotation
        glTranslatef(0.0, 0.0, zPos)

        # Floor
        z = 60.0 
        while z >= -1.0:
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_FLOOR])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, -10.0, z - 10.0)
                
            glEnd()

            # Ceiling
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_CEILING])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, 10.0, z)
                
            glEnd()

            
            # Left Wall
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_BRICK])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(-10.0, -10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z)
                
            glEnd()


            # Right Wall
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 1.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(10.0, -10.0, z)
                
            glEnd()
            z -= 10.0
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
        gluPerspective(90.0, fAspect, 1.0, 120.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
def specialkeyPressed(key, x, y):
        global zPos
        if key == GLUT_KEY_UP:
            zPos += 1.0
        elif key == GLUT_KEY_DOWN:
            zPos -= 1.0

        glutPostRedisplay()

def keyPressed(key, x, y):
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()
        elif key in (b'1', b'2', b'3', b'4', b'5', b'6'):
            for i in range(TEXTURE_COUNT):
                glBindTexture(GL_TEXTURE_2D, textures[i])
                if key == b'1':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                elif key == b'2':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                elif key == b'3':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                elif key == b'4':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
                elif key == b'5':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
                elif key == b'6':
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        
        glutPostRedisplay()
            
# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Tunnel")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    #glutIdleFunc(DrawGLScene)
    #glutTimerFunc( int(1.0/60.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()








