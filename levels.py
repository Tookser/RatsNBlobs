#TODO избавиться от этого файла, перенеся всё в mapgen

class Level_1(Level):
    def __init__(self):
        super().__init__(win_level=Level_2, from_file = True)
        #вроде эта тоже не нужна
        #global field_walls
        #строка ниже - в файле
        #field_walls[0][0] = field_walls[0][1] = field_walls[1][0] = True

    def monsters(self):
        Rat(0, 2)
        Rat(4, 2)
        Rat(4, 3)
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
        h.add_monster_spawn(3, 3, Rat, 48)

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

class Level_spawn(Level):
    def __init__(self):
        super().__init__(5, 10, x_player = 1, y_player = 1)
    def monsters(self):
        Rat(0, 2)
        Rat(4, 2)
    def spawns(self):
        h.add_monster_spawn(3, 3, Rat, 5)
 #       h.add_monster_spawn(3, 3, Rat, 5)
#        h.add_monster_spawn(9, 9, Blob, 20, infinite_repeat = False)
        
class Level_cave(Level):
    def __init__(self):
        self._generate_map = mapgen.cave_generator
        super().__init__(generate_map = True)
        
    def monsters(self):
        #for i in range(3):
            #Rat(*(self.get_random_free_cell()))
        pass

class Level_dungeon_room(Level):
    def __init__(self):
        self._generate_map = mapgen.room_dungeon_generator
        super().__init__(generate_map = True)

class Level_hallway(Level):
    def __init__(self):
        self._generate_map = mapgen.hallway_generator
        super().__init__(lg, generate_map = True)
