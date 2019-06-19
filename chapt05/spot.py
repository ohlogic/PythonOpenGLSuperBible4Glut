#!/usr/bin/python3

# Ben Smith
# Demonstrates OpenGL Spotlight
# benjamin.coder.smith@gmail.com
#
# based on Spot.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
ESCAPE = b'\033'

import sys
sys.path.append("../shared")

from fakeglut import glutSolidSphere, glutSolidCone

# Rotation amounts
xRot = 0.0
yRot = 0.0

# Light values and coordinates
lightArrayType = GLfloat * 4

lightPos = (GLfloat * 4)(0.0, 0.0, 75.0, 1.0)
specular = lightArrayType(1.0, 1.0, 1.0, 1.0)
specref =  lightArrayType(1.0, 1.0, 1.0, 1.0)
ambientLight = lightArrayType(0.5, 0.5, 0.5, 1.0)
spotDir = (GLfloat * 3)(0.0, 0.0, -1.0)

# Flags for effects
MODE_FLAT = 1
MODE_SMOOTH = 2
MODE_VERYLOW = 3
MODE_MEDIUM = 4
MODE_VERYHIGH = 5

iShade = MODE_FLAT
iTess = MODE_VERYLOW

def InitGL(Width, Height):


        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not try to display the back sides

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        # Supply a slight ambient light so the objects can be seen
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight)
        
        # The light is composed of just a diffuse and specular components
        glLightfv(GL_LIGHT0,GL_DIFFUSE,ambientLight)
        glLightfv(GL_LIGHT0,GL_SPECULAR,specular)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

        # Specific spot effects
        # Cut off angle is 60 degrees
        glLightf(GL_LIGHT0,GL_SPOT_CUTOFF,50.0)

        # Enable this light in particular
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # All materials hereafter have full specular reflectivity
        # with a high shine
        glMaterialfv(GL_FRONT, GL_SPECULAR,specref)
        glMateriali(GL_FRONT, GL_SHININESS,128)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )


    # Called to draw scene
def DrawGLScene():
        if iShade == MODE_FLAT:
            glShadeModel(GL_FLAT)
        else: # 	iShade = MODE_SMOOTH
            glShadeModel(GL_SMOOTH)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # First place the light 
        # Save the coordinate transformation
        glPushMatrix()	
        # Rotate coordinate system
        glRotatef(yRot, 0.0, 1.0, 0.0)
        glRotatef(xRot, 1.0, 0.0, 0.0)

        # Specify new position and direction in rotated coords.
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION,spotDir)

        # Draw a red cone to enclose the light source
        glColor3ub(255,0,0)	

        # Translate origin to move the cone out to where the light
        # is positioned.
        glTranslatef(lightPos[0],lightPos[1],lightPos[2])
        glutSolidCone(4.0,6.0,15,15)

        # Draw a smaller displaced sphere to denote the light bulb
        # Save the lighting state variables
        glPushAttrib(GL_LIGHTING_BIT)

        # Turn off lighting and specify a bright yellow sphere
        glDisable(GL_LIGHTING)
        glColor3ub(255,255,0)
        glutSolidSphere(3.0, 15, 15)

        # Restore lighting state variables
        glPopAttrib()

        # Restore coordinate transformations
        glPopMatrix()


        # Set material color and draw a sphere in the middle
        glColor3ub(0, 0, 255)

        if iTess == MODE_VERYLOW:
            glutSolidSphere(30.0, 7, 7)
        else: 
            if iTess == MODE_MEDIUM:
                glutSolidSphere(30.0, 15, 15)
            else: #  iTess = MODE_VERYHIGH
                glutSolidSphere(30.0, 50, 50)
        
        glutSwapBuffers()
        
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
        gluPerspective(35.0, fAspect, 1.0, 500.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -250.0)
        

def specialkeyPressed(key, x, y):
        global xRot, yRot
        if key == GLUT_KEY_UP:
            xRot -= 5.0
        elif key == GLUT_KEY_DOWN:
            xRot += 5.0
        elif key == GLUT_KEY_LEFT:
            xRot -= 5.0
        elif key == GLUT_KEY_RIGHT:
            xRot += 5.0

        if xRot > 356.0:
            xRot = 0.0
        elif xRot < -1.0:
            xRot = 355.0
            
        if yRot > 356.0:
            yRot = 0.0
        elif yRot < -1.0:
            yRot = 355.0

        glutPostRedisplay()
            
def keyPressed(key, x, y):
        global iShade, iTess
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()

        if key == b'1':
            iShade = MODE_FLAT
        elif key == b'2':
            iShade = MODE_SMOOTH
        elif key == b'3':
            iTess = MODE_VERYLOW
        elif key == b'4':
            iTess = MODE_MEDIUM
        elif key == b'5':
            iTess = MODE_VERYHIGH
            





# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Spot Light")
    
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






