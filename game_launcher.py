import pygame as pg
from game_processor import Game_Processor
pg.init()

# initializing window
pg.display.set_caption("super game")
pg.display.set_icon(pg.image.load("resources/icon.bmp"))

game = Game_Processor(state="gameplay")
while True:
    game.handle_state()

