#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)  # START

    # SEED DLA RANDOM()
    random.seed(33345)
    drawRectangle( 0, 0, 50, 50)    # FUNKCJA - PROSTOKAT Z DWOCH TROJKATOW

    glFlush()               # KONIEC

# FUNKCJA W.W.
def drawRectangle(x, y, a, b,d=1.0):

    # (x,y) - SRODEK prostokata
    # a - Dlugosc
    # b - Wysokosc
    # d - Stopien deformacji (domyslnie 0.0)

    # DEFORMACJA
    a = a * (1.0 + random.uniform(-d, d))
    b = b * (1.0 + random.uniform(-d, d))

    # KOLORY
    c1 = (random.random(), random.random(), random.random())  # lewy dolny
    c2 = (random.random(), random.random(), random.random())  # prawy dolny
    c3 = (random.random(), random.random(), random.random())  # prawy gorny
    c4 = (random.random(), random.random(), random.random())  # lewy gorny

    # TROJKAT 1
    glBegin(GL_TRIANGLES)
    # LEWY DOLNY
    glColor3f(*c1)
    glVertex2f(x-a/2.0, y-b/2.0)
    # PRAWY DOLNY
    glColor3f(*c2)
    glVertex2f(x+a/2.0, y-b/2.0)
    # PRAWY GORNY
    glColor3f(*c3)
    glVertex2f(x+a/2.0, y+b/2.0)
    glEnd()

    # TROJKAT 2
    glBegin(GL_TRIANGLES)
    # LEWY DOLNY
    glColor3f(*c1)
    glVertex2f(x-a/2.0, y-b/2.0)
    # LEWY GORNY
    glColor3f(*c4)
    glVertex2f(x-a/2.0, y+b/2.0)
    # PRAWY GORNY
    glColor3f(*c3)
    glVertex2f(x+a/2.0, y+b/2.0)
    glEnd()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
