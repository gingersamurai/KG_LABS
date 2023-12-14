from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
import sys
import threading
import time
from itertools import cycle

xrot = 0
yrot = 0
zrot = 0
h = 3.25  # высота по Оz
app = 4  # апроксимация
intensive = 10  # яркость
reflection = 116  # степень отражения
light_coord = (20, 30, 30)  # координаты источника света
zoom = 4  # зум


def DrawFn():
    global xrot, yrot, app, reflection, h
    # Сохраняем текущее состояние в стек
    glPushMatrix()
    # Задаём свойства материала - обе грани рассеивают свет, с параметрами rgb и alpha
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 0.0, 1.0, 1.0))
    # Задаём свойства материала - обе грани отражают свет, с параметрами rgb и alpha
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 0.0, 1.0, 1.0))
    # Задаём свойства материала - для обеих граней задаётся степень отражённого света
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128 - reflection)
    SetFigure(app + 1, h)
    # Возвращаемся в сохранённое состояние
    glPopMatrix()
    # Происходит смена буфера(работает с включённой двойной буфферизацией)
    glutSwapBuffers()


def SetFigure(app, h):
    x = numpy.linspace(-1, 1, app)
    y = 2*x**2
    verts = []
    for i in range(len(x) - 1):
        tmp = []
        tmp.append((x[i], y[i], 0))
        tmp.append((x[i], y[i], h))
        tmp.append((x[i+1], y[i+1], h))
        tmp.append((x[i+1], y[i+1], 0))
        verts.append(tmp)
    tmp = []
    tmp.append((x[-1], y[-1], 0))
    tmp.append((x[-1], y[-1], h))
    tmp.append((x[0], y[0], h))
    tmp.append((x[0], y[0], 0))
    verts.append(tmp)
    glBegin(GL_QUADS)
    for v in verts:
        n = numpy.cross(numpy.array(v[3]) - numpy.array(v[1]),
                        numpy.array(v[0]) - numpy.array(v[1]))
        # выставляем нормаль
        glNormal3fv(n)
        # задаём 4 координаты прямоугольника
        glVertex3fv(v[0])
        glVertex3fv(v[1])
        glVertex3fv(v[2])
        glVertex3fv(v[3])
    glEnd()
    l = [(x[i], y[i], 0) for i in range(len(x))]
    coord_centr = numpy.array([0, 1, 0])
    l2 = [(x[i], y[i], h) for i in range(len(x))]
    glBegin(GL_TRIANGLES)
    for i in range(0, len(l)):
        n = numpy.cross(coord_centr - numpy.array(l[i]),
                        numpy.array(l[i - 1]) - numpy.array(l[i]))
        # задаём нормаль и 3 координаты треугольника
        n = -n
        glNormal3fv(n)
        glVertex3fv(l[i - 1])
        glVertex3fv(l[i])
        glVertex3fv(coord_centr)

    coord_centr = numpy.array([0, 1, h])
    for i in range(0, len(l2)):
        n = numpy.cross(coord_centr - numpy.array(l2[i]),
                        numpy.array(l2[i - 1]) - numpy.array(l2[i]))
        # задаём нормаль и 3 координаты треугольника
        glNormal3fv(n)
        glVertex3fv(l2[i - 1])
        glVertex3fv(l2[i])
        glVertex3fv(coord_centr)
    glEnd()


def init():
    # устанавливаем стандартный свет и прозрачность
    glClearColor(255, 255, 255, 1.0)
    # Очищаем буфер глубины от предыдущих значений
    glClearDepth(1.0)
    # Включаем тест глубины
    glEnable(GL_DEPTH_TEST)
    # запрещаем сглаживание
    glShadeModel(GL_FLAT)
    # Фрагмент проходит тест, если его значение глубины меньше либо равно хранимому в буфере
    glDepthFunc(GL_LEQUAL)
    # Включаем тест глубины, чтобы отбросить не прорисовывать невидимые грани.
    glEnable(GL_DEPTH_TEST)
    # Нормали нормируются до единичной длины
    glEnable(GL_NORMALIZE)
    # уменьшаем ступенчатость прямых за счёт увеличение пикселей
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    # указываем, чтобы была хорошая коррекция
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    # Включаем освещение
    glEnable(GL_LIGHTING)
    # Режим освещённости для двух граней
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    # При задании нормалей приводить их к единичной длине
    glEnable(GL_NORMALIZE)


def ReshapeFn(width, height):
    # устанавливаем область просмотра
    glViewport(0, 0, width, height)
    # Переходим в режим проекта - для взаимодействия с окном окном проекта
    glMatrixMode(GL_PROJECTION)
    # считываем текущую матрицу
    glLoadIdentity()
    # задаём угол поля зрения, соотношение сторон, расстояние до ближайшей плоскости и дальшей плоскости
    gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
    # Переходим в режим просмотра (работать будем с просмотром)
    glMatrixMode(GL_MODELVIEW)
    # считываем текущую матрицу
    glLoadIdentity()
    # задаём координаты точки глаза наблюдателя, коорнаты центра экрана, направление вектора задающего поворот сцеры
    gluLookAt(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1, 0.0)


def DisplayFn():
    global zoom
    # очищаем цаетовой и глубинный буферы
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Переходим в режим просмотра (работать будем с просмотром)
    glMatrixMode(GL_MODELVIEW)
    # считываем текущую матрицу
    glLoadIdentity()
    # задаём координаты точки просмотра, центра, наплавдение вертикального вектора
    gluLookAt(10, 10, 10, 0, 0, 0, 0, 0, 1)
    glTranslatef(zoom, zoom, zoom)
    LightingFn()
    # Вращение вокруг осей
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glRotatef(zrot, 0, 0, 1)
    DrawFn()

def IntensiveChangeFn(x):
    global intensive
    intensive = x
    LightingFn()
    glutPostRedisplay()
    return 0

def ApproximationChangeFn(x):
    global app
    app = x
    glutPostRedisplay()
    return 0

def RotateFn():
    global zrot
    speed = [1 / 100000]
    # cycle(speed) --> speed, speed, speed
    for val in cycle(speed):
        begin = time.time()
        while time.time() - begin < 1:
            zrot += val
            glutPostRedisplay()

# x, y - коопдинаты курсора (необходимые параметры для glutKeyboardFunc())
def keys(key, x, y):
    global xrot, yrot, zrot, zoom
    if key == b'w':
        xrot += 2
    elif key == b's':
        xrot -= 2
    elif key == b'a':
        yrot += 2
    elif key == b'd':
        yrot -= 2
    elif key == b'q':
        zrot += 2
    elif key == b'e':
        zrot -= 2
    elif key == b'b':
        zoom += 1
    elif key == b'n':
        zoom -= 1
    elif key == b'z':
        IntensiveChangeFn(intensive + 5)
        LightingFn()
    elif key == b'x':
        IntensiveChangeFn(intensive - 5)
        LightingFn()
    elif key == b'c':
        ApproximationChangeFn(app + 1)
    elif key == b'v':
        ApproximationChangeFn(app - 1)
    # Перерисовка изображения
    glutPostRedisplay()


def LightingFn():
    global light_coord
    glEnable(GL_LIGHT0)
    # интенсивность цветов
    light_intensity = (1.0, 1.0, 1.0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  light_intensity)
    # w = 1.0: (x/w,y/w,z/w) == (x,y,z)
    light_position = (light_coord[0], light_coord[1], light_coord[2], 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    attenuation = float(101 - intensive) / 25.0
    # Расстояние между положением источника света и вершиной
    distance = numpy.sqrt(pow(light_coord[0], 2) +
                     pow(light_coord[1], 2) + pow(light_coord[2], 2))
    # 3 слагаемых формулы
    kQ = attenuation / (3.0 * distance * distance)
    kL = attenuation / (3.0 * distance)
    kC = attenuation / 3.0
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, kC)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, kL)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, kQ)


def main():
    glutInit(sys.argv)
    # Задаём режим отображения GLUT_RGBA - цветовой режим,
    # GLUT_DOUBLE - режим двойного буффера (отрисовка происходи на скрытом слое, затем меняется с видимым)
    # GLUT_DEPTH - скрывает невидимые линии при отрисовки объёмных фигур
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 400)
    glutInitWindowPosition(300, 150)
    glutCreateWindow(b"OpenGL labs")
    glutDisplayFunc(DisplayFn)
    glutReshapeFunc(ReshapeFn)
    glutKeyboardFunc(keys)
    init()
    # Создаём поток для постоянного изменения положения фигуры
    t = threading.Thread(target=RotateFn)
    # При завершении потока main поток поворота фигуры будет завершён
    t.daemon = True
    t.start()
    # циклический вызов функции отображения
    glutMainLoop()


if __name__ == "__main__":
    print("| WS -- rotate X\n| AD -- rotate Y\n| QE -- rotate Z\n| BN -- zoom\n| ZX -- change intensive\n| CV -- approximation")
    main()