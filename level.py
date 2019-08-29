class Level:
    '''Класс уровня'''

    def __init__(self, level_generator = None, width=10, height=4, x_player=2, y_player=2, win_level=None, from_file = False, field_walls_arg = None, obstacles_arg = None, generate_map = False):
        ''''''
        #TODO убрать generate_map он не нужен
        assert bool(field_walls_arg) == bool(obstacles_arg)

        

        global l
        l = self
        
        if level_generator is not None:
            global lg
            lg = level_generator
        

        global field_walls
        global obstacles
        
        
        monsters_message = None
        #загрузка карты из файла
        
        if level_generator is not None:
            field_walls, obstacles, self._width, self._height, x_player, y_player, monsters_message = lg.get_new_level()
        
        elif self._generate_map:
            field_walls, obstacles, self._width, self._height, x_player, y_player, monsters_message = self._generate_map()

        elif from_file:
            field_walls, obstacles, self._width, self._height, x_player, y_player = self._load_scene(self.__class__.__name__)
        else:
            height = width = 10
            self._height = self._width = width
            field_walls = [[False for j in range(height)] for i in range(width)] #TODO исправить красиво

            obstacles = [[False for j in range(height)] for i in range(width)]
        

        global field
        field = [[[] for j in range(self._height)] for i in range(self._width)]



        global irq
        irq = InfiniteRandomQueue()
        global h
        h = SpawnQueue()

        #здесь можно сделать предметы items
        global player
        old_player = player
        player = Player(x_player, y_player, old_player)

        #если передан запрос на монстров, выполнить его
        if monsters_message in [None, ""]:
            self.monsters()
        else:
            exec(monsters_message)
        self.spawns()

        self.win_level = win_level

        game.new_level(level_generator, l, field, field_walls, obstacles, irq, h, player)

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
    def _load_scene(file_name):
        '''загружает стены и препятствия (камни) из файла, сейчас INCORRECT - не находит позицию игрока, вместо этого 0,0
        TODO преобразовать в метод'''
        def test(l):
            '''тестирует на высоту и ширину'''
            for sub_list in l:
                assert len(sub_list) == len(l[0])
            return len(l[0]), len(l) 

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

            width, height = test(obstacles); test(field_walls) #TODO исправить красиво

            field_walls = transp(field_walls)
            obstacles = transp(obstacles)

            return field_walls, obstacles, width, height, 0, 0 #TODO позицию игрока по клетке @

    def _generate_map(self):
        '''генерирует карту DEPRECATED'''
        raise NotImplementedError

    def end_of_game(self):
        '''Переходит на следующий уровень и выдаёт состояние False if not
        1 if dead
        2 if win
        3 если закрыта
        >= 2 special (???)'''
        if player.is_die():
            return 1
        elif irq.ammount == 1:
            if lg is not None:
                if lg.is_new_level_avaiable():
                    self.goto_next_level()
                    return 0
                else:
                    return 2
            else: #TODO убрать старый вариант работы с уровнями
                if self.win_level is None:
                    return 2
                else:
                    self.goto_level(self.win_level)
                    return 0
        elif game.is_game_closed:
            return 3
        else:
            return 0

    def monsters(self):
        pass

    def spawns(self):
        pass

    def goto_level(self, level):
        '''версия старого варианта работы с уровнями'''
        level()

    def goto_next_level(self):
        '''версия при работающем генераторе'''
        Level(level_generator = lg)
        
    def is_correct_cell(self, x, y):
        '''проверяет клетку на существование'''
        return x in range(l.width) and y in range(l.height)
            
        
        
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
            
    def is_rock(self, x, y):
        if self.is_correct_cell(x, y):
            r1 = obstacles[x][y] == obstacles_types.stone
            return r1
        else:
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

    def get_random_free_cell(self):
        '''возвращает свободную клетку, IndexError если таких нет'''
        arr = []
        for i in range(l.width):
            for j in range(l.height):
                if self.is_free(i,j):
                    arr.append((i,j,))
        
        return random.choice(arr)
        
    def get_monster(self, x, y):
        '''проверяет на существо в клетке'''
        if self.is_monster_in(x, y):
            return field[x][y][0]
        else:
            #return None
            raise GameError("No creature in the cell")

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
