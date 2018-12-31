import abc
import random
import heapq
import time
import os
import collections
import bearlibterminal.terminal as t

import mapgen

debug_flag = False #при включённом функция debug выводит
animation_flag = False #анимация
side_help_flag = False #help on the game screen
reborn_flag = True #перерождение с полным HP на каждом уровне
numpad_movement_flag = True #управление с нумпада
fixed_view_flag = False #фиксированный размер обзора
diagonal_fridges_flag = True #перемещение холодильничков по диагонали
height_of_view = width_of_view = 7


#only for notepad++
os.chdir(os.path.dirname(os.path.abspath(__file__)))

resources_path = 'Resources'

player_health = 10.
player_damage = 1.5
player_color = ['red', 'red', 'darkest blue', 'darkest blue', \
'blue', 'blue', 'blue', 'green', 'green', 'white', 'white']

#delay after player's movement
after_delay = 1000
is_delay = False


background_color = 'black'
wall_color = 'white'
free_color = 'white'
help_color = 'white'
fridge_color = 'blue' #цвет холодильник
question_color = 'yellow' #цвет остальных препятствий
help_highlight_color = 'sky'
stone_color = 'grey'

neighbour_cells = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1), 
                (1, -1), (1, 0), (1, 1)
                ]

#возможные препятствия, новые - добавлять в конец, чтобы не сбилась нумерация
list_of_obstacles = ['space', 'wall', 'stone', 'fridge']
tuple_of_type_of_obstacles = collections.namedtuple('type_of_obstacles', ' '.join(list_of_obstacles))
#сами константы препятствий, использовать их
obstacles_types = tuple_of_type_of_obstacles(*range(len(list_of_obstacles)))

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

class WormError(Exception):
    pass

def debug(*text):
    if debug_flag:
        for el in text:
            print(el, ' ', end='')
        print('')

def debug_field():
    '''print all wormheads'''
    if debug_flag:
        debug('----')
        for x in range(width):
            for y in range(height):
                if field[x][y] != []:
                    #print('!')
                    if isinstance(field[x][y][0], WormHead):
                        w = field[x][y][0]
                        debug('O', x, '-', y, '-', 'o' if w._next is not None else '#',\
                        w._next, w._pred, len(w._segments), ' segments')

class Game():
    '''TODO'''
    def __init__(self):
        pass

    def cycle(self):
        '''основной цикл игры, ходы игрока и смерть'''
        while True:
            #TODO life bar
            #print(irq.ammount, ' ', player.health)
            irq.get().turn()
            if l.end_of_game():
                if not player.is_die():
                    v.win()
                    break
                elif player.is_die():
                    v.lose()
                    break
                else:
                    pass

                '''elif game.is_next_level(): ??'''


    def new_level(self, l, field, field_walls, obstacles, irq, h, player=None):
        '''update vars'''
        self.l = l
        self.field = field
        self.field_walls = field_walls
        self.obstacles = obstacles
        self.irq = irq
        self.h = h
        #if player is not None:
        self.player = player

class Vizualization():
    def __init__(self):
        self._corner = (2, 2)

    def animation_decorator(function_to_decorate):
        '''декоратор для всех функций анимации'''
        def dont_animate(self, *args, **kwargs):
            pass

        return function_to_decorate if animation_flag else dont_animate


    def start_vizualize(self):
        t.open()
        try:
            assert t.set('''window: title ='RATS''N''BLOBS 0.0.1', size=40x15;''')
            assert t.set('font: VeraMono.ttf, size=20')
            assert t.set('input.filter={keyboard+}')
        except:
            raise VizualizationError('can\'t set options')

    def vizualize(self):
        '''версия визуализации без окошка обзора'''

        def color_and_symbol(j, i):
            '''выдаёт цвет и символ для клетки'''
            if field_walls[j][i]:
                return (wall_color, '#')
            elif l.is_monster_in(j,i):
                return (l.get_monster(j,i).color, l.get_monster(j,i).letter)
            else:
                if obstacles[j][i] == obstacles_types.stone:
                    return (stone_color, 'o')
                elif obstacles[j][i] == obstacles_types.fridge:
                    return (fridge_color, 'f')
                elif obstacles[j][i] != obstacles_types.space:
                    return (question_color, '?')
                else:
                    return (free_color, '.')

        t.clear()
        t.bkcolor(t.color_from_name(background_color))
        t.color(t.color_from_name(wall_color))

        x, y = self._corner
        height, width = l.height, l.width

        t.print(x, y - 1, 'Don\'t press P to hel[color={}]p[/color].'.format(help_highlight_color))
        
        #i и j - координаты в окошке 
        #добавляется i_real и j_real (реальные координаты)
        if fixed_view_flag:
            t.print(x, y, '#' * (width + 2))
            t.print(x, y + height + 1, '#' * (width + 2))
            for i in range(height):
                t.color(t.color_from_name(wall_color))
                t.put(x, y + 1 + i, ord('#'))
                t.put(x + width + 1, y + 1 + i, ord('#'))
                for j in range(width):
                    color, symbol = color_and_symbol(j, i)
                    t.color(t.color_from_name(color))
                    t.put(x + 1 + j, y + 1 + i, ord(symbol))
        else:
            #только для одинаковых размеров по вертикали и горизонтали сейчас
            t.print(x, y, '-' * (width_of_view + 2))
            t.print(x, y + height_of_view + 1, '-' * (width_of_view + 2))
            
            sdvig = height_of_view // 2

            for i in range(height_of_view):
                t.color(t.color_from_name(wall_color))
                t.put(x, y + 1 + i, ord('|'))
                t.put(x + width_of_view + 1, y + 1 + i, ord('|'))
                for j in range(width_of_view):
                    i_real, j_real = i + player.y - sdvig, j + player.x - sdvig
                    if i_real in range(l.height) and j_real in range(l.width):
                        color, symbol = color_and_symbol(j_real, i_real)
                        t.color(t.color_from_name(color))
                        t.put(x + 1 + j, y + 1 + i, ord(symbol))
                    #если клетка за пределами поля, то стена
                    else:
                        t.color(t.color_from_name(wall_color))
                        t.put(x + 1 + j, y + 1 + i, ord('#'))
        
        
        if side_help_flag: self.side_help(x + width + 3, y + height // 2)

        #t.color(t.color_from_name(help_color))

        t.refresh()

    def end_vizualize(self):
        t.close()

    def side_help(self, x, y):
        t.color(t.color_from_name(help_color))
        t.print(x, y, 'TYU')
        t.print(x, y + 1, 'G@J')
        t.print(x, y + 2, 'BNM')

    @animation_decorator
    def fire(self, x, y, color1='yellow', color2='white', fire_time=45, zwerg_times=7):
        '''game field + 1
           corner->##
                   #F<-field'''
        saved_color, saved_bkcolor = t.TK_COLOR, t.TK_BKCOLOR

        x, y = x + self._corner[0] + 1, y + self._corner[1] + 1
        def put():
            t.put(x, y, symbol)
            t.refresh()
            t.delay(fire_time)

        symbol = t.pick(x, y)
        native_color = t.pick_color(x, y)
        t.color(native_color)
        native_background_color = t.pick_bkcolor(x, y)

        t.bkcolor(t.color_from_name(color1))
        put()

        def zwerg():
            t.bkcolor(t.color_from_name(color1))
            put()
            t.bkcolor(t.color_from_name(color2))
            put()

        for i in range(zwerg_times): zwerg()

        #restore


        t.color(native_color)
        #TEMPORARY HACK TODO
        t.bkcolor(t.color_from_name(background_color))
        #t.bkcolor(native_background_color)

        t.put(x, y, symbol)

        t.color(saved_color)
        t.bkcolor(saved_bkcolor)



        t.refresh()

    @animation_decorator
    def explosion(self, x, y, radius=2, form_diagonal=True, color1='yellow',\
    color2='white', fire_time=45, zwerg_times=4):
        '''explosion visualization
        form_diagonal - rotated 45* square'''
        if form_diagonal:
            saved_color, saved_bkcolor = t.TK_COLOR, t.TK_BKCOLOR
            previous_x, previous_y = x, y
            #x, y = x + self._corner[0] + 1, y + self._corner[1] + 1

            mas = range(-radius, radius + 1)
            mas2 = []
            for i in mas:
                for j in mas:
                    if abs(i) + abs(j) <= radius:
                        mas2.append((i, j))
            #print(mas2)
            #print(len(mas2))
            list_cells = [(x + i, y + j) for i, j in mas2 \
            if x + i in range(width) and (y + j) in range(height) and \
            not field_walls[x+i][y+j]]

            list_cells = [(x + self._corner[0] + 1, y + self._corner[1] + 1) \
            for x, y in list_cells]
            '''
            for i, j in mas2:
                print ('{0}+{1} {2}+{3}'.format(x, i, y, j))
                print (x + i, y + j)
            '''
            #print(list_cells)



            def put():
                '''the main change between explosion and fire'''
                for x_here, y_here in list_cells:
                    t.color(native_colors[(x_here, y_here)])
                    t.put(x_here, y_here, symbols[(x_here, y_here)])
                t.refresh()
                t.delay(fire_time)

            symbols = {(x, y):t.pick(x, y) for x, y in list_cells}
            native_colors = {(x, y):t.pick_color(x, y) for x, y in list_cells}
            #temporary hack TODO
            #not used
            native_background_color = {(x, y):t.pick_bkcolor(x, y) for x, y in list_cells}

            def zwerg():
                t.bkcolor(t.color_from_name(color1))
                put()
                t.bkcolor(t.color_from_name(color2))
                put()

            for i in range(zwerg_times): zwerg()

            #restore

            #TEMPORARY HACK TODO
            t.bkcolor(t.color_from_name(background_color))
            #t.bkcolor(native_background_color)
            for x_here, y_here in list_cells:
                t.color(native_colors[(x_here, y_here)])
                t.put(x_here, y_here, symbols[(x_here, y_here)])

            t.color(saved_color)
            t.bkcolor(saved_bkcolor)
        else:
            raise NotImplementedError

    def test_vizualize(self, field, height, width):
        '''тестовая текстовая визуализация, устарела'''
        def horizontal():
            for i in range(width + 2):
                print('#', end='')
            print('')
        horizontal()
        for i in range(height):
            print('#', end='')
            for j in range(width):
                if field[j][i] == []:
                    print('.', end='')
                else:
                    print('!', end='')
            print('#')
        horizontal()
        t.open()
        t.set('''window: title = RATS''N''BLOBS 0.0.1, size = 60x35''')
        t.refresh()
        key = t.read()
        if key == t.TK_K:
            t.close()
        else:
            color = t.color_from_name('light blue')
            t.set('''window: title = RATS''N''BLOBS 0.0.1, size = 60x35''')
            t.color(color)
            massiv = [color]*4
            for i in range(10):
                t.put_ext(2, 2 + i, i, i, 42, massiv)
                t.put_ext(2 + i, 2, i, i, 42, massiv)
                t.put_ext(2 + 10, 2 + i, i, i, 42, massiv)
                t.put_ext(2 + i, 2 + 10, i, i, 42, massiv)
            t.put(2 + 10, 2 + 10, 42)

            massiv2 = [color, color, t.color_from_name('red'), t.color_from_name('red')]
            t.put_ext(20, 20, 0, 0, 42, massiv2)

            t.refresh()
            t.delay(8000)
            t.close()

    def help(self):
        t.clear()
        t.color(t.color_from_name(help_color))
        #print(t.TK_WIDTH // 2, t.TK_HEIGHT // 2 - 1, 'Press to move:')
        t.print(10, 10 - 1, 'Press to move:')
        t.print(10, 10, 'TYU')
        t.print(10, 10 + 1, 'G@J')
        t.print(10, 10 + 2, 'BNM')
        t.print(10, 10 + 3, 'Press H to wait.')

        t.refresh()
        #t.delay(3000)

    def win(self):
        t.set('input.filter=keyboard') #important!

        t.color('yellow')
        t.print(v._corner[0] + width // 2 - 4, v._corner[1] + height + 2, \
        '!YOU WIN! PRESS ANY KEY...')
        t.refresh()

        key = t.read()

    def lose(self):
        t.set('input.filter=keyboard') #important!
        t.color('darker blue')
        t.print(v._corner[0] + width // 2 - 4, v._corner[1] + height + 2, \
        '...You lose..... PRESS ANY KEY...')
        t.refresh()

        #hack to solve problem
        #key = t.read()

        key = t.read()


class InfiniteRandomQueue:
    '''move from RtL, then throw LtR'''
    def __init__(self):
        self._left = []
        self._right = []
        self._ammount = 0
        self._rammount = 0
        self._lammount = 0
        self._turn_number = 0

    def append(self, item):
        '''add element'''
        self._right.append(item)
        random.shuffle(self._right)
        self._ammount += 1
        self._rammount += 1


    def get(self):
        '''get element from InfiniteRandomQueue'''
        if self._right == []:
            if self._left == []:
                raise IRQueueError('There is no items')
            self._right = self._left
            random.shuffle(self._right)
            self._left = []
            self._rammount, self._lammount = self._lammount, self._rammount
            self._turn_number += 1
            run_daemons()
        result = self._right[-1]
        self._left.append(result)
        del self._right[-1]

        self._rammount -= 1
        self._lammount += 1
        return result

    def delete(self, creature):
        try:
            self._right.remove(creature)
            self._rammount -= 1
            self._ammount -= 1
        except ValueError:
            try:
                self._left.remove(creature)
                self._lammount -= 1
                self._ammount -= 1
            except ValueError:
                raise IRQueueError('Can\'t delete from queue, there is no such creature')


    @property
    def ammount(self):
        return self._ammount

    @property
    def turn_number(self):
        return self._turn_number

class CellHolder(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, x, y):
        #if not field_walls[x][y]:
        if l.is_free(x, y):
            field[x][y].append(self)
        else:
            raise MoveError('something under the {} in {}:{}'.format(self.__class__.__name__, x, y))
        self._x = x
        self._y = y

class Creature(CellHolder, metaclass = abc.ABCMeta):
    '''human or monster or item(?)'''
    @abc.abstractmethod
    def __init__(self, x, y, health, damage, color, letter, current_health=None):
        super().__init__(x, y)
        irq.append(self)

        self._maxhealth = health
        self._health = health if current_health is None else current_health

        self._damage = damage
        self._color = color
        self._letter = letter

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def turn(self):
        '''think and select action'''
        pass

    def _real_move(self, x, y):
        '''перемещение без доп. проверок кроме смежности
        вызывается в move deprecated?'''
        if (abs(x-self.x) <= 1) and (abs(y-self.y) <= 1): #if adjust
            if x in range(width) and y in range(height):
                if abs(x-self.x) + abs(y-self.y) >= 1:
                    field[x][y] = [self]
                    field[self.x][self.y].remove(self)
                    self._x = x
                    self._y = y
                    
    def is_near(self, x, y):
        '''проверка на близость, deprecated?'''
        return ((abs(x-self.x) <= 1) and (abs(y-self.y) <= 1)) and\
        (x in range(width) and y in range(height)) and\
        ((x, y) != (self.x, self.y))


    def move(self, x, y):
        '''move. or attack or wait'''
        def movement():
            '''само перемещение'''
            field[x][y] = [self]
            field[self.x][self.y].remove(self)
            self._x = x
            self._y = y
            
        if (abs(x-self.x) <= 1) and (abs(y-self.y) <= 1): #if adjust
            if x in range(width) and y in range(height):
                if abs(x-self.x) + abs(y-self.y) >= 1:
                    #атака прежде всего
                    if l.is_monster_in(x, y):
                        self.attack(x, y)
                    #перемещение холодильника
                    elif (self.__class__.__name__ == 'Player') and l.is_fridge(x,y):
                        if l.move_fridges(self.x, self.y, x, y):
                            movement()
                    #игрок может ходить по камням, остальные - нет
                    elif (self.__class__.__name__ == 'Player' and 
                    (l.is_free_except_stones(x, y))) or \
                    l.is_free(x, y):
                        movement()
                            
        else:
            raise MoveError('distance is too long')

    def attack(self, x, y):
        '''attack!!!'''
        if x in range(width) and y in range(height):
            if (abs(x - self.x) <= 1) and (abs(y - self.y) <= 1) and \
            (abs(y - self.y) + abs(x - self.x) >= 1): #if adjust
                debug(x-self.x, y - self.y, x, y, self.x, self.y)
                if l.is_monster_in(x, y):
                    '''TODO to get_monster'''
                    field[x][y][0].suffer(self._damage)
                else:
                    #attack air
                    pass
            else:
                debug(x-self.x, y - self.y, x, y, self.x, self.y)
                raise AttackError('distance is too long')
        else:
            #attack wall
            pass

    def suffer(self, damage):
        '''receive damage'''
        self._health -= damage
        if damage != 0:
            v.fire(self.x, self.y)
        elif damage == 0:
            pass
            #ugly blue bump
            #v.fire(self.x, self.y, color1 = 'blue', color2 = 'white', \
            #fire_time = 70, zwerg_times = 1)

        if self._health <= 0:
            self._die()

    def _die(self):
        '''postmortem actions'''
        field[self.x][self.y].remove(self)
        irq.delete(self)

    @property
    def color(self):
        return self._color[int(self._health)]

    @property
    def letter(self):
        return self._letter

    @property
    def health(self):
        return self._health

class Player(Creature):
    def __init__(self, x, y, old_player=None):
        #super(Player, self).__init__(x, y, player_health, player_damage, player_color, '@')
        if old_player is None or reborn_flag:
            super().__init__(x, y, player_health, player_damage, player_color, '@')
        else:
            super().__init__(x, y, player_health, player_damage, player_color, \
            '@', current_health=old_player.health)
        self._is_die = False
        self._inventory = None

    '''def move(self, x, y):
        расширение перемещения (игрок может через камни, сдвигать холодильники и тд)
        if l.is_free_except_stones(x, y):
            self._real_move(x, y)'''
        
    
    def turn(self):
        keys_move = {t.TK_T:(-1, -1),
        t.TK_Y:(0, -1),
        t.TK_U:(1, -1),
        t.TK_G:(-1, 0),
        t.TK_H:(0, 0),
        t.TK_J:(1, 0),
        t.TK_B:(-1, 1),
        t.TK_N:(0, 1),
        t.TK_M:(1, 1)
        }

        numpad_keys_move = {t.TK_KP_7:(-1, -1),
        t.TK_KP_8:(0, -1),
        t.TK_KP_9:(1, -1),
        t.TK_KP_4:(-1, 0),
        t.TK_KP_5:(0, 0),
        t.TK_KP_6:(1, 0),
        t.TK_KP_1:(-1, 1),
        t.TK_KP_2:(0, 1),
        t.TK_KP_3:(1, 1)
        }

        help_key = t.TK_P
        
        pickup_drop_key = [t.TK_SPACE]
        #t.set('input.filter=[keyboard+]')

        v.vizualize()
        while True:
            key = t.read()
            if t.state(help_key):
                v.help()
            else:
                v.vizualize()

            if key in keys_move:
                movement = keys_move[key]
                self.move(self.x + movement[0], self.y + movement[1])
                break

            if numpad_movement_flag and key in numpad_keys_move:
                movement = numpad_keys_move[key]
                self.move(self.x + movement[0], self.y + movement[1])
                break
            
            if key in pickup_drop_key:
                if player.is_inventory():
                    player.drop_item()
                else:
                    player.pickup_item()
            '''is_movement = False
            for key in keys_move:
                if t.state(key):
                    movement = keys_move[key]
                    self.move(self.x + movement[0], self.y + movement[1])
                    is_movement = True
                    break
            if is_movement:
                break'''

        #t.set('input.filter=[]')
        v.vizualize()

        t.delay(after_delay if is_delay else 0)

    def is_inventory(self):
        '''возвращает инвентарь'''
        return self._inventory
    
    def pickup_item(self):
        '''поднять предмет'''
        if obstacles[self.x][self.y]:
            self._inventory = obstacles[self.x][self.y] 
            obstacles[self.x][self.y] = obstacles_types.space
        else:
            pass
    
    def drop_item(self):
        '''бросить предмет, с заменой'''
        if self.is_inventory():
            obstacles[self.x][self.y] = self._inventory
            self._inventory = None
        else:
            pass
    
    def _die(self):
        super()._die()
        self._is_die = True

    def is_die(self):
        return self._is_die

#подключает описания монстров
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


def run_daemons():
    if h != []:
        while h[0][0] == irq.turn_number:
            turn_number, funct, arguments = h.pop()
            funct(*arguments)

def spawn(x, y, type_of_monster, interval=0):
    '''interval 0 if without rerun'''
    add_monster(x, y, type_of_monster)
    if interval:
        heapq.heappush(h, (irq.turn_number + interval, spawn, (x, y, type_of_monster, interval)))

def add_spawn(x, y, type_of_monster, interval=10):
    heapq.heappush(h, (irq.turn_number + interval, spawn, (x, y, type_of_monster, interval)))



def test_spawns():
    add_spawn(3, 3, Rat, 10)

class Level(metaclass = abc.ABCMeta):
    '''TODO не помню что'''

    @abc.abstractmethod
    def __init__(self, width=10, height=4, x_player=2, y_player=2, win_level=None, from_file = False, field_walls_arg = None, obstacles_arg = None, generate_map = False):
        '''если установлен generate_map, то width и height могут быть изменены'''
        assert bool(field_walls_arg) == bool(obstacles_arg)
        
        global l
        l = self

        
        
        
        global field_walls
        global obstacles
        
        #загрузка карты из файла
        if generate_map:
            field_walls, obstacles, self._height, self._width = self.generate_map(height, width)
            
        elif from_file: 
            field_walls, obstacles = self._load_scene(self.__class__.__name__, width, height)
        else:
            field_walls = [[False for j in range(height)] for i in range(width)]
           
            obstacles = [[False for j in range(height)] for i in range(width)]
        
        
        global field
        field = [[[] for j in range(height)] for i in range(width)]
        
        
        
        global irq
        irq = InfiniteRandomQueue()
        global h
        h = []

        #TODO items bla-bla-bla TODO
        
        global player
        old_player = player
        player = Player(x_player, y_player, old_player)

        self.monsters()
        self.spawns()

        self.win_level = win_level

        game.new_level(l, field, field_walls, obstacles, irq, h, player)
    
    @staticmethod
    #def _load_walls(field_walls, file_name, width, height):
    def _load_walls(file_name, width, height):
        '''загружает стены из файла
        deprecated'''
        with open(os.path.join(resources_path, file_name + '_walls.txt')) as f:
            field_walls = f.readlines()
            field_walls = [s.strip() for s in field_walls]
            field_walls = [[c != '.' for c in s] for s in field_walls]
            
            #транспонирование
            #исправляет некоторые ошибочные файлы!
            assert len(field_walls) == height
            for sub_list in field_walls:
                assert len(sub_list) == width
            field_walls = list(map(list, zip(*field_walls))) 

            return field_walls
    
    @staticmethod
    def _load_scene(file_name, width, height):
        '''загружает стены и препятствия (камни) из файла'''
        def test(l):
            '''тестирует на высоту и ширину'''
            assert len(l) == height
            for sub_list in l:
                assert len(sub_list) == width

        def transp(l):
            '''транспонирует массив'''
            l = list(map(list, zip(*l))) 
            return l

        with open(os.path.join(resources_path, file_name + '.txt')) as f:
            '''
            ..o
            #.#
            ...
            типовая карта
            '''
            field_walls = f.readlines()
            field_walls = [s.strip() for s in field_walls]
            
            obstacles = [[(obstacles_types.stone if c == 'o' else obstacles_types.fridge if c == 'f' else obstacles_types.space) for c in s] for s in field_walls]
            field_walls = [[c == '#' for c in s] for s in field_walls]
            
            test(obstacles); test(field_walls)
                
            field_walls = transp(field_walls)
            obstacles = transp(obstacles)

            return field_walls, obstacles
    
    @abc.abstractmethod
    def generate_map(self):
        '''генерирует карту'''
        raise NotImplementedError
    
    def end_of_game(self):
        '''False if not
        1 if dead
        2 if win
        >=2 special'''
        if player.is_die():
            return 1
        elif irq.ammount == 1:
            if self.win_level is None:
                return 2
            else:
                self.goto_level(self.win_level)
                return 0
        else:
            return 0

    def monsters(self):
        pass

    def spawns(self):
        pass

    def goto_level(self, level):
        level()


    def is_free_except_stones(self, x, y):
        '''пустая ли клетка, камни не учитывает'''
        try:
            r1 = field[x][y] == []
            r2 = not field_walls[x][y]
            r3 = x >= 0 and y >= 0
            return r1 and r2 and r3
        except IndexError:
            return False
    
    def is_free(self, x, y):
        '''пустая ли клетка'''
        try:
            r1 = self.is_free_except_stones(x, y)
            r2 = obstacles[x][y] not in [obstacles_types.stone, obstacles_types.fridge]
            return r1 and r2
        except IndexError:
            return False

    def is_monster_in(self, x, y):
        try:
            r1 = field[x][y] == []
            r2 = not field_walls[x][y]
            r3 = x >= 0 and y >= 0

            return not r1 and r2 and r3
        except IndexError:
            return False

    def is_player_in(self, x, y):
        '''prbly to player. ?'''
        raise NotImplementedError
        try:
            r1 = field[x][y] == player
            r2 = not field_walls[x][y]
            r3 = x >= 0 and y >= 0

            return r1 and r2 and r3
        except IndexError:
            return False

    def is_fridge(self, x, y):
        '''холодильник ли'''
        try:
            return obstacles[x][y] == obstacles_types.fridge
        except IndexError:
            return False

    def get_monster(self, x, y):
        '''TODO debug'''
        if self.is_monster_in(x, y):
            return field[x][y][0]
        else:
            return None

    def move_fridges(self, bumper_x, bumper_y, fridge_x, fridge_y):
        '''перемещает холодильники
        вход не будет проверяться
        по диагонали пока можно
        bumper_x, bumper_y - координаты толкающего; fridge_x, fridge_y - толкаемого холодильника
        return True when fridges were moved, False if not
        '''
        assert abs(bumper_x - fridge_x) <= 1
        assert abs(bumper_y - fridge_y) <= 1
        
        if (abs((bumper_x - fridge_x)*(bumper_y - fridge_y)) == 1) and not diagonal_fridges_flag:
            return False
        
        delta_x, delta_y = fridge_x-bumper_x, fridge_y-bumper_y
        current_x, current_y = fridge_x, fridge_y
        #пока холодильник, сдвигаемся на дельту
        
        while l.is_fridge(current_x, current_y):
            current_x += delta_x
            current_y += delta_y
        #если клетка после всех пустая - ставим в неё холодильник и убираем холодильник из начальной
        if l.is_free(current_x, current_y):
            obstacles[current_x][current_y] = obstacles_types.fridge
            obstacles[fridge_x][fridge_y] = obstacles_types.space
            return True
        else:
            return False

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

class Level_1(Level):
    def __init__(self):
        super().__init__(win_level=Level_2, from_file = True)
        #вроде эта тоже не нужна
        #global field_walls
        #строка ниже - в файле
        #field_walls[0][0] = field_walls[0][1] = field_walls[1][0] = True

    def monsters(self):
        Rat(3, 2)
        #Rat(3, 2)
        #Rat(3, 2)
        Rat(4, 2)
        Rat(5, 2)
        Rat(7, 0)
        Rat(9, 2)

class Level_2(Level):
    def __init__(self):
        super().__init__(win_level=Level_3)

    def monsters(self):
        Blob(3, 2)
        Blob(7, 3)
        Blob(1, 1)
        Blob(1, 3)
        Blob(9, 2)
        Blob(9, 1)
        Blob(9, 0)
        Blob(4, 2)

class Level_3(Level):
    def __init__(self):
        super().__init__(win_level=None)

    def monsters(self):
        Creeper(3, 3)

class Level_worm(Level):
    def __init__(self):
        super().__init__(20, 10, x_player=17, y_player=7)

    def monsters(self):
        WormHead.create_worm([[6, 8], [6, 4], [0, 4], [0, 0]])

    def spawns(self):
        add_spawn(3, 3, Rat, 48)

class Level_empty(Level):
    def __init__(self):
        super().__init__(width = 7, height = 7, win_level=None)

    def monsters(self):
        Rat(3, 2)

class Level_fridges(Level):
    '''уровень с холодильниками'''
    def __init__(self):
        super().__init__(win_level=Level_2, width = 19, height = 8, from_file = True)
        #вроде эта тоже не нужна
        #global field_walls
        #строка ниже - в файле
        #field_walls[0][0] = field_walls[0][1] = field_walls[1][0] = True

    def monsters(self):
        Rat(1, 1)

v = Vizualization()
v.start_vizualize()
game = Game()
player = None

#Level_worm()
#Level_1()
#Level_empty()
Level_fridges()

#TODO подумать здесь
height, width = l.height, l.width

game.cycle()

v.end_vizualize()
