from datetime import datetime
import pygame as pg

t = 0
delta_t = 0

pg.init()
run = True
win_x, win_y = 800, 480
screen = pg.display.set_mode((win_x, win_y))

while (run):
    screen.fill((255, 255, 255))

    t = (str(datetime.now())[-9:-7]+str(datetime.now())[-6:-3])
    print(t)

    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
