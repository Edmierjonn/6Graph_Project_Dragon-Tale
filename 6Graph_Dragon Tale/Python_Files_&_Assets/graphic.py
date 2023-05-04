from graphics import *
from subprocess import call

def e():
    win = GraphWin("Dragon Tale", 1200, 800)

    bg_image = Image(Point(1200/2, 800/2), "assets/poster_final.png")
    bg_image.draw(win)

    start_image = Image(Point(600, 500), "assets/start.png")
    start_image.draw(win)


    pt1 = Point(445, 445)
    pt2 = Point(755, 550)

    rec = Rectangle(pt1, pt2)

    while True:

            try:
                m = win.getMouse()
            except GraphicsError:
                break

            if (m.getX() > pt1.getX()) and (m.getX() < pt2.getX()):
                if (m.getY() > pt1.getY()) and (m.getY() < pt2.getY()):
                    win.close()
                    call(["python", "main.py"])

e()
