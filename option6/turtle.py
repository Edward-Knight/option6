import atexit
import math
import platform
import random
from functools import lru_cache
from io import BytesIO
from tkinter import Canvas
from turtle import _CFG, RawTurtle, _Screen

from PIL import Image

if platform.system() == "Linux":
    import xvfbwrapper


@lru_cache(1)
def setup_xvfb() -> None:
    if platform.system() != "Linux":
        return

    xvfb = xvfbwrapper.Xvfb(1920, 1080)
    atexit.register(xvfb.stop)
    xvfb.start()


def make_turtle() -> Canvas:
    setup_xvfb()

    # todo: try and create more isolated? root/canvas/screen/turtle
    # root = Tk()
    # canvas = Canvas(root, height=1500, width=1500)
    # screen = TurtleScreen(canvas)
    # shelly = RawTurtle(screen)

    # create canvas and turtle
    screen = _Screen()
    shelly = RawTurtle(
        screen,
        shape=_CFG["shape"],
        undobuffersize=_CFG["undobuffersize"],
        visible=_CFG["visible"],
    )
    canvas = screen._canvas

    # set up turtle
    screen.tracer(0)  # don't animate (run in a single frame)
    shelly.hideturtle()

    # randomise variables for drawing
    forward = random.randrange(100, 300)
    left = random.randrange(100, 170)

    # setup drawing
    shelly.backward(forward / 2)
    x1, y1 = shelly.pos()
    shelly.color("purple", "red")
    shelly.pendown()
    shelly.begin_fill()

    # start drawing
    while True:
        shelly.forward(forward)
        shelly.left(left)
        x2, y2 = shelly.pos()
        if math.isclose(x1, x2, abs_tol=10) and math.isclose(y1, y2, abs_tol=10):
            break
    shelly.end_fill()

    # write the drawing to the screen
    screen.update()

    return canvas


def save_turtle(screen: Canvas) -> BytesIO:
    ps = screen.postscript()
    ps_f = BytesIO(ps.encode())
    img = Image.open(ps_f)
    png_f = BytesIO()
    img.save(png_f, format="png")
    png_f.seek(0)
    return png_f
