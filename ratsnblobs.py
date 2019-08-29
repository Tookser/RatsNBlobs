'''основной модуль, в котором всё'''
import abc
import random
import heapq
import time
import os
import collections

import bearlibterminal.terminal as t


import singleton

from obstacles import *
import mapgen
import log

#debug flag внутри
from debug_functions import * 
from keys import *


diagonal_fridges_flag = True #перемещение холодильничков по диагонали
reborn_flag = True #перерождение с полным HP на каждом уровне

animation_flag = False #анимация
side_help_flag = False #краткая справка справа от экрана

NUMPAD_MOVEMENT_FLAG = True #управление с нумпада




fixed_view_flag = False #фиксированный размер обзора
status_bar_flag = True #строка статуса
LOG_FLAG = True

HEIGHT_OF_VIEW = WIDTH_OF_VIEW = 13 #для нефиксированного поля зрения
WIDTH_OF_WINDOW = 40
HEIGHT_OF_WINDOW = 19

#NUMBER_OF_LOG_MESSAGES_TO_SHOW = 10
#DELAY_AFTER_MOVE = 200

#only for notepad++
os.chdir(os.path.dirname(os.path.abspath(__file__)))

resources_path = 'Resources'


player_health = 30.
player_damage = 1.5
SIZE_OF_INVENTORY = 10
player_color = ['red', 'red', 'red', 'red', 'red', \
                'yellow', 'yellow', 'yellow', 'yellow', 'yellow', \
                'green', 'green', 'green', 'green', 'green', \
                'light green', 'light green', 'light green', 'light green', 'light green', 'sky']

#delay after player's movement
after_delay = 1000
is_delay = False

#пауза после конца игры
PAUSE_AFTER_END_OF_GAME_FLAG = False
PAUSE_AFTER_END_OF_GAME_LENGTH = 2500

background_color = 'black'
poisoned_creature_background_color = 'light green'

wall_color = 'white'
free_color = 'white'
fridge_color = 'blue' #цвет холодильник
question_color = 'yellow' #цвет остальных препятствий
stone_color = 'grey'
sword_color = 'red'

help_color = 'white'
help_highlight_color = 'sky'
status_bar_color = 'white'
attack_number_color = 'red'
inventory_key_color = 'yellow'
inventory_return_key_color = 'sky'
passive_log_color = 'light grey'
active_log_color = 'white'


neighbour_cells = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]

#все клавиши перемещения, доступные здесь
ALL_KEYS_MOVE = keys_move.copy()
if NUMPAD_MOVEMENT_FLAG:
    ALL_KEYS_MOVE.update(numpad_keys_move)
    
ALL_KEYS_MOVE_WITHOUT_STANDING = ALL_KEYS_MOVE.copy()
try:
    del ALL_KEYS_MOVE_WITHOUT_STANDING[t.TK_H]
except KeyError:
    pass
try:
    del ALL_KEYS_MOVE_WITHOUT_STANDING[t.TK_KP_5]
except KeyError:
    pass
    

''' deprecated
#возможные препятствия, новые - добавлять в конец, чтобы не сбилась нумерация
list_of_obstacles = ['space', 'wall', 'stone', 'fridge', 'sword']
tuple_of_type_of_obstacles = collections.namedtuple('type_of_obstacles', ' '.join(list_of_obstacles))
#сами константы препятствий, использовать их
obstacles_types = tuple_of_type_of_obstacles(*range(len(list_of_obstacles)))
'''
class GameError(Exception):
    '''всё на него'''
    pass

class IRQueueError(Exception):
    pass

class VizualizationError(Exception):
    pass

class MoveError(Exception):
    pass

class AttackError(Exception):
    pass

class UseError(Exception):
    '''кидается если не удалось использовать предмет'''
    pass

class TurnCompleted(Exception):
    '''кидается, если инвентарь сделал ход (применение предмета)'''
    pass
    
class WormError(Exception):
    pass

class LevelError(Exception):
    pass

exec(open('game.py').read())
exec(open('vizualization.py').read())
exec(open('infiniterandomqueue.py').read())

exec(open('item.py').read())
exec(open('items.py').read())

exec(open('cellholder.py').read())
exec(open('creature.py').read())

exec(open('player.py').read())

exec(open('monsters.py').read())

def add_monster(x, y, type_of_monster):
    '''add monster realtime, in cell or adjust'''
    if l.is_free(x, y):
        type_of_monster(x, y)
    else:
        cells = []
        for x_a, y_a in ((0, -1), (0, 1), (1, 0), (-1, 0)):
            if l.is_free(x + x_a, y + y_a):
                cells.append((x + x_a, y + y_a))
        if cells != []:
            type_of_monster(*random.choice(cells))


exec(open('spawnqueue.py').read())

exec(open('level.py').read())
exec(open('levels.py').read())



if __name__ == "__main__":
    v = Vizualization()
    v.start_vizualize()
    game = Game()
    player = None


    lg = mapgen.LevelsGenerator1()
    Level(lg)

    game.cycle()

    v.end_vizualize()
else:
    raise GameError("Can't import this module")