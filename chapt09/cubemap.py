#!/usr/bin/python3

# Demonstrates a applying a cube map to an object (sphere) using
# texgen, and using the same map for the skybox applying the coordinates
# manually
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on: cubemap.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import time 

ESCAPE = b'\033'

from random import randint
from math import cos, sin

import sys
sys.path.append("../shared")

from math3d import M3DMatrix44f, m3dInvertMatrix44
from glframe import GLFrame
from fakeglut import glutSolidSphere
from gltools import gltDrawSphere

frameCamera = GLFrame()

# Six sides of a cube map
szCubeFaces = ["pos_x.jpg", "neg_x.jpg", "pos_y.jpg", "neg_y.jpg", "pos_z.jpg", "neg_z.jpg"]
cube = (GLenum * 6)(GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                     # pyglet reverses y axis
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                     GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                     GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_Z)

# Draw the skybox. This is just six quads, with texture
# coordinates set to the corners of the cube map
def DrawSkyBox():
    fExtent = 15.0
    
    glBegin(GL_QUADS)
    #######################
    # Negative X
    glTexCoord3f(-1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glTexCoord3f(-1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glTexCoord3f(-1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)
    
    glTexCoord3f(-1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)


    #######################
    #  Postive X
    glTexCoord3f(1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    
    glTexCoord3f(1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glTexCoord3f(1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)
    
    glTexCoord3f(1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)


    ########################
    # Negative Z 
    glTexCoord3f(-1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glTexCoord3f(1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    
    glTexCoord3f(1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)
    
    glTexCoord3f(-1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)


    ########################
    # Positive Z 
    glTexCoord3f(1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glTexCoord3f(-1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glTexCoord3f(-1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)
    
    glTexCoord3f(1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)


    #########################
    # Positive Y
    glTexCoord3f(-1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)
    
    glTexCoord3f(-1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)
    
    glTexCoord3f(1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)
    
    glTexCoord3f(1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)


    #########################
    # Negative Y
    glTexCoord3f(-1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glTexCoord3f(-1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glTexCoord3f(1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glTexCoord3f(1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    glEnd()


def InitGL(Width, Height):

        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
            
        # Set up texture maps        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)        
      
        # Load Cube Map images
        for i in range(6):
            # Load this texture map
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_GENERATE_MIPMAP, GL_TRUE)
            img = Image.open(szCubeFaces[i]).convert("RGB")
            raw_image = img.rotate(180).tobytes()
            glTexImage2D(cube[i], 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, raw_image)
            
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        
        # Enable cube mapping, and set texture environment to decal
        glEnable(GL_TEXTURE_CUBE_MAP)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    # Called to draw scene
def DrawGLScene():
        # Clear the window
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        glPushMatrix() 
        
        frameCamera.ApplyCameraTransform() # Move the camera about

        # Sky Box is manually textured
        glDisable(GL_TEXTURE_GEN_S)
        glDisable(GL_TEXTURE_GEN_T)
        glDisable(GL_TEXTURE_GEN_R)        
        DrawSkyBox()

        # Use texgen to apply cube map
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glEnable(GL_TEXTURE_GEN_R)

        glPushMatrix()
        glTranslatef(0.0, 0.0, -3.0)    
        
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        
        # Invert camera matrix (rotation only) and apply to 
        # texture coordinates
        m = M3DMatrix44f()
        invert = M3DMatrix44f()
        
        m = frameCamera.GetCameraOrientation()
        m3dInvertMatrix44(invert, m)
        glMultMatrixf(invert)
        
        gltDrawSphere(0.75, 41, 41)
        
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glPopMatrix()

        glutSwapBuffers() 
       

    # Respond to arrow keys by moving the camera frame of reference
def specialkeyPressed(key, x, y):
        global zPos
        if key == GLUT_KEY_UP:
            frameCamera.MoveForward(1.0)
        elif key == GLUT_KEY_DOWN:
            frameCamera.MoveForward(-1.0)
        elif key == GLUT_KEY_LEFT:
            frameCamera.RotateLocalY(0.1)
        elif key == GLUT_KEY_RIGHT:
            frameCamera.RotateLocalY(-0.1)
        
        glutPostRedisplay()
        
def keyPressed(key, x, y):
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()
            
    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        fAspect = float(w) / float(h)
        
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluPerspective(35.0, fAspect, 1.0, 2000.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("OpenGL Cube Maps")
    
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
