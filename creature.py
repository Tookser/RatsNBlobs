class Creature(CellHolder, metaclass = abc.ABCMeta):
    '''human or monster or item(?)'''
    @abc.abstractmethod
    def __init__(self, x, y, health, damage, color, letter, current_health=None, flag_through_rocks=False):
        '''current_health=None - если выставляется полное здоровье
        flag_through_rocks - может ли перемещаться поверх камней'''
        super().__init__(x, y)
        irq.append(self)

        self._maxhealth = health
        self._health = health if current_health is None else current_health
    
        
        self._poison_length = 0 #0 если не отравлен
        self._poison_damage = 0
        
        self._damage = damage
        
        self._flag_through_rocks = flag_through_rocks
        
        self._color = color
        self._letter = letter
        
        

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _poison_works(self):
        '''срабатывание яда'''
        self._poison_length -= 1
        self.suffer(self._poison_damage)
    
    def do_effects_after_turn(self):
        '''срабатывают эффекты вроде отравлений, сразу после хода существа'''
        if self._poison_length >= 0:
            self._poison_works()
        else:
            pass
    
    def turn(self):
        '''think and select action'''
        pass

    def _real_move(self, x, y):
        '''перемещение без доп. проверок кроме смежности
        вызывается в move deprecated?'''
        if (abs(x-self.x) <= 1) and (abs(y-self.y) <= 1): #if adjust
            if x in range(l.width) and y in range(l.height):
                if abs(x-self.x) + abs(y-self.y) >= 1:
                    field[x][y] = [self]
                    field[self.x][self.y].remove(self)
                    self._x = x
                    self._y = y

    def is_near(self, x, y):
        '''проверка на близость, deprecated?'''
        return ((abs(x-self.x) <= 1) and (abs(y-self.y) <= 1)) and\
        (x in range(l.width) and y in range(l.height)) and\
        ((x, y) != (self.x, self.y))


    def move(self, x, y):
        '''move. or attack or wait, если монстр или стена'''
        def movement():
            '''само перемещение'''
            field[x][y] = [self]
            field[self.x][self.y].remove(self)
            self._x = x
            self._y = y

        if (abs(x-self.x) <= 1) and (abs(y-self.y) <= 1): #if adjust
            if x in range(l.width) and y in range(l.height):
                if abs(x-self.x) + abs(y-self.y) >= 1:
                    #атака прежде всего
                    if l.is_monster_in(x, y):
                        self.attack(x, y)
                    #перемещение холодильника
                    elif (self.__class__.__name__ == 'Player') and l.is_fridge(x,y):
                        if l.move_fridges(self.x, self.y, x, y):
                            movement()

                    elif self._flag_through_rocks and l.is_rock(x, y) or \
                        l.is_free(x, y):
                        
                        movement()
                        
                    '''elif (self.__class__.__name__ == 'Player' and
                    (l.is_free_except_stones(x, y))) or \
                    l.is_free(x, y):
                        movement()'''

        else:
            raise MoveError('distance is too long')

    def attack(self, x, y):
        '''attack!!!'''
        if x in range(l.width) and y in range(l.height):
            if (abs(x - self.x) <= 1) and (abs(y - self.y) <= 1) and \
            (abs(y - self.y) + abs(x - self.x) >= 1): #if adjust
                debug(x-self.x, y - self.y, x, y, self.x, self.y)
                if l.is_monster_in(x, y):
                    creature = l.get_monster(x, y)
                    if creature == player:
                        if self.damage == 0:
                            v.log.add_message("{} pushes you.".format(self.__class__.__name__))
                        else:
                            v.log.add_message("{} attacks you.".format(self.name))
                    creature.suffer(self.damage)
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
        '''получение урона'''
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

    def receive_poison(self, poison_length, poison_damage):
        '''получение отравления. Заменяет предыдущее отравление'''
        self._poison_length = poison_length
        self._poison_damage = poison_damage
    
    def get_nearest_enemy(self):
        '''TODO сделать нормальный выбор врага'''
        for cell in neighbour_cells:
            cell = (cell[0] + player.x, cell[1] + player.y)
            if l.is_monster_in(*cell):
                return l.get_monster(*cell)
        else:
            raise GameError("Не могу найти ближайшего монстра")
    
    def _die(self):
        '''postmortem actions'''
        v.log.add_message("{} dies.".format(self.name))
        field[self.x][self.y].remove(self)
        irq.delete(self)

    @property
    def name(self):
        '''имя существа нужно для лога'''
        return self.__class__.__name__
    
    @property
    def color(self):
        return t.color_from_name(self._color[int(self._health)])

    @property
    def letter(self):
        return self._letter
	
    @property
    def background_color(self):
        return t.color_from_name(poisoned_creature_background_color) \
                if self._poison_length > 0 \
                else t.color_from_name(background_color)
	
	
    @property
    def health(self):
        return self._health
    
    @property
    def maxhealth(self):
        return self._maxhealth
    
    @property
    def damage(self):
        return self._damage
