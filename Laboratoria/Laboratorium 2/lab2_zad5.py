#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glShadeModel(GL_SMOOTH)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)  # START

    # WIERZCHOLKI TROJKATA GLOWNEGO (SRODEK w 0,0)
    ax, ay = 0.0, 60.0
    bx, by = -51.9615, -30.0
    cx, cy = 51.9615, -30.0

    # KOLORY WIERZCHOLKOW
    ca = (1.0, 0.0, 0.0)  # R
    cb = (0.0, 1.0, 0.0)  # G
    cc = (0.0, 0.0, 1.0)  # B

    # BAZA - TROJKAT GLOWNY
    glBegin(GL_TRIANGLES)
    glColor3f(*ca)
    glVertex2f(ax, ay)
    glColor3f(*cb)
    glVertex2f(bx, by)
    glColor3f(*cc)
    glVertex2f(cx, cy)
    glEnd()

    # KRZYWE KOCHA
    l = 3   # POZIOM REKURENCJI
    koch(ax, ay, bx, by, ca, cb, l)
    koch(bx, by, cx, cy, cb, cc, l)
    koch(cx, cy, ax, ay, cc, ca, l)

    glFlush()  # KONIEC

# FUNKCJA ZAD 5
def koch(x1, y1, x2, y2, c1, c2, l):

    # (x1, y1) - POCZATEK ODCINKA
    # (x2, y2) - KONIEC ODCINKA
    # c1, c2   - KOLORY WIERZCHOLKOW
    # l        - POZIOM REKURENCJI

    if l == 0:  # KONIEC
        return

    # PODZIAL ODCINKA NA 3 CZESCI (P2 i P4)
    x2_p = (2.0 * x1 + x2) / 3.0
    y2_p = (2.0 * y1 + y2) / 3.0

    x4_p = (x1 + 2.0 * x2) / 3.0
    y4_p = (y1 + 2.0 * y2) / 3.0

    # WEKTOR MIEDZY P2 i P4
    dx = x4_p - x2_p
    dy = y4_p - y2_p

    # WYZNACZENIE SZCZYTU P3 (OBROT O -60 STOPNI NA ZEWNATRZ)
    sqrt3_2 = math.sqrt(3) / 2.0            # WARTOSC SIN 60*
    x3_p = x2_p + 0.5 * dx + sqrt3_2 * dy
    y3_p = y2_p - sqrt3_2 * dx + 0.5 * dy

    # INTERPOLACJA KOLOROW DLA NOWYCH WIERZCHOLKOW
    c2_p = ((2.0 * c1[0] + c2[0]) / 3.0, (2.0 * c1[1] + c2[1]) / 3.0, (2.0 * c1[2] + c2[2]) / 3.0)
    c4_p = ((c1[0] + 2.0 * c2[0]) / 3.0, (c1[1] + 2.0 * c2[1]) / 3.0, (c1[2] + 2.0 * c2[2]) / 3.0)
    c3_p = ((c2_p[0] + c4_p[0]) / 2.0, (c2_p[1] + c4_p[1]) / 2.0, (c2_p[2] + c4_p[2]) / 2.0)

    # RYSOWANIE DOKLEJANEGO TROJKATA Z INTERPOLACJA
    glBegin(GL_TRIANGLES)
    glColor3f(*c2_p)
    glVertex2f(x2_p, y2_p)
    glColor3f(*c3_p)
    glVertex2f(x3_p, y3_p)
    glColor3f(*c4_p)
    glVertex2f(x4_p, y4_p)
    glEnd()

    # REKURENCJA DLA 4 NOWYCH ODCINKOW
    koch(x1, y1, x2_p, y2_p, c1, c2_p, l - 1)
    koch(x2_p, y2_p, x3_p, y3_p, c2_p, c3_p, l - 1)
    koch(x3_p, y3_p, x4_p, y4_p, c3_p, c4_p, l - 1)
    koch(x4_p, y4_p, x2, y2, c4_p, c2, l - 1)



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
