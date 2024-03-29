#!/usr/bin/python3

# Demonstrates an immersive 3D environment using actors
# and a camera. This version adds fog
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Fogged.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time 

ESCAPE = b'\033'

from random import randint
from math import cos, sin

import sys
sys.path.append("../shared")

from math3d import M3D_PI, M3DVector3f, M3DMatrix44f, m3dTransformVector3, m3dDegToRad, m3dRotationMatrix44, m3dGetPlaneEquation, m3dMakePlanarShadowMatrix
from glframe import GLFrame
from fakeglut import glutSolidSphere
from gltools import gltDrawTorus

NUM_SPHERES = 30
spheres = [GLFrame() for i in range(NUM_SPHERES)]
frameCamera = GLFrame()

# Light and material data

# pyglet reverses y direction
fLightPos = (GLfloat * 4)(-100.0, 100.0, 50.0, 1.0)

lightArrayType = GLfloat * 4
fNoLight = lightArrayType(0.0, 0.0, 0.0, 0.0)
fLowLight = lightArrayType(0.25, 0.25, 0.25, 1.0)
fBrightLight = lightArrayType(1.0, 1.0, 1.0, 1.0)

yRot = 0.0 # Rotation angle for animation

mShadowMatrix = M3DMatrix44f()

# Draw the ground as a series of triangle strips
def DrawGround():
    fExtent = 20.0
    fStep = 1.0
    y = -0.4
    
    iStrip = -fExtent
    
    while (iStrip <= fExtent):
        t = 0.0
        glBegin(GL_TRIANGLE_STRIP)
        
        glNormal3f(0.0, 1.0, 0.0) # All point up
        iRun = fExtent
        while (iRun >= -fExtent):
            glVertex3f(iStrip, y, iRun)
            
            glVertex3f(iStrip + fStep, y, iRun)
            
            iRun -= fStep
            
        glEnd()
        iStrip += fStep


# Draw random inhabitants and the rotating torus/sphere duo
def DrawInhabitants(nShadow):
    global yRot
    if nShadow == 0:
        pass #yRot += 0.5
    else:
        glColor3f(0.0, 0.0, 0.0)

    
    # Draw the randomly located spheres
    if nShadow == 0:
        glColor3f(0.0, 1.0, 0.0)

    for sphere in spheres:
        glPushMatrix()
        
        sphere.ApplyActorTransform()
        glutSolidSphere(0.3, 17, 9)
        
        glPopMatrix()
        
    glPushMatrix()
    # -y is up in pyglet
    glTranslatef(0.0, 0.1, -2.5)
    
    if nShadow == 0:
        glColor3f(0.0, 0.0, 1.0)
    
    glPushMatrix()
    glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 17, 9)
    glPopMatrix()
    
    if nShadow == 0:
        # Torus alone will be specular
        glColor3f(1.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, fBrightLight)
        
    glRotatef(yRot, 0.0, 1.0, 0.0)
    gltDrawTorus(0.35, 0.15, 61, 37)
    glMaterialfv(GL_FRONT, GL_SPECULAR, fNoLight)
    glPopMatrix()
        
def InitGL(Width, Height):
        global mShadowMatrix
        # Calculate shadow matrix
        vPoints = (M3DVector3f * 3)((0.0, -0.4, 0.0),
                                     (10.0, -0.4, 0.0),
                                     (5.0,-0.4, -5.0)
                                    )
       
        # Grayish background
        glClearColor(fLowLight[0], fLowLight[1], fLowLight[2], fLowLight[3])
             
        # Setup Fog parameters
        glEnable(GL_FOG)                   # Turn Fog on
        glFogfv(GL_FOG_COLOR, fLowLight)   # Set fog color to match background
        glFogf(GL_FOG_START, 5.0)         # How far away does the fog start
        glFogf(GL_FOG_END, 30.0)          # How far away does the fog stop
        glFogi(GL_FOG_MODE, GL_LINEAR)     # Which fog equation do I use?
             
        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, fNoLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, fLowLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, fBrightLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, fBrightLight)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        

        # Get the plane equation from three points on the ground
        vPlaneEquation = m3dGetPlaneEquation(vPoints[0], vPoints[1] , vPoints[2])
        
        # Calculate projection matrix to draw shadown on the ground
        mShadowMatrix = m3dMakePlanarShadowMatrix(vPlaneEquation, fLightPos)
        
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
            
        # Randomly place sphere inhabitants
        for sphere in spheres:
            # Pick a random location between -20 and 20 at .1 increments
            sphere.setOrigin(float(randint(-200, 200)) * 0.1, 0.0, float(randint(-200, 200)) * 0.1)

    # Called to draw scene
def DrawGLScene():
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_ACCUM_BUFFER_BIT)
            
        glPushMatrix()
        frameCamera.ApplyCameraTransform()
                
        # Position light before any other transformations
        glLightfv(GL_LIGHT0, GL_POSITION, fLightPos)
        
        # Draw the ground
        glColor3f(0.60, 0.40, 0.10)
        DrawGround()
        
        # Draw shadows first
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glMultMatrixf(mShadowMatrix)
        DrawInhabitants(1)
        glPopMatrix()
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        # Draw inhabitants normally
        DrawInhabitants(0)

        glPopMatrix()
            
        glutSwapBuffers() 
        
        
    # Respond to arrow keys by moving the camera frame of reference
def specialkeyPressed(key, x, y):
        if key == GLUT_KEY_UP:
            frameCamera.MoveForward(1.0)
        elif key == GLUT_KEY_DOWN:
            frameCamera.MoveForward(-1.0)
        elif key == GLUT_KEY_LEFT:
            frameCamera.RotateLocalY(0.1)
        elif key == GLUT_KEY_RIGHT:
            frameCamera.RotateLocalY(-0.1)

        glutPostRedisplay()
            
            
            
def keyPressed(*args):
        if args[0] == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()
            
            
            
def update(dt):
        global yRot
        yRot += 0.5
        
        glutPostRedisplay()
        
        glutTimerFunc( int(1.0/30.0), update, 0)

        time.sleep(1/30.0) #VERY simplistically run the app at ~30 fps, avoids high CPU usage!

        
        
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
        gluPerspective(35.0, fAspect, 1.0, 50.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
# Main program entry point
if __name__ == '__main__':


    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("OpenGL SphereWorld Demo + Fogged")
    
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()
    
    
    #glutIdleFunc(DrawGLScene)
    glutTimerFunc( int(1.0/30.0), update, 0)
    
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc (specialkeyPressed);

    # Initialize our window. 
    InitGL(640, 480)
    
    # Start Event Processing Engine	
    glutMainLoop()






