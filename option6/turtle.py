# type: ignore
import atexit
import math
import platform
import random
from functools import lru_cache
from io import BytesIO
from tkinter import Canvas
from turtle import _CFG, RawTurtle, _Screen
from typing import List, Tuple

from PIL import Image
from PIL.Image import Image as ImageClass

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
    shelly.pensize(2)

    # randomise variables for drawing
    forward = random.randrange(200, 400)
    left = random.randrange(130, 230)

    # setup drawing
    shelly.goto(-forward / 2, 0)
    x1, y1 = shelly.pos()
    shelly.color(tuple(random.random() for _ in range(3)), tuple(random.random() for _ in range(3)))
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
    img = trim_image(img)
    png_f = BytesIO()
    img.save(png_f, format="png")
    png_f.seek(0)
    return png_f


def get_border(image, trim_color, direction: str):
    x_func = iter
    y_func = iter
    x_adjust = 0
    y_adjust = 0
    if direction == "east":
        x_func = iter
        x_adjust = -1
    elif direction == "west":
        x_func = reversed
        x_adjust = 1
    elif direction == "north":
        y_func = iter
        y_adjust = -1
    elif direction == "south":
        y_func = reversed
        y_adjust = 1

    if y_adjust == 0:
        for x in x_func(range(image.width)):
            for y in y_func(range(image.height)):
                if image.getpixel((x, y)) != trim_color:
                    return x + x_adjust
    elif x_adjust == 0:
        for y in y_func(range(image.height)):
            for x in x_func(range(image.width)):
                if image.getpixel((x, y)) != trim_color:
                    return y + y_adjust


def get_border_rect(image, trim_color) -> List[int]:
    rect = []
    for direction in ["east", "north", "west", "south"]:
        rect.append(get_border(image, trim_color, direction))
    return rect


def trim_image(image: ImageClass, trim_color: Tuple[int, int, int] = (255, 255, 255)) -> ImageClass:
    """Trim the border from an image."""
    return image.crop(get_border_rect(image, trim_color))
