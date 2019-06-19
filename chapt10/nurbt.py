#!/usr/bin/python3

# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Nurbs.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import time 

ESCAPE = b'\033'

import sys
sys.path.append("../shared")

# NURBS object
global pNurb

# The number of control points for this curve
nNumPoints = 4 # 4 x 4

# Mesh extends four units -6 to +6 along x and y axis
# Lies in Z plane
#                 u  v  (x,y,z)	
ctrlPoints = (GLfloat * 3 * 4 * 4)(((-6.0, -6.0, 0.0),	# u = 0,	v = 0
                                     (-6.0, -2.0, 0.0),	#			v = 1
                                     (-6.0,  2.0, 0.0),	#			v = 2	
                                     (-6.0,  6.0, 0.0)), #			v = 3

                                    ((-2.0, -6.0, 0.0),	# u = 1	v = 0
                                     (-2.0, -2.0, 8.0),	#			v = 1
                                     (-2.0,  2.0, 8.0),	#			v = 2
                                     (-2.0,  6.0, 0.0)),	#			v = 3

                                    ((2.0, -6.0, 0.0 ), # u =2		v = 0
                                     (2.0, -2.0, 8.0 ), #			v = 1
                                     (2.0,  2.0, 8.0 ),	#			v = 2
                                     (2.0,  6.0, 0.0 )),#			v = 3

                                    ((6.0, -6.0, 0.0),	# u = 3	v = 0
                                     (6.0, -2.0, 0.0),	#			v = 1
                                     (6.0,  2.0, 0.0),	#			v = 2
                                     (6.0,  6.0, 0.0)))#			v = 3


# Knot sequence for the NURB
Knots = (GLfloat * 8)(0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0)

# Outside trimming points to include entire surface
outsidePts = (GLfloat * 2 * 5)((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)) # counter clockwise

# Inside trimming points to create triangle shaped hole in surface
insidePts = (GLfloat * 2 * 4)((0.25, 0.25), (0.5, 0.5), (0.75, 0.25), ( 0.25, 0.25)) # clockwise

lightArrayType = GLfloat * 4

def InitGL(Width, Height):

        global pNurb
        
        whiteLight = lightArrayType(0.7, 0.7, 0.7, 1.0)
        specular = lightArrayType(0.7, 0.7, 0.7, 1.0)
        shine = GLfloat(100.0)
        
        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, shine)
        
        # Automatically generate normals for evaluated surfaces
        glEnable(GL_AUTO_NORMAL)

        # Setup the Nurbs object
        pNurb = gluNewNurbsRenderer()

        # Install error handler to notify user of NURBS errors
       # GLVoid (*callback)()
       # TODO: python equiv?
#        gluNurbsCallback(pNurb, GLU_ERROR, (CallBack)NurbsErrorHandler)  

        gluNurbsProperty(pNurb, GLU_SAMPLING_TOLERANCE, 25.0)
        # Uncomment the next line and comment the one following to produce a
        # wire frame mesh.
        #gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_OUTLINE_POLYGON)
        gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_FILL)


    # Called to draw scene
def DrawGLScene():
        # Draw in Blue
        glColor3ub(0,0,220)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the modelview matrix stack
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Rotate the mesh around to make it easier to see
        glRotatef(330.0, 1.0,0.0,0.0)
        
        # Render the NURB
        # Begin the NURB definition
        gluBeginSurface(pNurb)
        
        # Evaluate the surface
        gluNurbsSurface(pNurb,	# pointer to NURBS renderer
            Knots,			# No. of knots and knot array u direction	
            Knots,			# No. of knots and knot array v direction
            ctrlPoints, # Control points
            GL_MAP2_VERTEX_3)		# Type of surface
            
        # Outer area, include entire curve
        gluBeginTrim (pNurb)
        gluPwlCurve (pNurb, outsidePts, GLU_MAP1_TRIM_2)
        gluEndTrim (pNurb)

        # Inner triangluar area
        gluBeginTrim (pNurb)
        gluPwlCurve (pNurb, insidePts, GLU_MAP1_TRIM_2)
        gluEndTrim (pNurb)
    
        # Done with surface
        gluEndSurface(pNurb)
        
        # Restore the modelview matrix
        glPopMatrix()

        glutSwapBuffers() 


def ReSizeGLScene(w, h):

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Perspective view
        gluPerspective (45.0, float(w)/float(h), 1.0, 40.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Viewing transformation, position for better view
        glTranslatef (0.0, 0.0, -20.0)

def keyPressed(key, x, y):
        if key == ESCAPE:
            glutDestroyWindow(window)
            sys.exit()



# Main program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Trimmed NURBS Surface")
    
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









