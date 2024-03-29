#!/usr/bin/python3

# Demonstrates shadow mapping
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on shadowmap.cpp
# OpenGL SuperBible, Chapter 14
# Program by Benjamin Lipchak

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB

from PIL import Image
import time 

ESCAPE = b'\033'

from math import cos, sin, atan, sqrt
from time import sleep

import sys
sys.path.append("../shared")
from sys import exit
from math3d import M3DMatrix44f, m3dLoadIdentity44, m3dTranslateMatrix44, m3dScaleMatrix44, m3dMatrixMultiply44, m3dTransposeMatrix44, m3dRadToDeg
from fakeglut import glutSolidCube, glutSolidSphere, glutSolidCone, glutSolidOctahedron, glutSolidTorus

ambientShadowAvailable = False
npotTexturesAvailable = False
controlCamera = True      # xyz keys will control lightpos
noShadows = False         # normal lighting
showShadowMap = False     # show the shadowmap texture

factor = 4.0                  # for polygon offset

windowWidth = 1024               # window size
windowHeight = 512

shadowWidth = 1024               # set based on window size
shadowHeight = 512
shadowTextureID = GLuint(0)

maxTexSize = GLint(0)                      # maximum allowed size for 1D/2D texture

ambientLight = (GLfloat * 4)(0.2, 0.2, 0.2, 1.0)
diffuseLight = (GLfloat * 4)(0.7, 0.7, 0.7, 1.0)
noLight = (GLfloat * 4)(0.0, 0.0, 0.0, 1.0)
lightPos = (GLfloat * 4)(100.0, 300.0, 100.0, 1.0)

cameraPos = (GLfloat * 4)(100.0, 150.0, 200.0, 1.0)
cameraZoom = 0.3

textureMatrix = M3DMatrix44f()
global strips
# Called to draw scene objects
def DrawModels(drawBasePlane):
    if drawBasePlane:
        # Draw plane that the objects rest on
        glColor3f(0.0, 0.0, 0.90) # Blue
        glNormal3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-100.0, -25.0, -100.0)
        glVertex3f(-100.0, -25.0, 100.0)
        glVertex3f(100.0,  -25.0, 100.0)
        glVertex3f(100.0,  -25.0, -100.0)
        glEnd()

    # Draw red cube
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(48.0)

    # Draw green sphere
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(-60.0, 0.0, 0.0)
    glutSolidSphere(25.0, 50, 50)
    glPopMatrix()

    # Draw yellow cone
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(60.0, 0.0, -24.0)
    glutSolidCone(25.0, 50.0, 50, 50)
    glPopMatrix()

    # Draw magenta torus
    glColor3f(1.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 60.0)
    glutSolidTorus(8.0, 16.0, 50, 50)
    glPopMatrix()

    # Draw cyan octahedron
    glColor3f(0.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, -60.0)
    glScalef(25.0, 25.0, 25.0)
    glutSolidOctahedron()
    glPopMatrix()

# Called to regenerate the shadow map
def RegenerateShadowMap():
    global textureMatrix, strips
    lightModelview = (GLfloat * 16)()
    lightProjection = (GLfloat * 16)()
    sceneBoundingRadius = 95.0 # based on objects in scene

    # Save the depth precision for where it's useful
    lightToSceneDistance = sqrt(lightPos[0] * lightPos[0] + lightPos[1] * lightPos[1] + lightPos[2] * lightPos[2])
    nearPlane = lightToSceneDistance - sceneBoundingRadius
    
    # Keep the scene filling the depth texture
    fieldOfView = m3dRadToDeg(2.0 * atan(sceneBoundingRadius / lightToSceneDistance))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fieldOfView, 1.0, nearPlane, nearPlane + (2.0 * sceneBoundingRadius))
    glGetFloatv(GL_PROJECTION_MATRIX, lightProjection)
    
    # Switch to light's point of view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(lightPos[0], lightPos[1], lightPos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glGetFloatv(GL_MODELVIEW_MATRIX, lightModelview)
    glViewport(0, 0, shadowWidth, shadowHeight)

    # Clear the depth buffer only
    glClear(GL_DEPTH_BUFFER_BIT)

    # All we care about here is resulting depth values
    glShadeModel(GL_FLAT)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_NORMALIZE)
    glColorMask(0, 0, 0, 0)

    # Overcome imprecision
    glEnable(GL_POLYGON_OFFSET_FILL)

    # Draw objects in the scene except base plane
    # which never shadows anything
    DrawModels(False)

    # Copy depth values into depth texture
    glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 0, 0, shadowWidth, shadowHeight, 0)

    # Restore normal drawing state
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glColorMask(1, 1, 1, 1)
    glDisable(GL_POLYGON_OFFSET_FILL)

    # Set up texture matrix for shadow map projection,
    # which will be rolled into the eye linear
    # texture coordinate generation plane equations
    tempMatrix = M3DMatrix44f()
    m3dLoadIdentity44(tempMatrix)
    m3dTranslateMatrix44(tempMatrix, 0.5, 0.5, 0.5)
    m3dScaleMatrix44(tempMatrix, 0.5, 0.5, 0.5)
    m3dMatrixMultiply44(textureMatrix, tempMatrix, lightProjection)
    m3dMatrixMultiply44(tempMatrix, textureMatrix, lightModelview)
    
    # transpose to get the s, t, r, and q rows for plane equations
    m3dTransposeMatrix44(textureMatrix, tempMatrix)
    # this seems sorta awkward, but I haven't hit on a better way to index into the array in a fashion that
    # pyglet will work with.
    strips = [(GLfloat * 4)(textureMatrix[4], textureMatrix[5], textureMatrix[6], textureMatrix[7]),
                (GLfloat * 4)(textureMatrix[8], textureMatrix[9], textureMatrix[10], textureMatrix[11]),
                (GLfloat * 4)(textureMatrix[12], textureMatrix[13], textureMatrix[14], textureMatrix[15]),
                ]
    
def InitGL(Width, Height):
        global maxTexSize, ambientShadowAvailable, npotTexturesAvailable

        
        print ("Shadow Mapping Demo\n")

        # Make sure required functionality is available!

        # if not gl_info.have_version(1, 4) and not gl_info.have_extension(GL_ARB_shadow):
            # print ("Neither OpenGL 1.4 nor GL_ARB_shadow extension is available!")
            # sleep(2)
            # exit(0)

        # # Check for optional extensions
        # if gl_info.have_extension(GL_ARB_shadow_ambient):
            # ambientShadowAvailable = True
        # else:
            # print ("GL_ARB_shadow_ambient extension not available!")
            # print ("Extra ambient rendering pass will be required.\n")
            # sleep(2)

        # if gl_info.have_version(2, 0) or gl_info.have_extension(GL_ARB_texture_non_power_of_two):
            # npotTexturesAvailable = True
        # else:
            # print ("Neither OpenGL 2.0 nor GL_ARB_texture_non_power_of_two extension")
            # print ("is available!  Shadow map will be lower resolution (lower quality).\n")
            # sleep(2)

        glGetIntegerv(GL_MAX_TEXTURE_SIZE, ctypes.byref(maxTexSize))

        print ("Controls:")
        print ("\tRight-click for menu\n")
        print ("\tx/X\t\tMove +/- in x direction")
        print ("\ty/Y\t\tMove +/- in y direction")
        print ("\tz/Z\t\tMove +/- in z direction\n")
        print ("\tf/F\t\tChange polygon offset factor +/-\n")
        print ("\tq\t\tExit demo\n")
        
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        # Hidden surface removal
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glPolygonOffset(factor, 0.0)

        # Set up some lighting state that never changes
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHT0)

        # Set up some texture state that never changes
        glGenTextures(1, ctypes.byref(shadowTextureID))
        glBindTexture(GL_TEXTURE_2D, shadowTextureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE, GL_INTENSITY)
        if (ambientShadowAvailable):
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FAIL_VALUE_ARB, 0.5)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)

        RegenerateShadowMap()

        
    # Called to draw scene
def DrawGLScene():
        # Track camera angle
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (windowWidth > windowHeight):
            ar = float(windowWidth) / float(windowHeight)
            glFrustum(-ar * cameraZoom, ar * cameraZoom, -cameraZoom, cameraZoom, 1.0, 1000.0)
        else:
            ar = float(windowHeight) / float(windowWidth)
            glFrustum(-cameraZoom, cameraZoom, -ar * cameraZoom, ar * cameraZoom, 1.0, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(cameraPos[0], cameraPos[1], cameraPos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glViewport(0, 0, windowWidth, windowHeight)
        
        # Track light position
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (showShadowMap):
            # Display shadow map for educational purposes
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glMatrixMode(GL_TEXTURE)
            glPushMatrix()
            glLoadIdentity()
            glEnable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_NONE)
            
            # Show the shadowMap at its actual size relative to window
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(-1.0, -1.0)
            glTexCoord2f(1.0, 0.0)
            glVertex2f((shadowWidth/windowWidth)*2.0-1.0, -1.0)
            glTexCoord2f(1.0, 1.0)
            glVertex2f((shadowWidth/windowWidth)*2.0-1.0, (shadowHeight/windowHeight)*2.0-1.0)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(-1.0, (shadowHeight/windowHeight)*2.0-1.0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_LIGHTING)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            gluPerspective(45.0, 1.0, 1.0, 1000.0)
            glMatrixMode(GL_MODELVIEW)
        
        elif noShadows:
            # Set up some simple lighting
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)

            # Draw objects in the scene including base plane
            DrawModels(True)
        
        else:
            if not ambientShadowAvailable:

                lowAmbient = (GLfloat * 4)(0.1, 0.1, 0.1, 1.0)
                lowDiffuse = (GLfloat * 4)(0.35, 0.35, 0.35, 1.0)

                # Because there is no support for an "ambient"
                # shadow compare fail value, we'll have to
                # draw an ambient pass first...
                glLightfv(GL_LIGHT0, GL_AMBIENT, lowAmbient)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, lowDiffuse)

                # Draw objects in the scene, including base plane
                DrawModels(True)

                # Enable alpha test so that shadowed fragments are discarded
                glAlphaFunc(GL_GREATER, 0.9)
                glEnable(GL_ALPHA_TEST)
                
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)

            # Set up shadow comparison
            glEnable(GL_TEXTURE_2D)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_R_TO_TEXTURE)

            # Set up the eye plane for projecting the shadow map on the scene
            glEnable(GL_TEXTURE_GEN_S)
            glEnable(GL_TEXTURE_GEN_T)
            glEnable(GL_TEXTURE_GEN_R)
            glEnable(GL_TEXTURE_GEN_Q)
            
            glTexGenfv(GL_S, GL_EYE_PLANE, textureMatrix)
            glTexGenfv(GL_T, GL_EYE_PLANE, strips[0])
            glTexGenfv(GL_R, GL_EYE_PLANE, strips[1])
            glTexGenfv(GL_Q, GL_EYE_PLANE, strips[2])

            # Draw objects in the scene, including base plane
            DrawModels(True)

            glDisable(GL_ALPHA_TEST)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_TEXTURE_GEN_S)
            glDisable(GL_TEXTURE_GEN_T)
            glDisable(GL_TEXTURE_GEN_R)
            glDisable(GL_TEXTURE_GEN_Q)
        
        
        if glGetError() != GL_NO_ERROR:
            print ("GL Error!\n")

        glutSwapBuffers() 

    # Called when the window has changed size (including when the window is created)
def ReSizeGLScene(w, h):

        global windowWidth, windowHeight, shadowWidth, shadowHeight
        windowWidth = shadowWidth = w
        windowHeight = shadowHeight = h
        
        if not npotTexturesAvailable:
            # Find the largest power of two that will fit in window.

            # Try each width until we get one that's too big
            i = 0
            while (1 << i) <= shadowWidth:
                i += 1
            shadowWidth = (1 << (i-1))

            # Now for height
            i = 0
            while (1 << i) <= shadowHeight:
                i += 1
            shadowHeight = (1 << (i-1))

        if shadowWidth > maxTexSize:
            shadowWidth = maxTexSize
        if shadowHeight > maxTexSize:
            shadowHeight = maxTexSize

        RegenerateShadowMap()

    # Respond to arrow keys by moving the camera frame of reference
def specialkeyPressed(key, x, y):
        global factor, cameraPos, lightPos, noShadows, showShadowMap, controlCamera

        if key == GLUT_KEY_UP:
            if (controlCamera):
                cameraPos[2] -= 5.0
            else:
                lightPos[2] -= 5.0
        elif key == GLUT_KEY_DOWN:
            if (controlCamera):
                cameraPos[2] += 5.0
            else:
                lightPos[2] += 5.0
        elif key == GLUT_KEY_LEFT:
            if (controlCamera):
                cameraPos[0] -= 5.0
            else:
                lightPos[0] -= 5.0
        elif key == GLUT_KEY_RIGHT:
            if (controlCamera):
                cameraPos[0] += 5.0
            else:
                lightPos[0] += 5.0
        glutPostRedisplay()


def keyPressed(key, x, y):
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()

        global factor, cameraPos, lightPos, noShadows, showShadowMap, controlCamera
        if key == b'f' or key == b'F':
            if key == b'F':
                factor += 1
                glPolygonOffset(factor, 0.0)
                RegenerateShadowMap()
            else:
                factor -= 1
                glPolygonOffset(factor, 0.0)
                RegenerateShadowMap()
        elif key == b'x' or key == b'X':
            if key == b'X':
                if (controlCamera):
                    cameraPos[0] -= 5.0
                else:
                    lightPos[0] -= 5.0
            else:
                if (controlCamera):
                    cameraPos[0] += 5.0
                else:
                    lightPos[0] += 5.0
        elif key == b'y' or key == b'Y':
            if key == b'Y':
                if (controlCamera):
                    cameraPos[1] -= 5.0
                else:
                    lightPos[1] -= 5.0
            else:
                if (controlCamera):
                    cameraPos[1] += 5.0
                else:
                    lightPos[1] += 5.0
        elif key == b'z' or key == b'Z':
            if key == b'Z':
                if (controlCamera):
                    cameraPos[2] -= 5.0
                else:
                    lightPos[2] -= 5.0
            else:
                if (controlCamera):
                    cameraPos[2] += 5.0
                else:
                    lightPos[2] += 5.0
            
        elif key == b'1':
            noShadows = not noShadows
            showShadowMap = False
        elif key == b'2':
            showShadowMap = not showShadowMap
            noShadows = False
        elif key == b'3':
            controlCamera = not controlCamera



        # We don't need to regenerate the shadow map
        # if only the camera angle changes
        if not controlCamera:
            RegenerateShadowMap();

        glutPostRedisplay()

# Main program entry point
if __name__ == '__main__':


    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Shadow Mapping Demo")
    
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








