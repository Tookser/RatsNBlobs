'''здесь различные генераторы карт'''
import random
import os

from obstacles import *

def _close_isolated(field_walls, x_player=0, y_player=0, only_by_side=True):
    '''проверяет, какая часть поля доступна шагами, и закрывает стенами оставшуюся
    only_by_side - только горизонтальные и вертикальные шаги
    TODO исправить flood algorithm'''
    assert not field_walls[x_player][y_player]
    
    def get_neighbours(x, y):
        '''выдаёт список соседей'''
        m = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if not only_by_side:
            m += [(1, 1), (-1, -1), (-1, 1), (1, -1)] 
        m = [(x+a, y+b) for (a, b) in m]
        return m
    
    
    width = len(field_walls)
    height = len(field_walls[0])
    print(width, height)
    avaiable_from_start_cells = [[False for j in range(height)] for i in range(width)]
    checked = [[False for j in range(height)] for i in range(width)]
    
    avaiable_from_start_cells[x_player][y_player] = True
    
    
    def check_cell(x,y):
        '''рекурсивная проверка клетки'''
        if not (x in range(width) and y in range(height)) or\
            checked[x][y]:
            return
        else:
            print(x, y)
            checked[x][y] = True
            avaiable_from_start_cells[x][y] = True
            
            neib = get_neighbours(x, y);
            for x_test, y_test in neib:
                if x_test in range(width) and y_test in range(height):
                    try:
                        if field_walls[x_test][y_test]:
                            checked[x_test][y_test] = True
                        else:
                            print("check", x_test, y_test)
                            check_cell(x_test, y_test)
                    except:
                        pass

    if field_walls[x_player][y_player]:
        raise Exception("player on the wall")
        
    check_cell(x_player, y_player)
    
    #если клетка недоступна из начальной, то делаем её стеной
    for i in range(height):
        for j in range(width):
            if not avaiable_from_start_cells[j][i]:
                field_walls[j][i] = True

def _load_scene(file_name, width, height):
    '''загружает стены и препятствия (камни) из файла, скопировано из ratsnblobs.py и пока не тестировалось вроде'''
    def test(l):
        '''тестирует на высоту и ширину'''
        assert len(l) == height
        for sub_list in l:
            assert len(sub_list) == width

    def transp(l):
        '''транспонирует массив'''
        l = list(map(list, zip(*l))) 
        return l

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    resources_path = 'Resources'
    with open(os.path.join(resources_path, file_name + '.txt')) as f:
        '''
        ..o
        #.#
        ...
        типовая карта
        '''
        field_walls = f.readlines()
        field_walls = [s.strip() for s in field_walls]
        
        '''obstacles = [[(obstacles_types.stone if c == 'o' 
        else obstacles_types.fridge if c == 'f' 
        else obstacles_types.space) 
        for c in s] 
        for s in field_walls]'''
        field_walls = [[c == '#' for c in s] for s in field_walls]
        
        #test(obstacles)
        test(field_walls)
            
        field_walls = transp(field_walls)
        #obstacles = transp(obstacles)

        return field_walls, None #obstacles                

def _test_vizualize(field_walls, width, height):
    '''тестовая текстовая визуализация, скопирован из ratsnblobs.py'''
    def horizontal():
        print(' ', end='')
        for i in range(width + 2):
            print('#', end='')
        print('')
        
    print('  ', end='')
    for i in range(width):
        print(i%10, end='')
    print('')
    horizontal()
    for i in range(height):
        print(str(i%10)+'#', end='')
        for j in range(width):
            #print(j, i)
            if field_walls[j][i] == False:
                print('.', end='')
            else:
                print('#', end='')
        print('#')
    horizontal()

def _false_double_array(width, height):
    '''создаёт массив из False'''
    return [[False for j in range(height)] for i in range(width)]

def _not_array(mas):
    '''not, но к двумерному списку'''
    for i in range(len(mas)):
        for j in range(len(mas[i])):
            mas[i][j] = not mas[i][j]
    return mas
        

def avaiable_from(walls, x, y):
    '''закрывает стеной все пустые клетки, недоступные из (x,y)'''
    avaiable_cells = []
    width = len(walls)
    height = len(walls[0])
    
    def test_recursive(x, y):
        nonlocal avaiable_cells
        if x in range(width) and y in range(height):
            if not walls[x][y]:
                if (x, y) not in avaiable_cells:
                    avaiable_cells.append((x, y,))
                    test_recursive(x, y + 1)
                    test_recursive(x, y - 1)
                    test_recursive(x + 1, y - 1)
                    test_recursive(x + 1, y)
                    test_recursive(x + 1, y + 1)
                    test_recursive(x - 1, y - 1)
                    test_recursive(x - 1, y)
                    test_recursive(x - 1, y + 1)
                test_recursive
        
    test_recursive(x, y)
    for i in range(width):
        for j in range(height):
            if not walls[i][j] and (i,j) not in avaiable_cells:
                walls[i][j] = True
    
    return walls
def _create_cave_map(x_size=20, y_size=10, cave_size=20, x_start=5, y_start=5, random_param=6):
    '''создаёт пещеру по алгоритму генерации леса отсюда http://rlgclub.ru/wiki/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F_%D0%BB%D0%B5%D1%81%D0%B0'''
    walls = [[True for i in range(y_size)] for j in range(x_size)]
    
    walls[x_start][y_start] = False 
    x_current, y_current = x_start, y_start
    
    for i in range(cave_size):
        array_sdvig = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for j in range(4):
            if (random.randint(1,random_param) == 1):
                try:
                    x_sdvig, y_sdvig = array_sdvig[j]
                    x_current += x_sdvig
                    y_current += y_sdvig
                    if not(x_current in range(x_size) and y_current in range(y_size)): 
                        raise IndexError
                    walls[x_current][y_current] = False;
                except IndexError:
                    x_current -= x_sdvig
                    y_current -= y_sdvig
    
    return walls
'''#старая версия, должна быть эквивалентна
        if (random.randint(1,random_param) == 1):
            try:
                x_current += 1
                if not(x_current in range(x_size) and y_current in range(y_size)): 
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                x_current -= 1;
        if (random.randint(1,random_param) == 1):
            try:
                y_current += 1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                y_current -= 1;
        if (random.randint(1,random_param) == 1):
            try:
                x_current += -1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                x_current -= -1;
        if (random.randint(1,random_param) == 1):
            try:
                y_current += -1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                y_current -= -1;'''
    
def _create_room_dungeon_map(width, height, random_param = 6, doors = True, width_limit = 5, height_limit = 5):
    '''создаёт карту из разделённых комнат, doors - с дверями'''
    walls = _false_double_array(width, height)
    small_limit = 5
    line_walls = [] #список стен (которые, в свою очередь, списки клеток) списков стен, в которых нужно будет пробивать двери - по одной
    
    def is_room_small(x1, y1, x2, y2, random_small = True):
        '''random_small - может ли комната по случайным причинам быть признана маленькой (неразделяемой)'''
        return abs(x1-x2) <= width_limit and abs(y1-y2) <= height_limit \
                or random.randint(1, random_param) == 1 and random_small
    
    def line(x1, y1, x2, y2):
        '''проводит линию между двумя клетками, обе включительно'''
        nonlocal walls
        assert x1==x2 or y1==y2
        line_walls.append([])
        
        if (x1 == x2):
            for i in range(y1, y2 + 1):
                walls[x1][i] = True
                line_walls[-1].append((x1, i))
        elif (y1 == y2):
            for i in range(x1, x2 + 1):
                walls[i][y1] = True
                line_walls[-1].append((i, y1))
        else:
            assert False
    
    def room(x1, y1, x2, y2, random_small = True):
        '''рекурсивно создаёт комнаты'''
        
        if (is_room_small(x1, y1, x2, y2, random_small)):
            pass
        else:
            avaiable = {0: abs(x1-x2)>small_limit, 1: abs(y1-y2)>small_limit}
            avaiable = {k:avaiable[k] for k in avaiable if avaiable[k]}
            
            choise = random.choice(list(avaiable.keys()))
            
            if (choise == 0):
                #по вертикали стенка
                wall_x = random.randint(x1+2, x2-2)
                line(wall_x, y1, wall_x, y2)
                room(x1, y1, wall_x-1, y2)
                room(wall_x+1, y1, x2, y2)
            elif (choise == 1):
                #по горизонтали стенка        
                wall_y = random.randint(y1+2, y2-2)
                line(x1, wall_y, x2, wall_y)
                room(x1, y1, x2, wall_y - 1)
                room(x1, wall_y + 1, x2, y2)
            else:
                assert False
                
    room(0, 0, width-1, height-1, random_small = False)
    
    if doors:
        for l in line_walls:
            x, y = random.choice(l)
            walls[x][y] = False

    return walls
    
def return_free(walls):
    '''возвращает свободную клетку'''
    arr = []
    for i in range(len(walls)):
        for j in range(len(walls[i])):
            if walls[i][j] == False:
                arr.append((i,j,))
    
    return random.choice(arr)

def count_free(walls):
    '''подсчитывает по массиву со стенами количество свободных клеток'''
    s = 0
    for column in walls:
        for cell in column:
            s += 1 if cell == False else 0
    return s


def _check_generator_wrapper(funct):
    '''обёртка для всех генераторов, проверяет сгенерированный карту на корректность и кидает MapGeneratorError если что не так'''
    def result_funct(*args, **kargs):
        def check_correct(mas):
            '''проверяет, что всё хорошо с длиной столбцов и строк'''
            for i in range(len(mas) - 1):
                if len(mas[i]) != len(mas[i+1]):
                    return False
            return True
            
            
        def check_complement(mas1, mas2):
            '''только после проверки корректности, проверяет соответствие длин'''
            return len(mas1) == len(mas2) and len(mas1[0]) == len(mas2[0])
            
        funct(*args, **kargs)
        wall, obstacles, x_size, y_size, x_player, y_player, monsters_message = args[0].tuple()
        if wall[x_player][y_player]:
            assert MapGeneratorError("игрок на стене")
        
        if not check_correct(wall) or not check_correct(obstacles):
            assert MapGeneratorError("некорректные массивы")
        
        if not check_complement(wall, obstacles):
            assert MapGeneratorError("Несоответствующие массивы")
        
        return (wall, obstacles, x_size, y_size, x_player, y_player, monsters_message)
            
    
    return result_funct
        

class LevelGenerating:
    '''класс задающий генерирующийся уровень'''
    def __init__(self):
        '''строка _monsters_string содержит код, который должен выполняться, в тч предметы...'''
        
        self._monsters_string = '' 
        self.height = self.width = -1
        pass

    def _initialize_free_cells(self):
        '''создаёт список свободных клеток'''
        arr = []
        for i in range(len(self.walls)):
            for j in range(len(self.walls[i])):
                if self.walls[i][j] == False:
                    arr.append((i,j,))
        
        self._free_cells = arr
    
    
    
    @property
    def walls(self):
        '''стены'''
        return self._walls
    
    @walls.setter
    def walls(self, w):
        '''при каждом переприсваивании walls обновляет список свободных клеток'''
        self._walls = w
        self._initialize_free_cells()
    '''
    @property
    def width(self):
        return len(self.walls)
        
    @property
    def height(self):
        return len(self.walls[0])
    '''
    def return_free(self):
        '''возвращает свободную клетку, убирая её из списка'''
        result = random.choice(self._free_cells)
        self._free_cells.remove(result)
        return result
    
    def delete_from_free(self, cell):
        '''удаление клетки из свободных. может быть использовано, например, 
            чтобы не ставить монстров около игрока'''
        self._free_cells.remove(cell)
    
    def add_monster(self, name, *param, **params):
        '''добавляет строку о монстре в сообщение'''
        parameters_string = ''
        for p in param:
            parameters_string += "{}, ".format(p)
        for k in params:
            parameters_string += "{} = {}, ".format(k, str(params[k]))
        parameters_string = parameters_string[:-2] #убираем запятую и пробел в конце
            
        s = "{}({})\n".format(name, parameters_string)
        
        self._monsters_string += s
    
    def tuple(self):
        '''возвращает содержимое объекта в виде tuple для использования в классе Level'''
        return (self.walls, self.obstacles, \
                self.width, self.height, \
                self.x_player, self.y_player, \
                self._monsters_string)
    

    @_check_generator_wrapper
    def room_dungeon_generator(self, width = 40, height = 40):
        l = self
        l.width = width
        l.height = height
        
        l.walls = _create_room_dungeon_map(l.width, l.height)
        l.obstacles = _false_double_array(l.width, l.height)
        #_test_vizualize(walls, x_size, y_size)
        l.x_player, l.y_player = l.return_free()
        
        #l.add_monster("Rat", *l.return_free())

    @_check_generator_wrapper
    def cave_generator(self, width = 40, height = 40, cave_size = 1000):
        l = self
        l.width = width
        l.height = height
        
        l.walls = _create_cave_map(x_size = l.width, y_size = l.height, cave_size = cave_size, x_start = l.width//2, y_start = l.height//2)
        
        l.obstacles = _false_double_array(l.width, l.height)
        #_test_vizualize(walls, x_size, y_size)
        l.x_player, l.y_player = l.return_free()
        
        #l.add_monster("Rat", *l.return_free())
        #l.add_monster("Rat", *l.return_free())
        #l.add_monster("Rat", *l.return_free())
        
        
    @_check_generator_wrapper
    def hallway_generator(self, width = 40, height = 40):
        l = self
        l.width = width
        l.height = height
        
        l.walls = _create_room_dungeon_map(l.width, l.height, doors = False)
        #print(l.walls)
        l.walls = _not_array(l.walls)
        
        l.obstacles = _false_double_array(l.width, l.height)
        
        
        l.x_player, l.y_player = l.return_free()
        #print (l.x_player, l.y_player)
        
        #print(l.x_player, l.y_player)
        l.walls = avaiable_from(l.walls, l.x_player, l.y_player)
        #_test_vizualize(l.walls, 40, 40)
        l.delete_from_free((l.x_player, l.y_player))
        
        
        
        #for i in range(10):
        #    l.add_monster("Rat", *l.return_free())
        
        #l.add_monster("Creeper", *l.return_free())
        #print(l._monsters_string)
        
    def print(self):
        '''тестовая текстовая визуализация, скопирована откуда-то выше (а там из из ratsnblobs.py), выводит только стены TODO сделать печать всего'''
        width, height = self.width, self.height
        field_walls = self.walls
        
        def horizontal():
            print(' ', end='')
            for i in range(width + 2):
                print('#', end='')
            print('')
            
        print('  ', end='')
        for i in range(width):
            print(i%10, end='')
        print('')
        horizontal()
        for i in range(height):
            print(str(i%10)+'#', end='')
            for j in range(width):
                #print(j, i)
                if field_walls[j][i] == False:
                    print('.', end='')
                else:
                    print('#', end='')
            print('#')
        horizontal()


    

class LevelsGenerator:
    def __init__(self, max_level=0):
        '''уровни нумеруются с 0
        max_level - последний доступный уровень'''
        self._current_level = -1
        self._max_level = max_level
    
    def is_new_level_avaiable(self):
        return self._current_level < self._max_level
    
    def get_new_level(self):
        raise NotImplementedError

class LevelsGenerator1(LevelsGenerator):
    '''генератор уровней для тестовой игры, три уровня, проходится с 20 здоровья'''
    def __init__(self):
        super(LevelsGenerator1, self).__init__()
        self._max_level = 2

    def get_new_level(self):
        assert self.is_new_level_avaiable()
        
        self._current_level += 1
        
        l = LevelGenerating()
        
        if self._current_level == 0:
            l.cave_generator(20, 20, cave_size = 300)
            l.add_monster("Rat", *l.return_free())
            l.add_monster("FatRat", *l.return_free())
            l.add_monster("FatRat", *l.return_free())
            l.add_monster("FatRat", *l.return_free())
            
            l.add_monster("Poison", *l.return_free())
            l.add_monster("Poison", *l.return_free())
            l.add_monster("Poison", *l.return_free())
            
        elif self._current_level == 1:
            l.hallway_generator(30, 30)
            for i in range(random.randint(7,10)):
                l.add_monster("RatSmart", *l.return_free())
            
            for i in range(3):
                sword_x, sword_y = l.return_free()
                l.obstacles[sword_x][sword_y] = obstacles_types.sword
                
        elif self._current_level == 2:
            l.cave_generator(23, 23, cave_size = 400)
            for i in range(random.randint(2,3)):
                l.add_monster("Creeper", *l.return_free())
            for i in range(random.randint(2,3)):
                l.add_monster("Rat", *l.return_free())
                
        return l.tuple()

def _test():
    '''тестовая функция'''
    #print(_create_monster_string("Cat", meow="yes", murp="no") + _create_monster_string("Rat"))
    #walls = _create_room_dungeon_map(40, 40)
    #_test_vizualize(walls, 40, 40)
    l = LevelGenerating()
    l.hallway_generator()
    l.print()

if __name__ == "__main__":
    #_test_forest()
    _test()
