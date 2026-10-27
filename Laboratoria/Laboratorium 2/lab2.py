#!/usr/bin/env python3
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_triangle(): #ocena3.5
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-35.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 70.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(35.0, 0.0)
    glEnd()

def draw_rectangle(x,y,a,b):
    hx = a/2.0
    hy = b/2.0
    bl = (x - hx, y - hy)  # bottom left
    tl = (x - hx, y + hy)  # top left
    tr = (x + hx, y + hy)  # top right
    br = (x + hx, y - hy)  # bottom right

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(*bl)
    glVertex2f(*tl)
    glVertex2f(*tr)
    glEnd()

    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(*bl)
    glVertex2f(*tr)
    glVertex2f(*br)
    glEnd()

def draw_rectangle_deformed(x, y, a, b, d=0.0):
    """
    Rysuje prostokąt o środku (x, y) i wymiarach a, b z możliwością deformacji d.
    """
    hx = a / 2.0
    hy = b / 2.0

    bl = (x - hx + random.uniform(-d, d), y - hy + random.uniform(-d, d))
    tl = (x - hx + random.uniform(-d, d), y + hy + random.uniform(-d, d))
    tr = (x + hx + random.uniform(-d, d), y + hy + random.uniform(-d, d))
    br = (x + hx + random.uniform(-d, d), y - hy + random.uniform(-d, d))

    color_bl = (random.random(), random.random(), random.random())
    color_tl = (random.random(), random.random(), random.random())
    color_tr = (random.random(), random.random(), random.random())
    color_br = (random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    # Pierwszy trójkąt: bl -> br -> tr
    glColor3f(*color_bl)
    glVertex2f(*bl)
    glColor3f(*color_br)
    glVertex2f(*br)
    glColor3f(*color_tr)
    glVertex2f(*tr)

    # Drugi trójkąt: bl -> tr -> tl
    glColor3f(*color_bl)
    glVertex2f(*bl)
    glColor3f(*color_tr)
    glVertex2f(*tr)
    glColor3f(*color_tl)
    glVertex2f(*tl)
    glEnd()


def draw_sierpinski_carpet(x, y, a, b, depth):
    """
    :parametry x, y: środek bieżącego prostokąta
    :parametry a, b: długości boków
    :parametr depth: stopień samopodobieństwa
    """
    # Warunek stopu rekurencji: na najniższym poziomie po prostu rysujemy prostokąt
    if depth == 0:
        draw_rectangle(x, y, a, b)
        return

    new_a = a / 3.0
    new_b = b / 3.0

    # Przesunięcia środków dla 8 otaczających prostokątów:
    # Siatka 3x3: dx, dy przyjmują wartości -1, 0, 1

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # Środkowy kwadrat/prostokąt zostaje pusty

            new_x = x + dx * new_a
            new_y = y + dy * new_b
            draw_sierpinski_carpet(new_x, new_y, new_a, new_b, depth - 1)

def draw_sierpinski_carpet_iterative(x, y, a, b, depth):
    """
    :parametry x, y: środek bieżącego prostokąta
    :parametry a, b: długości boków
    :parametr depth: stopień samopodobieństwa
    """
    # Lista przechowująca krotki (środek_x, środek_y, szerokość, wysokość)
    rectangles = [(x, y, a, b)]

    for _ in range(depth):
        next_rectangles = []

        for rx, ry, ra, rb in rectangles:
            new_a = ra / 3.0
            new_b = rb / 3.0

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue

                    new_x = rx + dx * new_a
                    new_y = ry + dy * new_b
                    next_rectangles.append((new_x, new_y, new_a, new_b))

        rectangles = next_rectangles

    # Rysujemy wszystkie zgromadzone prostokąty
    for rx, ry, ra, rb in rectangles:
        draw_rectangle(rx, ry, ra, rb)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(42)
    glColor3f(0.65, 0.25, 0.05)
    draw_sierpinski_carpet_iterative(0.0, 0.0, 150.0, 90.0, 0)

    glFlush()




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
